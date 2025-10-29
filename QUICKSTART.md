# Quick Start Guide

Get up and running with Music Manager in 5 minutes!

## Prerequisites Checklist

- [ ] Indigo 2025.1 or later installed
- [ ] At least one music plugin installed (Spotify, Apple Music, or VLC)
- [ ] At least one device created in each music plugin you use

## Installation (2 minutes)

1. **Download** the plugin from [Releases](https://github.com/yourusername/indigo-music-manager/releases)
2. **Unzip** the downloaded file
3. **Double-click** `MusicManager.indigoPlugin`
4. Click **Install Plugin** when Indigo prompts you
5. **Restart Indigo** if prompted

## Setup (3 minutes)

### Create Device

1. In Indigo: **Devices** → **New...**
2. Type: **Plugin** → **Music Manager**
3. Model: **Music Manager**
4. Name it: "Music Manager"
5. Click **Add**

### Configure Device

In the configuration dialog:

1. **Select your devices:**
   - Spotify Device: Choose your Spotify player (or "-- None --")
   - Apple Music Device: Choose your Apple Music player (or "-- None --")
   - VLC Device: Choose your VLC player (or "-- None --")

2. **Keep recommended settings:**
   - ✅ Auto-Exclusive Playback
   - Preferred Service: Use last active service
   - ☐ Update Indigo Variables (leave off for now)

3. Click **Save**

## Test It Out

### Test 1: Basic Control

1. Start playing music on Spotify or Apple Music
2. In Indigo, find your Music Manager device
3. Execute action: **Music Manager** → **Pause**
4. ✅ Music should pause!

### Test 2: Auto-Exclusive

1. Play music on Spotify
2. Start playing on Apple Music
3. ✅ Spotify should automatically pause!

### Test 3: Service Switching

1. With Apple Music playing, execute: **Switch to Spotify**
2. ✅ Apple Music pauses, Spotify becomes active

## You're Done! 🎉

Music Manager is now controlling your music services!

## What's Next?

### Add to Control Page

1. Open Control Pages editor
2. Add a new page or edit existing one
3. Add Text field showing: **Music Manager** → **status**
4. Add buttons for Play/Pause, Next, Previous
5. See current track and service at a glance!

### Create a Trigger

Example: Dim lights when music plays

```
Trigger Type: Device State Changed
Device: Music Manager
State: isPlaying
Becomes: true
Actions:
  - Dim living room lights to 30%
```

### Try Python Scripting

```python
# Get what's playing
music = indigo.devices["Music Manager"]
if music.states['isPlaying']:
    track = music.states['trackName']
    artist = music.states['artist']
    indigo.server.log(f"Now playing: {artist} - {track}")
```

## Need Help?

- 📖 Read the full [README](README.md)
- 📝 See [usage examples](docs/EXAMPLES.md)
- 🔧 Check [installation guide](INSTALL.md)
- 🐛 Report issues on [GitHub](https://github.com/yourusername/indigo-music-manager/issues)

## Quick Reference Card

### Common Actions
- Play/Pause Toggle
- Next Track
- Previous Track
- Set Volume
- Switch to Spotify/Apple Music/VLC

### Useful States
- `status` - What's playing with icon
- `isPlaying` - Boolean, is music playing?
- `trackName` - Current track
- `artist` - Current artist
- `activeService` - "spotify", "applemusic", "vlc", or "none"

### Tips
- ✅ Enable Auto-Exclusive for automatic service management
- 🎯 Use "Last Active" for smart service routing
- 📊 Status field shows which service with icons (🎵 🍎 🎬)
- 🔄 Plugin updates every 0.5 seconds automatically

Happy listening! 🎵
