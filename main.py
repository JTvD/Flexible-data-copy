from os import makedirs, path
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import logging

import utils
from helpers import diff, move_file


INPUT_FOLDER = "test_data/A"
OUTPUT_FOLDER = "test_data/B"
ID = "id"


if __name__ == "__main__":
    utils.setup_logger()
    input_dir = path.join(INPUT_FOLDER)
    ourput_dir = path.join(OUTPUT_FOLDER)

    # Check if system folder exists
    if not utils.check_direxists(ID):
        makedirs(ID)

    # Check if experiment was already processe d
    experiment_status_csv = path.join(ID, 'processed.csv')
    if utils.check_fileexists(experiment_status_csv):
        status_df = pd.read_csv(experiment_status_csv)
    else:
        # Create the overview
        status_list = diff(input_dir, ourput_dir)
        status_df = pd.DataFrame(status_list)
        status_df.to_csv(experiment_status_csv, index=False)

    logging.info(f"Start processing: {len(status_df.loc[status_df['status'] == 'new'])} new, {len(status_df.loc[status_df['status']== 'diff'])} diff, {len(status_df.loc[status_df['status']== 'same'])} same files, total: {len(status_df.loc[status_df['status']!= 'new dir'])} files and {len(status_df.loc[status_df['status']== 'new dir'])} folders")

    # Create folders
    for row in status_df.loc[status_df['status'] == 'new dir'].iterrows():
        makedirs(row['dest'])

    # Create a thread pool with 20 worker threads
    pool = ThreadPoolExecutor(max_workers=20)
    files_update_df = status_df[status_df['status'].isin(['diff', 'new'])]
    file_update_list = files_update_df.to_dict('records')

    if len (file_update_list) > 0:
        logging.info(f"Start moving {len(file_update_list)} files")
        # Run function
        result_list = []
        for result in pool.map(move_file, file_update_list):
            result_list.append(result)
        results_df = pd.DataFrame(result_list)

        # Overwrite the changed rows in the status dataframe
        cols = list(status_df.columns)
        status_df.set_index(status_df['source'], inplace=True)
        results_df.set_index(results_df['source'], inplace=True)
        # Matches based on index
        status_df.loc[status_df['source'].isin(results_df['source']), cols] = results_df[cols]
        status_df.reset_index(drop=True, inplace=True)
    else:
        logging.info("No files to move, all checksums match")
    result_csv = path.join(ID, 'res.csv')
    status_df.to_csv(result_csv, index=False)
