"""
Setup script for Thamyris application using PyInstaller
"""
import os
import sys
import shutil
from PyInstaller.__main__ import run

# Define application name
APP_NAME = "Thamyris"
VERSION = "1.0.0"

# Define paths
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.join(ROOT_DIR, "src")
RESOURCES_DIR = os.path.join(ROOT_DIR, "resources")
DIST_DIR = os.path.join(ROOT_DIR, "dist")
BUILD_DIR = os.path.join(ROOT_DIR, "build")
SPEC_FILE = os.path.join(ROOT_DIR, f"{APP_NAME.lower()}.spec")

# Create resources directory if it doesn't exist
os.makedirs(RESOURCES_DIR, exist_ok=True)

# Create subdirectories for resources
os.makedirs(os.path.join(RESOURCES_DIR, "sounds"), exist_ok=True)
os.makedirs(os.path.join(RESOURCES_DIR, "profiles"), exist_ok=True)
os.makedirs(os.path.join(RESOURCES_DIR, "themes"), exist_ok=True)
os.makedirs(os.path.join(RESOURCES_DIR, "macros"), exist_ok=True)

# Clean previous build
if os.path.exists(DIST_DIR):
    shutil.rmtree(DIST_DIR)
if os.path.exists(BUILD_DIR):
    shutil.rmtree(BUILD_DIR)
if os.path.exists(SPEC_FILE):
    os.remove(SPEC_FILE)

# Define PyInstaller arguments
pyinstaller_args = [
    '--name=%s' % APP_NAME,
    '--onedir',
    '--windowed',
    '--add-data=%s;%s' % (os.path.join(RESOURCES_DIR, '*'), 'resources'),
    '--icon=%s' % os.path.join(ROOT_DIR, 'resources', 'icon.ico'),
    '--noconfirm',
    '--clean',
    os.path.join(SRC_DIR, 'main.py')
]

# Run PyInstaller
run(pyinstaller_args)

# Copy additional files to the distribution directory
shutil.copy(os.path.join(ROOT_DIR, 'README.md'), os.path.join(DIST_DIR, APP_NAME))
shutil.copy(os.path.join(ROOT_DIR, 'LICENSE'), os.path.join(DIST_DIR, APP_NAME))

# Create empty resource directories in the distribution
os.makedirs(os.path.join(DIST_DIR, APP_NAME, 'resources', 'sounds'), exist_ok=True)
os.makedirs(os.path.join(DIST_DIR, APP_NAME, 'resources', 'profiles'), exist_ok=True)
os.makedirs(os.path.join(DIST_DIR, APP_NAME, 'resources', 'themes'), exist_ok=True)
os.makedirs(os.path.join(DIST_DIR, APP_NAME, 'resources', 'macros'), exist_ok=True)

print(f"Build completed! {APP_NAME} v{VERSION} has been packaged successfully.")
print(f"The application can be found in: {os.path.join(DIST_DIR, APP_NAME)}")
