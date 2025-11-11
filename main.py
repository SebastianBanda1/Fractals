#!/usr/bin/env python3
"""
Main entry point for the Fractal Visualizer application.

This script provides command-line interface and launches the web interface.
"""

import argparse
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.fractal_engine import FractalEngine, FractalConfig
from src.color_engine import ColorEngine, PaletteType  
from src.export_engine import ExportEngine, ResolutionPreset
from src.web_interface import main as run_web_interface


def generate_sample_wallpapers():
    """Generate a set of sample wallpapers with different fractals and colors."""
    print("Generating sample fractal wallpapers...")
    
    # Initialize engines
    fractal_engine = FractalEngine()
    color_engine = ColorEngine()
    export_engine = ExportEngine()
    
    # Sample configurations
    samples = [
        {
            'name': 'mandelbrot_classic',
            'type': 'mandelbrot',
            'config': FractalConfig(width=1920, height=1080, max_iter=256, zoom=1.0),
            'palette': PaletteType.CLASSIC
        },
        {
            'name': 'mandelbrot_fire',
            'type': 'mandelbrot', 
            'config': FractalConfig(width=1920, height=1080, max_iter=512, 
                                   center_x=-0.75, center_y=0.1, zoom=50.0),
            'palette': PaletteType.FIRE
        },
        {
            'name': 'julia_ocean',
            'type': 'julia',
            'config': FractalConfig(width=1920, height=1080, max_iter=256),
            'palette': PaletteType.OCEAN,
            'julia_params': {'c_real': -0.4, 'c_imag': 0.6}
        },
        {
            'name': 'burning_ship_cosmic',
            'type': 'burning_ship',
            'config': FractalConfig(width=1920, height=1080, max_iter=256,
                                   center_x=-1.8, center_y=-0.1, zoom=1.0),
            'palette': PaletteType.COSMIC
        }
    ]
    
    for sample in samples:
        print(f"  Generating {sample['name']}...")
        
        # Generate fractal data
        if sample['type'] == 'mandelbrot':
            iterations = fractal_engine.generate_mandelbrot(sample['config'])
        elif sample['type'] == 'julia':
            iterations = fractal_engine.generate_julia(
                sample['julia_params']['c_real'],
                sample['julia_params']['c_imag'], 
                sample['config']
            )
        elif sample['type'] == 'burning_ship':
            iterations = fractal_engine.generate_burning_ship(sample['config'])
        
        # Apply colors
        rgb_image = color_engine.apply_color_mapping(
            iterations, sample['palette'], smooth=True, 
            max_iter=sample['config'].max_iter
        )
        
        # Export as wallpaper
        export_engine.save_image(
            rgb_image, 
            f"{sample['name']}.png",
            subfolder="samples"
        )
    
    print("Sample wallpapers generated in output/samples/")


def main():
    """Main entry point with command line interface."""
    parser = argparse.ArgumentParser(
        description="Fractal Visualizer - Generate stunning fractal wallpapers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Launch web interface
  python main.py --web              # Launch web interface  
  python main.py --samples          # Generate sample wallpapers
  python main.py --cli              # Interactive CLI mode

For more information, visit: https://github.com/fractals/fractal-visualizer
        """
    )
    
    parser.add_argument(
        '--web', action='store_true',
        help='Launch the web interface (default)'
    )
    
    parser.add_argument(
        '--samples', action='store_true', 
        help='Generate sample wallpapers'
    )
    
    parser.add_argument(
        '--cli', action='store_true',
        help='Launch interactive CLI mode'
    )
    
    parser.add_argument(
        '--version', action='version',
        version='Fractal Visualizer 1.0.0'
    )
    
    args = parser.parse_args()
    
    # Welcome message
    print("Fractal Visualizer - High-Performance Wallpaper Generator")
    print("=" * 60)
    
    try:
        if args.samples:
            generate_sample_wallpapers()
        elif args.cli:
            print("Interactive CLI mode not yet implemented.")
            print("Use --web to launch the web interface instead.")
        else:
            # Default to web interface
            print("Launching web interface...")
            print("Open your browser to the URL shown below:")
            print()
            run_web_interface()
            
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()