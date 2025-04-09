#!/usr/bin/env python3

import os
import argparse
import shutil
import subprocess
import datetime

try:
    CURRENT_DIR = os.getcwd()
except:
    print("\n[ERROR-CODE-01] Unable to get current working directory.")
    exit(1)

RULE_DIR = os.path.join(CURRENT_DIR, "rules")
OUTPUT_DIR = os.path.join(CURRENT_DIR, "output")
INPUT_DIR = os.path.join(CURRENT_DIR, "input")

# Function to print the banner
def banner():
    print(r"""
        ____ ___  _  _ ____ ____ ____ _  _ 
        |__| |__] |_/  [__  |    |__| |\ | 
        |  | |    | \_ ___] |___ |  | | \| 

                                        -- by @h1dden --
    """)

def panic():
    print(r"""
      ______     ______  _______     _____  _______   _________            _______     _       ____  _____  _____   ______  
    .' ____ \  .' ___  ||_   __ \   |_   _||_   __ \ |  _   _  |          |_   __ \   / \     |_   \|_   _||_   _|.' ___  | 
    | (___ \_|/ .'   \_|  | |__) |    | |    | |__) ||_/ | | \_|  ______    | |__) | / _ \      |   \ | |    | | / .'   \_| 
     _.____`. | |         |  __ /     | |    |  ___/     | |     |______|   |  ___/ / ___ \     | |\ \| |    | | | |        
    | \____) |\ `.___.'\ _| |  \ \_  _| |_  _| |_       _| |_              _| |_  _/ /   \ \_  _| |_\   |_  _| |_\ `.___.'\ 
     \______.' `.____ .'|____| |___||_____||_____|     |_____|            |_____||____| |____||_____|\____||_____|`.____ .' 
                                                                                                                        """)

