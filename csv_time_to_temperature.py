import os
import sys
import pandas as pd
import numpy as np
import math
from os import path

HEADER_ROW = 'Time	Temperature	Weight	Weight	Deriv. Weight'

def find_nearest_idx(array,value):
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
        return idx-1
    else:
        return idx

def main(ftir_csv_file, tga_txt_file, out_file):
    os.makedirs(path.dirname(out_file), exist_ok=True)

    ftir_data = pd.read_csv(ftir_csv_file, index_col=0)

    # ------------------- Parse txt file -------------------
    with open(tga_txt_file, 'r') as f:
        txt_data = f.read()

    txt_lines = txt_data.split('\n')

    # Get line index that matches header row
    header_index = txt_lines.index(HEADER_ROW)
    if header_index == -1:
        print('Could not find header row in txt file')
        return
    
    # Create a DataFrame from the txt file
    header_info = txt_lines[header_index].split('\t')
    unit_info = txt_lines[header_index + 1].split('\t')
    tsv_header_data = [ f"{header} ({unit_info[i]})" for i, header in enumerate(header_info) ]
    tsv_body = txt_lines[header_index + 2:]
    tsv_body_parsed = [ line.split('\t') for line in tsv_body ]
    tsv_body_filtered = [ line for line in tsv_body_parsed if line[0] != '' ]
    tga_data = pd.DataFrame(tsv_body_filtered, columns=tsv_header_data)

    # Normalize row headers to first row
    ftir_data.index = ftir_data.index - ftir_data.index[0]

    # Convert row headers from seconds to minutes
    ftir_data.index = ftir_data.index / 60

    # Get the closest time value in the TGA data
    tga_time_data = tga_data[tga_data.columns[0]].values.astype(float)
    indexer = [ find_nearest_idx(tga_time_data, time) for time in ftir_data.index ]

    # # Create a new DataFrame with the temperature values
    ftir_data_by_temperature = ftir_data.copy()
    temperature_data = tga_data['Temperature (°C)']
    ftir_data_by_temperature.index = [ temperature_data[idx] for idx in indexer ]

    # Save the new DataFrame to a CSV file
    ftir_data_by_temperature.to_csv(out_file)


if __name__ == '__main__':
    csv_file = sys.argv[1]
    txt_file = sys.argv[2] if len(sys.argv) > 2 else None
    if txt_file is None:
        print('Please provide a txt file with the temperature values')

    out_dir = sys.argv[3] if len(sys.argv) > 3 else path.dirname(csv_file)
    out_file =path.join(out_dir, path.basename(csv_file) + '.csv')

    # Add a suffix if output to the same directory
    if out_dir == path.dirname(csv_file):
        out_file = path.splitext(out_file)[0] + '_temperature' + path.splitext(out_file)[1]
        
    main(csv_file, txt_file, out_file)
