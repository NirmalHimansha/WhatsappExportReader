#!/usr/bin/env python3
"""
WhatsApp Standalone HTML Generator
Embeds chat.json data directly into index.html for offline viewing
No server required - just double-click the output HTML!
"""

import json
import sys
import os

def generate_standalone_html(chat_json_path='chat.json', output_path='whatsapp_viewer.html'):
    """Generate a standalone HTML file with embedded chat data"""
    
    # Read the chat.json file
    try:
        with open(chat_json_path, 'r', encoding='utf-8') as f:
            chat_data = json.load(f)
        print(f"✓ Loaded {len(chat_data)} messages from {chat_json_path}")
    except FileNotFoundError:
        print(f"❌ Error: {chat_json_path} not found!")
        print("   Make sure you've run parser.py first to generate chat.json")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {chat_json_path}")
        print(f"   {e}")
        sys.exit(1)
    
    # Convert chat data to JavaScript format
    chat_data_js = json.dumps(chat_data, indent=2, ensure_ascii=False)
    
    # HTML template with embedded data
    html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WhatsApp Chat Viewer</title>
    <style>
:root {
    --bg-primary: #0b141a;
    --bg-secondary: #202c33;
    --bg-tertiary: #111b21;
    --header-bg: #202c33;
    --footer-bg: #202c33;
    --bubble-incoming: #202c33;
    --bubble-outgoing: #005c4b;
    --bubble-system: rgba(255, 255, 255, 0.06);
    --text-primary: #e9edef;
    --text-secondary: #8696a0;
    --text-tertiary: #667781;
    --text-system: #8696a0;
    --accent-blue: #53bdeb;
    --spacing-xs: 4px;
    --spacing-sm: 8px;
    --spacing-md: 12px;
    --spacing-lg: 16px;
    --radius-sm: 4px;
    --radius-md: 8px;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Helvetica Neue", Arial, sans-serif;
    background-color: var(--bg-primary);
    color: var(--text-primary);
    overflow: hidden;
    height: 100vh;
}

.chat-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
    max-width: 100%;
    margin: 0 auto;
    background-color: var(--bg-tertiary);
}

.chat-header {
    background-color: var(--header-bg);
    padding: var(--spacing-sm) var(--spacing-lg);
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    flex-shrink: 0;
}

.header-content {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
}

.contact-info {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
    flex: 1;
}

.contact-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
}

.contact-name {
    font-size: 16px;
    font-weight: 500;
    color: var(--text-primary);
}

.contact-status {
    font-size: 13px;
    color: var(--text-secondary);
}

.chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: var(--spacing-lg);
    background-image: repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(255, 255, 255, 0.01) 10px, rgba(255, 255, 255, 0.01) 20px);
    background-color: var(--bg-primary);
}

.chat-messages::-webkit-scrollbar { width: 6px; }
.chat-messages::-webkit-scrollbar-track { background: transparent; }
.chat-messages::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.1); border-radius: 3px; }

.loading {
    text-align: center;
    color: var(--text-secondary);
    padding: var(--spacing-lg);
}

.date-separator {
    text-align: center;
    margin: var(--spacing-lg) 0;
}

.date-separator span {
    display: inline-block;
    background-color: var(--bubble-system);
    color: var(--text-system);
    padding: 6px 12px;
    border-radius: var(--radius-md);
    font-size: 12px;
    font-weight: 500;
    box-shadow: 0 1px 1px rgba(0, 0, 0, 0.15);
}

.message-system {
    text-align: center;
    margin: var(--spacing-md) 0;
}

.system-content {
    display: inline-block;
    background-color: var(--bubble-system);
    color: var(--text-system);
    padding: 8px 12px;
    border-radius: var(--radius-md);
    font-size: 13px;
    max-width: 80%;
    box-shadow: 0 1px 1px rgba(0, 0, 0, 0.15);
}

.message {
    display: flex;
    margin-bottom: var(--spacing-sm);
    animation: messageSlide 0.2s ease-out;
}

