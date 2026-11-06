import os
import glob
import json
import pandas as pd

def import_results():
    tracker_path = "JoshTalks_Growth_Assessment/question_2/experiments/experiment_tracker.csv"
    screenshots_dir = "JoshTalks_Growth_Assessment/proof/screenshots"
    responses_dir = "JoshTalks_Growth_Assessment/proof/responses"
    
    os.makedirs(screenshots_dir, exist_ok=True)
    os.makedirs(responses_dir, exist_ok=True)
    
    if not os.path.exists(tracker_path):
        print(f"Tracker file not found at {tracker_path}")
        return
        
    df = pd.read_csv(tracker_path)
    print("=== DEEPGRAM PLAYGROUND EXPERIMENT STATUS ===")
    
    # Check JSON responses
    json_files = glob.glob(os.path.join(responses_dir, "*.json"))
    print(f"Found {len(json_files)} uploaded JSON responses in {responses_dir}")
    
    # Check screenshots
    img_files = glob.glob(os.path.join(screenshots_dir, "*.*"))
    print(f"Found {len(img_files)} uploaded screenshots in {screenshots_dir}\n")
    
    for idx, row in df.iterrows():
        exp_id = row['Exp_ID']
        sid = row['Session_ID']
        # Look for corresponding response file
        resp_file = os.path.join(responses_dir, f"{exp_id}_response.json")
        screenshot_file = row['Screenshot_Path']
        
        has_resp = os.path.exists(resp_file)
        has_shot = os.path.exists(screenshot_file)
        
        if has_resp:
            try:
                with open(resp_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                # extract metadata
                req_id = data.get('metadata', {}).get('request_id', '')
                channels = data.get('results', {}).get('channels', [])
                words_found = 0
                if channels:
                    alts = channels[0].get('alternatives', [])
                    if alts:
                        words_found = len(alts[0].get('words', []))
                
                df.at[idx, 'Observed_Request_ID'] = req_id
                df.at[idx, 'Observed_Words_Returned'] = words_found
                df.at[idx, 'Status'] = 'COMPLETED'
                df.at[idx, 'Validation_Notes'] = f"Imported from {exp_id}_response.json: {words_found} words found"
            except Exception as e:
                df.at[idx, 'Validation_Notes'] = f"Error reading JSON: {e}"
                
        print(f"[{exp_id}] {sid} | Model: {row['Model']} | Lang: {row['Language']}")
        print(f"   Benchmark Words: {row['Benchmark_Words']} | Observed Words: {row['Observed_Words_Returned']}")
        print(f"   Screenshot: {'FOUND' if has_shot else 'AWAITING'} | Status: {row['Status']}")
        print(f"   Notes: {row['Validation_Notes']}\n")
        
    df.to_csv(tracker_path, index=False)
    print(f"Updated tracker saved to {tracker_path}")

if __name__ == "__main__":
    import_results()

