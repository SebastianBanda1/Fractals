# 🌀 Fractal Visualizer

**High-Performance Fractal Generation and Wallpaper Creator**

Generate stunning fractal visualizations including Mandelbrot sets, Julia sets, and other escape-time fractals. Features real-time parameter adjustment, multiple color palettes, and high-resolution export capabilities for creating beautiful wallpapers.

![Fractal Examples](assets/fractal_preview.png)

## ✨ Features

### 🎨 **Multiple Fractal Types**
- **Mandelbrot Set** - The classic fractal with infinite detail
- **Julia Sets** - Beautiful variations with complex parameters  
- **Burning Ship** - Dramatic fractal resembling a ship
- **Extensible** - Easy to add new fractal algorithms

### 🌈 **Advanced Color Engine**
- **Predefined Palettes** - Classic, Fire, Ocean, Sunset, Cosmic, Electric, and more
- **Custom Gradients** - Create your own color schemes
- **Smooth Coloring** - Eliminates banding artifacts
- **Color Enhancement** - Contrast, brightness, and saturation controls
- **Multiple Color Spaces** - RGB, HSV, LAB support

### 🖼️ **High-Resolution Export**
- **Multiple Resolutions** - HD, Full HD, QHD, 4K, 8K support
- **Wallpaper Presets** - Standard desktop and mobile sizes
- **Format Options** - PNG, JPEG, WebP export
- **Batch Export** - Generate multiple resolutions at once
- **Quality Controls** - Compression and optimization settings

### 🚀 **Performance Optimized**
- **Numba JIT Compilation** - Lightning-fast computation
- **Parallel Processing** - Multi-core CPU utilization
- **Memory Efficient** - Handles large images smoothly
- **Real-time Preview** - Interactive parameter adjustment

### 🌐 **Interactive Web Interface**
- **Streamlit-based UI** - Beautiful, intuitive interface
- **Real-time Generation** - See changes instantly
- **Parameter Controls** - Zoom, pan, color adjustments
- **Preset Points** - Explore interesting fractal locations
- **Export Integration** - Direct wallpaper generation

## 🚀 Quick Start

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/fractals/fractal-visualizer.git
   cd fractal-visualizer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the web interface**
   ```bash
   python main.py
   ```

4. **Open your browser** to the displayed URL (usually `http://localhost:8501`)

### Command Line Usage

```bash
# Launch web interface (default)
python main.py

# Generate sample wallpapers
python main.py --samples

# Show help
python main.py --help
```

## 📖 Examples

### Basic Mandelbrot Generation

```python
from src.fractal_engine import FractalEngine, FractalConfig
from src.color_engine import ColorEngine, PaletteType
from src.export_engine import ExportEngine

# Create engines
fractal_engine = FractalEngine()
color_engine = ColorEngine()
export_engine = ExportEngine()

# Configure fractal
config = FractalConfig(
    width=1920, height=1080,
    max_iter=256, zoom=1.0
)

# Generate Mandelbrot set
iterations = fractal_engine.generate_mandelbrot(config)

# Apply colors
rgb_image = color_engine.apply_color_mapping(
    iterations, PaletteType.FIRE, smooth=True
)

# Export as wallpaper
export_engine.save_image(rgb_image, \"mandelbrot.png\")
```

### Interactive Web Interface

The web interface provides:

- **Real-time fractal generation** with parameter sliders
- **Multiple fractal types** with easy switching
- **Color palette selection** with live preview
- **Zoom and pan controls** for exploration
- **Export options** for multiple resolutions
- **Preset interesting points** to explore

![Web Interface](assets/web_interface.png)

### Batch Wallpaper Generation

```python
# Generate wallpapers in multiple resolutions
resolutions = ['Full HD', 'QHD', '4K', 'Ultrawide 2K']
saved_files = export_engine.save_wallpaper_set(
    rgb_image, \"my_fractal\", resolutions
)
```

## 🎨 Color Palettes

### Predefined Palettes

| Palette | Description | Best For |
|---------|-------------|----------|
| Classic | Traditional Mandelbrot colors | Classic fractals |
| Fire | Warm oranges and reds | Dramatic effects |
| Ocean | Cool blues and cyans | Calm, flowing fractals |
| Sunset | Purple to yellow gradient | Artistic wallpapers |
| Cosmic | Deep purples and violets | Space-themed images |
| Electric | Blue to white lightning | High-contrast details |
| Monochrome | Grayscale gradient | Minimalist designs |

### Custom Palettes

```python
# Create custom gradient
custom_palette = color_engine.create_gradient_palette(
    start_color=(0.1, 0.0, 0.2),  # Dark purple
    end_color=(1.0, 0.8, 0.3)     # Gold
)

# Apply to fractal
rgb_image = color_engine.apply_color_mapping(
    iterations, custom_palette
)
```

## 📐 Resolution Presets

### Desktop Wallpapers
- **HD**: 1280×720
- **Full HD**: 1920×1080  
- **QHD**: 2560×1440
- **4K**: 3840×2160
- **8K**: 7680×4320

### Ultrawide Support
- **Ultrawide 2K**: 3440×1440
- **Ultrawide 4K**: 5120×2160

