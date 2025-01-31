import requests
from tqdm import tqdm
import os
import argparse
import logging


def setup_logging(log_level, log_file):
    log_level_mapping = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }
    level = log_level_mapping.get(log_level.lower(), logging.INFO)

    handlers = []
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    handlers.append(logging.StreamHandler())

    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=handlers
    )


def downloading(url, local_filename=None, download_dir="."):
    if local_filename is None:
        local_filename = os.path.basename(url)

    full_path = os.path.join(download_dir, local_filename)

    if not os.path.exists(download_dir):
        try:
            os.makedirs(download_dir)
            logging.info(f"Created download directory: {download_dir}")
        except OSError as e:
            logging.error(f"Failed to create download directory {download_dir}: {e}")
            return 'error'

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
        with open(full_path, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
        if total_size != 0 and progress_bar.n != total_size:
            logging.error("An error occurred during the download!!!")
            return 'error'
        else:
            logging.info(f"File {full_path} downloaded successfully.")
    except requests.RequestException as e:
        logging.error(f"Request error: {e}")
        return 'error'
    except OSError as e:
        logging.error(f"File writing error: {e}")
        return 'error'


def main():
    parser = argparse.ArgumentParser(description='Download a file with a progress bar and log management.')
    parser.add_argument('url', type=str,
                        help='The URL of the file to download. This is a required argument.')
    parser.add_argument('-o', '--output', type=str,
                        help='The local filename to save the downloaded file. If not provided, '
                             'the filename will be extracted from the URL.')
    parser.add_argument('-d', '--directory', type=str, default=".",
                        help='The directory to save the downloaded file. Defaults to the current directory.')
    parser.add_argument('--log-level', type=str, default='info',
                        choices=['debug', 'info', 'warning', 'error', 'critical'],
                        help='Set the logging level. Available options are debug, info, warning, error, and critical. '
                             'Default is info.')
    parser.add_argument('--log-file', type=str, default=None,
                        help='Specify the log file path. If not provided, logs will only be shown in the console.')

    args = parser.parse_args()

    setup_logging(args.log_level, args.log_file)

    url = args.url
    local_filename = args.output
    download_dir = args.directory
    result = downloading(url, local_filename, download_dir)
    if result == 'error':
        logging.error("Download process failed.")