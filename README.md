# Geo-spatial Analysis of Sampling Fields

## Overview

This repository contains Python and R scripts developed for the research paper:

**Hydrological Controls on Soil Chemical Variability: Geo-Spatial Profiling of Semi-Arid Agricultural Soil Dataset from Maharashtra**

The codes support geospatial processing, visualization of topographic and hydrological features, and statistical analysis of soil chemical properties. The repository is intended to provide transparency and reproducibility for journal reviewers and other researchers.

---

## Author & Affiliation

**Author:** Paul Atograhnt *(as per GitHub username)*
**Affiliation:** HMR Institute of Technology and Management, Affiliated to Guru Gobind Singh Indraprastha University (GGSIPU), Delhi, India

---

## Repository Contents

### Python Scripts

The Python scripts focus on geospatial analysis and visualization:

* Downloading and merging Digital Elevation Model (DEM) data from OpenTopography
* Generating topographic contour maps
* Overlaying soil sampling locations and related attributes

Typical outputs include geospatial maps (PNG) and processed elevation grids.

### R Scripts

The R scripts focus on statistical analysis of soil data:

* Importing soil chemical datasets from Excel files
* Performing multiple linear regression analysis
* Computing standardized beta coefficients to assess relative importance of predictors
* Visualizing regression results using publication-quality plots

---

## Data Availability

The original datasets used in this study are **not included** in this repository.

* Data may contain location-specific or sensitive information
* Datasets are available from the author upon reasonable request
* Users may substitute their own datasets with matching structure to run the scripts

---

## Software Environment

The codes were developed and tested in the following environment:

* **Operating System:** Windows 10
* **Python:** Compatible with Python 3.x
* **R:** Compatible with R (version 4.x recommended)

### Key Python Libraries

* rasterio
* numpy
* matplotlib
* cartopy
* requests

### Key R Packages

* readxl
* lm.beta
* ggplot2
* dplyr

---

## How to Use

1. Clone this repository:

   ```bash
   git clone https://github.com/paulat0grant/Geo-spatial-Analysis-of-Sampling-Fields.git
   ```

2. Install the required Python and R dependencies.

3. For Python scripts:

   * Insert your own OpenTopography API key where required
   * Update file paths and bounding box coordinates as needed
   * Run scripts individually depending on the analysis required

4. For R scripts:

   * Provide the correct path to your Excel dataset
   * Ensure column order and variable definitions match those described in the script
   * Run the script to obtain regression results and plots

---

## AI-Assisted Code Generation Disclosure

Parts of the code in this repository were initially generated with the assistance of large language models:

* **ChatGPT** was used to assist in generating and structuring Python scripts
* **Gemini** was used to assist in generating R scripts for statistical analysis

All generated code was subsequently **reviewed, modified, and validated by the author**, who takes full responsibility for the correctness, interpretation, and scientific use of the results.

---

## License

This project is licensed under the **MIT License**.

The MIT License permits reuse, modification, and distribution of the code, provided that proper attribution is given. This license is suitable for code developed with AI assistance and later modified by the author.

---

## Notes for Reviewers

* Some scripts rely on external APIs (e.g., OpenTopography) and require an active internet connection
* Large geospatial files are not included to keep the repository lightweight
* All scripts are modular and can be run independently

---

## Citation

If you use this code in your research, please cite the associated paper and this GitHub repository.

---

*This repository is intended to support reproducible environmental and hydrological research.*

