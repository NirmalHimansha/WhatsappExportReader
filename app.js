/**
 * WhatsApp Chat Viewer
 * Renders chat.json into WhatsApp-style interface
 * Handles media, date separators, system messages, and multiline text
 */

class WhatsAppChatViewer {
    constructor(config = {}) {
        // Configuration
        this.currentUserName = config.currentUserName || 'You';
        this.chatJsonPath = config.chatJsonPath || 'chat.json';
        this.mediaPath = config.mediaPath || 'media/';
        
        // DOM elements
        this.messagesContainer = document.getElementById('chatMessages');
        this.lightbox = document.getElementById('lightbox');
        this.lightboxImage = document.getElementById('lightboxImage');
        this.lightboxVideo = document.getElementById('lightboxVideo');
        this.lightboxClose = document.getElementById('lightboxClose');
        
        // State
        this.messages = [];
        this.lastDate = null;
        
        // Initialize
        this.init();
    }
    
    async init() {
        try {
            // Load chat data
            await this.loadChat();
            
            // Render messages
            this.renderMessages();
            
            // Scroll to bottom
            this.scrollToBottom();
            
            // Setup event listeners
            this.setupEventListeners();
            
        } catch (error) {
            console.error('Failed to initialize chat viewer:', error);
            this.showError('Failed to load chat. Please ensure chat.json exists.');
        }
    }
    
    async loadChat() {
        try {
            const response = await fetch(this.chatJsonPath);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            this.messages = await response.json();
        } catch (error) {
            console.error('Error loading chat:', error);
            throw error;
        }
    }
    
    renderMessages() {
        // Clear loading message
        this.messagesContainer.innerHTML = '';
        
        // Render each message
        this.messages.forEach((message, index) => {
            this.renderMessage(message, index);
        });
    }
    
    renderMessage(message, index) {
        const messageDate = this.parseDate(message.timestamp);
        
        // Add date separator if date changed
        if (this.shouldShowDateSeparator(messageDate)) {
            this.addDateSeparator(messageDate);
            this.lastDate = messageDate;
        }
        
        // Render based on message type
        switch (message.type) {
            case 'system':
                this.renderSystemMessage(message);
                break;
            case 'text':
            case 'media':
                this.renderChatMessage(message);
                break;
            default:
                console.warn('Unknown message type:', message.type);
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
        
        systemMsg.innerHTML = `
            <div class="system-content">${this.escapeHtml(message.text)}</div>
        `;
        
        this.messagesContainer.appendChild(systemMsg);
    }
    
    renderChatMessage(message) {
        const messageDiv = document.createElement('div');
        
        // Determine if incoming or outgoing
        const isOutgoing = message.sender === this.currentUserName;
        messageDiv.className = `message ${isOutgoing ? 'outgoing' : 'incoming'}`;
        
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        
        let bubbleContent = '';
        
        // Add sender name for incoming messages
        if (!isOutgoing && message.sender) {
            bubbleContent += `<div class="message-sender">${this.escapeHtml(message.sender)}</div>`;
        }
        
        // Add media if present
        if (message.media) {
            bubbleContent += this.renderMedia(message.media);
        }
        
        // Add text if present
        if (message.text) {
            bubbleContent += `<div class="message-text">${this.escapeHtml(message.text)}</div>`;
        }
        
        // Add timestamp
        const time = this.formatTime(message.timestamp);
        bubbleContent += `<div class="message-time">${time}</div>`;
        
        bubble.innerHTML = bubbleContent;
        messageDiv.appendChild(bubble);
        this.messagesContainer.appendChild(messageDiv);
    }
    
    renderMedia(mediaFilename) {
        const mediaUrl = this.mediaPath + mediaFilename;
        const extension = this.getFileExtension(mediaFilename).toLowerCase();
        
        // Image formats
        if (['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(extension)) {
            return `
                <div class="message-media" data-media="${mediaUrl}" data-type="image">
                    <img src="${mediaUrl}" alt="Media" loading="lazy" 
                         onerror="this.parentElement.innerHTML='<div class=\\'media-not-found\\'>📷 Image not found: ${this.escapeHtml(mediaFilename)}</div>'">
                </div>
            `;
        }
        
        // Video formats
        if (['mp4', 'avi', 'mov', 'webm'].includes(extension)) {
            return `
                <div class="message-media" data-media="${mediaUrl}" data-type="video">
                    <video src="${mediaUrl}" 
                           onerror="this.parentElement.innerHTML='<div class=\\'media-not-found\\'>🎥 Video not found: ${this.escapeHtml(mediaFilename)}</div>'">
                    </video>
                    <div class="video-overlay"></div>
                </div>
            `;
        }
        
        // Audio formats
        if (['opus', 'mp3', 'm4a', 'ogg', 'wav'].includes(extension)) {
            return `
                <div class="audio-player">
                    <audio controls src="${mediaUrl}"
                           onerror="this.parentElement.innerHTML='<div class=\\'media-not-found\\'>🔊 Audio not found: ${this.escapeHtml(mediaFilename)}</div>'">
                        Your browser does not support audio playback.
                    </audio>
                </div>
            `;
        }
        
        // Other files
        return `
            <div class="media-not-found">
                📎 File: ${this.escapeHtml(mediaFilename)}
            </div>
        `;
    }
    
    setupEventListeners() {
        // Media click handler - event delegation
        this.messagesContainer.addEventListener('click', (e) => {
            const mediaElement = e.target.closest('.message-media');
            if (mediaElement) {
                const mediaUrl = mediaElement.dataset.media;
                const mediaType = mediaElement.dataset.type;
                this.openLightbox(mediaUrl, mediaType);
            }
        });
        
        // Lightbox close handlers
        this.lightboxClose.addEventListener('click', () => this.closeLightbox());
        this.lightbox.addEventListener('click', (e) => {
            if (e.target === this.lightbox) {
                this.closeLightbox();
            }
        });
        
        // Keyboard handler for lightbox
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
        this.messagesContainer.innerHTML = `
            <div class="loading" style="color: #ff4444;">
                ⚠️ ${message}
            </div>
        `;
    }
    
    // Utility methods
    
    parseDate(timestamp) {
        // Handle both ISO format and Date parseable strings
        return new Date(timestamp);
    }
    
    formatDateSeparator(date) {
        const today = new Date();
        const yesterday = new Date(today);
        yesterday.setDate(yesterday.getDate() - 1);
        
        // Check if today
        if (this.isSameDay(date, today)) {
            return 'TODAY';
        }
        
        // Check if yesterday
        if (this.isSameDay(date, yesterday)) {
            return 'YESTERDAY';
        }
        
        // Format as "MONTH DAY, YEAR"
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
        
        if (isNaN(date.getTime())) {
            return 'Invalid time';
        }
        
        let hours = date.getHours();
        const minutes = date.getMinutes();
        const ampm = hours >= 12 ? 'PM' : 'AM';
        
        hours = hours % 12;
        hours = hours ? hours : 12; // 0 should be 12
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

// Initialize the viewer when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Configuration options
    const config = {
        currentUserName: 'You', // Change this to match your name in the chat
        chatJsonPath: 'chat.json',
        mediaPath: 'media/'
    };
    
    // Create viewer instance
    new WhatsAppChatViewer(config);
});