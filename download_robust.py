import urllib.request
import time
import os
import re
from bs4 import BeautifulSoup

folders = {
    'deepgram_nova3': '1jMNYXZqIgGU8ns__qI3iCoMUK-bU8fFz',
    'reference': '1kLDKWQ4epW7tz9NLE42I2q_2Y68haHtg',
    'silero_vad': '186rm-0GPhEqiCt24sBm1xjOZcCyuh0k1'
}

opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')]
urllib.request.install_opener(opener)

def get_with_retry(url, retries=5, delay=2):
    for i in range(retries):
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read()
        except Exception as e:
            print(f"  Attempt {i+1} failed: {e}. Retrying in {delay}s...")
            time.sleep(delay)
            delay *= 2
    raise Exception(f"Failed to fetch {url} after {retries} retries.")

for folder_name, folder_id in folders.items():
    print(f"\n=== Processing folder: {folder_name} ({folder_id}) ===")
    os.makedirs(f"RTTM_files/{folder_name}", exist_ok=True)
    folder_url = f"https://drive.google.com/drive/folders/{folder_id}?usp=sharing"
    
    html = get_with_retry(folder_url).decode('utf-8', errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.find_all('tr', attrs={'data-selectable': True})
    print(f"Found {len(rows)} rows in {folder_name}")
    
    for r in rows:
        file_id = r.get('data-id')
        text = r.get_text(separator=' | ', strip=True)
        # extract filename ending in .rttm
        fname = None
        for part in text.split('|'):
            if '.rttm' in part:
                fname = part.strip()
                break
        if not fname:
            fname = f"{file_id}.rttm"
            
        out_path = f"RTTM_files/{folder_name}/{fname}"
        if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
            print(f"  [Skip existing] {fname} ({os.path.getsize(out_path)} bytes)")
            continue
            
        dl_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        try:
            data = get_with_retry(dl_url)
            with open(out_path, 'wb') as f:
                f.write(data)
            print(f"  [Downloaded] {fname} ({len(data)} bytes)")
            time.sleep(0.5) # polite delay
        except Exception as e:
            print(f"  [Error downloading {fname}]: {e}")

print("\nFinished checking all folders.")

