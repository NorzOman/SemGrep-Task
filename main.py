# Import required libraries
import platform
import shutil
import os
import time
import urllib.request
import zipfile
from colorama import Fore, init

# Initialize colorama
init()

# Defining global variables
is_kali = False
is_apt = False
is_dnf = False
is_jadx = False
is_semgrep = False
is_pip = False

# Function to print the banner
def banner():
    print(Fore.CYAN + "                                                                                ")
    print("                                                                                ")
    print("          ,((((((((((((((,       /(((((((((((((/       *((((((((((((((          ")
    print("       ,((((((((((((((((((((* ((((((((((((((((((((( /((((((((((((((((((((       ")
    print("      (((((((((,    ,((((((*(((((((((*     *(((((((((/(((((/     ,(((((((((     ")
    print("    ,(((((((            /(((((((((            ,(((((((((,            (((((((,   ")
    print("    ((((((,               (((((((               (((((((               (((((((   ")
    print("   ,((((((                ((((((*               /((((((               ,((((((   ")
    print("    ((((((*              ,(((((((               (((((((,              (((((((   ")
    print("    ,(((((((            ((((((((((,           *(((((((((/           ,(((((((    ")
    print("      (((((((((/,  ,*((((((((( (((((((,   *(((((((*(((((((((*   ,/(((((((((     ")
    print("        ((((((((((((((((((((  ((((((((((((((((((((, ,((((((((((((((((((((       ")
    print("           /(((((((((((((        ,(((((((((((((,        (((((((((((((*          ")
    print("                                                                                ")
    print("                                                            -Tushar H1dden      " + Fore.RESET)

def check_requirements():
    global is_kali, is_apt, is_dnf, is_jadx, is_semgrep, is_pip
    
    # Check OS
    time.sleep(0.5)
    os_name = platform.uname().system.lower()
    if "windows" in os_name:
        print('\n[!] Windows not supported by the script, check supported platforms on the github repo')
        exit(1)
    if "kali" in os_name:
        print('\n' + Fore.GREEN + '[-] Kali linux detected, enabling For-Kali mode')
        is_kali = True

    # Check package managers
    time.sleep(0.5)
    if shutil.which("apt"):
        is_apt = True
        print('\n' + Fore.GREEN + '[-] APT package manager found')
    elif shutil.which("dnf"):
        is_dnf = True
        print('\n' + Fore.GREEN + '[-] DNF package manager found')
    else:
        print('\n' + Fore.YELLOW + '[?] Neither APT nor DNF found')
        exit(1)

    # Check required tools
    time.sleep(0.5)
    jadx_path = os.path.expanduser('~/SemGrepTool/jadx/bin/jadx')
    if os.path.exists(jadx_path):
        os.environ["PATH"] += os.pathsep + os.path.dirname(jadx_path)
        is_jadx = True
        print('\n' + Fore.GREEN + '[-] Found jadx in ~/SemGrepTool/jadx...')
    else:
        print('\n' + Fore.RED + '[!] Required tool jadx was not found in the system...')
        is_jadx = False

    time.sleep(0.5)
    if shutil.which("semgrep"):
        print('\n' + Fore.GREEN + '[-] Required tool semgrep is installed...')
        is_semgrep = True
    else:
        print('\n' + Fore.RED + '[!] Required tool semgrep was not found in the system...')
        is_semgrep = False

    time.sleep(0.5)
    if shutil.which("pip") or shutil.which("pip3"):
        print('\n' + Fore.GREEN + '[-] Required tool pip is installed...')
        is_pip = True
    else:
        print('\n' + Fore.RED + '[!] Required tool pip was not found in the system...')
        is_pip = False

