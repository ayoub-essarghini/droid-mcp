# Droid MCP Server 🤖📱

A Headless Android Model Context Protocol (MCP) Server. 
Turns any Android device or emulator into an AI-native platform, allowing LLMs to interact directly with the OS.

## Features
- 👁️ **Read Screen:** Parses UI Automator XML into clean, semantic JSON.
- 👆 **Device Actions:** Tap coordinates and press physical system buttons.
- 🔋 **Device Info:** Retrieves battery, OS version, and model info.
- ⚡ **1-Click Auto-Linker:** A bulletproof GUI installer that auto-detects your Python environment and resolves absolute paths for seamless VS Code integration.

## Architecture
Built with Clean Architecture principles using Python 3.11+, Pydantic for strict data validation, and the official Anthropic MCP SDK. *Start small, stay lean, scale smart.*

---

## 🔌 Setup & Installation

This server is designed to work seamlessly with local LLMs (like Ollama) via MCP Clients such as Cline in VS Code.

### ⚠️ Prerequisites for macOS Users
If you are on a Mac and use Homebrew to manage Python, `tkinter` (required for the 1-Click UI) is not installed by default. Run this first:
```bash
brew install python-tk@3.11
```
*(Adjust the version number if you are using a different Python version).*

### 🚀 1-Click Auto-Link to VS Code (Cline)
Forget manual JSON configurations and path issues. Run the built-in GUI to automatically link this MCP server to your local AI Agent. It automatically captures your current environment's absolute paths.

1. Activate your virtual environment (if you use one).
2. Run the linker:
```bash
python link_gui.py
```
3. Click **"Link to Cline"**.
4. **Restart VS Code.** You will now see `droid-mcp` with a green indicator in your Cline MCP Servers list.

---

## 🎮 How to use with Cline (Prompt Examples)

Once connected, your LLM will automatically have access to the Android tools. Here is how you can command it:

**1. Information Gathering:**
> "Use your tools to check my connected Android device's battery level and OS version."

**2. Screen Reading:**
> "Read the current screen and list all the visible apps and buttons."

**3. Action & Interaction (The Boss Level):**
> "I want you to open Gmail. First, read the current screen to find the bounding box coordinates for 'Gmail'. Calculate the center X and Y coordinates. Finally, use the tap_screen tool to click exactly on that center point."