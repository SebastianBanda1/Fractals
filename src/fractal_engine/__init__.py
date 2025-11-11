"""
Fractal Engine Package

High-performance fractal computation with Numba acceleration.
"""

from .core import FractalEngine, FractalConfig
from .core import compute_mandelbrot, compute_julia, compute_burning_ship

__all__ = [
    'FractalEngine',
    'FractalConfig', 
    'compute_mandelbrot',
    'compute_julia',
    'compute_burning_ship',
]