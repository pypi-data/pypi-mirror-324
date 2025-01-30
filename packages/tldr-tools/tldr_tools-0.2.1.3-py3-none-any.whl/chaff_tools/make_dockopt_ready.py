import os
import argparse
import gzip
import shutil
import tarfile
import logging
from chaff_tools.yaml_wrangler import *


def gzip_db2_files(file_paths, output_dir):
    """Compress .db2 files into .db2.gz files and save them to the specified directory."""
    gzipped_files = []
    for file_path in file_paths:
        if os.path.exists(file_path) and file_path.endswith('.db2'):
            output_file = os.path.join(output_dir, os.path.basename(file_path) + '.gz')
            with open(file_path, 'rb') as f_in:
                with gzip.open(output_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            gzipped_files.append(output_file)
            logging.info(f"Compressed {file_path} to {output_file}")
        else:
            logging.warning(f"Skipping {file_path}, not a valid .db2 file.")
    return gzipped_files


def create_tgz_from_files(file_paths, tgz_file):
    """Create a .tgz archive from a list of files."""
    with tarfile.open(tgz_file, 'w:gz') as tar:
        for file_path in file_paths:
            tar.add(file_path, arcname=os.path.basename(file_path))
            logging.info(f"Added {file_path} to {tgz_file}")
    logging.info(f"Created tarball: {tgz_file}")


def process_contaminant_set(yaml_file, output_path):
    """Process the contaminant set, compress .db2 files, and create a .tgz archive."""
    os.makedirs(output_path, exist_ok=True)
    # Step 1: Load selected actives and contaminants from YAML
    selected_actives, selected_contaminants, _, _ = load_from_yaml(yaml_file)
    
    # Step 2: Combine selected actives and selected contaminants
    contaminant_set = selected_actives + selected_contaminants
    
    # Step 3: Compress .db2 files into .db2.gz files
    output_dir = 'gzipped_db2_files'
    os.makedirs(output_dir, exist_ok=True)
    
    # Make sure that all files in the contaminant set exist
    valid_files = [f for f in contaminant_set if os.path.exists(f)]
    if not valid_files:
        logging.error("No valid .db2 files found in contaminant set.")
        raise FileNotFoundError("No valid .db2 files found in contaminant set.")
    
    # Gzip the files
    gzipped_files = gzip_db2_files(valid_files, output_dir)
    
    # Step 4: Create the .tgz archive
    yaml_name = os.path.splitext(os.path.basename(yaml_file))[0]
    tgz_filename = f"{yaml_name}.tgz"
    tgz_file_path = os.path.join(output_path, tgz_filename)
    create_tgz_from_files(gzipped_files, tgz_file_path)
    logging.info(f"Contaminant set has been processed and saved as {tgz_filename}")

def main():
    # Command-line interface for checking job status
    parser = argparse.ArgumentParser(description="Given a chaff-tools prepared yaml file, prepare a .tgz file for DockOpt")
    parser.add_argument(
        '--yaml-file', type=str, required=True,
        help="Path to the .yaml file"
    )
    parser.add_argument(
        '--output', type=str, required=True,
        help="Name and path to desired output filename (e.g. some/path/here/active.tgz)"
    )
    
    args = parser.parse_args()
    process_contaminant_set(args.yaml_file, args.output)

if __name__ == "__main__":
    main()