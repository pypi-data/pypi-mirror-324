# HF Torch Cache

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

Efficient caching layer for Hugging Face models using PyTorch serialisation. Accelerate model initialisation while reducing disk redundancy by converting native Hugging Face checkpoints to optimised PyTorch format.

## Features

- 🚀 **Faster Initialisation**: Skip Hugging Face's config reloading on subsequent loads
- 💾 **Disk Efficiency**: Eliminate duplicate storage of model artifacts
- 🔍 **Auto Model Detection**: Dynamically selects appropriate model class from config
- 🧹 **Cache Management**: Optional cleanup of original Hugging Face cache artifacts
- 🔒 **Safety Controls**: Configurable weights-only loading for untrusted sources

## Installation

```bash
pip install hftorchcache
```

## Usage

### Basic Example

```python
from hftc import HFTorchCache

# Initialise cache manager
cache = HFTorchCache()

# Load model with automatic class detection
model, tokenizer = cache.load(
    "unsloth/DeepSeek-R1-Distill-Qwen-7B-bnb-4bit",
    map_location="cuda"
)
```

### Advanced Usage

```python
cache = HFTorchCache(
    cache_dir="/custom/cache/path",  # Default: ~/.cache/hftc
    cleanup_original=True            # Auto-delete original HF cache
)

# Load with explicit device placement and safety controls
model, tokenizer = cache.load(
    "unsloth/DeepSeek-R1-Distill-Qwen-7B-bnb-4bit",
    model_cls="AutoModelForCausalLM",    # Explicit class specification
    tokenizer_cls="AutoTokenizer",
    map_location=torch.device("cuda:0"),
    weights_only=False,                  # Enable for untrusted sources
    local_only=True                      # Prevent HF Hub fallback
    # **model_kwargs                     # Would be passed to `from_pretrained`
)
```

Note that you may need additional packages (e.g. `bitsandbytes`) to load cached models.

### Cleanup utilities

You can also use the internal `_cleanup_hf_cache` method to delete the entire model directories of
models you're done with, without trying to load them (as long as HuggingFace can find a snapshot).

```python
cache._cleanup_hf_cache("Qwen/Qwen2.5-7B-Instruct-GPTQ-Int8")
```

## API Reference

### `HFTorchCache`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `cache_dir` | str | `~/.cache/hftc` | Custom cache directory |
| `cleanup_original` | bool | True | Remove original HF cache after conversion |

### `load()`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model_name` | str | Required | HF model identifier |
| `model_cls` | str/type | "auto" | Model class specification |
| `tokenizer_cls` | str/type | "auto" | Tokenizer class specification |
| `map_location` | str/device | None | Torch device placement |
| `weights_only` | bool | False | Safe loading for untrusted sources |
| `local_only` | bool | False | Disable HF hub fallback |

## Implementation Notes

1. **First-Run Behavior**: Initial load converts HF checkpoint to optimized PyTorch format
2. **Subsequent Loads**: Directly loads serialised PyTorch artifacts (3-5x faster)
3. **Device Management**: Specify `map_location` to control device placement
4. **Security**: Use `weights_only=True` when loading untrusted models

## License

MIT License - See [LICENSE](LICENSE) for details

---

**Note**: This project is not affiliated with Hugging Face. Use with caution in production environments. Always verify model sources when using `weights_only=False`.
