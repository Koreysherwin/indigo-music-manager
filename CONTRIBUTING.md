# Contributing to Music Manager Plugin

First off, thank you for considering contributing to Music Manager! It's people like you that make this plugin better for everyone.

## Code of Conduct

This project and everyone participating in it is governed by a code of respect and professionalism. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** to demonstrate the steps
- **Describe the behavior you observed** and what you expected to see
- **Include screenshots** if relevant
- **Include your environment details:**
  - Indigo version
  - macOS version
  - Plugin version
  - Which music plugins you're using (Spotify, Apple Music, VLC)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Provide specific examples** of how this enhancement would be useful
- **Explain why this enhancement would be useful** to most users

### Pull Requests

1. Fork the repository
2. Create a new branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes
4. Test your changes thoroughly
5. Update documentation if needed
6. Commit your changes:
   ```bash
   git commit -m "Add feature: description of your feature"
   ```
7. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
8. Open a Pull Request

## Development Setup

### Prerequisites

- macOS with Indigo Domotics installed
- At least one music control plugin (Spotify, Apple Music, or VLC)
- Basic knowledge of Python 2.7 (Indigo's version)
- Text editor or IDE

### Getting Started

1. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/indigo-music-manager.git
   cd indigo-music-manager
   ```

2. Install the plugin in development mode:
   ```bash
   open MusicManager.indigoPlugin
   ```

3. Enable debug logging:
   - Go to Plugins → Music Manager → Configure
   - Check "Show debug information in log"

4. Make your changes to the plugin files

5. Reload the plugin in Indigo:
   - Plugins → Music Manager → Reload

### Project Structure

```
MusicManager.indigoPlugin/
└── Contents/
    ├── Info.plist          # Plugin metadata and version
    └── Server Plugin/
        ├── Actions.xml     # Action definitions
        ├── Devices.xml     # Device configuration UI
        ├── PluginConfig.xml # Plugin-wide settings
        └── plugin.py       # Main plugin logic
```

### Coding Style

- Follow PEP 8 style guide where applicable
- Use descriptive variable names
- Add comments for complex logic
- Keep methods focused and single-purpose
- Use docstrings for all methods

Example:
```python
def getSpotifyDeviceList(self, filter="", valuesDict=None, typeId="", targetId=0):
    """Return list of Spotify devices
    
    Returns a list of tuples (device_id, device_name) for all available
    Spotify devices. First item is always (0, "-- None --") to allow
    deselection.
    
    Returns:
        list: List of (int, str) tuples
    """
    deviceList = [(0, "-- None --")]
    # ... implementation
    return deviceList
```

### Testing

Before submitting a PR, test:

1. **Installation** - Fresh install works
2. **Configuration** - All configuration options work
3. **Service Switching** - Auto-exclusive behavior works
4. **All Actions** - Play, pause, next, previous, volume, etc.
5. **Edge Cases** - No devices configured, one device, all devices
6. **State Updates** - Device states update correctly

### Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests after the first line

Examples:
```
Add support for repeat mode in VLC

Fix device selection dropdown not showing devices
Fixes #123

Update documentation for service switching
```

## XML Configuration Guidelines

When modifying XML files:

### Devices.xml

- Keep field IDs descriptive and camelCase
- Use appropriate field types (menu, textfield, checkbox)
- Provide clear labels and descriptions
- Set sensible default values

### Actions.xml

- Action IDs should match callback method names
- Use descriptive action names
- Include ConfigUI for actions with parameters
- Keep callback method names consistent (action + PascalCase)

## Python Guidelines

### Plugin Methods

Key methods to understand:

- `startup()` - Plugin initialization
- `shutdown()` - Plugin cleanup
- `deviceStartComm(dev)` - Device starts
- `deviceStopComm(dev)` - Device stops
- `runConcurrentThread()` - Main monitoring loop
- `updateMusicStatus(dev)` - Updates device states

### Error Handling

Always wrap potentially failing code in try/except:

```python
try:
    # Your code here
    pass
except Exception as e:
    self.errorLog(u"Error description: {}".format(str(e)))
```

### Logging

Use appropriate log levels:

```python
self.debugLog(u"Debug message")      # Only when debug enabled
indigo.server.log(u"Info message")   # Normal operation
self.errorLog(u"Error message")      # Errors
```

## Documentation

When adding features:

1. Update README.md with usage examples
2. Update CHANGELOG.md with changes
3. Add inline code comments for complex logic
4. Update action/device descriptions in XML

## Release Process

Maintainers will:

1. Update version in `Info.plist`
2. Update CHANGELOG.md
3. Create a git tag
4. Create a GitHub release
5. Attach the `.indigoPlugin` file

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

## Recognition

Contributors will be recognized in:
- README.md acknowledgments section
- Release notes
- GitHub contributors page

Thank you for contributing! 🎵
