# WhatsApp Chat Viewer - Offline

Transform your WhatsApp chat exports into a beautiful, offline-viewable web interface with images, videos, and authentic WhatsApp styling.

![Version](https://img.shields.io/badge/version-1.0-blue)
![Python](https://img.shields.io/badge/python-3.6+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## 📋 Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [Detailed Setup](#detailed-setup)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)

---

## ✨ Features

- 🎨 **Authentic WhatsApp UI** - Dark mode with exact WhatsApp colors
- 📱 **Fully Responsive** - Works on desktop, tablet, and mobile
- 🖼️ **Media Support** - Images, videos, and audio files
- 📅 **Date Separators** - Organized by TODAY/YESTERDAY/DATE
- 💬 **System Messages** - Encryption notices, group events
- 🔍 **Lightbox Viewer** - Click images/videos for full-screen view
- 📦 **100% Offline** - No internet required, no server needed
- 🚀 **One-Click Open** - Just double-click the HTML file
- 🌍 **Portable** - Share with anyone (HTML + media folder)

---

## 🔧 Requirements

- **Python 3.6 or higher**
  - Download from: https://www.python.org/downloads/
  - ✅ Check "Add Python to PATH" during installation
- **WhatsApp Chat Export** (Android format)
- **Web Browser** (Chrome, Firefox, Edge, Safari)

---

## 🚀 Quick Start

### Before You Begin

**⚠️ IMPORTANT:** To get the correct layout (your messages on right/green, others on left/gray), you need to know YOUR name as it appears in the WhatsApp export.

1. Open your exported `chat.txt` file
2. Find a message you sent
3. Note your EXACT name: `18/11/2025, 11:31 am - YOUR NAME HERE: message`
4. Remember this - you'll need it in Step 3!

### Step 1: Export Your WhatsApp Chat

1. Open WhatsApp on your phone
2. Open the chat you want to export
3. Tap the **⋮** (three dots) → **More** → **Export chat**
4. Choose **"Include media"** (or "Without media" if you prefer)
5. Save the exported files to your computer

You'll get:
- A `.txt` file (e.g., `WhatsApp Chat with Contact.txt`)
- A folder with images/videos (if you included media)

### Step 2: Setup Project Folder

Create a folder and organize your files:

```
whatsapp-chat-viewer/
├── parser.py                  ← Copy from artifact #1
├── make_standalone.py         ← Copy from artifact #6
├── chat.txt                   ← Your WhatsApp export (rename if needed)
└── media/                     ← Create this folder
    ├── IMG-20251118-WA0000.jpg
    ├── IMG-20251124-WA0030.jpg
    └── (all other images/videos)
```

### Step 3: Run the Scripts

Open **Command Prompt** (Windows) or **Terminal** (Mac/Linux) in your project folder:

```bash
# 1. Parse the WhatsApp chat file
python parser.py "chat.txt" chat.json

# 2. Edit make_standalone.py - Change 'You' to YOUR NAME
#    (Open in text editor, find currentUserName: 'You', change it)

# 3. Generate standalone HTML viewer
python make_standalone.py

# 4. Done! Double-click whatsapp_viewer.html to open
```

**IMPORTANT:** In Step 2, change `currentUserName: 'You'` to your EXACT name from the chat file, otherwise all messages will appear on the same side!

---

## 📖 Detailed Setup

### 1. Install Python

**Windows:**
1. Download from https://www.python.org/downloads/
2. Run installer
3. ✅ **IMPORTANT:** Check "Add Python to PATH"
4. Click "Install Now"
5. Verify: Open Command Prompt and type `python --version`

**Mac:**
```bash
# Python 3 usually comes pre-installed
python3 --version

# If not installed, use Homebrew:
brew install python3
```

**Linux:**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### 2. Get the Code Files

#### Option A: Copy from Artifacts (Recommended)

1. **parser.py** - Copy code from Artifact #1 above
2. **make_standalone.py** - Copy code from Artifact #6 above

Save each file in your project folder.

#### Option B: Download from Repository

```bash
git clone https://github.com/yourusername/whatsapp-chat-viewer.git
cd whatsapp-chat-viewer
```

### 3. Prepare Your WhatsApp Export

1. **Rename your chat file** (optional but recommended):
   - From: `WhatsApp Chat with Contact Name (234).txt`
   - To: `chat.txt`

2. **Create media folder**:
   ```bash
   mkdir media
   ```

3. **Move all images/videos** to the `media/` folder:
   - `IMG-*.jpg`
   - `VID-*.mp4`
   - `PTT-*.opus` (voice messages)
   - Any other media files

### 4. Run the Parser

```bash
python parser.py "chat.txt" chat.json
```

**Expected Output:**
```
✓ Parsed 14 messages
✓ Saved to chat.json

Statistics:
  Text messages: 2
  Media messages: 11
  System messages: 1
```

This creates a `chat.json` file with structured data.

### 5. Generate Standalone HTML

```bash
python make_standalone.py
```

**Expected Output:**
```
============================================================
WhatsApp Standalone HTML Generator
============================================================

✓ Loaded 14 messages from chat.json
✓ Generated standalone HTML: whatsapp_viewer.html

🎉 Success! You can now:
   1. Double-click 'whatsapp_viewer.html' to open it
   2. No server needed!
   3. Make sure 'media/' folder is in the same directory
```

### 6. Open the Viewer

Simply **double-click** `whatsapp_viewer.html` - it opens in your default browser!

---

## 📂 File Structure

### Complete Project Layout

```
whatsapp-chat-viewer/
│
├── parser.py                     # Converts .txt to .json
├── make_standalone.py            # Creates standalone HTML
│
├── chat.txt                      # Your WhatsApp export (input)
├── chat.json                     # Parsed data (generated)
├── whatsapp_viewer.html          # Final viewer (generated) ⭐
│
└── media/                        # All images/videos
    ├── IMG-20251118-WA0000.jpg
    ├── IMG-20251124-WA0030.jpg
    ├── VID-20251210-WA0001.mp4
    └── ...
```

### Files You Create
- `parser.py` - Copy from artifact
- `make_standalone.py` - Copy from artifact
- `media/` folder - Create manually

### Files You Provide
- `chat.txt` - From WhatsApp export
- Media files in `media/` - From WhatsApp export

### Files Generated Automatically
- `chat.json` - Created by parser.py
- `whatsapp_viewer.html` - Created by make_standalone.py

---

## 🎮 Usage

### Basic Usage

```bash
# Standard workflow
python parser.py "chat.txt" chat.json
python make_standalone.py
# Then double-click whatsapp_viewer.html
```

### Advanced Usage

#### Custom Input/Output Names

```bash
# Parse a differently named file
python parser.py "My Chat Export.txt" output.json

# Then edit make_standalone.py to read from output.json
```

#### Multiple Chats

```bash
# Chat 1
python parser.py "chat_person1.txt" chat.json
python make_standalone.py
mv whatsapp_viewer.html person1_chat.html

# Chat 2
python parser.py "chat_person2.txt" chat.json
python make_standalone.py
mv whatsapp_viewer.html person2_chat.html
```

#### Without Media

If you exported without media:
```bash
# You don't need the media/ folder
python parser.py "chat.txt" chat.json
python make_standalone.py
# Opens fine, just shows "Image not found" for missing media
```

---

## 🎨 Customization

### Change Your Name

**IMPORTANT:** To get the correct layout (your messages on right/green, their messages on left/gray), you need to set your name.

By default, messages from "You" appear on the right (green bubbles). Change this to match YOUR name as it appears in the WhatsApp chat export.

**How to find your name:**
1. Open your `chat.txt` file
2. Look at the sender names in the format: `DD/MM/YYYY, H:MM am - Your Name: message`
3. Copy your exact name (including any special characters, spaces, or parentheses)

**Option 1: Edit make_standalone.py (Before generating)**

Find this line (around line 338):
```javascript
currentUserName: 'You',  // Change this to your name!
```

Change to your EXACT name from the chat:
```javascript
currentUserName: 'Alice Smith',  // Example - use your actual name
```

Then run `python make_standalone.py` again.

**Option 2: Edit the Generated HTML (After generating)**

Open `whatsapp_viewer.html` in a text editor and find:
```javascript
const config = {
    currentUserName: 'You',  // Change this to your name!
```

Change `'You'` to your exact name from the chat and save.

**Examples:**
- If your name in chat is `Alice` → use `'Alice'`
- If your name in chat is `Alice Smith` → use `'Alice Smith'`
- If your name in chat is `Alice (Work)` → use `'Alice (Work)'`

**Result:**
- ✅ Your messages → Right side (green bubbles)
- ✅ Other person's messages → Left side (gray bubbles)

### Change Contact Name in Header

Edit `make_standalone.py`, find:
```html
<div class="contact-name">WhatsApp Chat</div>
```

Change to:
```html
<div class="contact-name">Contact Name</div>
```

### Modify Media Folder Path

If your media is in a different folder:

Edit the `mediaPath` in `make_standalone.py`:
```javascript
mediaPath: 'my_media_folder/'
```

### Change Theme Colors

Edit the CSS variables in `make_standalone.py`:
```css
:root {
    --bubble-outgoing: #005c4b;  /* Your message color */
    --bubble-incoming: #202c33;  /* Their message color */
    --bg-primary: #0b141a;       /* Background */
}
```

---

## 🔍 Troubleshooting

### Problem: "python: command not found"

**Solution:**
```bash
# Try python3 instead
python3 parser.py "chat.txt" chat.json

# Or install Python from python.org
```

### Problem: "chat.json not found"

**Solution:**
1. Make sure you ran `parser.py` first
2. Check you're in the correct folder
3. Verify `chat.json` exists: `ls` (Mac/Linux) or `dir` (Windows)

### Problem: All messages on the same side

**Solution:**
This means your `currentUserName` doesn't match your name in the chat file.

1. Open `chat.txt` and find a message you sent
2. Look at the format: `18/11/2025, 11:31 am - YOUR NAME HERE: message`
3. Copy your EXACT name (case-sensitive, with spaces and special characters)
4. Update `currentUserName` to match exactly

Example:
```javascript
// If chat shows: "18/11/2025, 11:31 am - Alice Smith: Hello"
currentUserName: 'Alice Smith',  // Must match exactly!

// NOT: 'alice smith' (wrong case)
// NOT: 'Alice' (missing last name)
```

### Problem: Images not showing

**Solution:**
1. ✅ Check `media/` folder exists next to the HTML file
2. ✅ Check image filenames match exactly (case-sensitive on Mac/Linux)
3. ✅ Verify images are actually in the `media/` folder

**Test:**
```bash
# Windows
dir media\

# Mac/Linux
ls media/
```

### Problem: Parser fails / encoding error

**Solution:**
The chat file might have unusual encoding. Try:
```bash
# The parser auto-detects encoding, but if it fails:
# 1. Open chat.txt in Notepad
# 2. Save As → Encoding: UTF-8
# 3. Run parser again
```

### Problem: HTML shows "Failed to load chat"

**Solution:**
This was the localhost issue. Use `make_standalone.py` - it embeds the data so no server is needed!

### Problem: Videos don't play

**Solution:**
- Browser compatibility varies
- MP4 files work best
- Try a different browser (Chrome recommended)

### Problem: Parsing gives wrong number of messages

**Solution:**
Check your chat file format:
```
18/11/2025, 11:31 am - Sender Name: Message text
```

If format is different (iOS exports differ), the parser may need adjustment.

---

## ❓ FAQ

### Q: Can I use this with iPhone WhatsApp exports?

**A:** This parser is designed for Android exports. iPhone exports have a slightly different format. You may need to adjust the timestamp regex in `parser.py`.

### Q: How do I get my messages on the right and theirs on the left?

**A:** You MUST set your name correctly in the config:
1. Open your `chat.txt` file
2. Find your exact name as it appears: `DD/MM/YYYY, H:MM am - YOUR NAME: message`
3. Set `currentUserName: 'YOUR NAME'` (must match exactly, including spaces/capitals)
4. Re-run `make_standalone.py` or edit the HTML directly

If all messages appear on the same side, your name doesn't match!

### Q: Is my data safe?

**A:** Yes! Everything runs locally on your computer. No data is uploaded anywhere. It's 100% offline.

### Q: Can I edit messages in the viewer?

**A:** No, this is a read-only viewer. To edit, modify the `chat.json` file or the original `.txt` file and re-parse.

### Q: How do I share this with someone?

**A:** Zip these files together:
```
my_chat.zip
├── whatsapp_viewer.html
└── media/
    └── (all images)
```

Send the zip file. They just unzip and double-click the HTML!

### Q: Can I view multiple chats in one HTML?

**A:** Not currently. Each chat needs its own HTML file. You can generate multiple viewers and rename them.

### Q: Does this work on mobile?

**A:** Yes! The design is responsive. Just open the HTML file in your mobile browser.

### Q: Can I print the chat?

**A:** Yes! Open the HTML and use your browser's print function (Ctrl+P / Cmd+P). You can save as PDF.

### Q: What if I have thousands of messages?

**A:** The viewer handles large chats well. Performance depends on your device. If very slow, consider splitting the chat.

### Q: Can I search messages?

**A:** Not yet! This is a potential future feature. For now, use your browser's search (Ctrl+F / Cmd+F).

### Q: Does this support group chats?

**A:** Yes! The parser detects multiple senders automatically.

### Q: What about deleted messages?

**A:** WhatsApp exports show "This message was deleted" - the parser includes these as regular text.

### Q: Can I customize the appearance?

**A:** Yes! See the [Customization](#customization) section above.

---

## 📝 WhatsApp Export Format Reference

### Expected Text File Format

```
16/11/2025, 9:13 am - Messages and calls are end-to-end encrypted...
18/11/2025, 11:31 am - Contact Name: IMG-20251118-WA0000.jpg (file attached)
18/11/2025, 11:32 am - Contact Name: This is a message
with multiple lines
that continues here
19/12/2025, 7:26 pm - Contact Name: Another message
```

### Key Format Rules

- **Timestamp:** `DD/MM/YYYY, H:MM am/pm`
- **Separator:** ` - ` (space-dash-space)
- **Sender:** `Name: ` (ends with colon and space)
- **Media:** `filename.jpg (file attached)`
- **Multiline:** Lines without timestamps continue previous message
- **System messages:** No sender name

---

## 🛠️ Advanced Features

### Running Without make_standalone.py

If you prefer the original multi-file approach:

1. Use `index.html`, `style.css`, `app.js` from artifacts #3, #4, #5
2. Run a local server:
   ```bash
   python -m http.server 8000
   ```
3. Open `http://localhost:8000`

This approach requires a server but keeps files separate for easier editing.

### Batch Processing Multiple Chats

Create a batch script:

**Windows (batch.bat):**
```batch
@echo off
for %%f in (*.txt) do (
    python parser.py "%%f" "%%~nf.json"
    python make_standalone.py "%%~nf.json" "%%~nf.html"
)
```

**Mac/Linux (batch.sh):**
```bash
#!/bin/bash
for file in *.txt; do
    python3 parser.py "$file" "${file%.txt}.json"
    python3 make_standalone.py "${file%.txt}.json" "${file%.txt}.html"
done
```

---

## 📊 Technical Details

### Parser Specifications

- **Language:** Python 3.6+
- **Dependencies:** None (uses only standard library)
- **Input:** WhatsApp Android .txt export
- **Output:** JSON array of message objects
- **Encoding:** UTF-8 with fallback to latin-1
- **Unicode handling:** Normalizes U+202F (narrow no-break space)

### Message Object Schema

```json
{
  "timestamp": "2025-11-18T11:31:00",
  "sender": "Contact Name",
  "type": "text|media|system",
  "text": "Message content",
  "media": "filename.jpg"
}
```

### Viewer Specifications

- **Frontend:** Vanilla JavaScript (no frameworks)
- **Styling:** Pure CSS (no preprocessors)
- **Dependencies:** None (100% standalone)
- **Browser Support:** All modern browsers (Chrome, Firefox, Safari, Edge)
- **Mobile Support:** Fully responsive

---

## 🤝 Contributing

Found a bug? Want to add a feature? Contributions welcome!

1. Fork the repository
2. Create your feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

MIT License - feel free to use, modify, and distribute!

---

## 🙏 Credits

Created with ❤️ for preserving your WhatsApp memories offline.

---

## 📞 Support

Having issues? Check the [Troubleshooting](#troubleshooting) section first!

For additional help:
1. Double-check you followed all steps
2. Verify your Python version: `python --version`
3. Check file locations and names
4. Review error messages carefully

---

## 🎯 Quick Command Reference

```bash
# Check Python installed
python --version

# Parse WhatsApp export
python parser.py "chat.txt" chat.json

# Generate standalone viewer
python make_standalone.py

# View statistics only
python parser.py "chat.txt" /dev/null  # Mac/Linux
python parser.py "chat.txt" NUL        # Windows

# Run local server (if needed)
python -m http.server 8000
```

---

**🎉 Enjoy your WhatsApp chat viewer!**

*Last updated: January 2026*