#!/usr/bin/env python3
"""
High-Resolution Mandelbrot Deep Zoom

This example generates ultra-high resolution Mandelbrot images
with extreme zoom levels for detailed wallpapers.
"""

import sys
from pathlib import Path
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fractal_engine import FractalEngine, FractalConfig
from color_engine import ColorEngine, PaletteType
from export_engine import ExportEngine, ExportConfig


def main():
    """Generate high-resolution deep zoom Mandelbrot images."""
    print("🔍 High-Resolution Deep Zoom Generator")
    print("⚠️  Warning: This will generate large, detailed images!")
    
    # Create engines
    fractal_engine = FractalEngine()
    color_engine = ColorEngine()
    export_engine = ExportEngine()
    
    # Interesting zoom locations in the Mandelbrot set
    zoom_locations = [
        {
            'name': 'seahorse_valley_8k',
            'center_x': -0.7453,
            'center_y': 0.1127,
            'zoom': 2000.0,
            'width': 7680,
            'height': 4320,
            'max_iter': 1024,
            'palette': PaletteType.FIRE
        },
        {
            'name': 'elephant_valley_4k',
            'center_x': 0.25,
            'center_y': 0.0,
            'zoom': 100.0,
            'width': 3840,
            'height': 2160,
            'max_iter': 512,
            'palette': PaletteType.OCEAN
        },
        {
            'name': 'lightning_detail_4k',
            'center_x': -1.775,
            'center_y': 0.0,
            'zoom': 1000.0,
            'width': 3840,
            'height': 2160,
            'max_iter': 800,
            'palette': PaletteType.ELECTRIC
        }
    ]
    
    for location in zoom_locations:
        print(f"\n📍 Generating {location['name']}...")
        print(f"   Resolution: {location['width']}×{location['height']}")
        print(f"   Zoom: {location['zoom']}×")
        print(f"   Iterations: {location['max_iter']}")
        
        start_time = time.time()
        
        # Create configuration
        config = FractalConfig(
            width=location['width'],
            height=location['height'],
            max_iter=location['max_iter'],
            center_x=location['center_x'],
            center_y=location['center_y'],
            zoom=location['zoom']
        )
        
        # Estimate and display computation info
        total_pixels = config.width * config.height
        print(f"   Processing {total_pixels:,} pixels...")
        
        # Generate fractal with progress indication
        print("   🔄 Computing fractal...")
        iterations = fractal_engine.generate_mandelbrot(config)
        
        print("   🎨 Applying colors...")
        rgb_image = color_engine.apply_color_mapping(
            iterations,
            location['palette'],
            smooth=True,
            max_iter=config.max_iter,
            gamma=1.1
        )
        
        # Apply subtle enhancements
        print("   ✨ Enhancing image...")
        enhanced_image = color_engine.enhance_image(
            rgb_image,
            contrast=1.05,
            saturation=1.1
        )
        
        # Export with high quality settings
        print("   💾 Exporting...")
        export_config = ExportConfig(
            format="PNG",
            compression_level=3,  # Lower compression for max quality
            optimize=True
        )
        
        filename = f"{location['name']}_deepzoom.png"
        output_path = export_engine.save_image(
            enhanced_image,
            filename,
            export_config
        )
        
        generation_time = time.time() - start_time
        file_size = export_engine.estimate_file_size(
            config.width, config.height, "PNG"
        )
        
        print(f"   ✅ Complete! Generated in {generation_time:.1f}s")
        print(f"   📁 Saved: {output_path}")
        print(f"   📏 Estimated size: {file_size}")
    
    print("\n🎨 High-resolution deep zoom collection complete!")
    print("🖼️  These images are perfect for large displays and printing")


if __name__ == "__main__":
    main()