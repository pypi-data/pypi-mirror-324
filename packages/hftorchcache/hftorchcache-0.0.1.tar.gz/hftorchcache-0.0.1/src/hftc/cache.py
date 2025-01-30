from __future__ import annotations

import hashlib
import json
import logging
import shutil
from collections.abc import Callable
from importlib import import_module
from pathlib import Path
from typing import TYPE_CHECKING, Literal, TypeVar, Union

import torch
from platformdirs import user_cache_dir

if TYPE_CHECKING:
    from transformers import AutoTokenizer
    from transformers.modeling_utils import PreTrainedModel
    from transformers.models.auto.auto_factory import _BaseAutoModelClass
    from transformers.tokenization_utils_base import PreTrainedTokenizerBase

AutoModelT = TypeVar("AutoModelT", bound="_BaseAutoModelClass")
PretrainedModelT = TypeVar("PretrainedModelT", bound="PreTrainedModel")
PretrainedTokenizerT = TypeVar("PretrainedModelT", bound="PreTrainedTokenizerBase")

ModelT = Union[AutoModelT, PretrainedModelT]
TokenizerT = Union["AutoTokenizer", PretrainedTokenizerT]

logger = logging.getLogger(__package__)


def load_local_hf_model(
    hf_dir: Path,
    cls: Literal["auto"] | str | type[ModelT] = "auto",
    **model_kwargs,
) -> ModelT:
    match cls:
        case "auto":
            from transformers import AutoConfig

            model_config = AutoConfig.from_pretrained(hf_dir)
            # Could allow options here if this is ever an issue, here just pick #1
            model_cls_name = model_config.architectures[0]
            model_cls = getattr(import_module("transformers"), model_cls_name)
        case str() as model_cls_name:
            model_cls = getattr(import_module("transformers"), model_cls_name)
        case type() as model_cls:
            pass  # Could type check it here but just proceed
        case _ as unknown:
            raise TypeError(f"cls must be 'auto', a name or type, got {unknown}")

    return model_cls.from_pretrained(hf_dir, **model_kwargs)


def load_local_hf_tokenizer(
    hf_dir: Path,
    cls: Literal["auto"] | str | type[TokenizerT] = "auto",
) -> TokenizerT:
    match cls:
        case "auto":
            tokenizer_cls = AutoTokenizer
        case str() as tokenizer_cls_name:
            tokenizer_cls = getattr(import_module("transformers"), tokenizer_cls_name)
        case type() as tokenizer_cls:
            pass  # Could type check it here but just proceed
        case _:
            raise TypeError(
                f"tokenizer_cls must be 'auto', a name or type, got {tokenizer_cls}",
            )

    return tokenizer_cls.from_pretrained(hf_dir)


