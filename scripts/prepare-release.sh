#!/bin/bash
# Release preparation script for Music Manager Plugin

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Music Manager Plugin - Release Preparation${NC}"
echo "=============================================="

# Get version from Info.plist
VERSION=$(defaults read "$(pwd)/MusicManager.indigoPlugin/Contents/Info.plist" PluginVersion)
echo -e "${YELLOW}Current version: ${VERSION}${NC}"

# Check if version is in CHANGELOG
if ! grep -q "\[${VERSION}\]" CHANGELOG.md; then
    echo -e "${RED}Error: Version ${VERSION} not found in CHANGELOG.md${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Version found in CHANGELOG"

# Check if all required files exist
echo "Checking required files..."
required_files=(
    "README.md"
    "LICENSE"
    "CHANGELOG.md"
    "CONTRIBUTING.md"
    "INSTALL.md"
    ".gitignore"
    "MusicManager.indigoPlugin/Contents/Info.plist"
    "MusicManager.indigoPlugin/Contents/Server Plugin/plugin.py"
    "MusicManager.indigoPlugin/Contents/Server Plugin/Devices.xml"
    "MusicManager.indigoPlugin/Contents/Server Plugin/Actions.xml"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}Error: Missing required file: ${file}${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓${NC} $file"
done

# Create release directory
RELEASE_DIR="releases/v${VERSION}"
mkdir -p "$RELEASE_DIR"

# Create plugin zip
echo "Creating plugin archive..."
cd MusicManager.indigoPlugin
zip -r "../${RELEASE_DIR}/MusicManager-v${VERSION}.indigoPlugin.zip" . -x "*.DS_Store" -x "__pycache__/*"
cd ..

echo -e "${GREEN}✓${NC} Created ${RELEASE_DIR}/MusicManager-v${VERSION}.indigoPlugin.zip"

# Copy documentation to release
echo "Copying documentation..."
cp README.md "${RELEASE_DIR}/"
cp CHANGELOG.md "${RELEASE_DIR}/"
cp LICENSE "${RELEASE_DIR}/"
cp INSTALL.md "${RELEASE_DIR}/"

echo -e "${GREEN}✓${NC} Documentation copied"

# Extract release notes from CHANGELOG
echo "Extracting release notes..."
sed -n "/## \[${VERSION}\]/,/## \[/p" CHANGELOG.md | sed '$d' > "${RELEASE_DIR}/RELEASE_NOTES.md"

echo -e "${GREEN}✓${NC} Release notes extracted"

# Create checksums
echo "Generating checksums..."
cd "${RELEASE_DIR}"
shasum -a 256 "MusicManager-v${VERSION}.indigoPlugin.zip" > "MusicManager-v${VERSION}.indigoPlugin.zip.sha256"
cd ../..

echo -e "${GREEN}✓${NC} Checksums generated"

# Display summary
echo ""
echo "=============================================="
echo -e "${GREEN}Release v${VERSION} prepared successfully!${NC}"
echo "Location: ${RELEASE_DIR}"
echo ""
echo "Files created:"
echo "  - MusicManager-v${VERSION}.indigoPlugin.zip"
echo "  - MusicManager-v${VERSION}.indigoPlugin.zip.sha256"
echo "  - README.md"
echo "  - CHANGELOG.md"
echo "  - LICENSE"
echo "  - INSTALL.md"
echo "  - RELEASE_NOTES.md"
echo ""
echo "Next steps:"
echo "  1. Review release notes"
echo "  2. Test the plugin installation"
echo "  3. Commit changes: git add . && git commit -m 'Release v${VERSION}'"
echo "  4. Create tag: git tag -a v${VERSION} -m 'Release v${VERSION}'"
echo "  5. Push: git push && git push --tags"
echo "  6. Create GitHub release using RELEASE_NOTES.md"
echo ""
