# Desktop AI Agent for Windows

A simple Windows desktop AI assistant built with Python + Tkinter + the OpenAI API.

## Fastest way to get the EXE

This project includes a GitHub Actions workflow that builds the Windows `.exe`
on a real Windows runner, so you do not need to install Python on the target PC.

1. Create a GitHub repository.
2. Upload this entire folder.
3. Open **Actions** → **Build Windows EXE**.
4. Wait for the workflow to finish.
5. Open the completed workflow run and download the `DesktopAIAgent-Windows` artifact.
6. Extract it and run `DesktopAIAgent.exe`.

## Local Windows build

Install Python 3.11+ on Windows, then double-click `build_windows.bat`.
The finished executable will be in `dist\DesktopAIAgent.exe`.

## API key

The app asks for your OpenAI API key at runtime. The key is kept only in
the running process/environment for that session and is not bundled into the EXE.

Do not paste an API key into source code or commit one to GitHub.

## Current capabilities

- Desktop chat window
- Conversation context during the session
- OpenAI Responses API
- One-click API key setup
- Windows `.exe` packaging

The next version can add optional tools such as web search, selected-file
reading, app launching, voice, and other computer actions with confirmation prompts.