def install_requirements():
    global is_kali, is_apt, is_dnf, is_pip, is_semgrep, is_jadx
    print('\n' + Fore.YELLOW + '[?] Would you like to update the system? This can help with installation errors [Y/n]: ' + Fore.RESET)
    update_choice = input().lower()
    if update_choice == '' or update_choice == 'y':
        print('\n' + Fore.GREEN + '[-] Updating the system...' + Fore.RESET)
        if is_kali or is_apt:
            os.system('sudo apt update')
        elif is_dnf:
            os.system('sudo dnf update')

    # Setting up pip
    if not is_pip:
        print('\n' + Fore.YELLOW + '[?] pip is not installed. Would you like to install it? [Y/n]: ' + Fore.RESET)
        pip_choice = input().lower()
        if pip_choice == '' or pip_choice == 'y':
            print('\n' + Fore.RED + '[!] Installing pip...' + Fore.RESET)
            if is_kali or is_apt:
                os.system('sudo apt install python3-pip')
            elif is_dnf:
                os.system('sudo dnf install python3-pip')
            is_pip = True
        else:
            print('\n' + Fore.RED + '[!] pip installation rejected. Cannot proceed without pip. Exiting...' + Fore.RESET)
            exit(1)

    # Setting up semgrep
    if not is_semgrep:
        print('\n' + Fore.YELLOW + '[?] semgrep is not installed. Would you like to install it? [Y/n]: ' + Fore.RESET)
        semgrep_choice = input().lower()
        if semgrep_choice == '' or semgrep_choice == 'y':
            print('\n' + Fore.RED + '[!] Installing semgrep...' + Fore.RESET)
            try:
                if os.system('pip install semgrep --break-system-packages') != 0:
                    if os.system('pip3 install semgrep --break-system-packages') != 0:
                        raise Exception("Failed to install semgrep")
                is_semgrep = True
            except Exception as e:
                print('\n' + Fore.RED + f'[!] Error installing semgrep: {str(e)}' + Fore.RESET)
                exit(1)
        else:
            print('\n' + Fore.RED + '[!] semgrep installation rejected. Cannot proceed without semgrep. Exiting...' + Fore.RESET)
            exit(1)
    
    # Setting up jadx
    if not is_jadx:
        print('\n' + Fore.YELLOW + '[?] jadx is not installed. Would you like to install it? [Y/n]: ' + Fore.RESET)
        jadx_choice = input().lower()
        if jadx_choice == '' or jadx_choice == 'y':
            print('\n' + Fore.RED + '[!] Installing jadx...' + Fore.RESET)

            tool_dir = os.path.expanduser('~/SemGrepTool')
            jadx_dir = os.path.join(tool_dir, 'jadx')
            if not os.path.exists(jadx_dir):
                os.makedirs(jadx_dir)
            
            try:
                # Download jadx
                jadx_url = "https://github.com/skylot/jadx/releases/download/v1.5.1/jadx-1.5.1.zip"
                zip_path = os.path.join(jadx_dir, "jadx.zip")
                print('\n' + Fore.GREEN + '[-] Pulling jadx...This may take a while depending on your internet speed...Please be patient...' + Fore.RESET)
                urllib.request.urlretrieve(jadx_url, zip_path)
                
                # Extract zip
                print('\n' + Fore.GREEN + '[-] Extracting jadx...' + Fore.RESET)
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(jadx_dir)
                
                # Make jadx executable
                jadx_bin = os.path.join(jadx_dir, 'bin', 'jadx')
                print('\n' + Fore.GREEN + '[-] Making jadx executable...' + Fore.RESET)
                os.chmod(jadx_bin, 0o755)
                is_jadx = True

                # Cleanup
                os.remove(zip_path)
                print('\n' + Fore.GREEN + '[-] jadx installed successfully' + Fore.RESET)
            except Exception as e:
                print('\n' + Fore.RED + f'[!] Error installing jadx: {str(e)}' + Fore.RESET)
                exit(1)
        else:
            print('\n' + Fore.RED + '[!] jadx installation rejected. Cannot proceed without jadx. Exiting...' + Fore.RESET)
            exit(1)

def main():
    # Check if main directory exists
    tool_dir = os.path.expanduser('~/SemGrepTool')
    if not os.path.exists(tool_dir):
        os.makedirs(tool_dir)
        print('\n' + Fore.GREEN + '[-] Created working directory at ' + tool_dir + Fore.RESET)

    print("\n\n")
    banner()
    time.sleep(1)  # Wait for banner
    print("\n" + Fore.GREEN + "[-] Initializing the tool...")
    time.sleep(1)  # Wait for requirements-check
    check_requirements()
    time.sleep(1)
    if not is_jadx or not is_semgrep:
        print('\n' + Fore.RED + '[!] Required tools are not installed, installing them...')
        install_requirements()
    else:
        print('\n' + Fore.GREEN + '[-] All required tools are installed...')

    print('\n' + Fore.GREEN + '[-] Enter the path to the APK file: ' + Fore.RESET)
    apk_path = input().strip()
    
    if not os.path.exists(apk_path):
        print('\n' + Fore.RED + '[!] APK file not found!' + Fore.RESET)
        exit(1)
        
    # Create analysis directory
    apk_name = os.path.basename(apk_path).replace('.apk', '')
    analysis_dir = os.path.expanduser(f'~/SemGrepTool/{apk_name}_data')
    if not os.path.exists(analysis_dir):
        os.makedirs(analysis_dir)
        
    # Copy APK to analysis directory
    new_apk_path = os.path.join(analysis_dir, os.path.basename(apk_path))
    shutil.copy2(apk_path, new_apk_path)
    
    # Decompile APK
    decompiled_dir = os.path.join(analysis_dir, 'decompiledapk')
    print('\n' + Fore.GREEN + '[-] Decompiling APK...' + Fore.RESET)
    os.system(f'~/SemGrepTool/jadx/bin/jadx -d {decompiled_dir} {new_apk_path}')
    
    # Run semgrep
    print('\n' + Fore.GREEN + '[-] Running semgrep analysis...' + Fore.RESET)
    os.system(f'semgrep scan --config=auto {decompiled_dir}')

if __name__ == '__main__':
    main()