@keyframes messageSlide {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.message.incoming { justify-content: flex-start; }
.message.outgoing { justify-content: flex-end; }

.message-bubble {
    max-width: 65%;
    min-width: 100px;
    padding: 6px 9px 8px;
    border-radius: var(--radius-md);
    box-shadow: 0 1px 1px rgba(0, 0, 0, 0.15);
    word-wrap: break-word;
}

.message.incoming .message-bubble {
    background-color: var(--bubble-incoming);
    border-top-left-radius: var(--radius-sm);
}

.message.outgoing .message-bubble {
    background-color: var(--bubble-outgoing);
    border-top-right-radius: var(--radius-sm);
}

.message-sender {
    font-size: 13px;
    font-weight: 500;
    color: var(--accent-blue);
    margin-bottom: 4px;
}

.message-text {
    font-size: 14px;
    line-height: 1.4;
    color: var(--text-primary);
    white-space: pre-wrap;
    word-wrap: break-word;
}

.message-time {
    font-size: 11px;
    color: var(--text-tertiary);
    text-align: right;
    margin-top: 4px;
}

.message.outgoing .message-time {
    color: rgba(255, 255, 255, 0.5);
}

.message-media {
    margin-bottom: 6px;
    border-radius: var(--radius-md);
    overflow: hidden;
    cursor: pointer;
    position: relative;
}

.message-media img, .message-media video {
    display: block;
    max-width: 100%;
    height: auto;
    border-radius: var(--radius-md);
}

.video-overlay {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 60px;
    height: 60px;
    background-color: rgba(0, 0, 0, 0.5);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    pointer-events: none;
}

.video-overlay::after {
    content: '';
    width: 0;
    height: 0;
    border-style: solid;
    border-width: 12px 0 12px 20px;
    border-color: transparent transparent transparent white;
    margin-left: 4px;
}

.audio-player {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
    padding: var(--spacing-sm);
    background-color: rgba(0, 0, 0, 0.1);
    border-radius: var(--radius-md);
    margin-bottom: 6px;
}

.audio-player audio {
    flex: 1;
    height: 32px;
}

.media-not-found {
    padding: var(--spacing-md);
    background-color: rgba(0, 0, 0, 0.1);
    border-radius: var(--radius-md);
    text-align: center;
    color: var(--text-secondary);
    font-size: 13px;
    margin-bottom: 6px;
}

.chat-footer {
    background-color: var(--footer-bg);
    padding: var(--spacing-md) var(--spacing-lg);
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    text-align: center;
    flex-shrink: 0;
}

.footer-text {
    font-size: 13px;
    color: var(--text-secondary);
}

.lightbox {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.95);
    z-index: 1000;
    align-items: center;
    justify-content: center;
}

.lightbox.active { display: flex; }

.lightbox-content {
    position: relative;
    max-width: 90%;
    max-height: 90%;
}

.lightbox-close {
    position: absolute;
    top: -40px;
    right: 0;
    background: none;
    border: none;
    color: white;
    font-size: 40px;
    cursor: pointer;
    width: 40px;
    height: 40px;
    opacity: 0.8;
}

.lightbox-close:hover { opacity: 1; }

.lightbox-content img, .lightbox-content video {
    max-width: 100%;
    max-height: 80vh;
    display: block;
    border-radius: var(--radius-sm);
}

#lightboxVideo { display: none; }

@media (max-width: 768px) {
    .chat-messages { padding: var(--spacing-sm); }
    .message-bubble { max-width: 80%; }
}

