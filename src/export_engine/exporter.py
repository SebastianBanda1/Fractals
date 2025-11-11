"""
Export Engine Module

High-resolution image generation and export functionality for wallpapers.
Supports multiple formats and resolution presets.
"""

import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
import os
from typing import Tuple, Optional, Union, Dict
from dataclasses import dataclass
from pathlib import Path
import json
from datetime import datetime


@dataclass
class ExportConfig:
    """Configuration for image export."""
    format: str = "PNG"
    quality: int = 95  # For JPEG
    dpi: int = 300
    compression_level: int = 6  # For PNG
    optimize: bool = True
    add_metadata: bool = True


class ResolutionPreset:
    """Standard resolution presets for wallpapers."""
    
    # Common wallpaper resolutions
    HD = (1280, 720)
    FULL_HD = (1920, 1080) 
    QHD = (2560, 1440)
    UHD_4K = (3840, 2160)
    UHD_8K = (7680, 4320)
    
    # Ultrawide resolutions
    ULTRAWIDE_2K = (3440, 1440)
    ULTRAWIDE_4K = (5120, 2160)
    
    # Mobile resolutions
    MOBILE_HD = (720, 1280)
    MOBILE_FHD = (1080, 1920)
    MOBILE_QHD = (1440, 2560)
    
    # Square and custom ratios
    SQUARE_1K = (1024, 1024)
    SQUARE_2K = (2048, 2048)
    SQUARE_4K = (4096, 4096)
    
    @classmethod
    def get_all_presets(cls) -> Dict[str, Tuple[int, int]]:
        """Get all available resolution presets."""
        return {
            'HD': cls.HD,
            'Full HD': cls.FULL_HD,
            'QHD': cls.QHD,
            '4K': cls.UHD_4K,
            '8K': cls.UHD_8K,
            'Ultrawide 2K': cls.ULTRAWIDE_2K,
            'Ultrawide 4K': cls.ULTRAWIDE_4K,
            'Mobile HD': cls.MOBILE_HD,
            'Mobile FHD': cls.MOBILE_FHD,
            'Mobile QHD': cls.MOBILE_QHD,
            'Square 1K': cls.SQUARE_1K,
            'Square 2K': cls.SQUARE_2K,
            'Square 4K': cls.SQUARE_4K,
        }


