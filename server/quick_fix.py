#!/usr/bin/env python3
"""
Quick fix script for JokeBot setup issues
"""
import os
import shutil
import sys

def quick_fix():
    print("🔧 Running JokeBot Quick Fix...")
    print("=" * 50)
    
    artifacts_dir = 'artifacts'
    
    # Create artifacts directory if it doesn't exist
    if not os.path.exists(artifacts_dir):
        print(f"Creating {artifacts_dir} directory...")
        os.makedirs(artifacts_dir)
    
    # Check for model files in parent directories
    possible_source_dirs = [
        '.',
        '..',
        '../..',
        '../../models',
        '../models',
        'models'
    ]
    
    model_extensions = ['.pth', '.pt']
    found_files = []
    
    print("\n🔎 Searching for model files...")
    for source_dir in possible_source_dirs:
        if os.path.exists(source_dir):
            for item in os.listdir(source_dir):
                item_path = os.path.join(source_dir, item)
                if os.path.isfile(item_path) and any(item.endswith(ext) for ext in model_extensions):
                    found_files.append((item, item_path))
                    print(f"  Found: {item} in {source_dir}")
    
    if found_files:
        print(f"\n📦 Found {len(found_files)} model file(s).")
        
        # Pick the largest model file (likely the trained one)
        largest_file = max(found_files, key=lambda x: os.path.getsize(x[1]))
        file_name, file_path = largest_file
        
        print(f"\n📏 Largest model file: {file_name}")
        print(f"   Size: {os.path.getsize(file_path)/1024/1024:.2f} MB")
        
        # Copy to artifacts with a standard name
        dest_path = os.path.join(artifacts_dir, 'best_joke_model.pth')
        
        if os.path.exists(dest_path):
            print(f"\n⚠️ Model file already exists at {dest_path}")
            choice = input("Overwrite? (y/n): ").strip().lower()
            if choice != 'y':
                print("Keeping existing file.")
                return True
            else:
                print("Overwriting...")
        
        print(f"\n📋 Copying {file_name} to {dest_path}...")
        shutil.copy2(file_path, dest_path)
        
        # Also create symbolic links for other expected names
        alt_names = ['joke_classifier_final.pth', 'joke_model_weights.pth']
        
        for alt_name in alt_names:
            alt_path = os.path.join(artifacts_dir, alt_name)
            try:
                if not os.path.exists(alt_path):
                    os.symlink(dest_path, alt_path)
                    print(f"  Created symlink: {alt_name}")
            except:
                # On Windows or if symlink fails, copy instead
                if not os.path.exists(alt_path):
                    shutil.copy2(dest_path, alt_path)
                    print(f"  Copied as: {alt_name}")
        
        print(f"\n✅ Setup complete! Model ready in {artifacts_dir}/")
        
        # Check for tokenizer files
        print(f"\n🗣️ Checking for tokenizer files...")
        tokenizer_sources = [
            'tokenizer_vocab.json',
            '../tokenizer_vocab.json',
            '../../tokenizer_vocab.json'
        ]
        
        for source in tokenizer_sources:
            if os.path.exists(source):
                dest = os.path.join(artifacts_dir, os.path.basename(source))
                print(f"  Found {source}, copying...")
                shutil.copy2(source, dest)
        
        return True
    else:
        print(f"\n❌ No model files found!")
        print("\n💡 Please place your trained model file (.pth or .pt) in one of these locations:")
        print("   - server/artifacts/")
        print("   - server/")
        print("   - Jokes/ (parent directory)")
        print("\nThen run this script again.")
        return False

if __name__ == '__main__':
    # Change to server directory if needed
    if not os.path.exists('artifacts') and os.path.exists('server'):
        os.chdir('server')
        print("Changed to server directory")
    
    success = quick_fix()
    
    if success:
        print(f"\n🎉 Quick fix applied successfully!")
        print("Now run: python app.py")
    else:
        print(f"\n❌ Quick fix failed. Please check the instructions above.")
    
    sys.exit(0 if success else 1)