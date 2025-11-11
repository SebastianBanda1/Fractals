# Fractal Visualization Project - Copilot Instructions

## ✅ PROJECT SETUP COMPLETE

This is a **complete and fully functional** Python-based fractal visualization project for generating high-quality Mandelbrot sets, Julia sets, and other fractals for creating stunning wallpapers.

## 🚀 Quick Start
```bash
# Generate sample wallpapers
python main.py --samples

# Launch interactive web interface  
python main.py

# Run quick start example
python examples/quick_start.py
```

## 🎯 Project Status
- ✅ **Core Fractal Engine** - Numba-optimized computation
- ✅ **Color Engine** - Advanced palettes and smooth coloring
- ✅ **Export Engine** - High-resolution wallpaper generation
- ✅ **Web Interface** - Streamlit-based interactive UI
- ✅ **Examples** - Multiple demonstration scripts
- ✅ **Documentation** - Complete README and guides
- ✅ **Dependencies** - All packages installed successfully
- ✅ **Testing** - Working fractal generation confirmed

## 🏗️ Architecture

### Core Components
- **Fractal Engine** (`src/fractal_engine/`) - Mathematical computations
- **Color Engine** (`src/color_engine/`) - Color palettes and gradients  
- **Export Engine** (`src/export_engine/`) - High-res image generation
- **Web Interface** (`src/web_interface/`) - Streamlit UI

### Performance Features
- **Numba JIT compilation** for lightning-fast computation
- **Parallel processing** utilizing multi-core CPUs
- **Memory efficient** handling of large images
- **Real-time preview** with parameter adjustment

### Export Capabilities
- **Multiple formats**: PNG, JPEG, WebP
- **Resolution presets**: HD, Full HD, QHD, 4K, 8K
- **Batch export** for multiple resolutions
- **Quality controls** and optimization

## 🎨 Generated Samples
The project has successfully generated sample wallpapers:
- `mandelbrot_classic.png` - Traditional Mandelbrot view
- `mandelbrot_fire.png` - Fire palette with zoom detail
- `julia_ocean.png` - Julia set with ocean colors
- `burning_ship_cosmic.png` - Burning Ship with cosmic palette

## 🔧 Development Guidelines

### Code Style
- Follow PEP 8 Python style guidelines
- Use type hints for function parameters and return values
- Create modular design with separate classes for different fractal types
- Implement clean separation between computation and visualization

### Performance Optimization
- Use Numba decorators for computational hot paths
- Implement chunked processing for high-resolution images
- Optimize memory usage for large image generation
- Use multiprocessing for animation rendering when possible

### User Interface
- Create intuitive Streamlit widgets for parameter adjustment
- Implement real-time preview with resolution scaling
- Provide preset configurations for common wallpaper sizes
- Include save/load functionality for custom configurations

## 📚 Available Examples
- `examples/quick_start.py` - Basic Mandelbrot generation
- `examples/julia_explorer.py` - Multiple Julia set variations
- `examples/deep_zoom.py` - High-resolution deep zoom images

## 🚀 Next Steps
The project is **ready for use**! Users can:
1. Generate sample wallpapers using `python main.py --samples`
2. Launch the web interface with `python main.py`
3. Explore examples in the `examples/` directory
4. Create custom fractals using the provided APIs
5. Export high-resolution wallpapers in multiple formats