# #!/usr/bin/env python3
# """
# INSANE JOKE REACTOR 9000 - LAUNCHER
# """

# import os
# import sys
# import subprocess
# import time
# import webbrowser
# from threading import Thread
# import colorama
# from colorama import Fore, Style, Back

# colorama.init(autoreset=True)

# def print_banner():
#     """Print insane ASCII banner"""
#     banner = f"""
# {Fore.CYAN}
# ╔══════════════════════════════════════════════════════════════════════════════╗
# {Fore.MAGENTA}║{Fore.CYAN}    ██╗ ██████╗ ██╗  ██╗███████╗    {Fore.YELLOW}██████╗ ███████╗  █████╗  ██████╗████████╗{Fore.CYAN}    ║
# ║{Fore.MAGENTA}    ██║██╔═══██╗██║ ██╔╝██╔════╝    {Fore.YELLOW}██╔══██╗██╔════╝ ██╔══██╗██╔════╝╚══██╔══╝{Fore.MAGENTA}    ║
# ║{Fore.CYAN}    ██║██║   ██║█████╔╝ █████╗      {Fore.YELLOW}██████╔╝█████╗   ███████║██║        ██║   {Fore.CYAN}    ║
# ║{Fore.MAGENTA}    ██║██║   ██║██╔═██╗ ██╔══╝      {Fore.YELLOW}██╔══██╗██╔══╝   ██╔══██║██║        ██║   {Fore.MAGENTA}    ║
# ║{Fore.CYAN}    ██║╚██████╔╝██║  ██╗███████╗    {Fore.YELLOW}██║  ██║███████╗ ██║  ██║╚██████╗   ██║   {Fore.CYAN}    ║
# ║{Fore.MAGENTA}    ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝    {Fore.YELLOW}╚═╝  ╚═╝╚══════╝ ╚═╝  ╚═╝ ╚═════╝   ╚═╝   {Fore.MAGENTA}    ║
# ║                                                                              ║
# ║{Fore.GREEN}                    ⚡ JOKE REACTOR 9000 - VOICE ACTIVATED ⚡                    {Fore.MAGENTA}║
# ║{Fore.WHITE}                 Advanced AI Comedy Analysis with Battery Physics               {Fore.CYAN}║
# ╚══════════════════════════════════════════════════════════════════════════════╝
# {Style.RESET_ALL}
#     """
#     print(banner)

# def check_system():
#     """Check system requirements"""
#     print(f"{Fore.CYAN}[SYSTEM CHECK]{Style.RESET_ALL}")
    
#     # Check Python version
#     python_version = sys.version_info
#     if python_version.major == 3 and python_version.minor >= 8:
#         print(f"  {Fore.GREEN}✓ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
#     else:
#         print(f"  {Fore.RED}✗ Python 3.8+ required (found {python_version.major}.{python_version.minor})")
#         return False
    
#     # Check directories
#     directories = ['client', 'server', 'server/artifacts']
#     for directory in directories:
#         if os.path.exists(directory):
#             print(f"  {Fore.GREEN}✓ Directory: {directory}")
#         else:
#             print(f"  {Fore.YELLOW}⚠ Directory missing: {directory}")
    
#     # Check model files
#     artifacts_dir = 'server/artifacts'
#     if os.path.exists(artifacts_dir):
#         model_files = [f for f in os.listdir(artifacts_dir) if f.endswith(('.pth', '.json'))]
#         if model_files:
#             print(f"  {Fore.GREEN}✓ Found {len(model_files)} model files")
#         else:
#             print(f"  {Fore.YELLOW}⚠ No model files found (will use fallback mode)")
#     else:
#         print(f"  {Fore.YELLOW}⚠ Artifacts directory not found")
    
#     print()
#     return True

# def install_requirements():
#     """Install Python requirements"""
#     print(f"{Fore.CYAN}[INSTALLING DEPENDENCIES]{Style.RESET_ALL}")
    
#     requirements_file = 'server/requirements.txt'
#     if os.path.exists(requirements_file):
#         try:
#             subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
#             print(f"  {Fore.GREEN}✓ Requirements installed")
#         except subprocess.CalledProcessError as e:
#             print(f"  {Fore.RED}✗ Failed to install requirements: {e}")
#             return False
#     else:
#         print(f"  {Fore.YELLOW}⚠ Requirements file not found")
    
#     print()
#     return True

# def start_backend():
#     """Start the Flask backend server"""
#     print(f"{Fore.CYAN}[STARTING REACTOR CORE]{Style.RESET_ALL}")
    
#     backend_dir = 'server'
#     if not os.path.exists(backend_dir):
#         print(f"  {Fore.RED}✗ Backend directory not found")
#         return False
    
#     os.chdir(backend_dir)
    
#     # Check if port 5000 is available
#     import socket
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     result = sock.connect_ex(('localhost', 5000))
#     sock.close()
    
#     if result == 0:
#         print(f"  {Fore.YELLOW}⚠ Port 5000 is already in use")
#         print(f"  {Fore.WHITE}  Trying port 5001...")
#         port = 5001
#     else:
#         port = 5000
    