class ExportEngine:
    """
    Main export engine for generating high-quality fractal images.
    """
    
    def __init__(self, output_dir: str = "output"):
        """
        Initialize the export engine.
        
        Args:
            output_dir: Directory to save exported images
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.output_dir / "wallpapers").mkdir(exist_ok=True)
        (self.output_dir / "previews").mkdir(exist_ok=True)
        (self.output_dir / "animations").mkdir(exist_ok=True)
        (self.output_dir / "temp").mkdir(exist_ok=True)
    
    def save_image(self, rgb_array: np.ndarray, filename: str,
                   config: Optional[ExportConfig] = None,
                   subfolder: str = "wallpapers") -> str:
        """
        Save an RGB array as an image file.
        
        Args:
            rgb_array: RGB image array (0-1 values)
            filename: Output filename (without path)
            config: Export configuration
            subfolder: Subfolder within output directory
            
        Returns:
            Full path to saved file
        """
        if config is None:
            config = ExportConfig()
        
        # Ensure RGB values are in 0-255 range
        if rgb_array.max() <= 1.0:
            rgb_array = (rgb_array * 255).astype(np.uint8)
        else:
            rgb_array = rgb_array.astype(np.uint8)
        
        # Create PIL Image
        image = Image.fromarray(rgb_array, mode='RGB')
        
        # Build output path
        output_path = self.output_dir / subfolder / filename
        output_path.parent.mkdir(exist_ok=True)
        
        # Save based on format
        format_upper = config.format.upper()

        # Add metadata if requested
        pnginfo = None
        if config.add_metadata and format_upper == 'PNG':
            from PIL import PngImagePlugin
            pnginfo = PngImagePlugin.PngInfo()
            metadata = self._create_metadata()
            for key, value in metadata.items():
                pnginfo.add_text(key, str(value))
        
        # Save based on format
        if format_upper in ['PNG']:
            image.save(
                output_path,
                format=format_upper,
                optimize=config.optimize,
                compress_level=config.compression_level,
                pnginfo=pnginfo
            )
        elif format_upper in ['JPEG', 'JPG']:
            # Convert to RGB if not already (JPEG doesn't support alpha)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            image.save(
                output_path,
                format='JPEG',
                quality=config.quality,
                optimize=config.optimize,
                dpi=(config.dpi, config.dpi)
            )
        elif format_upper in ['WEBP']:
            image.save(
                output_path,
                format='WEBP',
                quality=config.quality,
                optimize=config.optimize,
                lossless=config.quality == 100
            )
        else:
            # Fallback for other formats
            image.save(output_path, format=format_upper)
        
        return str(output_path)
    
    def save_wallpaper_set(self, rgb_array: np.ndarray, base_name: str,
                          resolutions: Optional[list] = None,
                          config: Optional[ExportConfig] = None) -> Dict[str, str]:
        """
        Save the same fractal in multiple wallpaper resolutions.
        
        Args:
            rgb_array: Source RGB image array
            base_name: Base filename (without extension)
            resolutions: List of resolution names or tuples
            config: Export configuration
            
        Returns:
            Dictionary mapping resolution names to file paths
        """
        if resolutions is None:
            resolutions = ['Full HD', '4K', 'Ultrawide 2K']
        
        if config is None:
            config = ExportConfig()
        
        saved_files = {}
        preset_map = ResolutionPreset.get_all_presets()
        
        # Create PIL Image for resizing
        if rgb_array.max() <= 1.0:
            rgb_uint8 = (rgb_array * 255).astype(np.uint8)
        else:
            rgb_uint8 = rgb_array.astype(np.uint8)
        
        source_image = Image.fromarray(rgb_uint8, mode='RGB')
        
        for res in resolutions:
            if isinstance(res, str) and res in preset_map:
                target_size = preset_map[res]
                res_name = res
            elif isinstance(res, tuple) and len(res) == 2:
                target_size = res
                res_name = f"{res[0]}x{res[1]}"
            else:
                continue
            
            # Resize image
            resized_image = source_image.resize(target_size, Image.Resampling.LANCZOS)
            
            # Convert back to array for saving
            resized_array = np.array(resized_image)
            
            # Create filename
            filename = f"{base_name}_{res_name}.{config.format.lower()}"
            
            # Save
            file_path = self.save_image(resized_array, filename, config, "wallpapers")
            saved_files[res_name] = file_path
        
        return saved_files
    
    def create_preview(self, rgb_array: np.ndarray, filename: str,
                      max_size: Tuple[int, int] = (800, 600)) -> str:
        """
        Create a smaller preview version of the image.
        
        Args:
            rgb_array: RGB image array
            filename: Output filename
            max_size: Maximum dimensions for preview
            
        Returns:
            Path to preview file
        """
        # Convert to PIL Image
        if rgb_array.max() <= 1.0:
            rgb_uint8 = (rgb_array * 255).astype(np.uint8)
        else:
            rgb_uint8 = rgb_array.astype(np.uint8)
        
        image = Image.fromarray(rgb_uint8, mode='RGB')
        
        # Calculate preview size maintaining aspect ratio
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Convert back to array and save
        preview_array = np.array(image)
        
        preview_config = ExportConfig(format="PNG", quality=85)
        return self.save_image(preview_array, filename, preview_config, "previews")
    
    def apply_post_effects(self, rgb_array: np.ndarray,
                          sharpen: bool = False,
                          blur_radius: float = 0.0,
                          enhance_contrast: float = 1.0,
                          enhance_brightness: float = 1.0,
                          enhance_saturation: float = 1.0) -> np.ndarray:
        """
        Apply post-processing effects to enhance the image.
        
        Args:
            rgb_array: Input RGB array
            sharpen: Whether to apply sharpening filter
            blur_radius: Gaussian blur radius (0 = no blur)
            enhance_contrast: Contrast enhancement factor (1.0 = no change)
            enhance_brightness: Brightness enhancement factor (1.0 = no change)
            enhance_saturation: Saturation enhancement factor (1.0 = no change)
            
        Returns:
            Enhanced RGB array
        """
        # Convert to PIL Image for processing
        if rgb_array.max() <= 1.0:
            rgb_uint8 = (rgb_array * 255).astype(np.uint8)
        else:
            rgb_uint8 = rgb_array.astype(np.uint8)
        
        image = Image.fromarray(rgb_uint8, mode='RGB')
        
        # Apply filters
        if blur_radius > 0:
            image = image.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        
        if sharpen:
            image = image.filter(ImageFilter.SHARPEN)
        
        # Apply enhancements
        if enhance_contrast != 1.0:
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(enhance_contrast)
        
        if enhance_brightness != 1.0:
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(enhance_brightness)
        
        if enhance_saturation != 1.0:
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(enhance_saturation)
        
        # Convert back to array
        enhanced_array = np.array(image)
        
        # Normalize to 0-1 range
        return enhanced_array / 255.0
    
    def create_tiled_wallpaper(self, rgb_array: np.ndarray, 
                              tile_size: Tuple[int, int],
                              target_size: Tuple[int, int],
                              filename: str,
                              config: Optional[ExportConfig] = None) -> str:
        """
        Create a tiled wallpaper from a fractal pattern.
        
        Args:
            rgb_array: Source fractal image
            tile_size: Size of each tile
            target_size: Final wallpaper size
            filename: Output filename
            config: Export configuration
            
        Returns:
            Path to saved tiled wallpaper
        """
        if config is None:
            config = ExportConfig()
        
        # Convert to PIL Image
        if rgb_array.max() <= 1.0:
            rgb_uint8 = (rgb_array * 255).astype(np.uint8)
        else:
            rgb_uint8 = rgb_array.astype(np.uint8)
        
        tile_image = Image.fromarray(rgb_uint8, mode='RGB')
        tile_image = tile_image.resize(tile_size, Image.Resampling.LANCZOS)
        
        # Create target image
        wallpaper = Image.new('RGB', target_size, (0, 0, 0))
        
        # Calculate number of tiles needed
        tiles_x = (target_size[0] + tile_size[0] - 1) // tile_size[0]
        tiles_y = (target_size[1] + tile_size[1] - 1) // tile_size[1]
        
        # Paste tiles
        for y in range(tiles_y):
            for x in range(tiles_x):
                pos_x = x * tile_size[0]
                pos_y = y * tile_size[1]
                
                # Crop tile if it extends beyond target
                if pos_x + tile_size[0] > target_size[0] or pos_y + tile_size[1] > target_size[1]:
                    crop_width = min(tile_size[0], target_size[0] - pos_x)
                    crop_height = min(tile_size[1], target_size[1] - pos_y)
                    cropped_tile = tile_image.crop((0, 0, crop_width, crop_height))
                    wallpaper.paste(cropped_tile, (pos_x, pos_y))
                else:
                    wallpaper.paste(tile_image, (pos_x, pos_y))
        
        # Convert to array and save
        wallpaper_array = np.array(wallpaper)
        return self.save_image(wallpaper_array, filename, config, "wallpapers")
    
    def _create_metadata(self) -> dict:
        """Create metadata for saved images."""
        return {
            'Software': 'Fractal Visualizer',
            'Created': datetime.now().isoformat(),
            'Generator': 'Python Fractal Engine'
        }
    
    def export_settings(self, settings: dict, filename: str) -> str:
        """
        Export fractal settings to JSON file for reproducibility.
        
        Args:
            settings: Dictionary of fractal settings
            filename: JSON filename
            
        Returns:
            Path to saved settings file
        """
        settings_path = self.output_dir / "settings" / filename
        settings_path.parent.mkdir(exist_ok=True)
        
        # Add export timestamp
        export_data = {
            'exported_at': datetime.now().isoformat(),
            'settings': settings
        }
        
        with open(settings_path, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return str(settings_path)
    
    def load_settings(self, filename: str) -> dict:
        """Load fractal settings from JSON file."""
        settings_path = self.output_dir / "settings" / filename
        
        with open(settings_path, 'r') as f:
            data = json.load(f)
        
        return data.get('settings', {})
    
    def get_available_formats(self) -> list:
        """Get list of supported image formats."""
        return ['PNG', 'JPEG', 'WEBP', 'TIFF', 'BMP']
    
    def estimate_file_size(self, width: int, height: int, 
                          format: str = "PNG", quality: int = 95) -> str:
        """
        Estimate file size for given dimensions and format.
        
        Args:
            width: Image width
            height: Image height
            format: Output format
            quality: Quality setting
            
        Returns:
            Estimated file size as string
        """
        pixels = width * height
        
        if format.upper() == 'PNG':
            # PNG is typically 3-4 bytes per pixel for RGB
            bytes_estimate = pixels * 3.5
        elif format.upper() in ['JPEG', 'JPG']:
            # JPEG compression varies greatly
            compression_ratio = 20 - (quality / 5)  # Rough estimate
            bytes_estimate = pixels * 3 / compression_ratio
        elif format.upper() == 'WEBP':
            compression_ratio = 15 - (quality / 7)  # Rough estimate
            bytes_estimate = pixels * 3 / compression_ratio
        else:
            # Uncompressed RGB
            bytes_estimate = pixels * 3
        
        # Convert to human readable
        if bytes_estimate < 1024:
            return f"{int(bytes_estimate)} B"
        elif bytes_estimate < 1024 * 1024:
            return f"{bytes_estimate / 1024:.1f} KB"
        else:
            return f"{bytes_estimate / (1024 * 1024):.1f} MB"