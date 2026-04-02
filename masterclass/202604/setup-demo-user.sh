#!/bin/bash
# setup-demo-user.sh — Create a blank-slate user for the masterclass live demo
#
# Run as your normal user (with sudo access):
#   bash setup-demo-user.sh
#
# Then switch to the demo user:
#   su - masterclass
#
# To clean up after the masterclass:
#   sudo userdel -r masterclass

set -euo pipefail

DEMO_USER="${1:-masterclass}"
DEMO_HOME="/home/$DEMO_USER"

echo "=== Creating '$DEMO_USER' user for masterclass ==="

# Check if user already exists
if id "$DEMO_USER" &>/dev/null; then
    echo "User '$DEMO_USER' already exists."
    echo "To reset: sudo userdel -r $DEMO_USER && bash $0"
    echo "To just reset password: sudo passwd $DEMO_USER"
    exit 1
fi

# Create user (adduser is more reliable on Debian/Ubuntu than useradd)
sudo adduser --disabled-password --gecos "Masterclass Demo" "$DEMO_USER"

# Verify creation
if ! id "$DEMO_USER" &>/dev/null; then
    echo "ERROR: Failed to create user '$DEMO_USER'. Check system logs."
    exit 1
fi

if [ ! -d "$DEMO_HOME" ]; then
    echo "ERROR: Home directory $DEMO_HOME was not created."
    exit 1
fi

# Set password interactively
echo ""
echo "Set a password for '$DEMO_USER':"
sudo passwd "$DEMO_USER"

echo ""
echo "=== User '$DEMO_USER' created and verified ==="
echo ""
echo "The user has:"
echo "  ✓ git (system-level)"
echo "  ✓ Empty home directory"
echo "  ✗ No Node.js / nvm"
echo "  ✗ No opencode"
echo "  ✗ No gh authentication"
echo "  ✗ No PPQ.ai config"
echo "  ✗ No Chrome DevTools MCP"
echo ""
echo "This is exactly what a participant starts with."
echo ""
echo "To switch to this user:"
echo "  su - $DEMO_USER"
echo ""
echo "To switch back:"
echo "  exit"
echo ""
echo "During the masterclass, follow SETUP.md step by step."
echo ""
echo "To clean up after:"
echo "  sudo userdel -r $DEMO_USER"