@media (min-width: 769px) {
    .chat-container {
        max-width: 1000px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
}
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <div class="header-content">
                <div class="contact-info">
                    <div class="contact-avatar">💬</div>
                    <div>
                        <div class="contact-name">WhatsApp Chat</div>
                        <div class="contact-status">Offline viewer - Double-click to open</div>
                    </div>
                </div>
            </div>
        </div>

        <div class="chat-messages" id="chatMessages">
            <div class="loading">Loading chat...</div>
        </div>

        <div class="chat-footer">
            <p class="footer-text">This is an offline viewer. No messages can be sent.</p>
        </div>
    </div>

    <div class="lightbox" id="lightbox">
        <div class="lightbox-content">
            <button class="lightbox-close" id="lightboxClose">&times;</button>
            <img id="lightboxImage" src="" alt="">
            <video id="lightboxVideo" controls></video>
        </div>
    </div>

    <script>
const CHAT_DATA = ''' + chat_data_js + ''';

class WhatsAppChatViewer {
    constructor(config = {}) {
        this.currentUserName = config.currentUserName || 'You';
        this.mediaPath = config.mediaPath || 'media/';
        this.messagesContainer = document.getElementById('chatMessages');
        this.lightbox = document.getElementById('lightbox');
        this.lightboxImage = document.getElementById('lightboxImage');
        this.lightboxVideo = document.getElementById('lightboxVideo');
        this.lightboxClose = document.getElementById('lightboxClose');
        this.messages = CHAT_DATA;
        this.lastDate = null;
        this.init();
    }
    
    init() {
        try {
            this.renderMessages();
            this.scrollToBottom();
            this.setupEventListeners();
        } catch (error) {
            console.error('Failed to initialize:', error);
            this.showError('Failed to load chat data.');
        }
    }
    
    renderMessages() {
        this.messagesContainer.innerHTML = '';
        this.messages.forEach((message) => {
            this.renderMessage(message);
        });
    }
    
    renderMessage(message) {
        const messageDate = this.parseDate(message.timestamp);
        if (this.shouldShowDateSeparator(messageDate)) {
            this.addDateSeparator(messageDate);
            this.lastDate = messageDate;
        }
        
        switch (message.type) {
            case 'system':
                this.renderSystemMessage(message);
                break;
            case 'text':
            case 'media':
                this.renderChatMessage(message);
                break;
        }
    }
    
    shouldShowDateSeparator(currentDate) {
        if (!this.lastDate) return true;
        return currentDate.getFullYear() !== this.lastDate.getFullYear() ||
               currentDate.getMonth() !== this.lastDate.getMonth() ||
               currentDate.getDate() !== this.lastDate.getDate();
    }
    
    addDateSeparator(date) {
        const separator = document.createElement('div');
        separator.className = 'date-separator';
        const dateText = this.formatDateSeparator(date);
        separator.innerHTML = `<span>${dateText}</span>`;
        this.messagesContainer.appendChild(separator);
    }
    
    renderSystemMessage(message) {
        const systemMsg = document.createElement('div');
        systemMsg.className = 'message-system';
        systemMsg.innerHTML = `<div class="system-content">${this.escapeHtml(message.text)}</div>`;
        this.messagesContainer.appendChild(systemMsg);
    }
    
    renderChatMessage(message) {
        const messageDiv = document.createElement('div');
        const isOutgoing = message.sender === this.currentUserName;
        messageDiv.className = `message ${isOutgoing ? 'outgoing' : 'incoming'}`;
        
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        
        let bubbleContent = '';
        if (!isOutgoing && message.sender) {
            bubbleContent += `<div class="message-sender">${this.escapeHtml(message.sender)}</div>`;
        }
        if (message.media) {
            bubbleContent += this.renderMedia(message.media);
        }
        if (message.text) {
            bubbleContent += `<div class="message-text">${this.escapeHtml(message.text)}</div>`;
        }
        
        const time = this.formatTime(message.timestamp);
        bubbleContent += `<div class="message-time">${time}</div>`;
        
        bubble.innerHTML = bubbleContent;
        messageDiv.appendChild(bubble);
        this.messagesContainer.appendChild(messageDiv);
    }
    
    renderMedia(mediaFilename) {
        const mediaUrl = this.mediaPath + mediaFilename;
        const extension = this.getFileExtension(mediaFilename).toLowerCase();
        
        if (['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(extension)) {
            return `<div class="message-media" data-media="${mediaUrl}" data-type="image">
                <img src="${mediaUrl}" alt="Media" loading="lazy" 
                     onerror="this.parentElement.innerHTML='<div class=\\'media-not-found\\'>📷 Image not found: ${this.escapeHtml(mediaFilename)}</div>'">
            </div>`;
        }
        
        if (['mp4', 'avi', 'mov', 'webm'].includes(extension)) {
            return `<div class="message-media" data-media="${mediaUrl}" data-type="video">
                <video src="${mediaUrl}" onerror="this.parentElement.innerHTML='<div class=\\'media-not-found\\'>🎥 Video not found</div>'"></video>
                <div class="video-overlay"></div>
            </div>`;
        }
        
        if (['opus', 'mp3', 'm4a', 'ogg', 'wav'].includes(extension)) {
            return `<div class="audio-player">
                <audio controls src="${mediaUrl}">Your browser does not support audio.</audio>
            </div>`;
        }
        
        return `<div class="media-not-found">📎 File: ${this.escapeHtml(mediaFilename)}</div>`;
    }
    
    setupEventListeners() {
        this.messagesContainer.addEventListener('click', (e) => {
            const mediaElement = e.target.closest('.message-media');
            if (mediaElement) {
                const mediaUrl = mediaElement.dataset.media;
                const mediaType = mediaElement.dataset.type;
                this.openLightbox(mediaUrl, mediaType);
            }
        });
        
        this.lightboxClose.addEventListener('click', () => this.closeLightbox());
        this.lightbox.addEventListener('click', (e) => {
            if (e.target === this.lightbox) this.closeLightbox();
        });
        
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.lightbox.classList.contains('active')) {
                this.closeLightbox();
            }
        });
    }
    
    openLightbox(mediaUrl, mediaType) {
        this.lightbox.classList.add('active');
        if (mediaType === 'image') {
            this.lightboxImage.src = mediaUrl;
            this.lightboxImage.style.display = 'block';
            this.lightboxVideo.style.display = 'none';
        } else if (mediaType === 'video') {
            this.lightboxVideo.src = mediaUrl;
            this.lightboxVideo.style.display = 'block';
            this.lightboxImage.style.display = 'none';
        }
    }
    
    closeLightbox() {
        this.lightbox.classList.remove('active');
        this.lightboxImage.src = '';
        this.lightboxVideo.src = '';
        this.lightboxVideo.pause();
    }
    
    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
    
    showError(message) {
        this.messagesContainer.innerHTML = `<div class="loading" style="color: #ff4444;">⚠️ ${message}</div>`;
    }
    
    parseDate(timestamp) {
        return new Date(timestamp);
    }
    
    formatDateSeparator(date) {
        const today = new Date();
        const yesterday = new Date(today);
        yesterday.setDate(yesterday.getDate() - 1);
        
        if (this.isSameDay(date, today)) return 'TODAY';
        if (this.isSameDay(date, yesterday)) return 'YESTERDAY';
        
        const options = { month: 'long', day: 'numeric', year: 'numeric' };
        return date.toLocaleDateString('en-US', options).toUpperCase();
    }
    
    isSameDay(date1, date2) {
        return date1.getFullYear() === date2.getFullYear() &&
               date1.getMonth() === date2.getMonth() &&
               date1.getDate() === date2.getDate();
    }
    
    formatTime(timestamp) {
        const date = this.parseDate(timestamp);
        if (isNaN(date.getTime())) return 'Invalid time';
        
        let hours = date.getHours();
        const minutes = date.getMinutes();
        const ampm = hours >= 12 ? 'PM' : 'AM';
        hours = hours % 12;
        hours = hours ? hours : 12;
        const minutesStr = minutes < 10 ? '0' + minutes : minutes;
        return `${hours}:${minutesStr} ${ampm}`;
    }
    
    getFileExtension(filename) {
        const parts = filename.split('.');
        return parts.length > 1 ? parts.pop() : '';
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // IMPORTANT: Change 'You' to YOUR name as it appears in the chat
    // This determines which messages go on the right (green) side
    const config = {
        currentUserName: 'You',  // Change this to your name!
        mediaPath: 'media/'
    };
    new WhatsAppChatViewer(config);
});
    </script>
</body>
</html>
'''
    
    # Write the output HTML file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_template)
        print(f"✓ Generated standalone HTML: {output_path}")
        print(f"\n🎉 Success! You can now:")
        print(f"   1. Double-click '{output_path}' to open it")
        print(f"   2. No server needed!")
        print(f"   3. Make sure 'media/' folder is in the same directory")
        print(f"\n💡 Tip: You can rename the file or move it anywhere (keep media/ folder with it)")
    except Exception as e:
        print(f"❌ Error writing output file: {e}")
        sys.exit(1)


def main():
    print("=" * 60)
    print("WhatsApp Standalone HTML Generator")
    print("=" * 60)
    print()
    
    # Check if chat.json exists
    if not os.path.exists('chat.json'):
        print("❌ chat.json not found!")
        print("\n📋 Steps to fix:")
        print("   1. Make sure you're in the correct folder")
        print("   2. Run parser.py first to generate chat.json:")
        print("      python parser.py chat.txt chat.json")
        print()
        sys.exit(1)
    
    # Generate the standalone HTML
    output_filename = 'whatsapp_viewer.html'
    generate_standalone_html('chat.json', output_filename)
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    main()