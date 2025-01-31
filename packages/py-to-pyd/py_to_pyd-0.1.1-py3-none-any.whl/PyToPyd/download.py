import requests
from tqdm import tqdm
import os
import argparse

def downloading(url, local_filename=None):
    if local_filename is None:
        local_filename = os.path.basename(url)
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
    with open(local_filename, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size != 0 and progress_bar.n != total_size:
        print("An error occurred during the download!!!")
        return 'error'
    else:
        print(f"file {local_filename} Download completed.")


def main():
    parser = argparse.ArgumentParser(description='Download a file with a progress bar.')
    parser.add_argument('url', type=str, help='The URL of the file to download.')
    parser.add_argument('-o', '--output', type=str, help='The local filename to save the downloaded file.')
    args = parser.parse_args()

    url = args.url
    local_filename = args.output
    downloading(url, local_filename)