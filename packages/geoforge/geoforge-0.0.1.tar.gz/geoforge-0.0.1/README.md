# GeoForge

GeoForge is a comprehensive command-line toolkit for processing and manipulating geospatial data. It provides a collection of tools to help you work with various geospatial data formats efficiently.

## Features

Currently supported features:
- Convert regular GeoTIFF files to Cloud Optimized GeoTIFF (COG) format
- Batch processing capabilities
- Flexible compression options
- Detailed logging and progress tracking

## Installation

```bash
pip install geoforge
```

Or install from source:

```bash
git clone https://github.com/yourusername/geoforge.git
cd geoforge
pip install -e .
```

## Usage

GeoForge is organized into different command groups based on functionality. Here are some examples:

### Format Conversion Tools

Convert regular GeoTIFF files to Cloud Optimized GeoTIFF (COG):

```bash
geoforge format convert-cog -i /path/to/input/dir -o /path/to/output/dir
```

Required Options:
- `-i, --input-dir`: Input directory containing GeoTIFF files
- `-o, --output-dir`: Output directory for COG files

Optional Options:
- `-c, --compression`: Compression method [lzw|jpeg|deflate|zstd|webp] (default: lzw)
- `-t, --tile-size`: Tile size in pixels, must be a power of 2 (default: 512)

### General Help

To see all available commands:
```bash
geoforge -h
# or
geoforge --help
```

To get help for a specific command group:
```bash
geoforge format -h
```

To get help for a specific command:
```bash
geoforge format convert-cog -h
```

## Development

### Requirements
- Python 3.7+
- Dependencies listed in requirements.txt

### Setting up Development Environment

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
