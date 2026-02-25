#!/usr/bin/env python3
"""
Joke Quality Evaluator - Application Launcher
Run this script to start both backend and frontend
"""

import os
import sys
import subprocess
import time
import webbrowser
from threading import Thread

def start_backend():
    """Start the Flask backend server"""
    backend_dir = os.path.join(os.path.dirname(__file__), 'server')
    os.chdir(backend_dir)
    
    print("🚀 Starting backend server...")
    print(f"📁 Backend directory: {backend_dir}")
    
    # Check if requirements are installed
    try:
        import flask
        import torch
        import transformers
        print("✅ All dependencies found")
    except ImportError as e:
        print(f"⚠️ Missing dependency: {e}")
        print("Installing requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Start Flask server
    cmd = [sys.executable, "app.py"]
    
    if sys.platform == "win32":
        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        subprocess.Popen(cmd)
    
    time.sleep(3)  # Give server time to start

def start_frontend():
    """Open the frontend in browser"""
    time.sleep(5)  # Wait for backend to fully start
    
    print("🌐 Opening frontend in browser...")
    url = "http://localhost:5000"
    
    try:
        webbrowser.open(url)
        print(f"✅ Frontend opened at: {url}")
    except Exception as e:
        print(f"⚠️ Could not open browser: {e}")
        print(f"Please manually open: {url}")

def check_artifacts():
    """Check if model artifacts exist"""
    artifacts_dir = os.path.join(os.path.dirname(__file__), 'server', 'artifacts')
    
    if not os.path.exists(artifacts_dir):
        print(f"❌ Artifacts directory not found: {artifacts_dir}")
        print("Please make sure your model files are in server/artifacts/")
        return False
    
    # Check for model files
    expected_files = [
        'best_joke_model.pth',
        'joke_classifier_final.pth', 
        'joke_model_weights.pth',
        'tokenizer_vocab.json',
        'model_info.json'
    ]
    
    found_files = []
    for file in expected_files:
        path = os.path.join(artifacts_dir, file)
        if os.path.exists(path):
            found_files.append(file)
    
    if found_files:
        print(f"✅ Found {len(found_files)} model files: {', '.join(found_files)}")
        return True
    else:
        print("❌ No model files found in artifacts directory")
        print("The app will run in fallback mode")
        return True  # Still allow app to run in fallback mode

def main():
    """Main launcher function"""
    print("=" * 60)
    print("🤖 JOKE QUALITY EVALUATOR - FULL STACK APPLICATION")
    print("=" * 60)
    
    # Check artifacts
    check_artifacts()
    
    # Start backend in separate thread
    backend_thread = Thread(target=start_backend)
    backend_thread.daemon = True
    backend_thread.start()
    
    # Start frontend
    frontend_thread = Thread(target=start_frontend)
    frontend_thread.daemon = True
    frontend_thread.start()
    
    print("\n✅ Application started successfully!")
    print("\n📊 Application Information:")
    print(f"   Frontend: http://localhost:5000")
    print(f"   Backend API: http://localhost:5000/evaluate")
    print(f"   Health check: http://localhost:5000/health")
    print("\n🎯 How to use:")
    print("   1. Enter a joke in the text box or use voice input")
    print("   2. Click 'Evaluate Joke'")
    print("   3. Watch the AI analyze and rate your joke")
    print("   4. See how it affects the joke battery")
    print("\n⚠️ Press Ctrl+C to stop the application")
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Shutting down application...")
        sys.exit(0)

if __name__ == "__main__":
    main()