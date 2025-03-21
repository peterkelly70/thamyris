"""
User guide for Thamyris - Discord Soundboard for Online Roleplaying
"""

# Thamyris User Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Main Interface](#main-interface)
4. [Managing Sounds](#managing-sounds)
5. [Using Tabs](#using-tabs)
6. [Channel Mixer](#channel-mixer)
7. [Ambient Player](#ambient-player)
8. [Profiles](#profiles)
9. [Hotkeys](#hotkeys)
10. [Macros](#macros)
11. [Settings](#settings)
12. [Discord Integration](#discord-integration)
13. [Tips and Tricks](#tips-and-tricks)

## Introduction

Thamyris is a feature-rich soundboard application designed specifically for online roleplaying groups. Named after the Greek bard who challenged the Muses, Thamyris allows game masters to enhance their storytelling with sound effects and ambient tracks played directly into Discord voice channels.

This guide will walk you through all the features of Thamyris and help you get the most out of the application during your roleplaying sessions.

## Getting Started

### First Launch

When you first launch Thamyris, you'll need to set up your Discord bot connection:

1. Click on **Settings** in the menu bar, then select **Discord Settings**
2. Enter your Discord bot token
3. Click **Save**

If you don't have a Discord bot token yet, see the [Discord Integration](#discord-integration) section for instructions on creating one.

### Creating Your First Profile

1. Click on **File** in the menu bar, then select **New Profile**
2. Enter a name for your profile (e.g., "Fantasy Campaign")
3. Click **Create**

You'll now have a blank profile with one empty tab. Let's add some sounds!

## Main Interface

The Thamyris interface consists of several key areas:

- **Menu Bar**: Access to File, Edit, Tools, and Help menus
- **Tab Bar**: Switch between different tabs of sounds
- **Sound Grid**: Contains sound buttons for the current tab
- **Channel Mixer**: Control volume for different audio channels
- **Ambient Player**: Manage background ambient tracks
- **Status Bar**: Shows connection status and current profile

## Managing Sounds

### Adding Sounds

1. Click the **+** button in the sound grid or right-click in an empty area and select **Add Sound**
2. Browse to select an audio file
3. Configure the sound properties:
   - **Name**: A descriptive name for the sound
   - **Channel**: Which audio channel to play the sound on
   - **Volume**: The volume level for this specific sound
   - **Playback Mode**: Choose between Play Once, Play N Times, or Loop
   - **Tags**: Add tags to help organize and find your sounds
   - **Color**: Choose a color for the sound button
   - **Fade In/Out**: Enable smooth transitions at the start/end of the sound

4. Click **Save** to add the sound to your tab

### Editing Sounds

1. Right-click on a sound button and select **Edit**
2. Modify any properties as needed
3. Click **Save** to apply your changes

### Playing Sounds

- **Left-click** on a sound button to play it once
- **Right-click** on a sound button to access additional options:
  - **Play**: Play the sound
  - **Stop**: Stop the sound if it's currently playing
  - **Edit**: Open the sound editor
  - **Delete**: Remove the sound from the tab

### Tagging Sounds

Tags help you organize and find your sounds quickly:

1. When adding or editing a sound, enter tags in the **Tags** field, separated by commas
   (e.g., "dragon,roar,loud")
2. Use the search bar at the top of the sound grid to filter sounds by tag

## Using Tabs

Tabs help you organize sounds by category, scene, or any other grouping that makes sense for your campaign.

### Creating Tabs

1. Click the **+** button in the tab bar
2. Enter a name for the tab (e.g., "Combat", "Tavern", "Forest")
3. Click **Create**

### Managing Tabs

- **Click** on a tab to switch to it
- **Right-click** on a tab to access additional options:
  - **Rename**: Change the tab name
  - **Delete**: Remove the tab and all its sounds
  - **Move Left/Right**: Reorder tabs

## Channel Mixer

The Channel Mixer allows you to control the volume of different audio channels independently:

- **Ambient**: Background ambient tracks
- **Effects 1-3**: Sound effects channels

Each channel has its own volume slider. This allows you to create a mix that works for your session, such as lowering ambient sounds while keeping effects loud.

## Ambient Player

The Ambient Player is designed for background tracks that play continuously:

1. Click the **Select Ambient** dropdown to choose from your ambient tracks
2. Use the **Play/Pause** button to control playback
3. Adjust the **Volume** slider to set the ambient level
4. Enable **Auto-duck** to automatically lower ambient volume when effects play

## Profiles

Profiles allow you to save and load different soundboard setups for different campaigns or sessions.

### Saving Profiles

1. Click **File** > **Save Profile** or **Save Profile As**
2. Enter a name for the profile
3. Click **Save**

Profiles are saved with the `.profile` extension in the profiles directory.

### Loading Profiles

1. Click **File** > **Open Profile**
2. Select a profile from the list
3. Click **Load**

## Hotkeys

Hotkeys allow you to trigger sounds with keyboard shortcuts, even when Thamyris isn't in focus.

### Setting Up Hotkeys

1. Click **Tools** > **Hotkey Editor**
2. Click **Add Hotkey**
3. Enter an action name (usually the sound name)
4. Click **Record Hotkey** and press the key combination you want to use
5. Click **Add**

### Using Hotkeys

Once configured, simply press the assigned key combination to trigger the sound, even when playing other applications.

## Macros

Macros allow you to create sequences of sounds with specific timing.

### Creating Macros

1. Click **Tools** > **Macro Editor**
2. Click **New Macro**
3. Enter a name for the macro
4. Add steps to the macro:
   - Select a sound from the dropdown
   - Set the delay before playing (in seconds)
   - Click **Add Step**
5. Arrange steps using the up/down arrows
6. Click **Save**

### Playing Macros

1. Click **Tools** > **Macros**
2. Select a macro from the list
3. Click **Play**

You can also assign hotkeys to macros for quick access.

## Settings

### Application Settings

Access these by clicking **Settings** > **Preferences**:

- **Appearance**: Change theme, font size, and font family
- **Audio**: Set default volume levels and fade durations
- **Voice Ducking**: Configure how ambient tracks reduce in volume when effects play
- **Startup**: Choose which profile to load at startup

### Discord Settings

Access these by clicking **Settings** > **Discord Settings**:

- **Bot Token**: Your Discord bot authentication token
- **Command Prefix**: The prefix for bot commands (default: !)
- **Auto-Join**: Whether to automatically join the voice channel

## Discord Integration

Thamyris integrates with Discord to play sounds directly into voice channels.

### Setting Up a Discord Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **New Application** and give it a name
3. Go to the **Bot** tab and click **Add Bot**
4. Under the Token section, click **Copy** to copy your bot token
5. Enable the **Server Members Intent** and **Message Content Intent**
6. Go to the **OAuth2** tab, then **URL Generator**
7. Select the **bot** scope and the following permissions:
   - View Channels
   - Send Messages
   - Connect
   - Speak
8. Copy the generated URL and open it in your browser to invite the bot to your server

### Connecting to Discord

1. In Thamyris, go to **Settings** > **Discord Settings**
2. Paste your bot token
3. Click **Save**
4. Click **Connect** to connect to Discord

### Discord Commands

When the bot is in your server, you can use these commands:

- `!join`: Makes the bot join your current voice channel
- `!leave`: Makes the bot leave the voice channel
- `!stop`: Stops all currently playing sounds

## Tips and Tricks

- **Organize by Scene**: Create tabs for different locations or scenes in your campaign
- **Color Coding**: Use different colors for different types of sounds (e.g., red for combat, blue for ambient)
- **Layering**: Play multiple sounds simultaneously to create rich audio environments
- **Quick Access**: Assign hotkeys to your most frequently used sounds
- **Preparation**: Create macros for complex scenes ahead of time
- **Tagging System**: Use consistent tags to make finding sounds easier
- **Volume Balance**: Use the channel mixer to find the perfect balance between ambient tracks and effects
- **Fade Effects**: Use fade in/out for smoother transitions, especially for ambient tracks

---

We hope this guide helps you get the most out of Thamyris! If you have any questions or feedback, please visit our GitHub repository or contact support.
