import subprocess
import sys

def install_package(package_name):
    try:
        # Run the pip install command
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", package_name])
        print(f"Successfully uninstalled {package_name}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to uninstall {package_name}. Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    packages = ["z3-solver", "numpy"]
    
    for package in packages:
        install_package(package)


if __name__ == "__main__":
    main()
