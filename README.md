# Music Manager Plugin for Indigo

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Indigo Version](https://img.shields.io/badge/Indigo-2025.1+-blue.svg)](https://www.indigodomo.com/)
[![Version](https://img.shields.io/badge/version-1.2.3-green.svg)](https://github.com/yourusername/indigo-music-manager/releases)

A unified control plugin for [Indigo Domotics](https://www.indigodomo.com/) that manages Spotify, Apple Music, and VLC with seamless switching and automatic mutual exclusion.

## Features

- **🎵 Unified Control** - One device to control all your music services
- **🔄 Auto-Exclusive Playback** - Automatically pauses other services when one starts playing
- **🎯 Smart Service Switching** - Seamlessly switch between Spotify, Apple Music, and VLC
- **📊 Combined Status Display** - See what's playing from any service at a glance
- **🔌 Flexible Configuration** - Use any combination of one, two, or all three services
- **📝 Variable Integration** - Optional Indigo variable updates for advanced automation

## Screenshots

![Configuration Dialog](docs/images/config-dialog.png)
*Configure which music services to manage*

![Control Page](docs/images/control-page.png)
*Unified control interface with service indicators*

## Requirements

- **Indigo 2025.1 or later**
- **At least one of the following plugins:**
  - [Spotify Control Plugin](https://www.indigodomo.com/pluginstore/spotify-control/)
  - [Apple Music Control Plugin](https://www.indigodomo.com/pluginstore/apple-music-control/)
  - [VLC Control Plugin](https://www.indigodomo.com/pluginstore/vlc-control/)

> **Note:** You need at least one media player plugin for Music Manager to be useful. It's designed to work best with two or more services.

## Installation

### Quick Install

1. Download the latest release from the [Releases page](https://github.com/yourusername/indigo-music-manager/releases)
2. Double-click the `MusicManager.indigoPlugin` file to install
3. Restart Indigo server if prompted
4. Create a Music Manager device (Devices → New... → Plugin → Music Manager)

### From Source

```bash
git clone https://github.com/yourusername/indigo-music-manager.git
cd indigo-music-manager
open MusicManager.indigoPlugin
```

## Quick Start

1. **Install Required Plugins** - Install and configure at least one music player plugin
2. **Create Music Manager Device**:
   - Go to **Devices** → **New...**
   - Type: **Plugin** → **Music Manager**
   - Model: **Music Manager**
3. **Configure Device**:
   - Select your music player devices from the dropdowns
   - Choose "-- None --" for any service you don't want to use
   - Enable "Auto-Exclusive Playback" (recommended)
   - Set your preferred service for when nothing is playing
4. **Start Controlling** - Use the unified actions to control any active service!

## Configuration

### Device Settings

| Setting | Description | Default |
|---------|-------------|---------|
| **Spotify Device** | Your Spotify Player device (or "-- None --") | None |
| **Apple Music Device** | Your Apple Music Player device (or "-- None --") | None |
| **VLC Device** | Your VLC Player device (or "-- None --") | None |
| **Auto-Exclusive Playback** | Automatically pause other services when one starts | ON |
| **Preferred Service** | Which service to use when nothing is playing | Last Active |
| **Update Indigo Variables** | Create/update variables with music data | OFF |
| **Variable Prefix** | Prefix for created variables | Music |

### Preferred Service Options

- **Always prefer Spotify** - Commands default to Spotify when idle
- **Always prefer Apple Music** - Commands default to Apple Music when idle
- **Always prefer VLC** - Commands default to VLC when idle
- **Use last active service** - Commands go to whichever service played last

## Usage

### Basic Playback Control

```python
# Play/pause on active service
indigo.device.execute("Music Manager", action="playpause")

# Next track
indigo.device.execute("Music Manager", action="nextTrack")

# Set volume to 50%
indigo.device.execute("Music Manager", action="setVolume", props={"volume": "50"})
```

### Service Switching

```python
# Switch to Spotify (pauses others)
indigo.device.execute("Music Manager", action="switchToSpotify")

# Switch to Apple Music (pauses others)
indigo.device.execute("Music Manager", action="switchToAppleMusic")

# Switch to VLC (pauses others)
indigo.device.execute("Music Manager", action="switchToVLC")
```

### Triggers

Create triggers based on which service is playing:

```
Trigger: Device State Changed
Device: Music Manager
State: "spotifyPlaying" becomes true
Action: Turn on Spotify-themed lighting

Trigger: Device State Changed
Device: Music Manager
State: "appleMusicPlaying" becomes true
Action: Turn on Apple Music-themed lighting

Trigger: Device State Changed
Device: Music Manager
State: "isPlaying" becomes true
Action: Dim the lights
```

### Advanced Scripting

```python
# Get the Music Manager device
music = indigo.devices["Music Manager"]

# Check which service is active
if music.states['activeService'] == 'spotify':
    indigo.server.log("Spotify is active")
elif music.states['activeService'] == 'applemusic':
    indigo.server.log("Apple Music is active")
elif music.states['activeService'] == 'vlc':
    indigo.server.log("VLC is active")

# Check what's playing
if music.states['isPlaying']:
    track = music.states['trackName']
    artist = music.states['artist']
    indigo.server.log(f"Now playing: {artist} - {track}")
```

## Available Actions

### Playback Control
- Play
- Pause
- Play/Pause Toggle
- Stop All
- Next Track
- Previous Track

### Volume Control
- Set Volume
- Volume Up
- Volume Down
- Mute
- Unmute

### Service Control
- Switch to Spotify
- Switch to Apple Music
- Switch to VLC

### Playback Options
- Set Shuffle
- Set Repeat
- Skip Forward
- Skip Backward

### Utility
- Update Now (force immediate status refresh)

## Device States

| State | Type | Description |
|-------|------|-------------|
| `activeService` | String | Current active service ("spotify", "applemusic", "vlc", "none") |
| `isPlaying` | Boolean | True if active service is playing |
| `isPaused` | Boolean | True if active service is paused |
| `isStopped` | Boolean | True if all services are stopped |
| `spotifyPlaying` | Boolean | True if Spotify is playing |
| `appleMusicPlaying` | Boolean | True if Apple Music is playing |
| `vlcPlaying` | Boolean | True if VLC is playing |
| `trackName` | String | Current track name |
| `artist` | String | Current artist |
| `album` | String | Current album |
| `playerPosition` | Number | Position in seconds |
| `playerPositionFormatted` | String | Position as MM:SS |
| `duration` | Number | Track length in seconds |
| `durationFormatted` | String | Duration as MM:SS |
| `progressPercent` | Number | Playback progress (0-100%) |
| `soundVolume` | Number | Current volume (0-100) |
| `status` | String | Human-readable status with icons |

## How Auto-Exclusive Works

When **Auto-Exclusive Playback** is enabled:

1. **Start Spotify** → Apple Music and VLC automatically pause
2. **Start Apple Music** → Spotify and VLC automatically pause
3. **Start VLC** → Spotify and Apple Music automatically pause
4. **All stopped** → Commands route to your preferred service

This ensures only one service plays at a time without manual intervention.

## Troubleshooting

### Plugin Not Switching Services
- Verify all required plugins are installed and running
- Check that device IDs are correctly configured
- Ensure "Auto-Exclusive Playback" is enabled
- Check Indigo log for errors

### Commands Not Working
- Verify the active service has music queued
- Test commands directly on the underlying plugin
- Check that the music app is running on your Mac

### Status Not Updating
- Plugin polls every 0.5 seconds
- Try "Update Now" action to force refresh
- Verify underlying devices are updating properly

### Can't Deselect a Device
- Make sure you're using version 1.2.3 or later
- Select "-- None --" from the dropdown to deselect

## Development

### Project Structure

```
music-manager/
├── MusicManager.indigoPlugin/
│   └── Contents/
│       ├── Info.plist
│       └── Server Plugin/
│           ├── Actions.xml
│           ├── Devices.xml
│           ├── PluginConfig.xml
│           └── plugin.py
├── CHANGELOG.md
├── LICENSE
└── README.md
```

### Building from Source

The plugin is ready to use as-is. To modify:

1. Clone the repository
2. Edit files in `MusicManager.indigoPlugin/`
3. Install by double-clicking the `.indigoPlugin` file
4. Restart Indigo to load changes

### Running with Debug

Enable debug logging in Plugin Configuration:
- Go to **Plugins** → **Music Manager** → **Configure...**
- Check "Show debug information in log"
- View detailed logging in Indigo's Event Log

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

- Developed for [Indigo Domotics](https://www.indigodomo.com/)
- Icons: 🎵 Spotify, 🍎 Apple Music, 🎬 VLC
- Inspired by the need for unified music control across multiple services

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/indigo-music-manager/issues)
- **Forum**: [Indigo Forums](https://forums.indigodomo.com/)
- **Documentation**: [Wiki](https://github.com/yourusername/indigo-music-manager/wiki)

## Acknowledgments

- Thanks to the Indigo Domotics team for the excellent platform
- Thanks to all contributors and testers
- Special thanks to the Indigo community for feedback and support

---

**Note:** This plugin is a coordinator/manager and does not directly control music services. It requires the individual control plugins (Spotify, Apple Music, VLC) to be installed and functioning properly.
