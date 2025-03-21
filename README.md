# Thamyris - Discord Soundboard for Online Roleplaying

Thamyris is a feature-rich, customizable soundboard application designed for online roleplaying groups (e.g., D&D). The app connects to Discord and allows live playback of sound effects and ambient tracks during sessions.

## Features

- **Discord Integration**: Connects as a bot to Discord voice channels and plays audio clips directly into the voice chat.
- **Modern GUI**: Built with PyQt6 for a responsive and customizable interface.
- **Tabbed Soundboard Interface**: Organize sounds into tabs for different campaigns or settings.
- **Simultaneous Sound Playback**: Multiple sounds can play at once for rich layering of effects.
- **Channel-Based Audio Mixing**: 4 independent audio channels with individual volume control.
- **Ambient Background Playback**: Looping ambient tracks with quick-switch capability.
- **Profiles**: Save/load complete soundboard setups as named profiles.
- **Voice Ducking**: Automatically reduces ambient volume when other sounds are triggered.
- **Fade In/Out Controls**: Smooth transitions between sounds.
- **Hotkey & MIDI Integration**: Assign hotkeys to trigger specific sounds.
- **Drag & Drop Sound Assignment**: Easily assign new sound files to buttons.
- **Macro Buttons**: Create sequences of sounds with defined delays.
- **Sound Tagging System**: Tag sounds for easy organization and filtering.

## Installation

### Prerequisites

- Windows 10/11, macOS, or Linux
- Python 3.8 or higher (if running from source)
- Discord account with a registered bot

### Option 1: Using the Executable (Windows)

1. Download the latest release from the [Releases](https://github.com/yourusername/thamyris/releases) page
2. Extract the ZIP file to a location of your choice
3. Run `Thamyris.exe`

### Option 2: Running from Source

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/thamyris.git
   cd thamyris
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python src/main.py
   ```

## Discord Bot Setup

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application and set up a bot
3. Enable the "Server Members Intent" and "Message Content Intent" under the Bot settings
4. Copy your bot token
5. Create a `.env` file in the application directory with the following content:
   ```
   DISCORD_BOT_TOKEN=your_bot_token_here
   ```
6. Invite the bot to your server using the OAuth2 URL generator with the following permissions:
   - View Channels
   - Send Messages
   - Connect
   - Speak

## Usage

### First Launch

1. Start Thamyris
2. Go to Settings and configure your Discord bot connection
3. Create a new profile or load an existing one

### Adding Sounds

1. Click the "+" button on any tab to add a new sound
2. Select an audio file from your computer
3. Configure the sound properties (name, volume, channel, etc.)
4. Add tags to help organize your sounds

### Creating Tabs

1. Click the "+" button in the tab bar to create a new tab
2. Enter a name for the tab
3. Add sounds to the tab

### Playing Sounds

1. Click on a sound button to play it once
2. Right-click on a sound button for additional options:
   - Edit sound properties
   - Delete sound
   - Change playback mode (play once, repeat, loop)

### Using Profiles

1. Go to File > Save Profile to save your current setup
2. Go to File > Open Profile to load a different profile
3. Profiles are saved with the `.profile` extension in the `profiles` directory

### Using Hotkeys

1. Go to Tools > Hotkey Editor
2. Assign hotkeys to specific sounds
3. Use the hotkeys to trigger sounds even when the application is not in focus

### Creating Macros

1. Go to Tools > Macro Editor
2. Create a new macro and add sound steps with timing
3. Save the macro and assign a hotkey if desired

## Customization

### Themes

1. Go to Settings > Themes
2. Select a built-in theme or create your own
3. Themes are saved with the `.theme` extension in the `themes` directory

### Settings

1. Go to Settings > Preferences
2. Configure application settings:
   - Font size and family
   - Default volume levels
   - Voice ducking settings
   - Fade in/out durations

## File Structure

- `profiles/`: Saved soundboard profiles
- `sounds/`: Imported sound files
- `themes/`: Custom themes
- `macros/`: Saved macro sequences

## Troubleshooting

### Discord Connection Issues

- Ensure your bot token is correct in the `.env` file
- Check that your bot has the necessary permissions
- Verify that your Discord application is running

### Audio Playback Issues

- Check that your sound files are in a supported format (MP3, WAV, OGG, FLAC)
- Ensure your system's audio output is working correctly
- Try adjusting the volume levels in the application

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Named after Thamyris, the Greek bard who challenged the Muses
- Built with PyQt6, discord.py, and other open-source libraries
