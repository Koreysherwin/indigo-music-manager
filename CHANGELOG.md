# Changelog

## [1.2.3] - 2025-10-29

### Fixed
- Fixed device configuration to allow deselecting music players
- Added "-- None --" option to all three device dropdowns (Spotify, Apple Music, VLC)
- Now properly supports using only one or two services instead of requiring all three

## [1.2.2] - 2025-01-09

### Fixed
- Fixed device list population in configuration dialog
- Added dynamic device list methods (getSpotifyDeviceList, getAppleMusicDeviceList, getVLCDeviceList)
- Fixed XML List element syntax with explicit `filter=""` attribute
- Device dropdowns now properly show available Spotify, Apple Music, and VLC devices

## [1.1.1] - 2025-01-09

### Fixed
- Fixed XML format compatibility with Indigo 2025
- Fixed empty device ID handling to prevent integer conversion errors

## [1.1.0] - 2025-01-09

### Added
- VLC support
- Three-way mutual exclusion (Spotify, Apple Music, VLC)
- Switch to VLC action
- VLC Playing state for triggers
- VLC icon (🎬) in status displays

### Changed
- Updated service switching actions to pause all other services
- Enhanced service detection to handle VLC's different state names

## [1.0.0] - 2025-01-09

### Added
- Initial release
- Unified control interface for Spotify and Apple Music
- Automatic mutual exclusion between services
- Service switching actions
- Combined status display with service icons
- Variable integration
- Active service tracking
- Preferred service setting
