import os
import sys
import spectrochempy as scp
import pandas as pd

DATA_DIR = 'data'
OUT_DIR = 'csv_files'

def convert_omnic_to_csv(in_file, out_file):

    X = scp.read_omnic(in_file)

    y_data = X.data
    x_data = X.x.data
    row_names = X.y.data

    # Save CSV with values
    df = pd.DataFrame(y_data, index=row_names, columns=x_data)
    df.to_csv(out_file)


def main(in_dir, out_dir):

    os.makedirs(out_dir, exist_ok=True)

    data_dirs = [ os.path.join(in_dir, dir) for dir in os.listdir(in_dir) if os.path.isdir(os.path.join(in_dir, dir)) ]

    for spa_folder in data_dirs:
        out_file = os.path.join(out_dir, os.path.basename(spa_folder) + '.csv')
        convert_omnic_to_csv(spa_folder, out_file)

if __name__ == '__main__':
    in_dir = sys.argv[1] if len(sys.argv) > 1 else DATA_DIR
    out_dir = sys.argv[2] if len(sys.argv) > 2 else OUT_DIR
    main(in_dir, out_dir)
