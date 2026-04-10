# Music Manager Plugin for Indigo

Unified control over Spotify, Apple Music, and VLC with automatic mutual exclusion for Indigo Domotics.

## Overview

Music Manager provides a single Indigo device that can monitor and control supported music player plugins from one place. It keeps playback states in sync, tracks the currently active service, and can automatically pause one service when another starts playing.

This plugin is intended to simplify automation and control page design when you use more than one music source in Indigo.

## Features

- Unified control for Spotify, Apple Music, and VLC
- Automatic mutual exclusion between enabled services
- Active service tracking
- Combined now playing status
- Optional Indigo variable updates for automation
- Works with one, two, or all three supported player plugins
- Supports a preferred service when nothing is currently playing

## Requirements

- Indigo 2025.1 or later
- At least one supported player plugin installed and working:
  - Spotify Control Plugin
  - Apple Music Control Plugin
  - VLC Control Plugin

Music Manager is most useful when two or more services are configured, but it can still be used with a single service as a unified control layer.

## Installation

1. Download the latest release from the repository Releases page.
2. Double-click `MusicManager.indigoPlugin` to install.
3. Restart the Indigo Server if prompted.
4. In Indigo, create a new device:
   - Devices -> New
   - Type: Plugin
   - Plugin: Music Manager
   - Model: Music Manager

## Configuration

In the device configuration dialog, assign any combination of the following:

- Spotify device
- Apple Music device
- VLC device

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
- `trackName`
- `artist`
- `album`
- `playStatus`

Exact state availability depends on which services are configured and what data the underlying player plugins provide.

## Actions

Music Manager provides unified actions such as:

- Play / Pause
- Play
- Pause
- Stop
- Next Track
- Previous Track
- Volume Up
- Volume Down
- Set Volume
- Switch to Spotify
- Switch to Apple Music
- Switch to VLC
- Refresh Status

Actions are routed to the currently active service, or to the preferred service when nothing is playing.

## Notes

- At least one player plugin must be configured.
- Automatic mutual exclusion depends on the configured player devices being available and responding normally.
- Service-specific metadata depends on what the underlying player plugin reports.
- This plugin is designed for Indigo users who want one clean music control layer across multiple services.

## Version History

### 1.2.4
- Fixed action execution errors when one service starts while another is playing
- Corrected command routing for supported player plugins
- Improved mutual exclusion behavior
- Cleared stale unified status values when no service is active

## Support

Issues and suggestions can be submitted through the GitHub Issues page for this repository.

## License

MIT License
