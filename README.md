# Droid MCP Server 🤖📱

A Headless Android Model Context Protocol (MCP) Server. 
Turns any Android device or emulator into an AI-native platform, allowing LLMs to interact directly with the OS.

## Features
- 👁️ **Read Screen:** Parses UI Automator XML into clean, semantic JSON.
- 👆 **Device Actions:** Tap coordinates and press physical system buttons.
- 🔋 **Device Info:** Retrieves battery, OS version, and model info.

## Architecture
Built with Clean Architecture principles using Python 3.11+, Pydantic for strict data validation, and the official MCP SDK.

## Usage (Local AI with Ollama)
This server is designed to work seamlessly with local LLMs via Ollama and MCP Clients (like Cline/Continue.dev).