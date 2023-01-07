import argparse
import pandas as pd
import os
from numpy import nan
from pathlib import Path

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-dir', '-b', help='path to the base directory in each all the images/ subfolders reside',
                        required=False)
    parser.add_argument('--full-path', '-f', help='if used, the program will treat the paths in the CSV as full paths '
                                                  'and will ignore the base-dir variable', action='store_true')
    parser.add_argument('--path', '-p', help='the path to the CSV', required=True)
    parser.add_argument('--column-name', '-c', help='the name of the column in the csv that stores the paths to the images',
                         default='path')
    return parser.parse_args()

def join_file_path(base_dir, file_name):
    return os.path.join(base_dir, file_name)
    
def format_file_path(file_path):
    return f"{file_path}".replace('\'', '').replace('"', '')

def check_if_exists(df: pd.DataFrame, column_name, is_full, base_dir=None) -> pd.DataFrame:
    num_of_rows = df.shape[0]
    indexes_to_drop = [] # the rows cannot be dropped immediately when found
    if is_full:
        base_dir = ""
    else:
        base_dir = f"{base_dir}/"
    for i in range(num_of_rows):
        if (df.iloc[i][column_name] == nan):
            print(f"found a bad csv record: {df.iloc[i][column_name]}")

        file_name = "{}.jpg".format(df.iloc[i][column_name])
        full_file_path = join_file_path(base_dir, file_name)
        formated_file_path = format_file_path(full_file_path)

        if (i % 2000 == 0):
            print(f"Done {i}/{num_of_rows}")
        
        if not os.path.exists(formated_file_path):
            print(f"found bad entry: {full_file_path}")
            indexes_to_drop.append(i)
            
    # df.drop(index=indexes_to_drop, inplace=True)
    print(f"num of rows: {df.shape[0]}")
    return df

def main():
    args = parse_arguments()
    base_dir = args.base_dir
    is_full = args.full_path
    if base_dir is None and not is_full:
        print("Error: no base_dir was provided and the full_path flag was not used either- cannot determine file paths")
        return
    csv_path = args.path
    column_name = args.column_name
    df = pd.read_csv(csv_path)
    df = check_if_exists(df, column_name, is_full, base_dir)
    df.to_csv(csv_path)


# if __name__ == "_main_":
main()