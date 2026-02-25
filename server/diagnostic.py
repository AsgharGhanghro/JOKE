#!/usr/bin/env python3
"""
Check model file structure
"""
import os
import struct

def check_model_file():
    print("🔍 Analyzing model file...")
    
    model_path = 'artifacts/best_joke_model.pth'
    
    if not os.path.exists(model_path):
        print(f"❌ File not found: {model_path}")
        return
    
    print(f"📏 File size: {os.path.getsize(model_path):,} bytes")
    
    # Read first 100 bytes
    with open(model_path, 'rb') as f:
        first_bytes = f.read(100)
    
    print(f"\n📊 First 100 bytes (hex):")
    hex_str = ' '.join(f'{b:02x}' for b in first_bytes[:50])
    print(f"   {hex_str}")
    if len(first_bytes) > 50:
        hex_str = ' '.join(f'{b:02x}' for b in first_bytes[50:100])
        print(f"   {hex_str}")
    
    print(f"\n📊 First 100 bytes (ASCII):")
    ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in first_bytes[:50])
    print(f"   {ascii_str}")
    if len(first_bytes) > 50:
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in first_bytes[50:100])
        print(f"   {ascii_str}")
    
    # Check for common file signatures
    print(f"\n🔍 Checking file signature:")
    
    signatures = {
        b'\x80\x02': "Python pickle file",
        b'\x50\x4b\x03\x04': "ZIP file (PyTorch 1.6+)",
        b'\x50\x4b\x05\x06': "ZIP file (empty)",
        b'\x50\x4b\x07\x08': "ZIP file (spanned)",
        b'PK\x03\x04': "ZIP file (alternative)",
        b'\x89PNG\r\n\x1a\n': "PNG image",
        b'\xff\xd8\xff': "JPEG image",
        b'\x00\x00\x00': "Possible NULL padding",
    }
    
    found = False
    for sig, desc in signatures.items():
        if first_bytes.startswith(sig):
            print(f"   ✅ {desc}")
            found = True
            break
    
    if not found:
        # Check for PyTorch v0.1.10 - v0.1.12
        if len(first_bytes) >= 8:
            magic_number, version = struct.unpack('<QQ', first_bytes[:16])
            if magic_number == 0x1950a86a20d64ce8:
                print(f"   ✅ PyTorch file v{version}")
                found = True
    
    if not found:
        print(f"   ❓ Unknown file format")
    
    # Try to read as text
    print(f"\n📝 Trying to read as text...")
    try:
        with open(model_path, 'r', encoding='utf-8', errors='ignore') as f:
            first_line = f.readline(500).strip()
            print(f"   First line: {first_line[:100]}...")
    except:
        print("   Cannot read as text (binary file)")
    
    # Check if it's actually a PNG (confusion matrix)
    if first_bytes.startswith(b'\x89PNG'):
        print(f"\n⚠️ This appears to be a PNG image, not a model file!")
        print(f"   File might be misnamed. Check if it's actually confusion_matrix.png")

if __name__ == '__main__':
    check_model_file()