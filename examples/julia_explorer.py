#!/usr/bin/env python3
"""
Julia Set Explorer - Generate Beautiful Julia Set Variations

This example creates multiple Julia sets with different parameters.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fractal_engine import FractalEngine, FractalConfig
from color_engine import ColorEngine, PaletteType
from export_engine import ExportEngine


def main():
    """Generate a collection of Julia set wallpapers."""
    print("🌸 Julia Set Explorer: Creating beautiful variations...")
    
    # Create engines
    fractal_engine = FractalEngine()
    color_engine = ColorEngine()
    export_engine = ExportEngine()
    
    # Julia set parameters - each creates a different shape
    julia_sets = [
        {'c_real': -0.4, 'c_imag': 0.6, 'name': 'spiral', 'palette': PaletteType.OCEAN},
        {'c_real': -0.8, 'c_imag': 0.156, 'name': 'lightning', 'palette': PaletteType.ELECTRIC},
        {'c_real': -0.7269, 'c_imag': 0.1889, 'name': 'dragon', 'palette': PaletteType.FIRE},
        {'c_real': 0.285, 'c_imag': 0.01, 'name': 'flower', 'palette': PaletteType.SUNSET},
        {'c_real': -0.123, 'c_imag': 0.745, 'name': 'crystal', 'palette': PaletteType.COSMIC},
    ]
    
    # Configuration for high-quality output
    config = FractalConfig(
        width=2560,   # QHD resolution
        height=1440,
        max_iter=512,  # High detail
        center_x=0.0,
        center_y=0.0,
        zoom=1.0
    )
    
    for julia_set in julia_sets:
        print(f"  Generating {julia_set['name']} Julia set...")
        
        # Generate Julia set
        iterations = fractal_engine.generate_julia(
            julia_set['c_real'], 
            julia_set['c_imag'], 
            config
        )
        
        # Apply colors with smooth gradients
        rgb_image = color_engine.apply_color_mapping(
            iterations,
            julia_set['palette'],
            smooth=True,
            max_iter=config.max_iter,
            gamma=1.2  # Slight gamma for better contrast
        )
        
        # Enhance the image
        enhanced_image = color_engine.enhance_image(
            rgb_image,
            contrast=1.1,
            saturation=1.2
        )
        
        # Export with multiple resolutions
        filename = f"julia_{julia_set['name']}"
        export_engine.save_wallpaper_set(
            enhanced_image,
            filename,
            resolutions=['Full HD', 'QHD', '4K']
        )
        
        print(f"    ✅ Exported {julia_set['name']} in multiple resolutions")
    
    print("\n🎨 Julia set collection complete!")
    print("📁 Check the output/wallpapers/ directory for your images")


if __name__ == "__main__":
    main()