# Odysee: High-Performance Multi-Modal Deep Learning Framework

[![PyPI version](https://badge.fury.io/py/odysee.svg)](https://badge.fury.io/py/odysee)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Documentation Status](https://readthedocs.org/projects/odysee/badge/?version=latest)](https://odysee.readthedocs.io/en/latest/?badge=latest)

Odysee is a cutting-edge deep learning framework designed for efficient processing of both text and images, with support for context windows up to 4M tokens. Built with performance in mind, it leverages Rust and Metal acceleration on Apple Silicon.

## 🚀 Key Features

- **4M Token Context Windows**: Efficiently handle extremely long sequences
- **Multi-Modal Processing**: Seamlessly work with both text and images
- **Metal Acceleration**: Optimized for Apple Silicon with Metal Performance Shaders
- **Memory Efficient**: Advanced gradient checkpointing and sparse attention
- **Cross-Language Integration**: Combines Python, Rust, and C++ for optimal performance

## 📦 Installation

```bash
# Via pip (recommended)
pip install odysee

# From source
git clone https://github.com/threatthriver/odysee.git
cd odysee

# Install Rust toolchain (if not already installed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install Python dependencies
pip install -r requirements.txt

# Build Rust extensions
cd rust
cargo build --release
cd ..

# Install in development mode
pip install -e .
```

## 🚀 Quick Start

```python
from odysee.routing import MultiModalDynamicRouter, RoutingConfig
from PIL import Image

# Initialize router
config = RoutingConfig(
    routing_dim=1024,
    num_heads=8,
    max_context_length=4_000_000
)
router = MultiModalDynamicRouter(config)

# Process text
text_embeddings = get_embeddings(text)  # Your embedding function
routed_text, stats = router.route(text_embeddings)

# Process image
image = Image.open("example.jpg")
routed_image = router.route_image(image)
```

## 📚 Documentation

Full documentation is available at [odysee.readthedocs.io](https://odysee.readthedocs.io/).

Key documentation sections:
- [Installation Guide](https://odysee.readthedocs.io/installation.html)
- [API Reference](https://odysee.readthedocs.io/api.html)
- [Examples & Tutorials](https://odysee.readthedocs.io/examples.html)
- [Performance Optimization](https://odysee.readthedocs.io/performance.html)

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please read our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## 📊 Benchmarks

| Model Size | Context Length | Memory Usage | Throughput |
|------------|---------------|--------------|------------|
| Small      | 1M tokens     | 8GB          | 1000 tok/s |
| Medium     | 2M tokens     | 16GB         | 800 tok/s  |
| Large      | 4M tokens     | 32GB         | 500 tok/s  |

## 🔬 Research

If you use Odysee in your research, please cite:

```bibtex
@software{odysee2024,
  title = {Odysee: High-Performance Multi-Modal Deep Learning Framework},
  author = {ThreatThriver Team},
  year = {2024},
  url = {https://github.com/threatthriver/odysee}
}
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=threatthriver/odysee&type=Date)](https://star-history.com/#threatthriver/odysee&Date)

## 📫 Contact

- GitHub Issues: For bug reports and feature requests
- Discussions: For questions and community discussions
- Email: support@threatthriver.com
