import sys
import os
sys.path.append(os.getcwd())

from src.encryption.vault import SimpleVault
import pandas as pd

vault = SimpleVault()

# Test round-trip
original = "Nguyen Van A - CCCD: 012345678901"
encrypted = vault.encrypt_data(original)
print("Encrypted:", encrypted)

decrypted = vault.decrypt_data(encrypted)
print("Decrypted:", decrypted)
if decrypted == original:
    print("Encryption round-trip PASSED!")
else:
    print("Encryption round-trip FAILED!")
