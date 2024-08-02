# OMNIC to CSV
This script converts OMNIC files to CSV files. 

## Installation
Install `spectrochempy` and `pandas` into a virtual environment. 
```bash
pip install spectrochempy pandas
```

For your convenience, the `environment.yml` file is provided for creating a conda environment. 
```bash
conda env create -f environment.yml
```

## Getting Started
In OMNIC, export the data as `.spa` files by selecting the desired data and clicking `Series > Split Series File > Ok`.

Make sure you save this **collection** of `.spa` files in a directory indicating the series name.

```
<series_name>
    <series_name>0000.spa
    <series_name>0001.spa
    <series_name>0002.spa
    ...
```

## Usage
The `omnic_to_csv.py` script takes a directory of OMNIC `.spa` collections and converts them to CSV files corresponding to the collection names.

```bash
python omnic_to_csv.py <input_file> <output_file>
```

## Example
```bash
python omnic_to_csv.py data csv_files
```

### Data
```
data
    series1
        series1000.spa
        series1001.spa
        series1002.spa
    series2
        series2000.spa
        series2001.spa
        series2002.spa
```

### CSV Files
```
csv_files
    series1.csv
    series2.csv
```