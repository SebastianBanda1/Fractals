#!/usr/bin/env python3
"""
Test script to verify the fractal visualizer installation and basic functionality.
"""

import sys
import time
import traceback
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test that all modules can be imported."""
    print("🧪 Testing module imports...")
    
    try:
        from fractal_engine import FractalEngine, FractalConfig
        print("  Fractal engine imported successfully")
        
        from color_engine import ColorEngine, PaletteType
        print("  Color engine imported successfully")
        
        from export_engine import ExportEngine, ResolutionPreset
        print("  Export engine imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"  Import error: {e}")
        traceback.print_exc()
        return False


def test_fractal_generation():
    """Test basic fractal generation."""
    print("\\nTesting fractal generation...")
    
    try:
        from fractal_engine import FractalEngine, FractalConfig
        from color_engine import ColorEngine, PaletteType
        
        # Create engines
        fractal_engine = FractalEngine()
        color_engine = ColorEngine()
        
        # Create a small test fractal
        config = FractalConfig(
            width=100,
            height=100,
            max_iter=50,
            center_x=0.0,
            center_y=0.0,
            zoom=1.0
        )
        
        start_time = time.time()
        
        # Generate Mandelbrot set
        iterations = fractal_engine.generate_mandelbrot(config)
        print(f"  Mandelbrot generation: {time.time() - start_time:.3f}s")
        
        # Test coloring
        rgb_image = color_engine.apply_color_mapping(
            iterations, PaletteType.CLASSIC, smooth=True, max_iter=config.max_iter
        )
        print(f"  Color mapping successful")
        
        # Verify output shape
        expected_shape = (config.height, config.width, 3)
        if rgb_image.shape == expected_shape:
            print(f"  Output shape correct: {rgb_image.shape}")
        else:
            print(f"  Wrong shape: got {rgb_image.shape}, expected {expected_shape}")
            return False
            
        return True
        
    except Exception as e:
        print(f"  Fractal generation error: {e}")
        traceback.print_exc()
        return False


def test_julia_set():
    """Test Julia set generation."""
    print("\\n🌸 Testing Julia set generation...")
    
    try:
        from fractal_engine import FractalEngine, FractalConfig
        
        fractal_engine = FractalEngine()
        
        config = FractalConfig(width=50, height=50, max_iter=30)
        
        start_time = time.time()
        iterations = fractal_engine.generate_julia(-0.4, 0.6, config)
        
        print(f"  Julia set generation: {time.time() - start_time:.3f}s")
        print(f"  Output shape: {iterations.shape}")
        
        return True
        
    except Exception as e:
        print(f"  Julia set error: {e}")
        return False


def test_color_palettes():
    """Test different color palettes."""
    print("\\nTesting color palettes...")
    
    try:
        from color_engine import ColorEngine, PaletteType
        import numpy as np
        
        color_engine = ColorEngine()
        
        # Create test data
        test_iterations = np.random.randint(0, 100, (20, 20))
        
        # Test different palettes
        palettes_to_test = [
            PaletteType.CLASSIC,
            PaletteType.FIRE,
            PaletteType.OCEAN,
        ]
        
        for palette in palettes_to_test:
            rgb_image = color_engine.apply_color_mapping(
                test_iterations, palette, smooth=False, max_iter=100
            )
            print(f"  {palette.value} palette: {rgb_image.shape}")
        
        return True
        
    except Exception as e:
        print(f"  Color palette error: {e}")
        return False


def test_export_functionality():
    """Test export functionality."""
    print("\\n💾 Testing export functionality...")
    
    try:
        from export_engine import ExportEngine, ResolutionPreset
        import numpy as np
        
        export_engine = ExportEngine()
        
        # Create test image
        test_image = np.random.rand(100, 100, 3)
        
        # Test saving
        output_path = export_engine.save_image(
            test_image, 
            "test_fractal.png",
            subfolder="test"
        )
        
        print(f"  Image saved to: {output_path}")
        
        # Check if file exists
        if Path(output_path).exists():
            print("  Export file verification successful")
            # Clean up test file
            Path(output_path).unlink()
            print("  Test file cleaned up")
        else:
            print("  Export file not found")
            return False
            
        return True
        
    except Exception as e:
        print(f"  Export error: {e}")
        return False


def test_performance():
    """Test performance with different settings."""
    print("\\nTesting performance...")
    
    try:
        from fractal_engine import FractalEngine, FractalConfig
        
        fractal_engine = FractalEngine()
        
        # Test different sizes
        test_configs = [
            {"size": "Small", "width": 100, "height": 100, "max_iter": 50},
            {"size": "Medium", "width": 200, "height": 200, "max_iter": 100},
            {"size": "Large", "width": 400, "height": 400, "max_iter": 200},
        ]
        
        for test_config in test_configs:
            config = FractalConfig(
                width=test_config["width"],
                height=test_config["height"],
                max_iter=test_config["max_iter"]
            )
            
            start_time = time.time()
            iterations = fractal_engine.generate_mandelbrot(config)
            generation_time = time.time() - start_time
            
            pixels_per_second = (config.width * config.height) / generation_time
            
            print(f"  {test_config['size']} ({config.width}×{config.height}): "
                  f"{generation_time:.3f}s ({pixels_per_second:,.0f} pixels/sec)")
        
        return True
        
    except Exception as e:
        print(f"  Performance test error: {e}")
        return False


def main():
    """Run all tests."""
    print("Fractal Visualizer Installation Test")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Fractal Generation", test_fractal_generation),
        ("Julia Sets", test_julia_set),
        ("Color Palettes", test_color_palettes),
        ("Export Functionality", test_export_functionality),
        ("Performance", test_performance),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\\nRunning {test_name}...")
        try:
            if test_func():
                print(f"{test_name} PASSED")
                passed += 1
            else:
                print(f"{test_name} FAILED")
        except Exception as e:
            print(f"{test_name} CRASHED: {e}")
    
    print("\\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your fractal visualizer is ready to use.")
        print("\\nQuick start:")
        print("  python main.py                 # Launch web interface")
        print("  python examples/quick_start.py # Generate sample wallpaper")
    else:
        print(f" {total - passed} test(s) failed. Check the error messages above.")
        
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)