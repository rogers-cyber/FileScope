# FileScope v1.0.0 – Professional File & Folder Finder Tool (Full Source Code)

FileScope v1.0.0 is a modern Python desktop application designed for **fast, recursive searching of folders, files, and text inside files**.  
This repository contains the **full source code**, enabling full customization of search logic, UI styling, threading behavior, and progress animations for professional or personal workflows.

------------------------------------------------------------
🌟 FEATURES
------------------------------------------------------------

- 📁 Recursive Folder Scanning — Search entire directory trees
- 📂 Folder Name Search — Instantly locate folders by name
- 📄 File Name Search — Find files by partial or full name
- 🔍 Word-in-File Search — Search text content inside files
- ⚡ Multithreaded Search Engine — Smooth, responsive UI during scans
- 📊 Hybrid Animated Progress Bar
  - Indeterminate glow while indexing
  - Smooth real-time progress updates
- ✨ Glowing Gradient Animation — Professional visual feedback
- 🔢 Live Match Counter — Displays results as they are found
- ❌ Cancelable Search — Stop scans safely at any time
- 🖱️ Interactive Results List
  - Double-click to open files or folders
- ⌨️ Keyboard Support — Press Enter to start search
- 🎨 Modern Dark UI — Clean, professional interface
- 🧩 Cross-Platform Support — Windows, macOS, and Linux
- 🔒 100% Local Processing — No internet usage or data collection

------------------------------------------------------------
🚀 INSTALLATION
------------------------------------------------------------

1. Clone or download this repository:

git clone https://github.com/rogers-cyber/FileScope.git  
cd FileScope

2. Install required Python packages:

pip install PySide6

3. Run the application:

python FileScope.py

4. Optional: Build a standalone executable using PyInstaller:

pyinstaller --onefile --windowed FileScope.py

------------------------------------------------------------
💡 USAGE
------------------------------------------------------------

1. Select Root Folder:
   - Click **Browse** to choose the directory to search.

2. Choose Search Type:
   - Folder Name
   - File Name
   - Word in File

3. Enter Search Query:
   - Type the text you want to find.

4. Start Search:
   - Click **Search** or press **Enter**
   - Progress bar animates while scanning

5. Monitor Progress:
   - Smooth progress updates with glowing animation
   - Live match counter updates instantly

6. Review Results:
   - Found paths appear in the results list

7. Open Items:
   - Double-click any result to open it in your system’s file manager

8. Cancel Search:
   - Click **Cancel** to safely stop the scan

9. About / Info:
   - Click **About** for tool details and features

------------------------------------------------------------
⚙️ CONFIGURATION OPTIONS
------------------------------------------------------------

Option               Description
-------------------- --------------------------------------------------
Root Folder           Starting directory for recursive search
Search Type           Folder Name / File Name / Word in File
Search Query          Text to locate
Search Button         Start search process
Cancel Button         Stop active search
Progress Bar          Visual search progress indicator
Match Counter         Total results found
Results List          Displays found paths
About Dialog          Built-in tool overview

------------------------------------------------------------
📦 DEPENDENCIES
------------------------------------------------------------

- Python 3.10+
- PySide6 — Qt-based GUI framework
- OS / Subprocess — Platform-aware file handling
- QThread — Background search processing
- QTimer — Smooth animation and UI updates

------------------------------------------------------------
📝 NOTES
------------------------------------------------------------

- FileScope performs **local filesystem scanning only**
- No files are modified during searches
- Word-in-file search uses UTF-8 with error handling
- Large directories may take time depending on disk speed
- UI styling and animations are fully customizable
- Ideal for IT professionals, developers, analysts, and power users

------------------------------------------------------------
👤 ABOUT
------------------------------------------------------------

FileScope is developed and maintained by **Mate Technologies**, providing professional-grade Python productivity tools.

Website: https://matetools.gumroad.com

------------------------------------------------------------
📜 LICENSE
------------------------------------------------------------

Distributed as commercial source code.  
You may use it for personal or commercial projects.  
Redistribution, resale, or rebranding as a competing product is not allowed.