class HFTorchCache:
    """Cache manager for Hugging Face models using PyTorch serialisation"""

    def __init__(self, cache_dir: str | None = None, cleanup_original: bool = True):
        """
        Initialise the cache manager.

        Args:
            cache_dir: Custom cache directory path. Defaults to ~/.cache/hftc
            cleanup_original: Whether to remove original HF cache after serialisation
        """
        self.cache_dir = Path(cache_dir or user_cache_dir("hftc")).expanduser()
        self.cleanup_original = cleanup_original
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_path(self, model_name: str, config: dict = None) -> Path:
        """Generate a unique cache path for the model"""
        safe_name = model_name.replace("/", "--")
        # Include config hash in filename for different model variants
        config_str = json.dumps(config or {}, sort_keys=True)
        config_hash = hashlib.sha256(config_str.encode()).hexdigest()[:8]
        filename = f"{safe_name}-{config_hash}"
        return self.cache_dir / f"{filename}.pt"

    def load(
        self,
        model_name: str,
        model_cls: Literal["auto"] | str | type[ModelT] = "auto",
        tokenizer_cls: Literal["auto"] | str | type[TokenizerT] = "auto",
        map_location: str | torch.device | dict | Callable | None = None,
        weights_only: bool = False,
        local_only: bool = False,
        **model_kwargs,
    ) -> tuple[ModelT, TokenizerT]:
        """
        Load a model and tokeniser, using cached version if available.
        Note that by default `weights_only` is False: use on trusted sources only.

        Args:
            model_name: Hugging Face model identifier
            model_cls: Model class to use (default: "auto" uses first
                       architecture in config). Strings are looked up in
                       `transformers` namespace so model class names or AutoModel*
                       class names will work, or pass the class itself.
            tokenizer_cls: Tokenizer class to use (default: "auto" uses AutoTokenizer).
                           Strings are looked up in `transformers` namespace so
                           tokenizer class names will work, or pass the class itself.
            map_location: Target device for model loading, see `torch.load` docs.
            weights_only: Initialise model from weights (default: False, faster).
            local_only: Prevent fallback to loading model from HF Hub (default: False).
            **model_kwargs: Additional arguments for `from_pretrained`.

        Returns:
            Tuple of (model, tokeniser)
        """
        hftc_cache = self._get_cache_path(
            model_name,
            config={"weights_only": weights_only},
        )

        if hftc_cache.exists():
            logger.info(f"Loading cached model from {hftc_cache}")
            try:
                model, tokenizer = torch.load(
                    hftc_cache,
                    map_location=map_location,
                    weights_only=weights_only,
                )
            except Exception as e:
                logger.warning(f"Failed to load cached model: {e}")
                hftc_cache.unlink(missing_ok=True)

        if not hftc_cache.exists():
            from huggingface_hub import hf_hub_download
            from huggingface_hub.errors import LocalEntryNotFoundError

            logger.info(f"Transferring HuggingFace model to {hftc_cache}")
            model_kwargs = {**dict(low_cpu_mem_usage=True), **model_kwargs}

            try:
                hf_cache_dir = hf_hub_download(
                    model_name, filename="", local_files_only=local_only
                )
            except LocalEntryNotFoundError as exc:
                # Cache miss when `local_files_only` is True - do not load from HF Hub
                raise FileNotFoundError(
                    f"No local HF cache for {model_name} nor pre-existing hftc cache",
                ) from exc
            else:
                logger.info(f"Loading cached model from {hftc_cache}")
                model = load_local_hf_model(hf_cache_dir, cls=model_cls, **model_kwargs)
                tokenizer = load_local_hf_tokenizer(hf_cache_dir, cls=tokenizer_cls)
                # Cache the loaded model
                logger.info(f"Caching model to {hftc_cache}")
                torch.save((model.cpu(), tokenizer), hftc_cache)
                model, tokenizer = torch.load(
                    hftc_cache, map_location=map_location, weights_only=weights_only
                )

        # Cleanup original HF cache if requested
        if self.cleanup_original:
            self._cleanup_hf_cache(model_name)

        return model, tokenizer

    def _cleanup_hf_cache(self, model_name: str) -> None:
        """Remove original HF cache files for the model"""
        try:
            from huggingface_hub import hf_hub_download
            from transformers.utils import TRANSFORMERS_CACHE

            hf_cache = Path(TRANSFORMERS_CACHE)
            # Get the model's cache directory by using hf_hub_download
            model_path = Path(
                hf_hub_download(model_name, filename="", local_files_only=True)
            )
            # Get the root model directory (removes snapshots/hash part)
            model_dir = hf_cache / model_path.relative_to(TRANSFORMERS_CACHE).parts[0]

            if model_dir.exists():
                shutil.rmtree(model_dir)
                logger.info(f"Cleaned up HF cache directory: {model_dir}")
        except Exception as e:
            logger.warning(f"Failed to cleanup HF cache: {e}")
        return

    def clear_cache(self, model_name: str | None = None) -> None:
        """
        Clear cached models.

        Args:
            model_name: Specific model to clear, or all if None
        """
        if model_name:
            hftc_cache = self._get_cache_path(model_name)
            hftc_cache.unlink(missing_ok=True)
        else:
            shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir(parents=True)
        return
