"""
Color Engine Module

Advanced color palette and gradient systems for fractal visualization.
Supports multiple color spaces, custom gradients, and artistic effects.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from typing import List, Tuple, Optional, Union
from enum import Enum
import colorcet as cc


class ColorSpace(Enum):
    """Available color spaces for palette generation."""
    RGB = "rgb"
    HSV = "hsv"
    LAB = "lab"
    LCH = "lch"


class PaletteType(Enum):
    """Predefined palette types."""
    CLASSIC = "classic"
    FIRE = "fire"
    OCEAN = "ocean"
    SUNSET = "sunset"
    COSMIC = "cosmic"
    ELECTRIC = "electric"
    MONOCHROME = "monochrome"
    PASTEL = "pastel"
    NEON = "neon"
    EARTH = "earth"
    ICE = "ice"
    RAINBOW = "rainbow"


def smooth_coloring(iterations: np.ndarray, max_iter: int, 
                   escape_radius: float = 2.0) -> np.ndarray:
    """
    Apply smooth coloring to remove banding artifacts.
    
    Args:
        iterations: Raw iteration counts
        max_iter: Maximum iterations used
        escape_radius: Escape radius used in computation
        
    Returns:
        Smoothed iteration values as floats
    """
    # Avoid division by zero
    mask = iterations < max_iter
    smoothed = iterations.astype(np.float64)
    
    # Apply smooth coloring formula where points escaped
    if np.any(mask):
        # This is a simplified smooth coloring - for full smoothing,
        # you'd need the final z values from the iteration
        smoothed[mask] = iterations[mask] + 1 - np.log2(np.log2(escape_radius))
    
    return smoothed


class ColorEngine:
    """
    Main color engine for generating beautiful fractal visualizations.
    """
    
    def __init__(self):
        """Initialize the color engine with default settings."""
        self.predefined_palettes = self._create_predefined_palettes()
    
    def _create_predefined_palettes(self) -> dict:
        """Create a collection of predefined color palettes."""
        palettes = {}
        
        # Classic Mandelbrot colors
        palettes[PaletteType.CLASSIC] = [
            (0.0, 0.0, 0.0),      # Black for set
            (0.0, 0.2, 0.5),      # Dark blue
            (0.0, 0.4, 1.0),      # Blue
            (0.0, 0.8, 1.0),      # Light blue
            (1.0, 1.0, 0.0),      # Yellow
            (1.0, 0.6, 0.0),      # Orange
            (1.0, 0.0, 0.0),      # Red
        ]
        
        # Fire palette
        palettes[PaletteType.FIRE] = [
            (0.0, 0.0, 0.0),      # Black
            (0.2, 0.0, 0.0),      # Dark red
            (0.5, 0.0, 0.0),      # Red
            (0.8, 0.2, 0.0),      # Orange-red
            (1.0, 0.5, 0.0),      # Orange
            (1.0, 0.8, 0.0),      # Yellow-orange
            (1.0, 1.0, 0.5),      # Light yellow
            (1.0, 1.0, 1.0),      # White
        ]
        
        # Ocean palette
        palettes[PaletteType.OCEAN] = [
            (0.0, 0.0, 0.1),      # Deep blue
            (0.0, 0.1, 0.3),      # Dark blue
            (0.0, 0.2, 0.5),      # Blue
            (0.0, 0.4, 0.7),      # Light blue
            (0.2, 0.6, 0.8),      # Sky blue
            (0.5, 0.8, 0.9),      # Light cyan
            (0.8, 0.95, 0.95),    # Almost white
        ]
        
        # Sunset palette
        palettes[PaletteType.SUNSET] = [
            (0.1, 0.0, 0.2),      # Dark purple
            (0.3, 0.1, 0.4),      # Purple
            (0.6, 0.2, 0.4),      # Pink-purple
            (0.8, 0.4, 0.3),      # Pink-orange
            (0.9, 0.6, 0.2),      # Orange
            (1.0, 0.8, 0.3),      # Yellow-orange
            (1.0, 0.9, 0.7),      # Light yellow
        ]
        
        # Cosmic palette
        palettes[PaletteType.COSMIC] = [
            (0.0, 0.0, 0.0),      # Black space
            (0.1, 0.0, 0.2),      # Dark purple
            (0.2, 0.0, 0.4),      # Purple
            (0.4, 0.2, 0.6),      # Light purple
            (0.6, 0.4, 0.8),      # Violet
            (0.8, 0.6, 0.9),      # Light violet
            (1.0, 0.8, 1.0),      # Almost white
        ]
        
        # Electric palette
        palettes[PaletteType.ELECTRIC] = [
            (0.0, 0.0, 0.0),      # Black
            (0.0, 0.1, 0.3),      # Dark blue
            (0.0, 0.3, 0.6),      # Blue
            (0.2, 0.5, 0.8),      # Light blue
            (0.5, 0.8, 1.0),      # Cyan
            (0.8, 1.0, 0.8),      # Light green
            (1.0, 1.0, 1.0),      # White
        ]
        
        # Monochrome palette
        palettes[PaletteType.MONOCHROME] = [
            (0.0, 0.0, 0.0),      # Black
            (0.2, 0.2, 0.2),      # Dark gray
            (0.4, 0.4, 0.4),      # Gray
            (0.6, 0.6, 0.6),      # Light gray
            (0.8, 0.8, 0.8),      # Lighter gray
            (1.0, 1.0, 1.0),      # White
        ]
        
        return palettes
    
    def create_custom_palette(self, colors: List[Tuple[float, float, float]], 
                            positions: Optional[List[float]] = None) -> mcolors.LinearSegmentedColormap:
        """
        Create a custom color palette from RGB color points.
        
        Args:
            colors: List of RGB tuples (values 0-1)
            positions: Optional list of positions (0-1) for each color
            
        Returns:
            Custom colormap
        """
        if positions is None:
            positions = np.linspace(0, 1, len(colors))
        
        # Create colormap dictionary
        cdict = {'red': [], 'green': [], 'blue': []}
        
        for i, (pos, color) in enumerate(zip(positions, colors)):
            cdict['red'].append((pos, color[0], color[0]))
            cdict['green'].append((pos, color[1], color[1]))
            cdict['blue'].append((pos, color[2], color[2]))
        
        return mcolors.LinearSegmentedColormap('custom', cdict)
    
    def get_palette(self, palette_type: Union[PaletteType, str]) -> mcolors.LinearSegmentedColormap:
        """
        Get a predefined color palette.
        
        Args:
            palette_type: Type of palette to retrieve
            
        Returns:
            Matplotlib colormap
        """
        if isinstance(palette_type, str):
            try:
                palette_type = PaletteType(palette_type.lower())
            except ValueError:
                palette_type = PaletteType.CLASSIC
        
        if palette_type in self.predefined_palettes:
            colors = self.predefined_palettes[palette_type]
            return self.create_custom_palette(colors)
        
        # Fallback to matplotlib colormaps
        palette_map = {
            PaletteType.RAINBOW: 'rainbow',
            PaletteType.ICE: 'winter',
            PaletteType.EARTH: 'terrain',
        }
        
        if palette_type in palette_map:
            return plt.get_cmap(palette_map[palette_type])
        
        return self.create_custom_palette(self.predefined_palettes[PaletteType.CLASSIC])
    
    def apply_color_mapping(self, iterations: np.ndarray, 
                          palette: Union[PaletteType, str, mcolors.Colormap],
                          smooth: bool = True,
                          max_iter: Optional[int] = None,
                          gamma: float = 1.0) -> np.ndarray:
        """
        Apply color mapping to iteration data.
        
        Args:
            iterations: Raw iteration counts
            palette: Color palette to use
            smooth: Whether to apply smooth coloring
            max_iter: Maximum iterations (needed for smooth coloring)
            gamma: Gamma correction factor
            
        Returns:
            RGB image array (height, width, 3)
        """
        # Get the colormap
        if isinstance(palette, (PaletteType, str)):
            cmap = self.get_palette(palette)
        else:
            cmap = palette
        
        # Apply smooth coloring if requested
        if smooth and max_iter is not None:
            colored_data = smooth_coloring(iterations, max_iter)
        else:
            colored_data = iterations.astype(np.float64)
        
        # Normalize the data
        if colored_data.max() > 0:
            normalized = colored_data / colored_data.max()
        else:
            normalized = colored_data
        
        # Apply gamma correction
        if gamma != 1.0:
            normalized = np.power(normalized, gamma)
        
        # Apply colormap
        rgb_image = cmap(normalized)[:, :, :3]  # Remove alpha channel
        
        return rgb_image
    
    def create_gradient_palette(self, start_color: Tuple[float, float, float],
                              end_color: Tuple[float, float, float],
                              steps: int = 256) -> mcolors.LinearSegmentedColormap:
        """
        Create a simple gradient palette between two colors.
        
        Args:
            start_color: Starting RGB color (0-1)
            end_color: Ending RGB color (0-1)
            steps: Number of steps in gradient
            
        Returns:
            Gradient colormap
        """
        colors = [start_color, end_color]
        return self.create_custom_palette(colors)
    
    def create_hsv_palette(self, hue_start: float, hue_end: float,
                          saturation: float = 1.0, value: float = 1.0,
                          steps: int = 256) -> mcolors.LinearSegmentedColormap:
        """
        Create a palette by varying hue in HSV color space.
        
        Args:
            hue_start: Starting hue (0-360)
            hue_end: Ending hue (0-360)
            saturation: Fixed saturation (0-1)
            value: Fixed value/brightness (0-1)
            steps: Number of steps
            
        Returns:
            HSV-based colormap
        """
        hues = np.linspace(hue_start / 360.0, hue_end / 360.0, steps)
        colors = []
        
        for hue in hues:
            rgb = mcolors.hsv_to_rgb((hue, saturation, value))
            colors.append(rgb)
        
        positions = np.linspace(0, 1, steps)
        return self.create_custom_palette(colors, positions.tolist())
    
    def enhance_image(self, rgb_image: np.ndarray, 
                     contrast: float = 1.0,
                     brightness: float = 0.0,
                     saturation: float = 1.0) -> np.ndarray:
        """
        Apply post-processing enhancements to the fractal image.
        
        Args:
            rgb_image: RGB image array
            contrast: Contrast factor (1.0 = no change)
            brightness: Brightness offset (-1 to 1)
            saturation: Saturation factor (1.0 = no change)
            
        Returns:
            Enhanced RGB image
        """
        enhanced = rgb_image.copy()
        
        # Apply contrast
        if contrast != 1.0:
            enhanced = ((enhanced - 0.5) * contrast) + 0.5
        
        # Apply brightness
        if brightness != 0.0:
            enhanced = enhanced + brightness
        
        # Apply saturation
        if saturation != 1.0:
            # Convert to HSV for saturation adjustment
            hsv = mcolors.rgb_to_hsv(enhanced)
            hsv[:, :, 1] *= saturation
            enhanced = mcolors.hsv_to_rgb(hsv)
        
        # Clip values to valid range
        enhanced = np.clip(enhanced, 0, 1)
        
        return enhanced
    
    def get_available_palettes(self) -> List[str]:
        """Get list of all available palette names."""
        predefined = [p.value for p in PaletteType]
        matplotlib_palettes = ['viridis', 'plasma', 'inferno', 'magma', 'cividis',
                             'twilight', 'twilight_shifted', 'hsv', 'turbo']
        return predefined + matplotlib_palettes
    
    def create_cyclic_palette(self, base_colors: List[Tuple[float, float, float]],
                            cycles: int = 1) -> mcolors.LinearSegmentedColormap:
        """
        Create a palette that cycles through colors multiple times.
        
        Args:
            base_colors: Base colors to cycle through
            cycles: Number of times to repeat the cycle
            
        Returns:
            Cyclic colormap
        """
        if cycles < 1:
            cycles = 1
        
        extended_colors = []
        extended_positions = []
        
        for cycle in range(cycles):
            start_pos = cycle / cycles
            end_pos = (cycle + 1) / cycles
            
            for i, color in enumerate(base_colors):
                pos = start_pos + (end_pos - start_pos) * (i / (len(base_colors) - 1))
                extended_colors.append(color)
                extended_positions.append(pos)
        
        return self.create_custom_palette(extended_colors, extended_positions)