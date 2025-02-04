# Glacier Velocity Processing

This Python package processes Sentinel-1 SAR data to compute glacier velocity from offset tracking methods. It includes several preprocessing steps, including orbit file application, thermal noise removal, speckle filtering, and terrain correction, among others. This package is designed for users working with remote sensing data for glaciology, providing tools to handle and process raw Sentinel-1 data for velocity mapping.

## Features

- **Preprocessing**: The package includes functions for preprocessing Sentinel-1 SAR data, including:
  - **Orbit File Application**: Applies orbit file corrections to the raw data.
  - **Thermal Noise Removal**: Removes thermal noise from the raw data.
  - **Calibration**: Converts radar intensity values into physically meaningful measurements (e.g., backscatter coefficients).
  - **Speckle Filtering**: Applies refined Lee filtering for speckle reduction.
  - **Subset**: Crops the data to the region of interest (ROI).
  - **Terrain Correction**: Corrects for topographic effects and georeferences the data.
  - **Offset Tracking**: Computes glacier velocity based on offset tracking methods.

- **Flexible**: Customize parameters for the offset tracking procedure, such as azimuth spacing, range spacing, and correlation thresholds.

## Installation

You can install this package using pip (from TestPyPI or PyPI once it's uploaded).

To install from TestPyPI (for testing):

```bash
pip install --index-url https://test.pypi.org/simple/ --no-deps offsetglacier
