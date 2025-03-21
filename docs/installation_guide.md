"""
Installation guide for Thamyris - Discord Soundboard for Online Roleplaying
"""

# Thamyris Installation Guide

This guide will walk you through the process of installing and setting up Thamyris on your system.

## System Requirements

- **Operating System**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 20.04+ recommended)
- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: 500MB for the application plus space for your sound files
- **Internet Connection**: Required for Discord integration
- **Sound Card**: Any compatible sound card or audio interface

## Installation Methods

### Method 1: Using the Pre-built Executable (Windows)

1. Download the latest release from the [Releases](https://github.com/yourusername/thamyris/releases) page
2. Extract the ZIP file to a location of your choice
3. Run `Thamyris.exe` to start the application

### Method 2: Using the Pre-built Package (macOS)

1. Download the latest release from the [Releases](https://github.com/yourusername/thamyris/releases) page
2. Mount the DMG file
3. Drag the Thamyris application to your Applications folder
4. Open the application from your Applications folder

### Method 3: Installing from Source (All Platforms)

#### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional, for cloning the repository)

#### Steps

1. **Get the Source Code**

   Either download the source code from the [Releases](https://github.com/yourusername/thamyris/releases) page or clone the repository:

   ```bash
   git clone https://github.com/yourusername/thamyris.git
   cd thamyris
   ```

2. **Create a Virtual Environment (Recommended)**

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**

   ```bash
   # Windows
   python src/main.py

   # macOS/Linux
   python3 src/main.py
   ```

## Discord Bot Setup

Thamyris requires a Discord bot to function properly. Follow these steps to create and set up your bot:

1. **Create a Discord Application**
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications)
   - Click "New Application" and give it a name (e.g., "Thamyris Soundboard")
   - Click "Create"

2. **Set Up a Bot**
   - In your application, go to the "Bot" tab
   - Click "Add Bot"
   - Confirm by clicking "Yes, do it!"

3. **Configure Bot Permissions**
   - Under the "Privileged Gateway Intents" section, enable:
     - Server Members Intent
     - Message Content Intent
   - Click "Save Changes"

4. **Get Your Bot Token**
   - In the "Bot" tab, under the "TOKEN" section, click "Copy"
   - Keep this token secure and don't share it with others

5. **Invite the Bot to Your Server**
   - Go to the "OAuth2" tab, then "URL Generator"
   - Under "Scopes", select "bot"
   - Under "Bot Permissions", select:
     - View Channels
     - Send Messages
     - Connect
     - Speak
   - Copy the generated URL and open it in your browser
   - Select your server and click "Authorize"

6. **Configure Thamyris to Use Your Bot**
   - Start Thamyris
   - Go to Settings > Discord Settings
   - Paste your bot token in the "Bot Token" field
   - Click "Save"

## Troubleshooting Installation Issues

### Windows Issues

- **Missing DLL Error**: Install the latest [Visual C++ Redistributable](https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads)
- **Application Won't Start**: Make sure you have extracted all files from the ZIP archive

### macOS Issues

- **"App is from an unidentified developer"**: Right-click the app and select "Open" instead of double-clicking
- **Permission Issues**: Go to System Preferences > Security & Privacy and allow the application

### Linux Issues

- **Missing Libraries**: Install required libraries with your package manager:
  ```bash
  # Ubuntu/Debian
  sudo apt-get install libpulse0 libasound2 ffmpeg
  
  # Fedora
  sudo dnf install pulseaudio-libs alsa-lib ffmpeg
  ```

- **Audio Issues**: Make sure PulseAudio is installed and running:
  ```bash
  pulseaudio --start
  ```

### Discord Integration Issues

- **Bot Won't Connect**: Double-check your bot token and make sure it's entered correctly
- **Bot Can't Join Voice Channel**: Make sure the bot has the necessary permissions in your Discord server
- **No Audio in Discord**: Check that your bot has permission to speak in the voice channel

## Updating Thamyris

### Updating the Executable Version

1. Download the latest release
2. Extract it to a new location
3. Copy your profiles, sounds, and settings from the old installation to the new one

### Updating the Source Version

1. Pull the latest changes:
   ```bash
   git pull origin main
   ```
2. Update dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Next Steps

After installation, refer to the [User Guide](user_guide.md) for instructions on how to use Thamyris effectively for your roleplaying sessions.

If you encounter any issues not covered in this guide, please check the [GitHub Issues](https://github.com/yourusername/thamyris/issues) page or create a new issue.
