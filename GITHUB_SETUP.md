# Setting Up on GitHub

This guide walks you through uploading the Music Manager plugin to GitHub.

## Initial Setup

### 1. Create GitHub Repository

1. Go to [GitHub](https://github.com) and log in
2. Click the **+** icon → **New repository**
3. Repository name: `indigo-music-manager`
4. Description: `Unified music control plugin for Indigo Domotics - manage Spotify, Apple Music, and VLC`
5. Choose **Public** (recommended for open source)
6. ✅ Add a README file: **No** (we already have one)
7. ✅ Add .gitignore: **No** (we already have one)
8. Choose a license: **MIT** (or use our existing LICENSE)
9. Click **Create repository**

### 2. Upload Files

#### Option A: Using Git Command Line

```bash
# Navigate to the music-manager directory
cd music-manager

# Initialize git repository
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit - Music Manager v1.2.3"

# Add remote repository (replace yourusername)
git remote add origin https://github.com/yourusername/indigo-music-manager.git

# Push to GitHub
git branch -M main
git push -u origin main
```

#### Option B: Using GitHub Desktop

1. Open GitHub Desktop
2. File → Add Local Repository
3. Choose the `music-manager` directory
4. Click "Publish repository"
5. Check "Keep this code private" if desired
6. Click "Publish Repository"

#### Option C: Using GitHub Web Interface

1. In your new repository, click "uploading an existing file"
2. Drag and drop all files/folders from `music-manager`
3. Commit message: "Initial commit - Music Manager v1.2.3"
4. Click "Commit changes"

## Repository Configuration

### 3. Set Up Repository Settings

Go to repository **Settings**:

#### About Section
1. Click the gear icon next to "About"
2. Description: `Unified music control plugin for Indigo Domotics`
3. Website: Your plugin or Indigo website
4. Topics: Add tags like:
   - `indigo-plugin`
   - `home-automation`
   - `music-control`
   - `spotify`
   - `apple-music`
   - `vlc`

#### Features
- ✅ Issues (for bug reports and feature requests)
- ✅ Discussions (for community Q&A)
- ☐ Projects (optional)
- ☐ Wiki (optional, if you want extensive docs)

### 4. Create Initial Release

1. Go to **Releases** → **Create a new release**
2. Tag version: `v1.2.3`
3. Target: `main`
4. Release title: `Music Manager v1.2.3`
5. Description: Copy from `CHANGELOG.md` for v1.2.3
6. Attach files:
   - Upload `MusicManager-v1.2.3.indigoPlugin.zip`
7. Click **Publish release**

## GitHub Features to Enable

### Issues

Already set up with templates in `.github/ISSUE_TEMPLATE/`:
- Bug reports
- Feature requests

### Discussions

Enable in Settings → Features → Discussions:
- Create categories: General, Q&A, Show and Tell

### Actions

Already configured in `.github/workflows/release.yml`:
- Automatic release creation when you push a tag

### Branch Protection (Optional)

Settings → Branches → Add rule:
- Branch name pattern: `main`
- ✅ Require pull request reviews before merging
- ✅ Require status checks to pass before merging

## Maintaining the Repository

### Making Updates

```bash
# Make changes to files
# Then commit and push

git add .
git commit -m "Description of changes"
git push
```

### Creating New Releases

```bash
# Update version in Info.plist
# Update CHANGELOG.md

# Run release script (optional)
./scripts/prepare-release.sh

# Commit changes
git add .
git commit -m "Release v1.2.4"
git push

# Create and push tag
git tag -a v1.2.4 -m "Release v1.2.4"
git push --tags

# GitHub Actions will automatically create the release
```

### Handling Issues

When someone reports an issue:
1. Thank them for the report
2. Try to reproduce the issue
3. Label appropriately (bug, enhancement, question)
4. Assign to yourself if working on it
5. Close when resolved with explanation

### Handling Pull Requests

When someone submits a PR:
1. Review the code changes
2. Test the changes locally
3. Provide feedback if needed
4. Approve and merge when ready
5. Thank the contributor!

## Best Practices

### Commit Messages

Use clear, descriptive commit messages:
- ✅ `Fix device selection not showing VLC devices`
- ✅ `Add support for shuffle mode`
- ❌ `Fixed stuff`
- ❌ `Update`

### Branching

For new features:
```bash
git checkout -b feature/new-feature-name
# Make changes
git push -u origin feature/new-feature-name
# Create pull request on GitHub
```

For bug fixes:
```bash
git checkout -b fix/bug-description
# Make changes
git push -u origin fix/bug-description
# Create pull request on GitHub
```

### Versioning

Follow [Semantic Versioning](https://semver.org/):
- **Major** (1.0.0): Breaking changes
- **Minor** (0.1.0): New features, backwards compatible
- **Patch** (0.0.1): Bug fixes

### Documentation

Keep docs updated:
- README.md for overview
- CHANGELOG.md for all changes
- EXAMPLES.md for usage examples
- INSTALL.md for setup instructions

## Promoting Your Plugin

### Indigo Plugin Store

1. Contact Indigo support to list your plugin
2. Provide: plugin file, description, screenshots
3. Link to your GitHub repository

### Indigo Forums

1. Create a thread in the Plugin Development forum
2. Include: description, features, download link
3. Respond to user questions and feedback

### Social Media

Share on:
- Reddit (r/homeautomation, r/smarthome)
- Twitter/X with #HomeAutomation #Indigo
- Home automation Discord servers

## Support Resources

- [GitHub Docs](https://docs.github.com/)
- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Semantic Versioning](https://semver.org/)

## Checklist

Before making repository public:

- [ ] All files committed and pushed
- [ ] README.md is complete and accurate
- [ ] LICENSE file included
- [ ] CHANGELOG.md up to date
- [ ] No sensitive information in code
- [ ] No hardcoded passwords or API keys
- [ ] Plugin tested and working
- [ ] Repository description set
- [ ] Topics/tags added
- [ ] First release created
- [ ] Issues and Discussions enabled

## Your Repository URLs

Once created, your repository will be at:
- Main: `https://github.com/yourusername/indigo-music-manager`
- Issues: `https://github.com/yourusername/indigo-music-manager/issues`
- Releases: `https://github.com/yourusername/indigo-music-manager/releases`
- Discussions: `https://github.com/yourusername/indigo-music-manager/discussions`

**Remember to update all instances of `yourusername` in the documentation with your actual GitHub username!**

Happy sharing! 🚀
