# Masterclass Setup Guide

## Lightning Payment Integration with Blink API + AI Coding Tools

This guide walks you through setting up a complete AI-assisted development environment from scratch. By the end, you'll have everything needed to build and deploy a Lightning payment website.

**Time required:** ~15 minutes  
**OS:** Linux (Ubuntu/Debian) or WSL on Windows  
**Cost:** ~$5 one-time (for PPQ.ai LLM credits, paid with Lightning)

---

## Step 1: Terminal

You need a Linux terminal. If you're on:
- **Linux:** You're good. Open your terminal.
- **macOS:** Open Terminal.app. You're good.
- **Windows:** Install WSL first:
  ```bash
  wsl --install -d Ubuntu
  ```
  Then open the Ubuntu terminal.

## Step 2: Git

Check if git is installed:
```bash
git --version
```

If not:
```bash
sudo apt update && sudo apt install -y git
```

Configure your identity:
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

## Step 3: GitHub CLI (`gh`)

The GitHub CLI lets AI agents create repos, enable Pages, and push code — all from the terminal.

```bash
# Install gh (Ubuntu/Debian)
sudo apt install -y gh

# Or install the latest version:
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update && sudo apt install -y gh
```

Authenticate:
```bash
gh auth login
```
Follow the prompts — choose GitHub.com, HTTPS, and authenticate via browser.

Verify:
```bash
gh auth status
```

## Step 4: Node.js

OpenCode and Chrome DevTools MCP need Node.js.

```bash
# Install nvm (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash

# Load nvm into current shell (do NOT use 'source ~/.bashrc' — it may not work in all shells)
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Install Node.js 20 (use a specific version, not --lts, to avoid lookup issues)
nvm install 20
```

Verify:
```bash
node --version   # Should show v20.x
npm --version
```

## Step 5: OpenCode

OpenCode is the AI coding agent that runs in your terminal.

```bash
# Install opencode
curl -fsSL https://opencode.ai/install | bash

# Add to PATH for current session and future sessions
export PATH=$HOME/.opencode/bin:$PATH
echo 'export PATH=$HOME/.opencode/bin:$PATH' >> ~/.bashrc
```

Verify:
```bash
opencode --version
```

## Step 6: PPQ.ai Account + API Key

PPQ.ai gives you access to cheap LLM models. You can top up with Lightning — no subscription needed.

1. Go to **https://ppq.ai**
2. Create an account
3. Top up with Lightning (~$5 worth of sats)
4. Go to Settings → API Keys → Create new key
5. Copy the API key (starts with `sk-`)

## Step 7: Configure OpenCode

Create the config file:

```bash
mkdir -p ~/.config/opencode
```

Copy the example config from this repo:
```bash
cp opencode-config-example.json ~/.config/opencode/opencode.json
```

Or create it manually:
```bash
cat > ~/.config/opencode/opencode.json << 'EOF'
{
  "$schema": "https://opencode.ai/config.json",
  "model": "ppq/minimax/minimax-m2.5",
  "provider": {
    "ppq": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "PPQ.AI",
      "options": {
        "baseURL": "https://api.ppq.ai",
        "apiKey": "YOUR_PPQ_API_KEY_HERE"
      },
      "models": {
        "minimax/minimax-m2.5": {
          "name": "MiniMax M2.5",
          "limit": {
            "context": 196608,
            "output": 16384
          }
        }
      }
    }
  }
}
EOF
```

**Replace `YOUR_PPQ_API_KEY_HERE` with your actual PPQ.ai API key.**

## Step 8: Chrome DevTools MCP (Optional)

This lets the AI agent control a web browser — open pages, click buttons, take screenshots to test its own work.

```bash
npm install -g chrome-devtools-mcp
```

Add it to your OpenCode config by editing `~/.config/opencode/opencode.json` and adding an `"mcp"` section:

```json
{
  "mcp": {
    "chrome-devtools": {
      "type": "local",
      "command": ["chrome-devtools-mcp"],
      "enabled": true
    }
  }
}
```

## Step 9: Blink Account

1. Download Bitcoin Beach Wallet (Blink) on your phone
2. Create an account and choose a username
3. Your Lightning address will be `username@blink.sv`

You'll use this username in the donation page we build.

## Step 10: Test Everything

```bash
# Test GitHub CLI
gh repo list --limit 1

# Test OpenCode
cd /tmp
mkdir test-project && cd test-project
git init
opencode
```

In the OpenCode prompt, type:
```
What model are you? What tools do you have available?
```

If it responds and lists tools including bash, you're ready.

---

## Quick Reference

| Tool | Install command | What it does |
|------|----------------|-------------|
| `git` | `sudo apt install git` | Version control |
| `gh` | `sudo apt install gh` | GitHub from terminal |
| `node` | `nvm install 20` | JavaScript runtime |
| `opencode` | `curl -fsSL https://opencode.ai/install \| bash` | AI coding agent |
| `chrome-devtools-mcp` | `npm install -g chrome-devtools-mcp` | Browser automation for AI |

## Cost Breakdown

| Item | Cost | Notes |
|------|------|-------|
| GitHub account | Free | Repos, Pages, Actions |
| GitHub Pages hosting | Free | Static sites |
| Blink account | Free | Lightning wallet + username |
| PPQ.ai (MiniMax M2.5) | ~$0.30/session | Top up with Lightning |
| OpenCode | Free | Open source |
| Chrome DevTools MCP | Free | npm package |
| **Total** | **~$5 one-time** | For PPQ.ai credits |

---

*This guide was created for the Africa Free Routing Lightning Payment Integration Masterclass, April 2, 2026.*
