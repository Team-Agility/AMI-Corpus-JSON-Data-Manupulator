import requests
import zipfile
import time
import sys
import os

DATASET_URL = 'https://objectstorage.ap-mumbai-1.oraclecloud.com/n/bm7noglpf2jq/b/FYP-Data/o/Dataset_JSON_Converted.zip'

local_filename = DATASET_URL.split('/')[-1]
r = requests.head(DATASET_URL)
downloading_file_size = int(r.headers['Content-Length'])

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

def resume_download(resume_byte_pos):
  with open(local_filename, "ab") as f:
    print("Resuming %s" % local_filename)
    resume_header = {'Range': 'bytes=%d-' % resume_byte_pos}
    response = requests.get(DATASET_URL, headers=resume_header, stream=True)
    start_download(f, response, resume_byte_pos)

def download_from_beggining():
  with open(local_filename, "wb") as f:
    print("Downloading %s" % local_filename)
    response = requests.get(DATASET_URL, stream=True)
    total_length = response.headers.get('content-length')

    if total_length is None:
      f.write(response.content)
    else:
      start_download(f, response)

if os.path.exists(local_filename):
  existing_file_size = int(os.stat(local_filename).st_size)
  if existing_file_size == downloading_file_size:
    print('File Already Downloaded')
  else:
    resume_download(existing_file_size)
else:
  download_from_beggining()


with zipfile.ZipFile(local_filename, 'r') as zip_ref:
  print('\n\nExtracting Dataset. It may take some time ...')
  zip_ref.extractall()

print('Dataset Extracted.')
try:
  os.remove(local_filename)
except OSError:
  pass