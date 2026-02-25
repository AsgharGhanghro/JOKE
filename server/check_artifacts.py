#!/usr/bin/env python3
"""
Check exactly what's in your artifacts directory
"""
import os
import sys

def check_artifacts():
    print("🔍 Checking artifacts directory...")
    print("=" * 50)
    
    # Current directory
    print(f"Current directory: {os.getcwd()}")
    
    # Check if artifacts exists
    artifacts_dir = 'artifacts'
    if not os.path.exists(artifacts_dir):
        print(f"❌ ERROR: '{artifacts_dir}' directory does not exist!")
        print(f"Looking for: {os.path.abspath(artifacts_dir)}")
        return False
    
    print(f"✅ Found artifacts directory: {os.path.abspath(artifacts_dir)}")
    
    # List all files
    print(f"\n📂 Contents of artifacts directory:")
    files = os.listdir(artifacts_dir)
    
    if not files:
        print("❌ Directory is EMPTY!")
        return False
    
    for i, file in enumerate(files, 1):
        file_path = os.path.join(artifacts_dir, file)
        if os.path.isfile(file_path):
            size = os.path.getsize(file_path)
            print(f"{i:2}. {file:30} - {size:,} bytes ({size/1024/1024:.2f} MB)")
        else:
            print(f"{i:2}. {file:30} - [DIRECTORY]")
    
    # Check for model files
    print(f"\n🔎 Looking for model files:")
    model_files = []
    for file in files:
        if file.endswith('.pth') or file.endswith('.pt'):
            model_files.append(file)
    
    if model_files:
        print(f"✅ Found {len(model_files)} model file(s):")
        for model_file in model_files:
            path = os.path.join(artifacts_dir, model_file)
            size = os.path.getsize(path)
            print(f"  - {model_file} ({size/1024/1024:.2f} MB)")
    else:
        print("❌ NO model files found!")
        print("Model files should have .pth or .pt extension")
    
    # Check what the model loader is looking for
    print(f"\n🔧 What model_loader.py expects:")
    possible_files = [
        'best_joke_model.pth',
        'joke_classifier_final.pth', 
        'joke_model_weights.pth',
        'best_model.pth',
        'model.pth',
        'model.pt'
    ]
    
    for expected_file in possible_files:
        exists = os.path.exists(os.path.join(artifacts_dir, expected_file))
        status = "✅ FOUND" if exists else "❌ NOT FOUND"
        print(f"  {expected_file:30} - {status}")
    
    return len(model_files) > 0

if __name__ == '__main__':
    success = check_artifacts()
    print(f"\n" + "=" * 50)
    if success:
        print("✅ Artifacts directory looks good!")
        print("\n💡 If model is still not loading, check:")
        print("   1. File permissions")
        print("   2. Corrupted model file")
        print("   3. PyTorch version compatibility")
    else:
        print("❌ Issues found with artifacts directory!")
    
    sys.exit(0 if success else 1)