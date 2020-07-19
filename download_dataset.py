import urllib.request
import requests
import zipfile
import json
import time
import sys
import os

DATASET_METADATA = 'https://objectstorage.ap-mumbai-1.oraclecloud.com/p/fQ4itlKZosP5gtaFpJNk0jZTzDvtXQBm2RefZPZJNS0/n/bm7noglpf2jq/b/FYP-Data/o/updates.json'

def have_internet():
    try:
        _ = requests.get(DATASET_METADATA, timeout=5)
        return True
    except requests.ConnectionError:
        print("Download Failed: No internet connection available.")
        return False
        
def count_dataset_files():
    number_files = sum([len(files) for r, d, files in os.walk('dataset')])
    return number_files

def start_download(f, response, dl=0):
  timer = time.time()
  download_speed = 0.00
  tmp_dl = 0
  total_length = response.headers.get('content-length')
  total_length = int(total_length) + dl
  for data in response.iter_content(chunk_size=4096):
    time_escaped = time.time() - timer
    dl += len(data)
    if time_escaped >= 1.00:
      download_speed = (dl - tmp_dl)/(time_escaped*1024)
      if download_speed >= 1000.00:
        download_speed = str(round(download_speed/1024, 2)) + 'MB/s'
      else:
        download_speed = str(round(download_speed, 2)) + 'KB/s'
      tmp_dl = dl
      timer = time.time()

    f.write(data)
    done = int(50 * dl / total_length)
    sys.stdout.write("\r[%s%s] %s%s (%sMB/%sMB) %s" % ('=' * done, ' ' * (50-done), done * 2, '%', dl//(1024*1024), total_length//(1024*1024), download_speed))    
    sys.stdout.flush()

def resume_download(dataset_url, resume_byte_pos):
  local_filename = dataset_url.split('/')[-1]
  with open(local_filename, "ab") as f:
    print("Resuming %s" % local_filename)
    resume_header = {'Range': 'bytes=%d-' % resume_byte_pos}
    response = requests.get(dataset_url, headers=resume_header, stream=True)
    start_download(f, response, resume_byte_pos)

def download_from_beggining(dataset_url):
  local_filename = dataset_url.split('/')[-1]
  with open(local_filename, "wb") as f:
    print("Downloading %s" % local_filename)
    response = requests.get(dataset_url, stream=True)
    total_length = response.headers.get('content-length')

    if total_length is None:
      f.write(response.content)
    else:
      start_download(f, response)

if not os.path.exists('dataset/metadata.json') and os.path.exists('dataset') and count_dataset_files() >= 299: 
    with open('dataset/metadata.json', 'w', encoding='utf-8') as f:
        json.dump({ "version": "1.0" }, f, ensure_ascii=False, indent=4)
        
# Check Internet Connection
if not have_internet():
    sys.exit()

# Download Dataset Metadata
with urllib.request.urlopen(DATASET_METADATA) as url:
    data = json.loads(url.read().decode())
    latest_version = data['latest_version']
    updates_urls = data['updates']
  
# Check for Updates
DATASET_URLS = []
if os.path.exists('dataset/metadata.json'):  
    with open('dataset/metadata.json') as f:
        d = json.load(f)
        current_version = d['version']
        for version, url in data['updates'].items():
            if version > current_version:
                DATASET_URLS.append(url) 
else:
    for version, url in data['updates'].items():
        DATASET_URLS.append(url)
        
# Download updates
if len(DATASET_URLS) == 0:
    print('Dataset is already Upto Date')
else:
    for DATASET_URL in DATASET_URLS:
        local_filename = DATASET_URL.split('/')[-1]
        r = requests.head(DATASET_URL)
        downloading_file_size = int(r.headers['Content-Length'])

        if os.path.exists(local_filename):
          existing_file_size = int(os.stat(local_filename).st_size)
          if existing_file_size == downloading_file_size:
            print('File Already Downloaded')
          else:
            resume_download(DATASET_URL, existing_file_size)
        else:
          download_from_beggining(DATASET_URL)


        with zipfile.ZipFile(local_filename, 'r') as zip_ref:
          print('\n\nExtracting Dataset. It may take some time ...')
          zip_ref.extractall()

        print('Dataset Extracted.')
        try:
          os.remove(local_filename)
        except OSError:
          pass