#!/bin/bash
# setup-demo-user.sh — Create a blank-slate "demo" user for the masterclass live demo
#
# Run as your normal user (with sudo access):
#   bash setup-demo-user.sh
#
# Then switch to the demo user:
#   su - demo
#
# To clean up after the masterclass:
#   sudo userdel -r demo

set -euo pipefail

DEMO_USER="masterclass"
DEMO_HOME="/home/$DEMO_USER"

echo "=== Creating demo user for masterclass ==="

# Create user with home directory and bash shell
if id "$DEMO_USER" &>/dev/null; then
    echo "User '$DEMO_USER' already exists. Delete first with: sudo userdel -r $DEMO_USER"
    exit 1
fi

sudo useradd -m -s /bin/bash "$DEMO_USER"
sudo passwd "$DEMO_USER"

echo ""
echo "=== Demo user created ==="
echo ""
echo "The demo user has:"
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
echo "To switch to demo user:"
echo "  su - demo"
echo ""
echo "To switch back:"
echo "  exit"
echo ""
echo "During the masterclass, follow SETUP.md step by step."
echo ""
echo "To clean up after:"
echo "  sudo userdel -r demo"
