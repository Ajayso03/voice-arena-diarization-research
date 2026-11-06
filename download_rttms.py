import urllib.request
import re
from bs4 import BeautifulSoup
import os

folders = {
    'deepgram_nova3': '1jMNYXZqIgGU8ns__qI3iCoMUK-bU8fFz',
    'reference': '1kLDKWQ4epW7tz9NLE42I2q_2Y68haHtg',
    'silero_vad': '186rm-0GPhEqiCt24sBm1xjOZcCyuh0k1'
}

for folder_name, folder_id in folders.items():
    print(f"Fetching folder {folder_name} ({folder_id})...")
    url = f"https://drive.google.com/drive/folders/{folder_id}?usp=sharing"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find_all('tr', attrs={'data-selectable': True})
        print(f"Found {len(rows)} items in {folder_name}")
        os.makedirs(f"RTTM_files/{folder_name}", exist_ok=True)
        for r in rows:
            file_id = r.get('data-id')
            text = r.get_text(separator=' | ', strip=True)
            print(f"  {file_id}: {text}")
            # Try to download
            # Extract filename from text
            fname = text.split('|')[1].strip() if '|' in text else f"{file_id}.rttm"
            if not fname.endswith('.rttm'):
                # find part that ends with .rttm
                for part in text.split('|'):
                    if '.rttm' in part:
                        fname = part.strip()
                        break
            dl_url = f"https://drive.google.com/uc?export=download&id={file_id}"
            out_path = f"RTTM_files/{folder_name}/{fname}"
            urllib.request.urlretrieve(dl_url, out_path)
            print(f"    Downloaded to {out_path} ({os.path.getsize(out_path)} bytes)")
    except Exception as e:
        print(f"Error fetching {folder_name}: {e}")

