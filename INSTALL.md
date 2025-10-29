# Installation Guide

This guide will walk you through installing and configuring the Music Manager plugin for Indigo.

## Prerequisites

Before installing Music Manager, ensure you have:

1. **Indigo 2025.1 or later** installed and running
2. **At least one music control plugin** installed:
   - Spotify Control Plugin
   - Apple Music Control Plugin  
   - VLC Control Plugin
3. At least one device created for each music plugin you want to use

## Step 1: Install Required Music Plugins

If you haven't already, install at least one of these plugins from the Indigo Plugin Store:

### Spotify Control Plugin
1. Go to **Plugins** → **Manage Plugins...**
2. Search for "Spotify Control"
3. Click **Install** and follow the prompts
4. Create a Spotify device and configure it

### Apple Music Control Plugin
1. Go to **Plugins** → **Manage Plugins...**
2. Search for "Apple Music Control"
3. Click **Install** and follow the prompts
4. Create an Apple Music device and configure it

### VLC Control Plugin
1. Go to **Plugins** → **Manage Plugins...**
2. Search for "VLC Control"
3. Click **Install** and follow the prompts
4. Create a VLC device and configure it

## Step 2: Download Music Manager

### Option A: Download Release (Recommended)

1. Visit the [Releases page](https://github.com/yourusername/indigo-music-manager/releases)
2. Download the latest `MusicManager-vX.X.X.indigoPlugin.zip`
3. Unzip the file (double-click on macOS)
4. Continue to Step 3

### Option B: Clone from GitHub

```bash
git clone https://github.com/yourusername/indigo-music-manager.git
cd indigo-music-manager
```

## Step 3: Install the Plugin

1. **Double-click** the `MusicManager.indigoPlugin` file
2. Indigo will open and prompt you to install the plugin
3. Click **Install Plugin**
4. If prompted, **restart the Indigo server**

## Step 4: Create a Music Manager Device

1. In Indigo, go to **Devices** → **New...**
2. In the "Type" dropdown, select **Plugin**
3. In the "Plugin" dropdown, select **Music Manager**
4. In the "Model" dropdown, select **Music Manager**
5. Give your device a name (e.g., "Music Manager")
6. Click **Add**

## Step 5: Configure the Device

The configuration dialog will appear. Configure as follows:

### Music Service Devices

For each music service you want to manage:

- **Spotify Device**: Select your Spotify Player device
- **Apple Music Device**: Select your Apple Music Player device
- **VLC Device**: Select your VLC Player device

Select "-- None --" for any service you don't want to use.

> **Tip**: You can use any combination of one, two, or all three services!

### Behavior Settings

- **Auto-Exclusive Playback**: ✅ (Recommended)
  - When enabled, starting one service automatically pauses the others
  
- **Preferred Service**: Choose from:
  - **Use last active service** (Default) - Routes commands to whichever service played last
  - **Always prefer Spotify** - Defaults to Spotify when nothing is playing
  - **Always prefer Apple Music** - Defaults to Apple Music when nothing is playing
  - **Always prefer VLC** - Defaults to VLC when nothing is playing

### Variable Integration (Optional)

- **Update Indigo Variables**: ☐ (Leave unchecked unless you need it)
  - When enabled, creates/updates Indigo variables with music data
  - Useful for advanced automation scenarios

- **Variable Prefix**: `Music` (if variables enabled)
  - Variables will be named like `MusicTrackName`, `MusicArtist`, etc.

### Save Configuration

Click **Save** to apply your settings.

## Step 6: Verify Installation

1. Open the **Devices** window in Indigo
2. Find your Music Manager device
3. Look at its status - you should see service icons (🎵 🍎 🎬)
4. Try playing music on one of your services
5. The Music Manager status should update to show what's playing

## Step 7: Test Basic Functionality

### Test Play/Pause
1. Start playing music on Spotify (or your configured service)
2. In Indigo, execute the action: **Music Manager** → **Pause**
3. Music should pause
4. Execute: **Music Manager** → **Play**
5. Music should resume

### Test Auto-Exclusive (if enabled)
1. Play music on Spotify
2. Start playing music on Apple Music
3. Spotify should automatically pause
4. Only Apple Music should be playing

### Test Service Switching
1. With Apple Music playing, execute: **Music Manager** → **Switch to Spotify**
2. Apple Music should pause
3. Spotify is now the active service

## Troubleshooting Installation

### Plugin Won't Install
- Make sure you're running Indigo 2025.1 or later
- Try restarting Indigo
- Check file permissions on the downloaded plugin

### No Devices in Dropdowns
- Verify music control plugins are installed and enabled
- Check that devices have been created for each music plugin
- Try clicking the refresh icon next to the dropdown

### Auto-Exclusive Not Working
- Verify "Auto-Exclusive Playback" is checked in device settings
- Make sure both music plugins are running and responding
- Check Indigo Event Log for errors

### Status Not Updating
- Verify the underlying music devices are updating properly
- Check that the music apps are running on your Mac
- Try the "Update Now" action to force a refresh

## Next Steps

Now that Music Manager is installed:

1. **Create Triggers** - Set up triggers for when music starts/stops
2. **Add to Control Pages** - Add Music Manager to your control pages
3. **Create Scenes** - Include music control in your automation scenes
4. **Write Scripts** - Use Python to create advanced music automations

See the [README.md](README.md) for usage examples and advanced features.

## Getting Help

If you encounter issues:

1. Enable debug logging:
   - **Plugins** → **Music Manager** → **Configure...**
   - Check "Show debug information in log"
   
2. Check the Indigo Event Log for errors

3. Search [existing issues](https://github.com/yourusername/indigo-music-manager/issues)

4. Create a [new issue](https://github.com/yourusername/indigo-music-manager/issues/new) with:
   - Your Indigo version
   - Plugin version
   - Steps to reproduce the problem
   - Relevant log output

## Uninstallation

To uninstall Music Manager:

1. Delete the Music Manager device(s)
2. Go to **Plugins** → **Manage Plugins...**
3. Find "Music Manager" and click **Uninstall**
4. Restart Indigo if prompted

Your music control plugins will continue to work independently.