def check_tool(tool_name, version_arg="--version"):
    try:
        result = subprocess.run(
            [tool_name, version_arg],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        output = result.stdout.decode().strip() or result.stderr.decode().strip()
        return "Working"
    except FileNotFoundError as e:
        return e
    except subprocess.CalledProcessError as e:
        return e


def check():
    # First check the os , if its windows , quit the session
    if os.name == 'nt':
        print("\n[ERROR-CODE-O2] Windows OS detected.")
        exit(1)
    
    # Given that this insnt windows anymore , it might be linux so lets check if its kali
    try:
        with open("/etc/os-release") as f:
            os_info = f.read().lower()
            if "kali" in os_info:
                print("\n[INFO] Kali Linux detected.")
            else:
                print("\n[ERROR-CODE-O3] This script is made kali-specific only")
                print("[BYPASS] Install semgrep and jadx manually and add to path, and use --skip-check to bypass this check")
                exit(1)
    except FileNotFoundError:
        print("\n[WARNING-CODE-01] /etc/os-release file not found. Unable to determine OS. Still continuing....")


    # Checking if all the directories exist
    if not os.path.exists(RULE_DIR):
        print(f"\n[ERRO-CODE-04] Rules directory does not exist: {RULE_DIR}")
        exit(1)
    
    if not os.path.exists(OUTPUT_DIR):
        print(f"\n[ERROR-CODE-05] Output directory does not exist: {OUTPUT_DIR}")
        exit(1)
    
    if not os.path.exists(INPUT_DIR):
        print(f"\n[ERROR-CODE-06] Input directory does not exist: {INPUT_DIR}")
        exit(1)


    # Checking if the required tools are installed
    jadx_path = shutil.which("jadx")
    if not jadx_path:
        print("\n[WARNING-CODE-02] JADX is not installed or not in PATH.")

        print("\n[INFO] Installing JADX...")
        try:
            subprocess.run(["sudo","apt", "install", "jadx"], check=True)
            print("\n[INFO] JADX installed successfully.")
            print("[INFO] Now checking if JADX is working...")
            out_jadx = check_tool("jadx")
            if out_jadx == "Working":
                print("\n[INFO] JADX is working fine.")
            else:
                print("\n[ERROR-CODE-07] JADX is not working properly.")
                print(f"Reason: {out_jadx}")
        except subprocess.CalledProcessError as e:
            print(f"\n[ERROR-CODE-07] Failed to install JADX: {e}")
            exit(1)
    else:
        print("\n[INFO] JADX is already installed.")


    semgrep_path = shutil.which("semgrep")
    if not semgrep_path:
        print("\n[WARNING-CODE-O3] Semgrep is not installed or not in PATH. Nothing to worry about.")

        print("\n[INFO] Installing semgrep...")
        try:
            subprocess.run(["pip","install", "semgrep", "--break-system-packages"], check=True)
            print("\n[INFO] Semgrep installed successfully.")
            print("[INFO] Now checking if semgrep is working...")
            out_semgrep = check_tool("semgrep")
            if out_semgrep == "Working":
                print("\n[INFO] Semgrep is working fine.")
            else:
                print("\n[ERROR-CODE-07] Semgrep is not working properly.")
                print(f"Reason: {out_semgrep}")

        except subprocess.CalledProcessError as e:
            print(f"\n[ERROR-CODE-08] Failed to install semgrep: {e}")
            exit(1)
    else:
        print("\n[INFO] Semgrep is already installed.")


def scan(apk_path):
    # First lets check if the path exists:
    if not os.path.exists(apk_path):
        print(f"\n[ERROR-CODE-09] APK file does not exist: {apk_path}")
        exit(1)
    
    # Now since we have the apk , first lets try to decode it with 
    
    # First copy the apk into the input directory
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    input_path = os.path.join(INPUT_DIR, timestamp)
    output_path = os.path.join(OUTPUT_DIR, timestamp)
    
    try:
        os.makedirs(input_path, exist_ok=True)
        os.makedirs(output_path, exist_ok=True)
        print(f"\n[INFO] Created input and output directories: {input_path}, {output_path}")
    except Exception as e:
        print(f"\n[WARNING-CODE-04] Script Panic , Failed to create directories : {e}")

    try:
        shutil.copy(apk_path, input_path)
        print(f"\n[INFO] APK file copied to input directory: {input_path}")
    except Exception as e:
        print(f"\n[WARNING-CODE-05] Script Panic , Failed to copy apk : {e}")
    
    # Now lets decode the apk using jadx
    try:
        print(f"\n[INFO] Decompiling APK using JADX...(Might take some time)")
        result = subprocess.run(
            [
                "sudo",
                "jadx",
                "-d", output_path,
                apk_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
    except subprocess.CalledProcessError as e:
        panic()
        print(f"\n[ERROR-CODE-10] Failed to decompile APK: {e}")
        print("Reason: This could be due to issues with JADX or the APK itself.")
        exit(1)
    
    # Now lets run semgrep on the output directory
    # First using custom rules folder and store custom.json in output directory and 

    # then using the default rules and store default.json in output directory
    # First: Using custom rules and storing custom.json
    try:
        print(f"\n[INFO] Running Semgrep with custom rules...(Might take some time)")
        result = subprocess.run(
            [
                "semgrep",
                "--config", RULE_DIR,
                "--json",
                "-o", os.path.join(output_path, "custom.json"),
                output_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
    except subprocess.CalledProcessError as e:
        panic()
        print(f"\n[ERROR-CODE-11] Failed to run Semgrep with custom rules: {e}")
        print("Reason: This could be due to issues with Semgrep or the output directory.")
        print("stderr:", e.stderr.decode())
        exit(1)

    # Then: Using default (auto) rules and storing default.json
    try:
        print(f"\n[INFO] Running Semgrep with default rules...(Might take some time)")
        result = subprocess.run(
            [
                "semgrep",
                "--config", "auto",
                "--json",
                "-o", os.path.join(output_path, "default.json"),
                output_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
    except subprocess.CalledProcessError as e:
        panic()
        print(f"\n[ERROR-CODE-12] Failed to run Semgrep with default rules: {e}")
        print("Reason: This could be due to issues with Semgrep or the output directory.")
        print("stderr:", e.stderr.decode())
        exit(1)

    print(f"\n[INFO] Semgrep scan completed. Results saved to {output_path}")
    print(f"\n[INFO] Custom rules output: {os.path.join(output_path, 'custom.json')}")
    print(f"\n[INFO] Default rules output: {os.path.join(output_path, 'default.json')}")
    print(f"\n[INFO] Decompiled APK output: {output_path}")
    



def main():
    banner()

    parser = argparse.ArgumentParser(description="APK Scanner")
    parser.add_argument('-a', '--apk', help='Path to APK file', required=True)
    parser.add_argument('--skip-check', action='store_true', help='Skip tool check')
    args = parser.parse_args()

    if args.skip_check:
        print("\n[INFO] Skipping tool check...")
    else:
        check()

    apk_path = args.apk
    scan(apk_path)

main()
