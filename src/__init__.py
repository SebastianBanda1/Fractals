"""
Fractal Visualizer - High-Performance Fractal Generation and Wallpaper Creator

A complete Python package for generating stunning fractal visualizations including
Mandelbrot sets, Julia sets, and other escape-time fractals. Features real-time
parameter adjustment, multiple color palettes, and high-resolution export
capabilities for creating beautiful wallpapers.
"""

from .fractal_engine import FractalEngine, FractalConfig
from .color_engine import ColorEngine, PaletteType
from .export_engine import ExportEngine, ResolutionPreset
from .web_interface import FractalApp

__version__ = "1.0.0"
__author__ = "Fractal Team"

__all__ = [
    'FractalEngine',
    'FractalConfig',
    'ColorEngine', 
    'PaletteType',
    'ExportEngine',
    'ResolutionPreset',
    'FractalApp',
]