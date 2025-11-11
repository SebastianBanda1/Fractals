"""
Fractal Engine Core Module

High-performance fractal computation engine with Numba JIT compilation.
Supports Mandelbrot sets, Julia sets, and other escape-time fractals.
"""

import numpy as np
import numba
from typing import Tuple, Optional, Union
from dataclasses import dataclass


@dataclass
class FractalConfig:
    """Configuration for fractal generation."""
    width: int = 1920
    height: int = 1080
    max_iter: int = 256
    escape_radius: float = 2.0
    center_x: float = 0.0
    center_y: float = 0.0
    zoom: float = 1.0
    
    @property
    def aspect_ratio(self) -> float:
        return self.width / self.height


@numba.jit(nopython=True, cache=True)
def mandelbrot_point(c_real: float, c_imag: float, max_iter: int, escape_radius: float) -> int:
    """
    Calculate the number of iterations for a single point in the Mandelbrot set.
    
    Args:
        c_real: Real part of the complex number
        c_imag: Imaginary part of the complex number
        max_iter: Maximum number of iterations
        escape_radius: Escape radius threshold
        
    Returns:
        Number of iterations before escape (max_iter if point doesn't escape)
    """
    z_real = 0.0
    z_imag = 0.0
    
    for i in range(max_iter):
        if z_real * z_real + z_imag * z_imag > escape_radius * escape_radius:
            return i
        
        # z = z^2 + c
        new_real = z_real * z_real - z_imag * z_imag + c_real
        new_imag = 2.0 * z_real * z_imag + c_imag
        
        z_real = new_real
        z_imag = new_imag
    
    return max_iter


@numba.jit(nopython=True, cache=True)
def julia_point(z_real: float, z_imag: float, c_real: float, c_imag: float, 
                max_iter: int, escape_radius: float) -> int:
    """
    Calculate the number of iterations for a single point in a Julia set.
    
    Args:
        z_real: Real part of the initial z value
        z_imag: Imaginary part of the initial z value
        c_real: Real part of the Julia set parameter
        c_imag: Imaginary part of the Julia set parameter
        max_iter: Maximum number of iterations
        escape_radius: Escape radius threshold
        
    Returns:
        Number of iterations before escape
    """
    for i in range(max_iter):
        if z_real * z_real + z_imag * z_imag > escape_radius * escape_radius:
            return i
        
        # z = z^2 + c
        new_real = z_real * z_real - z_imag * z_imag + c_real
        new_imag = 2.0 * z_real * z_imag + c_imag
        
        z_real = new_real
        z_imag = new_imag
    
    return max_iter


@numba.jit(nopython=True, cache=True)
def burning_ship_point(c_real: float, c_imag: float, max_iter: int, escape_radius: float) -> int:
    """
    Calculate the number of iterations for a single point in the Burning Ship fractal.
    
    Args:
        c_real: Real part of the complex number
        c_imag: Imaginary part of the complex number
        max_iter: Maximum number of iterations
        escape_radius: Escape radius threshold
        
    Returns:
        Number of iterations before escape
    """
    z_real = 0.0
    z_imag = 0.0
    
    for i in range(max_iter):
        if z_real * z_real + z_imag * z_imag > escape_radius * escape_radius:
            return i
        
        # z = (|Re(z)| + i|Im(z)|)^2 + c
        z_real_abs = abs(z_real)
        z_imag_abs = abs(z_imag)
        
        new_real = z_real_abs * z_real_abs - z_imag_abs * z_imag_abs + c_real
        new_imag = 2.0 * z_real_abs * z_imag_abs + c_imag
        
        z_real = new_real
        z_imag = new_imag
    
    return max_iter


@numba.jit(nopython=True, cache=True, parallel=True)
def compute_mandelbrot(width: int, height: int, center_x: float, center_y: float, 
                      zoom: float, max_iter: int, escape_radius: float) -> np.ndarray:
    """
    Compute the Mandelbrot set for the entire image using parallel processing.
    
    Args:
        width: Image width in pixels
        height: Image height in pixels
        center_x: X coordinate of the center point
        center_y: Y coordinate of the center point
        zoom: Zoom factor (higher = more zoomed in)
        max_iter: Maximum number of iterations
        escape_radius: Escape radius threshold
        
    Returns:
        2D array of iteration counts
    """
    result = np.zeros((height, width), dtype=np.int32)
    
    # Calculate the complex plane bounds
    aspect_ratio = width / height
    half_width = 2.0 / zoom
    half_height = half_width / aspect_ratio
    
    x_min = center_x - half_width
    x_max = center_x + half_width
    y_min = center_y - half_height
    y_max = center_y + half_height
    
    # Parallel computation
    for row in numba.prange(height):
        y = y_min + (y_max - y_min) * row / (height - 1)
        
        for col in range(width):
            x = x_min + (x_max - x_min) * col / (width - 1)
            result[row, col] = mandelbrot_point(x, y, max_iter, escape_radius)
    
    return result