#     # Start server
#     print(f"  {Fore.WHITE}Starting backend on port {port}...")
    
#     if sys.platform == "win32":
#         # Windows
#         subprocess.Popen([sys.executable, "app.py"], 
#                         creationflags=subprocess.CREATE_NEW_CONSOLE)
#     else:
#         # Unix/Linux/Mac
#         subprocess.Popen([sys.executable, "app.py"])
    
#     time.sleep(5)  # Give server time to start
#     os.chdir('..')
    
#     print(f"  {Fore.GREEN}✓ Backend started on http://localhost:{port}")
#     print()
#     return port

# def start_frontend(port):
#     """Open the frontend in browser"""
#     print(f"{Fore.CYAN}[ACTIVATING USER INTERFACE]{Style.RESET_ALL}")
    
#     time.sleep(3)  # Wait for backend to fully start
    
#     url = f"http://localhost:{port}"
    
#     print(f"  {Fore.WHITE}Opening {url} in browser...")
    
#     try:
#         webbrowser.open(url)
#         print(f"  {Fore.GREEN}✓ Browser opened")
#     except Exception as e:
#         print(f"  {Fore.YELLOW}⚠ Could not open browser: {e}")
#         print(f"  {Fore.WHITE}  Please manually open: {url}")
    
#     print()

# def show_controls():
#     """Show control instructions"""
#     print(f"{Fore.CYAN}[CONTROLS]{Style.RESET_ALL}")
#     print(f"  {Fore.WHITE}🎤 Voice Input: Click the glowing orb to record")
#     print(f"  {Fore.WHITE}⚡ Battery: Watch it react to joke quality")
#     print(f"  {Fore.WHITE}📊 Analysis: See detailed breakdown of each joke")
#     print(f"  {Fore.WHITE}🎮 Effects: Battery explosions, energy waves, sparks")
#     print(f"  {Fore.WHITE}🏆 Achievements: Unlock awards for great jokes")
#     print()

# def run_diagnostics():
#     """Run system diagnostics"""
#     print(f"{Fore.CYAN}[RUNNING DIAGNOSTICS]{Style.RESET_ALL}")
    
#     # Test backend connection
#     import requests
#     try:
#         response = requests.get('http://localhost:5000/health', timeout=2)
#         if response.status_code == 200:
#             print(f"  {Fore.GREEN}✓ Backend connection: HEALTHY")
#             data = response.json()
#             if data.get('model_loaded'):
#                 print(f"  {Fore.GREEN}✓ AI Model: LOADED")
#             else:
#                 print(f"  {Fore.YELLOW}⚠ AI Model: FALLBACK MODE")
#         else:
#             print(f"  {Fore.YELLOW}⚠ Backend connection: UNSTABLE")
#     except:
#         print(f"  {Fore.RED}✗ Backend connection: FAILED")
    
#     # Check voice support
#     try:
#         import speech_recognition
#         print(f"  {Fore.GREEN}✓ Voice recognition: SUPPORTED")
#     except:
#         print(f"  {Fore.YELLOW}⚠ Voice recognition: NOT AVAILABLE")
    
#     print()

# def main():
#     """Main launcher function"""
#     print_banner()
    
#     if not check_system():
#         print(f"{Fore.RED}System check failed. Exiting.{Style.RESET_ALL}")
#         return
    
#     # Install requirements
#     if not install_requirements():
#         print(f"{Fore.YELLOW}Continuing with existing installations...{Style.RESET_ALL}")
    
#     # Start backend
#     port = start_backend()
#     if not port:
#         print(f"{Fore.RED}Failed to start backend. Exiting.{Style.RESET_ALL}")
#         return
    
#     # Show controls
#     show_controls()
    
#     # Start frontend
#     start_frontend(port)
    
#     # Run diagnostics
#     Thread(target=run_diagnostics).start()
    
#     print(f"{Fore.GREEN}{'='*70}{Style.RESET_ALL}")
#     print(f"{Fore.GREEN}🚀 JOKE REACTOR 9000 - READY FOR DEPLOYMENT{Style.RESET_ALL}")
#     print(f"{Fore.GREEN}{'='*70}{Style.RESET_ALL}")
#     print()
#     print(f"{Fore.WHITE}💡 Tips:{Style.RESET_ALL}")
#     print(f"  • Speak clearly into your microphone")
#     print(f"  • Try different joke styles and deliveries")
#     print(f"  • Watch the battery react to your comedy")
#     print(f"  • Unlock achievements with great jokes")
#     print(f"  • Adjust sensitivity for different reactions")
#     print()
#     print(f"{Fore.YELLOW}⚠ Press Ctrl+C to shutdown the reactor{Style.RESET_ALL}")
#     print()
    
#     # Keep alive
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         print(f"\n{Fore.RED}🛑 SHUTTING DOWN REACTOR...{Style.RESET_ALL}")
#         sys.exit(0)

# if __name__ == "__main__":
#     main()