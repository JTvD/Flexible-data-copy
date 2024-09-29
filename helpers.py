from os import path, walk
import utils
import shutil


def diff(input_dir: str, ourput_dir: str):
    """Helper function to determine the difference two folders
    Return:
        list of dicts with the file status: new, same, diff and the new directories: new dir
    """
    status_list = []
    for cwd, dirs, files in walk(input_dir):
        # List all not existing directories
        for dir in dirs:
            source_dir = path.join(cwd, dir)
            dir_path = path.relpath(source_dir, input_dir)
            new_dir = path.join(ourput_dir, dir_path)
            if not utils.check_direxists(new_dir):
                status_list.append({'source': source_dir,
                                    'dest': new_dir,
                                    'size': 0,
                                    'source_checksum': 0,
                                    'dest_checksum': 0,
                                    'status': 'new dir'})
        for file in files:
            source_file = path.join(cwd, file)
            file_path = path.relpath(source_file, input_dir)
            dest_file = path.join(ourput_dir, file_path)
            # New files
            if not utils.check_fileexists(dest_file):
                status_list.append({'source': source_file,
                                    'dest': dest_file,
                                    'size': path.getsize(source_file),
                                    'source_checksum': utils.generate_file_md5(source_file),
                                    'dest_checksum': 0,
                                    'status': 'new'})
            else:
                source_checksum = utils.generate_file_md5(source_file)
                dest_checksum = utils.generate_file_md5(dest_file)
                if source_checksum == dest_checksum:
                    status_list.append({'source': source_file,
                                        'dest': dest_file,
                                        'size': path.getsize(source_file),
                                        'source_checksum': source_checksum,
                                        'dest_checksum': dest_checksum,
                                        'status': 'same'})
                else:
                    status_list.append({'source': source_file,
                                        'dest': dest_file,
                                        'size': path.getsize(source_file),
                                        'source_checksum': source_checksum,
                                        'dest_checksum': dest_checksum,
                                        'status': 'diff'})
    return status_list


def move_file(file_status):
    """Helper function to move a file from the source to the destination.
    Checks the copy by calculating the checksum.
    Return:
        dict with the file status: new, same, diff
    """
    shutil.copyfile(file_status['source'], file_status['dest'])

    # Check transfer
    file_status['dest_checksum'] = utils.generate_file_md5(file_status['dest'])
    if file_status['source_checksum'] == file_status['dest_checksum']:
        file_status['status'] = 'same'
    else:
        file_status['status'] = 'diff'
    return file_status