@numba.jit(nopython=True, cache=True, parallel=True)
def compute_julia(width: int, height: int, center_x: float, center_y: float, 
                 zoom: float, c_real: float, c_imag: float, max_iter: int, 
                 escape_radius: float) -> np.ndarray:
    """
    Compute a Julia set for the entire image using parallel processing.
    
    Args:
        width: Image width in pixels
        height: Image height in pixels
        center_x: X coordinate of the center point
        center_y: Y coordinate of the center point
        zoom: Zoom factor
        c_real: Real part of the Julia set parameter
        c_imag: Imaginary part of the Julia set parameter
        max_iter: Maximum number of iterations
        escape_radius: Escape radius threshold
        
    Returns:
        2D array of iteration counts
    """
    result = np.zeros((height, width), dtype=np.int32)
    
    # Calculate the complex plane bounds
    aspect_ratio = width / height
    half_width = 2.0 / zoom
    half_height = half_width / aspect_ratio
    
    x_min = center_x - half_width
    x_max = center_x + half_width
    y_min = center_y - half_height
    y_max = center_y + half_height
    
    # Parallel computation
    for row in numba.prange(height):
        y = y_min + (y_max - y_min) * row / (height - 1)
        
        for col in range(width):
            x = x_min + (x_max - x_min) * col / (width - 1)
            result[row, col] = julia_point(x, y, c_real, c_imag, max_iter, escape_radius)
    
    return result


@numba.jit(nopython=True, cache=True, parallel=True)
def compute_burning_ship(width: int, height: int, center_x: float, center_y: float, 
                        zoom: float, max_iter: int, escape_radius: float) -> np.ndarray:
    """
    Compute the Burning Ship fractal for the entire image.
    
    Args:
        width: Image width in pixels
        height: Image height in pixels
        center_x: X coordinate of the center point
        center_y: Y coordinate of the center point
        zoom: Zoom factor
        max_iter: Maximum number of iterations
        escape_radius: Escape radius threshold
        
    Returns:
        2D array of iteration counts
    """
    result = np.zeros((height, width), dtype=np.int32)
    
    # Calculate the complex plane bounds
    aspect_ratio = width / height
    half_width = 2.0 / zoom
    half_height = half_width / aspect_ratio
    
    x_min = center_x - half_width
    x_max = center_x + half_width
    y_min = center_y - half_height
    y_max = center_y + half_height
    
    # Parallel computation
    for row in numba.prange(height):
        y = y_min + (y_max - y_min) * row / (height - 1)
        
        for col in range(width):
            x = x_min + (x_max - x_min) * col / (width - 1)
            result[row, col] = burning_ship_point(x, y, max_iter, escape_radius)
    
    return result


class FractalEngine:
    """
    Main fractal computation engine with support for multiple fractal types.
    """
    
    def __init__(self, config: Optional[FractalConfig] = None):
        """
        Initialize the fractal engine.
        
        Args:
            config: Fractal configuration. If None, uses default config.
        """
        self.config = config or FractalConfig()
    
    def generate_mandelbrot(self, config: Optional[FractalConfig] = None) -> np.ndarray:
        """Generate Mandelbrot set with current or provided configuration."""
        cfg = config or self.config
        return compute_mandelbrot(
            cfg.width, cfg.height, cfg.center_x, cfg.center_y,
            cfg.zoom, cfg.max_iter, cfg.escape_radius
        )
    
    def generate_julia(self, c_real: float, c_imag: float, 
                      config: Optional[FractalConfig] = None) -> np.ndarray:
        """Generate Julia set with given parameters."""
        cfg = config or self.config
        return compute_julia(
            cfg.width, cfg.height, cfg.center_x, cfg.center_y,
            cfg.zoom, c_real, c_imag, cfg.max_iter, cfg.escape_radius
        )
    
    def generate_burning_ship(self, config: Optional[FractalConfig] = None) -> np.ndarray:
        """Generate Burning Ship fractal."""
        cfg = config or self.config
        return compute_burning_ship(
            cfg.width, cfg.height, cfg.center_x, cfg.center_y,
            cfg.zoom, cfg.max_iter, cfg.escape_radius
        )
    
    def set_config(self, config: FractalConfig):
        """Update the fractal configuration."""
        self.config = config
    
    def get_interesting_points(self, fractal_type: str = "mandelbrot") -> list[dict]:
        """
        Get a list of interesting points to explore for each fractal type.
        
        Returns:
            List of dictionaries with 'name', 'center_x', 'center_y', 'zoom' keys
        """
        if fractal_type.lower() == "mandelbrot":
            return [
                {"name": "Overview", "center_x": -0.5, "center_y": 0.0, "zoom": 1.0},
                {"name": "Seahorse Valley", "center_x": -0.75, "center_y": 0.1, "zoom": 50.0},
                {"name": "Elephant Valley", "center_x": 0.25, "center_y": 0.0, "zoom": 100.0},
                {"name": "Lightning", "center_x": -1.775, "center_y": 0.0, "zoom": 1000.0},
                {"name": "Spiral", "center_x": -0.7456, "center_y": 0.1130, "zoom": 2000.0},
                {"name": "Feather", "center_x": -0.2, "center_y": 0.8, "zoom": 500.0},
            ]
        elif fractal_type.lower() == "burning_ship":
            return [
                {"name": "Overview", "center_x": -1.8, "center_y": -0.1, "zoom": 1.0},
                {"name": "Ship Detail", "center_x": -1.75, "center_y": -0.03, "zoom": 100.0},
                {"name": "Mast", "center_x": -1.62, "center_y": -0.0405, "zoom": 2000.0},
            ]
        else:
            return [{"name": "Center", "center_x": 0.0, "center_y": 0.0, "zoom": 1.0}]