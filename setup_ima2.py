# -*- coding: utf-8 -*-
import os, shutil, subprocess, json

# Step 1: Get existing credentials from old token script
client_id = ''
api_key = ''
try:
    result = subprocess.run(
        ['powershell.exe', '-NoProfile', '-ExecutionPolicy', 'Bypass',
         '-File', 'C:/Program Files/QClaw/resources/openclaw/config/skills/ima/get-token.ps1'],
        capture_output=True, text=True, timeout=10
    )
    if result.stdout.strip():
        creds = json.loads(result.stdout.strip())
        client_id = creds.get('client_id', '')
        api_key = creds.get('api_key', '')
        print("Found existing credentials from old token script")
except Exception as e:
    print(f"Could not read old token script: {e}")

# Step 2: Save to new config location
config_dir = os.path.expanduser('~/.config/ima')
os.makedirs(config_dir, exist_ok=True)

if client_id and api_key:
    with open(os.path.join(config_dir, 'client_id'), 'w') as f:
        f.write(client_id)
    with open(os.path.join(config_dir, 'api_key'), 'w') as f:
        f.write(api_key)
    print(f"Credentials saved to {config_dir}")
else:
    print("ERROR: No credentials found")
    print("Please visit https://ima.qq.com/agent-interface to get your Client ID and API Key")

# Step 3: Copy new skill files to local directory
src = r'C:\Users\jin\.qclaw\workspace\ima-skills-1.1.2\ima-skill'
dst = r'C:\Users\jin\.qclaw\resources\openclaw\config\skills\ima_local'
os.makedirs(dst, exist_ok=True)

copied = []
for root, dirs, files in os.walk(src):
    rel = os.path.relpath(root, src)
    dst_root = os.path.join(dst, rel) if rel != '.' else dst
    os.makedirs(dst_root, exist_ok=True)
    for f in files:
        src_f = os.path.join(root, f)
        dst_f = os.path.join(dst_root, f)
        try:
            shutil.copy2(src_f, dst_f)
            rel_path = os.path.join(rel, f) if rel != '.' else f
            copied.append(rel_path)
        except Exception as e:
            print(f"FAILED: {f}: {e}")

print(f"New skill installed to: {dst}")
print(f"Files copied: {len(copied)}")
for c in copied:
    print(f"  {c}")
