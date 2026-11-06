import urllib.request
import re
import json

url = 'https://drive.google.com/drive/folders/1Z3vd_9nPBFyzAiF6v28QoZCFmBzz1ENW?usp=sharing'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        with open('drive_page.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("Wrote drive_page.html, length:", len(html))
        
        # Look for zip file references or filenames
        # Patterns in Google Drive initial data:
        # e.g. ["fileName.zip", ... "id" ...]
        zips = set(re.findall(r'[\w\.-]+\.zip', html, re.I))
        rttms = set(re.findall(r'[\w\.-]+\.rttm', html, re.I))
        print("ZIPs found in HTML:", zips)
        print("RTTMs found in HTML:", rttms)
        
        # Find drive file IDs
        # Look for 33-char drive IDs
        # usually 1[a-zA-Z0-9_-]{32}
        candidates = set(re.findall(r'1[a-zA-Z0-9_-]{32}', html))
        print("Candidate IDs count:", len(candidates))
        for c in candidates:
            if c != '1Z3vd_9nPBFyzAiF6v28QoZCFmBzz1ENW':
                print("Candidate ID:", c)
except Exception as e:
    print("Error:", e)

