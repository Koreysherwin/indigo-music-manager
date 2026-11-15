# Music Manager Plugin for Indigo

Unified control over Spotify, Apple Music, VLC, and Airfoil Satellite with automatic mutual exclusion for Indigo Domotics.

Download the [latest published release](https://github.com/Koreysherwin/indigo-music-manager/releases/latest).

## Overview

Music Manager provides a single Indigo device that can monitor and control supported music player plugins from one place. It keeps playback states in sync, tracks the currently active service, and can automatically pause one service when another starts playing.

This plugin is intended to simplify automation and control page design when you use more than one music source in Indigo.

## Features

- Unified control for Spotify, Apple Music, VLC, and Airfoil Satellite
- Automatic mutual exclusion between enabled services
- Active service tracking
- Combined now playing status
- Optional Indigo variable updates for automation
- Works with one or more of the four supported player plugins
- Supports a preferred service when nothing is currently playing

## Requirements

- Indigo 2025.1 or later
- At least one supported player plugin installed and working:
  - Spotify Control Plugin
  - Apple Music Control Plugin
  - VLC Control Plugin
  - Airfoil Satellite Plugin

Music Manager is most useful when two or more services are configured, but it can still be used with a single service as a unified control layer.

## Installation

1. Download `MusicManager.indigoPlugin.zip` from the [latest release](https://github.com/Koreysherwin/indigo-music-manager/releases/latest) and extract it.
2. Double-click `MusicManager.indigoPlugin` to install.
3. Restart the Indigo Server if prompted.
4. In Indigo, create a new device:
   - Devices -> New
   - Type: Plugin
   - Plugin: Music Manager
   - Model: Music Manager

## Upgrading to 1.2.8

The plugin identifier has changed to `com.sherwinsound.musicmanager`. Back up your Indigo database before upgrading. The developer successfully installed 1.2.8 over the previous version and confirmed normal operation. Other installations may require existing devices, actions or scripts referencing the old identifier to be reassigned. Check automations after upgrading.

## Configuration

In the device configuration dialog, assign any combination of the following:

- Spotify device
- Apple Music device
- VLC device
- Airfoil Satellite device

Additional options:

- Auto-Exclusive Playback  
  When enabled, Music Manager pauses other configured services when a new one starts playing.

- Preferred Service  
  Determines which service receives commands when nothing is currently playing.

- Update Indigo Variables  
  Optionally creates or updates Indigo variables with current playback information.

- Variable Prefix  
  Prefix used for any variables created by the plugin.

## How It Works

Music Manager watches the configured player devices and maintains a unified state. When playback starts on one service, it can automatically pause the others to prevent overlapping audio and conflicting automation states.

The plugin exposes device states you can use in control pages, triggers, and scripts to reflect the active service and current playback details.

## Common Use Cases

- One control page for multiple music services
- Automatic pause of Spotify when Apple Music starts
- Lighting or room automation based on which service is active
- Shared variables for track, artist, album, and playback state
- Simpler scripting when multiple player plugins are installed

## Device States

Typical states include:

- `activeService`
- `isPlaying`
- `spotifyPlaying`
- `appleMusicPlaying`
- `vlcPlaying`
- `airfoilPlaying`
- `trackName`
- `artist`
- `album`
- `status`
- `isPaused`
- `isStopped`
- `playerPosition` and `playerPositionFormatted`
- `duration` and `durationFormatted`
- `progressPercent`
- `soundVolume`

Exact state availability depends on which services are configured and what data the underlying player plugins provide.

## Actions

Music Manager provides unified actions such as:

- Play / Pause
- Play
- Pause
- Stop All
- Next Track
- Previous Track
- Volume Up
- Volume Down
- Set Volume
- Switch to Spotify
- Switch to Apple Music
- Switch to VLC
- Switch to Airfoil Satellite
- Mute / Unmute
- Set Shuffle / Set Repeat
- Skip Forward / Skip Backward
- Update Now

Playback actions generally target the active or preferred service. Stop All and service switching can affect multiple configured players. Available controls depend on the underlying player plugin; Airfoil Satellite monitoring does not guarantee remote transport control of the sending application.

For Indigo scripts, use the owning plugin's action API rather than `indigo.device.execute()`. For example, with `managerDeviceId` set to your Music Manager device ID:

```python
manager = indigo.server.getPlugin(indigo.devices[managerDeviceId].pluginId)
manager.executeAction("pause", deviceId=managerDeviceId)
```

## Notes

- At least one player plugin must be configured.
- Automatic mutual exclusion depends on the configured player devices being available and responding normally.
- Service-specific metadata depends on what the underlying player plugin reports.
- This plugin is designed for Indigo users who want one clean music control layer across multiple services.

## Version History

### 1.2.8
- Changed the plugin identifier to `com.sherwinsound.musicmanager`.
- Corrected bundle format metadata and GitHub Issues support URL.
- No playback logic changes.
- Developer-tested in-place upgrade from the preceding version.

### 1.2.7
- Improved Apple Music device picker compatibility.
- Includes Airfoil Satellite support and safe state updates for existing devices.

### 1.2.6
- Safely filters state updates when newly introduced Airfoil states have not yet registered on an upgraded device.

### 1.2.5
- Added Airfoil Satellite monitoring, preferred service selection, switching action, and unified metadata and mutual exclusion integration.

### 1.2.4
- Fixed action execution errors when one service starts while another is playing
- Corrected command routing for supported player plugins
- Improved mutual exclusion behavior
- Cleared stale unified status values when no service is active

## Support

Issues and suggestions can be submitted through [GitHub Issues](https://github.com/Koreysherwin/indigo-music-manager/issues). Include your Indigo version, Music Manager version, configured player plugins, and relevant log messages. See the [changelog](CHANGELOG.md) for release history.

## License

MIT License
