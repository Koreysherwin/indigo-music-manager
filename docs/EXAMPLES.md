# Usage Examples

This document provides practical examples of how to use Music Manager in various scenarios.

## Table of Contents

- [Basic Control](#basic-control)
- [Service Switching](#service-switching)
- [Triggers](#triggers)
- [Python Scripting](#python-scripting)
- [Advanced Automation](#advanced-automation)
- [Control Page Integration](#control-page-integration)

## Basic Control

### Simple Play/Pause

The most common use case - control whichever service is active:

```applescript
-- Play/pause toggle (works with any active service)
tell application "Indigo" to execute action "Music Manager - Play/Pause Toggle"

-- Next track
tell application "Indigo" to execute action "Music Manager - Next Track"

-- Previous track
tell application "Indigo" to execute action "Music Manager - Previous Track"
```

### Volume Control

```applescript
-- Set volume to 50%
tell application "Indigo" to execute action "Music Manager - Set Volume" with value "50"

-- Volume up by 10
tell application "Indigo" to execute action "Music Manager - Volume Up" with value "10"

-- Volume down by 10
tell application "Indigo" to execute action "Music Manager - Volume Down" with value "10"

-- Mute
tell application "Indigo" to execute action "Music Manager - Mute"

-- Unmute
tell application "Indigo" to execute action "Music Manager - Unmute"
```

### Stop All Services

```applescript
-- Stop all music services at once
tell application "Indigo" to execute action "Music Manager - Stop All"
```

## Service Switching

### Switch Between Services

```applescript
-- Switch to Spotify (and pause others)
tell application "Indigo" to execute action "Music Manager - Switch to Spotify"

-- Switch to Apple Music (and pause others)
tell application "Indigo" to execute action "Music Manager - Switch to Apple Music"

-- Switch to VLC (and pause others)
tell application "Indigo" to execute action "Music Manager - Switch to VLC"
```

### Python Service Switching

```python
# Switch to Spotify
indigo.device.execute("Music Manager", action="switchToSpotify", props={"pauseOther": True})

# Switch to Apple Music without pausing others
indigo.device.execute("Music Manager", action="switchToAppleMusic", props={"pauseOther": False})
```

## Triggers

### Trigger on Playback State Changes

**Dim lights when any music starts:**

```
Trigger Type: Device State Changed
Device: Music Manager
State: isPlaying
Becomes: true
Action: Dim lights to 30%
```

**Restore lights when music stops:**

```
Trigger Type: Device State Changed
Device: Music Manager
State: isStopped
Becomes: true
Action: Set lights to 100%
```

### Trigger on Specific Service

**Different lighting for each service:**

```
Trigger: Music Manager - spotifyPlaying becomes true
Action: Set lights to green

Trigger: Music Manager - appleMusicPlaying becomes true
Action: Set lights to pink

Trigger: Music Manager - vlcPlaying becomes true
Action: Set lights to orange
```

### Trigger on Track Changes

```
Trigger Type: Device State Changed
Device: Music Manager
State: trackName
Changes
Action: Display notification with new track name
```

## Python Scripting

### Check Current Status

```python
# Get the Music Manager device
music = indigo.devices["Music Manager"]

# Check which service is active
active_service = music.states['activeService']
indigo.server.log(f"Active service: {active_service}")

# Check if anything is playing
if music.states['isPlaying']:
    track = music.states['trackName']
    artist = music.states['artist']
    album = music.states['album']
    indigo.server.log(f"Now playing: {artist} - {track} ({album})")
else:
    indigo.server.log("No music playing")
```

### Get Current Progress

```python
music = indigo.devices["Music Manager"]

position = music.states['playerPositionFormatted']
duration = music.states['durationFormatted']
progress = music.states['progressPercent']

indigo.server.log(f"Progress: {position} / {duration} ({progress}%)")
```

### Control Based on State

```python
music = indigo.devices["Music Manager"]

# Only play if not already playing
if not music.states['isPlaying']:
    indigo.device.execute("Music Manager", action="play")

# Pause if Spotify is playing
if music.states['spotifyPlaying']:
    indigo.device.execute("Music Manager", action="pause")
```

## Advanced Automation

### Time-Based Service Selection

```python
import datetime

# Get current hour
hour = datetime.datetime.now().hour
music_manager = indigo.devices["Music Manager"]

# Morning: Apple Music for calm playlists
if 6 <= hour < 9:
    indigo.device.execute("Music Manager", action="switchToAppleMusic")
    indigo.device.execute("Apple Music Player", action="playPlaylist", 
                         props={"playlistName": "Morning Calm"})
    
# Work hours: Spotify for focus music
elif 9 <= hour < 17:
    indigo.device.execute("Music Manager", action="switchToSpotify")
    indigo.device.execute("Spotify Player", action="playPlaylist",
                         props={"playlistUri": "spotify:playlist:37i9dQZEVXcQ9COmYvdRRZ"})
    
# Evening: VLC for local media
elif 17 <= hour < 22:
    indigo.device.execute("Music Manager", action="switchToVLC")
    indigo.device.execute("VLC Player", action="playFile",
                         props={"filePath": "/path/to/evening/playlist.m3u"})
```

### Room-Based Music Control

```python
# Different rooms prefer different services
room_services = {
    "Living Room": "applemusic",
    "Office": "spotify",
    "Bedroom": "spotify",
    "Media Room": "vlc"
}

# Get current room from variable
current_room = indigo.variables["CurrentRoom"].value

# Switch to preferred service for this room
if current_room in room_services:
    service = room_services[current_room]
    
    if service == "spotify":
        indigo.device.execute("Music Manager", action="switchToSpotify")
    elif service == "applemusic":
        indigo.device.execute("Music Manager", action="switchToAppleMusic")
    elif service == "vlc":
        indigo.device.execute("Music Manager", action="switchToVLC")
    
    # Now play appropriate music for the room
    indigo.device.execute("Music Manager", action="play")
```

### Volume Based on Time of Day

```python
import datetime

hour = datetime.datetime.now().hour
music_manager = indigo.devices["Music Manager"]

# Set volume based on time
if 6 <= hour < 8:  # Early morning
    volume = 20
elif 8 <= hour < 22:  # Day/evening
    volume = 50
else:  # Late night
    volume = 15

indigo.device.execute("Music Manager", action="setVolume", props={"volume": str(volume)})
```

### Presence-Based Auto-Pause

```python
# Pause music when everyone leaves
home_occupied = indigo.variables["HomeOccupied"].value == "true"
music_manager = indigo.devices["Music Manager"]

if not home_occupied and music_manager.states['isPlaying']:
    indigo.device.execute("Music Manager", action="pause")
    indigo.server.log("Paused music - everyone left home")
```

### Smart Volume Fade

```python
import time

# Gradually fade out music
music_manager = indigo.devices["Music Manager"]
current_volume = music_manager.states['soundVolume']

# Fade from current volume to 0 over 10 seconds
steps = 10
volume_step = current_volume / steps

for i in range(steps):
    new_volume = int(current_volume - (volume_step * (i + 1)))
    indigo.device.execute("Music Manager", action="setVolume", 
                         props={"volume": str(new_volume)})
    time.sleep(1)

# Finally pause
indigo.device.execute("Music Manager", action="pause")
```

## Control Page Integration

### Status Display

Add Music Manager to a control page to show what's playing:

**Status Field:**
- **State to Display:** `status`
- Shows: "🎵 ▶ Artist - Track Name"

**Example Status Values:**
- `🎵 ▶ The Beatles - Hey Jude` (Spotify playing)
- `🍎 ⏸ Taylor Swift - Anti-Hero` (Apple Music paused)
- `🎬 ▶ movie.mp4` (VLC playing)
- `🎵 ⏹ Not Playing` (Stopped)

### Control Buttons

**Play/Pause Button:**
- **Action:** Music Manager - Play/Pause Toggle
- **Shows:** Active service state

**Next/Previous Buttons:**
- **Previous Action:** Music Manager - Previous Track
- **Next Action:** Music Manager - Next Track

**Volume Slider:**
- **State:** soundVolume
- **Min:** 0
- **Max:** 100
- **Action:** Music Manager - Set Volume

### Service Selector

Create buttons to switch between services:

**Spotify Button:**
- **Action:** Music Manager - Switch to Spotify
- **State to show:** spotifyPlaying (highlights when active)

**Apple Music Button:**
- **Action:** Music Manager - Switch to Apple Music
- **State to show:** appleMusicPlaying (highlights when active)

**VLC Button:**
- **Action:** Music Manager - Switch to VLC
- **State to show:** vlcPlaying (highlights when active)

### Progress Display

**Current Track:**
- **State:** trackName

**Artist:**
- **State:** artist

**Progress Bar:**
- **State:** progressPercent
- **Type:** Progress indicator (0-100)

**Time Display:**
- **State:** playerPositionFormatted / durationFormatted
- **Shows:** "2:45 / 4:32"

## Variable-Based Automation

If you've enabled variable updates, you can use them in triggers and conditions:

```python
# Access variables
track = indigo.variables["MusicTrackName"].value
artist = indigo.variables["MusicArtist"].value
is_playing = indigo.variables["MusicIsPlaying"].value == "True"

# Use in conditions
if "Beethoven" in artist and is_playing:
    # Turn on classical music lighting scene
    indigo.actionGroup.execute("Classical Music Scene")
```

## Error Handling

Always check if device exists and is configured:

```python
try:
    music = indigo.devices["Music Manager"]
    
    # Check if any service is configured
    spotify_id = music.pluginProps.get('spotifyDeviceId', 0)
    apple_id = music.pluginProps.get('appleMusicDeviceId', 0)
    vlc_id = music.pluginProps.get('vlcDeviceId', 0)
    
    if not any([spotify_id, apple_id, vlc_id]):
        indigo.server.log("Music Manager has no services configured")
    else:
        # Safe to use
        indigo.device.execute(music, action="playpause")
        
except KeyError:
    indigo.server.log("Music Manager device not found")
```

## Tips and Best Practices

1. **Use Auto-Exclusive** - Let Music Manager handle pausing services
2. **Check States First** - Verify state before taking action
3. **Handle Errors** - Always use try/except in Python scripts
4. **Use the Right Service** - Some features work better on specific services
5. **Update Frequency** - Plugin updates every 0.5 seconds, don't poll faster
6. **Service Availability** - Check that music apps are running before complex operations

## More Examples

For more examples and community contributions, see:
- [GitHub Discussions](https://github.com/yourusername/indigo-music-manager/discussions)
- [Indigo Forums](https://forums.indigodomo.com/)
- [Wiki](https://github.com/yourusername/indigo-music-manager/wiki)
