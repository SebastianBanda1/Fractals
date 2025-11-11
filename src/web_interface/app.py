"""
Streamlit Web Interface for Fractal Visualization

Interactive fractal explorer with real-time parameter adjustment and preview.
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
from typing import Dict, Any, Optional

# Import our fractal modules
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from fractal_engine import FractalEngine, FractalConfig
from color_engine import ColorEngine, PaletteType
from export_engine import ExportEngine, ResolutionPreset, ExportConfig


class FractalApp:
    """Main Streamlit application for fractal visualization."""
    
    def __init__(self):
        """Initialize the fractal application."""
        self.fractal_engine = FractalEngine()
        self.color_engine = ColorEngine()
        self.export_engine = ExportEngine()
        
        # Initialize session state
        if 'fractal_data' not in st.session_state:
            st.session_state.fractal_data = None
        if 'current_image' not in st.session_state:
            st.session_state.current_image = None
        if 'zoom_history' not in st.session_state:
            st.session_state.zoom_history = []
    
    def run(self):
        """Run the Streamlit application."""
        st.set_page_config(
            page_title="🌀 Fractal Visualizer",
            page_icon="🌀",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        st.title("🌀 Fractal Visualizer & Wallpaper Generator")
        st.markdown("*Create stunning fractal visualizations and high-resolution wallpapers*")
        
        # Sidebar for controls
        self._create_sidebar()
        
        # Main content area
        col1, col2 = st.columns([3, 1])
        
        with col1:
            self._create_main_view()
        
        with col2:
            self._create_info_panel()
    
    def _create_sidebar(self):
        """Create the sidebar with fractal controls."""
        with st.sidebar:
            st.header("🎛️ Fractal Controls")
            
            # Fractal type selection
            fractal_type = st.selectbox(
                "Fractal Type",
                ["Mandelbrot", "Julia Set", "Burning Ship"],
                help="Select the type of fractal to generate"
            )
            
            # Basic parameters
            st.subheader("📐 Parameters")
            
            col1, col2 = st.columns(2)
            with col1:
                center_x = st.number_input("Center X", value=0.0, step=0.1, format="%.6f")
                width = st.selectbox("Width", [800, 1280, 1920, 2560, 3840], index=2)
            
            with col2:
                center_y = st.number_input("Center Y", value=0.0, step=0.1, format="%.6f")
                height = st.selectbox("Height", [600, 720, 1080, 1440, 2160], index=2)
            
            zoom = st.slider("Zoom", min_value=0.1, max_value=10000.0, value=1.0, step=0.1)
            max_iter = st.slider("Max Iterations", min_value=50, max_value=1000, value=256)
            
            # Julia set specific parameters
            julia_params = {}
            if fractal_type == "Julia Set":
                st.subheader("🌸 Julia Parameters")
                julia_params['c_real'] = st.slider("C Real", -2.0, 2.0, -0.4, 0.01)
                julia_params['c_imag'] = st.slider("C Imaginary", -2.0, 2.0, 0.6, 0.01)
            
            # Color settings
            st.subheader("🎨 Colors")
            palette_type = st.selectbox(
                "Color Palette",
                self.color_engine.get_available_palettes(),
                index=0
            )
            
            smooth_coloring = st.checkbox("Smooth Coloring", value=True)
            gamma = st.slider("Gamma Correction", 0.1, 3.0, 1.0, 0.1)
            
            # Post-processing
            st.subheader("✨ Enhancement")
            contrast = st.slider("Contrast", 0.5, 2.0, 1.0, 0.1)
            brightness = st.slider("Brightness", -0.5, 0.5, 0.0, 0.1)
            saturation = st.slider("Saturation", 0.0, 2.0, 1.0, 0.1)
            
            # Generate button
            if st.button("🎬 Generate Fractal", type="primary"):
                self._generate_fractal(
                    fractal_type, center_x, center_y, zoom, width, height,
                    max_iter, palette_type, smooth_coloring, gamma,
                    contrast, brightness, saturation, julia_params
                )
            
            # Preset interesting points
            st.subheader("📍 Interesting Points")
            if fractal_type.lower().replace(" ", "_") in ["mandelbrot", "burning_ship"]:
                interesting_points = self.fractal_engine.get_interesting_points(
                    fractal_type.lower().replace(" ", "_")
                )
                
                for point in interesting_points:
                    if st.button(f"🎯 {point['name']}", key=f"preset_{point['name']}"):
                        st.session_state.preset_point = point
                        st.experimental_rerun()
    
    def _create_main_view(self):
        """Create the main fractal display area."""
        if st.session_state.current_image is not None:
            st.image(st.session_state.current_image, use_column_width=True)
            
            # Export options
            st.subheader("💾 Export Options")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                export_format = st.selectbox("Format", ["PNG", "JPEG", "WEBP"])
                quality = st.slider("Quality", 70, 100, 95) if export_format != "PNG" else 95
            
            with col2:
                resolutions = st.multiselect(
                    "Resolutions",
                    list(ResolutionPreset.get_all_presets().keys()),
                    default=["Full HD", "4K"]
                )
            
            with col3:
                filename = st.text_input("Filename", "fractal_wallpaper")
                
                if st.button("📁 Export Wallpapers"):
                    self._export_wallpapers(filename, export_format, quality, resolutions)
        
        else:
            st.info("👆 Use the sidebar controls to generate your first fractal!")
            
            # Show some example images or instructions
            st.markdown("""
            ### 🚀 Quick Start Guide:
            
            1. **Choose a fractal type** from the sidebar
            2. **Adjust parameters** like zoom and center point
            3. **Select colors** from our beautiful palette collection
            4. **Generate** your fractal visualization
            5. **Export** in multiple resolutions for wallpapers
            
            ### 🎨 Featured Fractals:
            - **Mandelbrot Set**: The classic fractal with infinite detail
            - **Julia Sets**: Beautiful variations with complex parameters
            - **Burning Ship**: A dramatic fractal resembling a ship
            """)
    
    def _create_info_panel(self):
        """Create the information and statistics panel."""
        st.subheader("ℹ️ Information")
        
        if st.session_state.fractal_data is not None:
            data = st.session_state.fractal_data
            config = data['config']
            
            st.write(f"**Type:** {data['type']}")
            st.write(f"**Resolution:** {config.width}×{config.height}")
            st.write(f"**Zoom:** {config.zoom:.2f}×")
            st.write(f"**Center:** ({config.center_x:.6f}, {config.center_y:.6f})")
            st.write(f"**Iterations:** {config.max_iter}")
            
            if 'generation_time' in data:
                st.write(f"**Generation Time:** {data['generation_time']:.2f}s")
            
            # Color distribution
            if 'color_stats' in data:
                st.subheader("📊 Color Statistics")
                st.write(f"**Unique Colors:** {data['color_stats']['unique_colors']}")
                st.write(f"**In Set:** {data['color_stats']['in_set_percentage']:.1f}%")
        
        # Performance tips
        st.subheader("⚡ Performance Tips")
        st.markdown("""
        - **Lower iterations** for faster preview
        - **Higher iterations** for detailed exports  
        - **Smaller resolution** for real-time exploration
        - **Larger resolution** for wallpaper quality
        """)
        
        # Zoom history
        if st.session_state.zoom_history:
            st.subheader("📜 Zoom History")
            for i, entry in enumerate(reversed(st.session_state.zoom_history[-5:])):
                if st.button(f"↩️ {entry['name']}", key=f"history_{i}"):
                    self._apply_zoom_point(entry)
    
    def _generate_fractal(self, fractal_type: str, center_x: float, center_y: float,
                         zoom: float, width: int, height: int, max_iter: int,
                         palette_type: str, smooth_coloring: bool, gamma: float,
                         contrast: float, brightness: float, saturation: float,
                         julia_params: Dict[str, float]):
        """Generate a fractal with the given parameters."""
        
        with st.spinner('🎨 Generating fractal...'):
            start_time = time.time()
            
            # Create fractal configuration
            config = FractalConfig(
                width=width,
                height=height,
                max_iter=max_iter,
                center_x=center_x,
                center_y=center_y,
                zoom=zoom
            )
            
            # Generate fractal data
            try:
                if fractal_type == "Mandelbrot":
                    iterations = self.fractal_engine.generate_mandelbrot(config)
                elif fractal_type == "Julia Set":
                    iterations = self.fractal_engine.generate_julia(
                        julia_params['c_real'], julia_params['c_imag'], config
                    )
                elif fractal_type == "Burning Ship":
                    iterations = self.fractal_engine.generate_burning_ship(config)
                else:
                    raise ValueError(f"Unknown fractal type: {fractal_type}")
                
                # Apply color mapping
                rgb_image = self.color_engine.apply_color_mapping(
                    iterations, palette_type, smooth_coloring, max_iter, gamma
                )
                
                # Apply enhancements
                if contrast != 1.0 or brightness != 0.0 or saturation != 1.0:
                    rgb_image = self.color_engine.enhance_image(
                        rgb_image, contrast, brightness, saturation
                    )
                
                generation_time = time.time() - start_time
                
                # Store in session state
                st.session_state.fractal_data = {
                    'type': fractal_type,
                    'config': config,
                    'iterations': iterations,
                    'rgb_image': rgb_image,
                    'generation_time': generation_time,
                    'palette': palette_type,
                    'julia_params': julia_params,
                    'color_stats': self._calculate_color_stats(iterations, max_iter)
                }
                
                st.session_state.current_image = rgb_image
                
                # Add to zoom history
                history_entry = {
                    'name': f"{fractal_type} {zoom:.1f}x",
                    'center_x': center_x,
                    'center_y': center_y,
                    'zoom': zoom,
                    'fractal_type': fractal_type,
                    'julia_params': julia_params
                }
                st.session_state.zoom_history.append(history_entry)
                
                st.success(f"✨ Fractal generated in {generation_time:.2f} seconds!")
                
            except Exception as e:
                st.error(f"❌ Error generating fractal: {str(e)}")
    
    def _export_wallpapers(self, filename: str, export_format: str, 
                          quality: int, resolutions: list):
        """Export the current fractal as wallpapers."""
        if st.session_state.fractal_data is None:
            st.error("❌ No fractal to export! Generate one first.")
            return
        
        try:
            with st.spinner('💾 Exporting wallpapers...'):
                rgb_image = st.session_state.fractal_data['rgb_image']
                
                export_config = ExportConfig(
                    format=export_format,
                    quality=quality
                )
                
                saved_files = self.export_engine.save_wallpaper_set(
                    rgb_image, filename, resolutions, export_config
                )
                
                st.success(f"✅ Exported {len(saved_files)} wallpapers!")
                
                # Show export details
                for res_name, file_path in saved_files.items():
                    file_size = self.export_engine.estimate_file_size(
                        *ResolutionPreset.get_all_presets()[res_name],
                        export_format, quality
                    )
                    st.write(f"📁 {res_name}: {file_path} (~{file_size})")
                
                # Also save settings for reproducibility
                settings = {
                    'fractal_type': st.session_state.fractal_data['type'],
                    'config': {
                        'width': st.session_state.fractal_data['config'].width,
                        'height': st.session_state.fractal_data['config'].height,
                        'center_x': st.session_state.fractal_data['config'].center_x,
                        'center_y': st.session_state.fractal_data['config'].center_y,
                        'zoom': st.session_state.fractal_data['config'].zoom,
                        'max_iter': st.session_state.fractal_data['config'].max_iter,
                    },
                    'palette': st.session_state.fractal_data['palette'],
                    'julia_params': st.session_state.fractal_data['julia_params'],
                }
                
                settings_file = self.export_engine.export_settings(
                    settings, f"{filename}_settings.json"
                )
                st.write(f"⚙️ Settings: {settings_file}")
                
        except Exception as e:
            st.error(f"❌ Export failed: {str(e)}")
    
    def _calculate_color_stats(self, iterations: np.ndarray, max_iter: int) -> Dict[str, Any]:
        """Calculate statistics about the fractal coloring."""
        unique_values = np.unique(iterations)
        in_set_count = np.sum(iterations == max_iter)
        total_pixels = iterations.size
        
        return {
            'unique_colors': len(unique_values),
            'in_set_percentage': (in_set_count / total_pixels) * 100,
            'total_pixels': total_pixels
        }
    
    def _apply_zoom_point(self, point: Dict[str, Any]):
        """Apply a zoom point from history or presets."""
        # This would update the UI controls - in a real app you'd need
        # to handle this through session state or URL parameters
        st.session_state.zoom_point = point
        st.experimental_rerun()


def main():
    """Main entry point for the Streamlit app."""
    app = FractalApp()
    app.run()


if __name__ == "__main__":
    main()