### Mobile Wallpapers
- **Mobile HD**: 720×1280
- **Mobile FHD**: 1080×1920
- **Mobile QHD**: 1440×2560

### Custom Resolutions
```python
# Any custom resolution
custom_config = FractalConfig(width=5000, height=3000)
```

## 🔍 Interesting Fractal Locations

### Mandelbrot Set Highlights

| Location | Coordinates | Zoom | Description |
|----------|-------------|------|-------------|
| Overview | (-0.5, 0.0) | 1× | Classic full view |
| Seahorse Valley | (-0.75, 0.1) | 50× | Intricate seahorse patterns |
| Elephant Valley | (0.25, 0.0) | 100× | Elephant-like bulb detail |
| Lightning | (-1.775, 0.0) | 1000× | Lightning-like tendrils |
| Spiral | (-0.7456, 0.113) | 2000× | Beautiful spiral formations |

### Julia Set Favorites

```python
# Beautiful Julia set parameters
julia_params = [
    {'c_real': -0.4, 'c_imag': 0.6},    # Spiral dragon
    {'c_real': -0.8, 'c_imag': 0.156},  # Lightning bolt
    {'c_real': 0.285, 'c_imag': 0.01},  # Flower pattern
    {'c_real': -0.123, 'c_imag': 0.745} # Crystal formation
]
```

## 🛠️ Advanced Usage

### Performance Tuning

```python
# For real-time exploration (faster)
preview_config = FractalConfig(
    width=800, height=600,
    max_iter=128
)

# For final wallpapers (higher quality)  
export_config = FractalConfig(
    width=3840, height=2160,
    max_iter=1024
)
```

### Color Enhancement

```python
# Apply post-processing effects
enhanced_image = color_engine.enhance_image(
    rgb_image,
    contrast=1.2,      # Increase contrast
    brightness=0.1,    # Slight brightness boost
    saturation=1.3     # More vivid colors
)
```

### Custom Export Settings

```python
# High-quality PNG export
export_config = ExportConfig(
    format=\"PNG\",
    compression_level=3,  # Lower = better quality
    optimize=True
)

# High-quality JPEG export
export_config = ExportConfig(
    format=\"JPEG\", 
    quality=98,
    optimize=True
)
```

## 📊 Performance Benchmarks

| Resolution | Iterations | Generation Time* | File Size (PNG) |
|------------|------------|------------------|-----------------|
| 1920×1080 | 256 | ~2-5 seconds | ~8-15 MB |
| 2560×1440 | 256 | ~4-8 seconds | ~15-25 MB |
| 3840×2160 | 512 | ~15-30 seconds | ~35-60 MB |
| 7680×4320 | 1024 | ~60-120 seconds | ~150-300 MB |

*Times vary based on CPU and fractal complexity

## 🏗️ Project Structure

```
fractales/
├── src/                          # Source code
│   ├── fractal_engine/           # Core fractal computation
│   │   ├── core.py              # Mandelbrot, Julia, Burning Ship
│   │   └── __init__.py
│   ├── color_engine/             # Color palettes and mapping
│   │   ├── palettes.py          # Color palette definitions
│   │   └── __init__.py
│   ├── export_engine/            # Image export and formatting
│   │   ├── exporter.py          # High-res export functionality
│   │   └── __init__.py
│   ├── web_interface/            # Streamlit web UI
│   │   ├── app.py               # Main Streamlit application
│   │   └── __init__.py
│   └── __init__.py
├── examples/                     # Example scripts
│   ├── quick_start.py           # Basic Mandelbrot generation
│   ├── julia_explorer.py        # Julia set variations
│   └── deep_zoom.py             # High-resolution deep zooms
├── tests/                        # Unit tests
├── docs/                         # Documentation
├── assets/                       # Images and resources
├── output/                       # Generated wallpapers
│   ├── wallpapers/              # Final wallpaper exports
│   ├── previews/                # Low-res previews
│   └── settings/                # Saved configurations
├── main.py                       # Main entry point
├── requirements.txt              # Python dependencies
├── pyproject.toml               # Project configuration
└── README.md                    # This file
```

## 🔧 Dependencies

### Core Dependencies
- **NumPy** - Numerical computations
- **Numba** - JIT compilation for performance
- **Matplotlib** - Color mapping and palettes
- **Pillow** - Image processing and export
- **Streamlit** - Web interface

### Optional Dependencies
- **SciPy** - Advanced mathematical functions
- **OpenCV** - Additional image processing
- **Plotly** - Interactive plots
- **ImageIO** - Animation support

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

1. **Fork and clone** the repository
2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```
3. **Install development dependencies**
   ```bash
   pip install -e .[dev]
   ```
4. **Run tests**
   ```bash
   pytest
   ```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Benoit Mandelbrot** - For discovering the Mandelbrot set
- **Gaston Julia** - For Julia set mathematics  
- **NumPy/SciPy community** - For excellent scientific computing tools
- **Streamlit team** - For the beautiful web framework

## 📞 Support

- **Documentation**: [Read the Docs](https://fractal-visualizer.readthedocs.io)
- **Issues**: [GitHub Issues](https://github.com/fractals/fractal-visualizer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/fractals/fractal-visualizer/discussions)

---

**Happy fractal generation! 🌀✨**