import os
import re

def scan_for_secrets():
    # Regex for 12-digit CCCD
    cccd_pattern = re.compile(r'\b\d{12}\b')
    # Regex for phone number
    phone_pattern = re.compile(r'\b0[35789]\d{8}\b')
    
    secret_found = False
    print("Starting Security Scan for PII leaks...")
    
    for root, dirs, files in os.walk("."):
        if ".git" in dirs:
            dirs.remove(".git")
        if "venv" in dirs:
            dirs.remove("venv")
            
        for file in files:
            if file.endswith((".py", ".csv", ".txt", ".md")):
                path = os.path.join(root, file)
                # Skip the data directory as it's expected to have PII in raw
                if "data/raw" in path:
                    continue
                
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        for i, line in enumerate(f, 1):
                            if cccd_pattern.search(line):
                                print(f"⚠️ POTENTIAL LEAK: 12-digit number found in {path}:{i}")
                                secret_found = True
                            if phone_pattern.search(line):
                                if "regex=" in line or "text =" in line: # Skip the detector code itself
                                    continue
                                print(f"⚠️ POTENTIAL LEAK: Phone number found in {path}:{i}")
                                secret_found = True
                except Exception:
                    pass

    if not secret_found:
        print("OK: No PII leaks detected in code files.")
    else:
        print("FAIL: Scan failed: Secrets detected. Please remove them before committing.")


if __name__ == "__main__":
    scan_for_secrets()
