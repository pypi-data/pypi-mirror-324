#!/usr/bin/env python3
import glob
import logging
import os
from datetime import datetime
from pathlib import Path

import click
import rasterio
from rasterio.enums import Resampling
from rasterio.io import MemoryFile
from rasterio.shutil import copy
from tqdm import tqdm

# Add context settings to handle -h flag
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

def setup_logging(output_dir):
    """Set up logging configuration"""
    log_dir = Path(output_dir) / 'logs'
    log_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = log_dir / f'geoforge_{timestamp}.log'

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

class GeoTiffProcessor:
    def __init__(self, logger):
        self.logger = logger

    def get_overview_levels(self, height, width):
        """Calculate appropriate overview levels"""
        max_dimension = max(height, width)
        levels = []
        factor = 2

        while max_dimension // factor >= 512:
            levels.append(factor)
            factor *= 2

        return levels

    def calculate_compression_ratio(self, input_path, output_path):
        """Calculate and return the compression ratio"""
        input_size = os.path.getsize(input_path)
        output_size = os.path.getsize(output_path)
        return (1 - (output_size / input_size)) * 100

    def validate_tiff(self, path):
        """Validate if the file is a valid GeoTIFF"""
        try:
            with rasterio.open(path) as src:
                return True
        except rasterio.errors.RasterioIOError:
            return False

    def convert_to_cog(self, input_path, output_path, compression='lzw', tile_size=512):
        """Convert a GeoTIFF to a Cloud Optimized GeoTIFF"""
        try:
            with rasterio.open(input_path) as src:
                self.logger.info(f"Processing {input_path}")
                self.logger.info(f"Input specs: {src.profile}")

                levels = self.get_overview_levels(src.height, src.width)
                self.logger.info(f"Calculated overview levels: {levels}")

                profile = src.profile.copy()
                profile.update({
                    'driver': 'GTiff',
                    'tiled': True,
                    'blockxsize': tile_size,
                    'blockysize': tile_size,
                    'compress': compression,
                    'predictor': 2,
                    'interleave': 'pixel'
                })

                with MemoryFile() as memfile:
                    with memfile.open(**profile) as mem:
                        data = src.read()
                        mem.write(data)

                        self.logger.info("Generating overviews...")
                        mem.build_overviews(levels, Resampling.average)

                        copy(
                            mem,
                            output_path,
                            driver='GTiff',
                            tiled=True,
                            blockxsize=tile_size,
                            blockysize=tile_size,
                            compress=compression,
                            predictor=2,
                            copy_src_overviews=True,
                            interleave='pixel'
                        )

            ratio = self.calculate_compression_ratio(input_path, output_path)
            self.logger.info(f"Compression ratio achieved: {ratio:.2f}%")
            return True

        except Exception as e:
            self.logger.error(f"Error converting {input_path}: {str(e)}")
            return False

    def process_directory(self, input_dir, output_dir, compression='lzw', tile_size=512):
        """Process all GeoTIFF files in a directory and convert them to COGs"""
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)

        self.logger.info(f"Starting batch conversion process")
        self.logger.info(f"Input directory: {input_dir}")
        self.logger.info(f"Output directory: {output_dir}")
        self.logger.info(f"Compression method: {compression}")
        self.logger.info(f"Tile size: {tile_size}x{tile_size}")

        tiff_patterns = ['*.tif', '*.tiff', '*.TIF', '*.TIFF']
        tiff_files = []
        for pattern in tiff_patterns:
            tiff_files.extend(glob.glob(os.path.join(input_dir, pattern)))

        if not tiff_files:
            self.logger.warning("No TIFF files found in input directory")
            return

        valid_files = []
        self.logger.info("Validating input files...")
        for file in tqdm(tiff_files, desc="Validating files"):
            if self.validate_tiff(file):
                valid_files.append(file)
            else:
                self.logger.warning(f"Invalid or corrupted TIFF: {file}")

        self.logger.info(f"Found {len(valid_files)} valid GeoTIFF files")

        successful = 0
        failed = 0

        for input_file in tqdm(valid_files, desc="Converting to COG"):
            filename = Path(input_file).name
            output_file = output_dir / f'cog_{filename}'

            if self.convert_to_cog(input_file, output_file, compression, tile_size):
                successful += 1
            else:
                failed += 1

        self.logger.info("=== Conversion Summary ===")
        self.logger.info(f"Total files processed: {len(valid_files)}")
        self.logger.info(f"Successfully converted: {successful}")
        self.logger.info(f"Failed conversions: {failed}")

        if failed > 0:
            self.logger.warning("Some conversions failed. Check the log file for details.")

# CLI Command Groups
@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """GeoForge - A comprehensive toolkit for geospatial data processing"""
    pass

@cli.group()
def format():
    """Tools for converting and reformatting geospatial data"""
    pass

@format.command(name='convert-cog')
@click.option('-i', '--input-dir', required=True, help='Input directory containing GeoTIFF files')
@click.option('-o', '--output-dir', required=True, help='Output directory for COG files')
@click.option('-c', '--compression',
              type=click.Choice(['lzw', 'jpeg', 'deflate', 'zstd', 'webp']),
              default='lzw',
              show_default=True,
              help='[OPTIONAL] Compression method to use')
@click.option('-t', '--tile-size',
              type=int,
              default=512,
              show_default=True,
              help='[OPTIONAL] Tile size in pixels (must be a power of 2)')
def convert_cog(input_dir, output_dir, compression, tile_size):
    """Convert regular GeoTIFF files to Cloud Optimized GeoTIFF (COG) format.

    This command processes all GeoTIFF files in the input directory and converts them
    to Cloud Optimized GeoTIFF (COG) format, which is optimized for efficient web access
    and streaming. The converted files will be saved in the output directory with the
    prefix 'cog_'.
    """
    if not (tile_size & (tile_size - 1) == 0) or tile_size <= 0:
        raise click.BadParameter("Tile size must be a positive power of 2")

    logger = setup_logging(output_dir)
    processor = GeoTiffProcessor(logger)
    processor.process_directory(input_dir, output_dir, compression, tile_size)

if __name__ == '__main__':
    cli()
