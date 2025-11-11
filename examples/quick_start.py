#!/usr/bin/env python3
"""
Quick Start Example - Generate a Basic Mandelbrot Wallpaper

This example shows how to quickly generate a Mandelbrot set wallpaper.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fractal_engine import FractalEngine, FractalConfig
from color_engine import ColorEngine, PaletteType
from export_engine import ExportEngine, ResolutionPreset


def main():
    """Generate a basic Mandelbrot wallpaper."""
    print("🌀 Quick Start: Generating Mandelbrot wallpaper...")
    
    # Create engines
    fractal_engine = FractalEngine()
    color_engine = ColorEngine()
    export_engine = ExportEngine()
    
    # Configure fractal (Full HD resolution)
    config = FractalConfig(
        width=1920,
        height=1080,
        max_iter=256,
        center_x=-0.5,  # Classic Mandelbrot view
        center_y=0.0,
        zoom=1.0
    )
    
    # Generate the Mandelbrot set
    print("  Computing fractal...")
    iterations = fractal_engine.generate_mandelbrot(config)
    
    # Apply beautiful colors
    print("  Applying colors...")
    rgb_image = color_engine.apply_color_mapping(
        iterations, 
        PaletteType.FIRE,  # Use fire palette
        smooth=True,
        max_iter=config.max_iter
    )
    
    # Export as wallpaper
    print("  Exporting image...")
    output_path = export_engine.save_image(
        rgb_image, 
        "mandelbrot_quickstart.png"
    )
    
    print(f"✅ Wallpaper saved to: {output_path}")
    print("🎨 Open the image to see your fractal wallpaper!")


if __name__ == "__main__":
    main()