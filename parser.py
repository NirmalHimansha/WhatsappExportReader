#!/usr/bin/env python3
"""
WhatsApp Chat Export Parser
Converts WhatsApp Android .txt exports to structured JSON
Handles multiline messages, media attachments, system messages, and Unicode normalization
"""

import re
import json
import unicodedata
from datetime import datetime
from typing import List, Dict, Optional

class WhatsAppParser:
    # Timestamp pattern: DD/MM/YYYY, H:MM am|pm
    # Must account for optional Unicode spaces before am/pm
    TIMESTAMP_PATTERN = re.compile(
        r'^(\d{1,2}/\d{1,2}/\d{4}),\s+(\d{1,2}:\d{2})\s*([ap]m)\s*-\s*(.*)$',
        re.IGNORECASE
    )
    
    # Media attachment patterns
    MEDIA_PATTERN = re.compile(r'(.*?)\s*\(file attached\)\s*$', re.IGNORECASE)
    
    def __init__(self, chat_file: str):
        self.chat_file = chat_file
        self.messages: List[Dict] = []
        self.current_message: Optional[Dict] = None
    
    def normalize_text(self, text: str) -> str:
        """Normalize Unicode characters, especially U+202F (narrow no-break space)"""
        # Replace U+202F and other non-breaking spaces with regular space
        text = text.replace('\u202f', ' ')
        text = text.replace('\xa0', ' ')
        # Normalize Unicode to NFC form
        text = unicodedata.normalize('NFC', text)
        return text.strip()
    
    def parse_timestamp(self, date_str: str, time_str: str, period: str) -> str:
        """Convert DD/MM/YYYY, H:MM am/pm to ISO-8601 timestamp"""
        try:
            # Parse date
            day, month, year = map(int, date_str.split('/'))
            
            # Parse time
            hour, minute = map(int, time_str.split(':'))
            
            # Convert to 24-hour format
            period = period.lower()
            if period == 'pm' and hour != 12:
                hour += 12
            elif period == 'am' and hour == 12:
                hour = 0
            
            # Create datetime and convert to ISO format
            dt = datetime(year, month, day, hour, minute, 0)
            return dt.isoformat()
        except (ValueError, IndexError) as e:
            # Fallback for malformed timestamps
            return f"Invalid timestamp: {date_str} {time_str} {period}"
    
    def extract_media(self, text: str) -> tuple[str, Optional[str]]:
        """
        Extract media filename from message text
        Returns: (remaining_text, media_filename)
        """
        match = self.MEDIA_PATTERN.match(text)
        if match:
            media_filename = match.group(1).strip()
            # Check if it's a valid media file
            if any(media_filename.lower().endswith(ext) for ext in 
                   ['.jpg', '.jpeg', '.png', '.webp', '.gif', '.mp4', 
                    '.avi', '.mov', '.opus', '.mp3', '.m4a', '.pdf', '.doc', '.docx']):
                return '', media_filename
        return text, None
    
    def is_system_message(self, sender_and_text: str) -> tuple[bool, str]:
        """
        Detect system messages (no sender name with colon)
        System messages don't have a "Sender: " format
        """
        # If there's no colon, it's likely a system message
        if ':' not in sender_and_text:
            return True, sender_and_text.strip()
        
        # Check for common system message patterns
        system_patterns = [
            'Messages and calls are end-to-end encrypted',
            'created group',
            'added',
            'removed',
            'left',
            'changed the subject',
            'changed this group\'s icon',
            'You deleted this message',
            'This message was deleted',
        ]
        
        for pattern in system_patterns:
            if pattern.lower() in sender_and_text.lower():
                return True, sender_and_text.strip()
        
        return False, sender_and_text
    
    def parse_message_line(self, sender_and_text: str) -> tuple[Optional[str], str, str, Optional[str]]:
        """
        Parse sender and message content
        Returns: (sender, message_type, text, media_filename)
        """
        # Check if system message
        is_system, text = self.is_system_message(sender_and_text)
        
        if is_system:
            return None, 'system', text, None
        
        # Split sender and text
        if ':' in sender_and_text:
            sender, text = sender_and_text.split(':', 1)
            sender = sender.strip()
            text = text.strip()
        else:
            # Edge case: no colon found
            return None, 'system', sender_and_text.strip(), None
        
        # Check for media
        text, media = self.extract_media(text)
        
        if media:
            return sender, 'media', text, media
        elif text:
            return sender, 'text', text, None
        else:
            # Empty message - will be filtered out
            return sender, 'empty', '', None
    
    def finalize_current_message(self):
        """Add current message to messages list if valid"""
        if self.current_message and self.current_message['type'] != 'empty':
            # Clean up empty text for media-only messages
            if self.current_message['type'] == 'media' and not self.current_message['text']:
                self.current_message['text'] = ''
            self.messages.append(self.current_message)
        self.current_message = None
    
    def parse(self) -> List[Dict]:
        """Parse the WhatsApp chat file"""
        try:
            with open(self.chat_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(self.chat_file, 'r', encoding='latin-1') as f:
                lines = f.readlines()
        
        for line in lines:
            # Normalize Unicode
            line = self.normalize_text(line)
            
            # Skip completely empty lines
            if not line:
                continue
            
            # Try to match timestamp pattern
            match = self.TIMESTAMP_PATTERN.match(line)
            
            if match:
                # Finalize previous message
                self.finalize_current_message()
                
                # Extract components
                date_str = match.group(1)
                time_str = match.group(2)
                period = match.group(3)
                sender_and_text = match.group(4)
                
                # Parse timestamp
                timestamp = self.parse_timestamp(date_str, time_str, period)
                
                # Parse message content
                sender, msg_type, text, media = self.parse_message_line(sender_and_text)
                
                # Create new message
                self.current_message = {
                    'timestamp': timestamp,
                    'sender': sender,
                    'type': msg_type,
                    'text': text,
                    'media': media
                }
            else:
                # Continuation of previous message (multiline)
                if self.current_message:
                    # Append to existing text with newline
                    if self.current_message['text']:
                        self.current_message['text'] += '\n' + line
                    else:
                        self.current_message['text'] = line
        
        # Finalize last message
        self.finalize_current_message()
        
        return self.messages
    
    def save_json(self, output_file: str):
        """Save parsed messages to JSON file"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.messages, f, ensure_ascii=False, indent=2)
        print(f"✓ Parsed {len(self.messages)} messages")
        print(f"✓ Saved to {output_file}")


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python parser.py <chat_file.txt> [output.json]")
        print("\nExample:")
        print("  python parser.py chat.txt chat.json")
        sys.exit(1)
    
    chat_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'chat.json'
    
    parser = WhatsAppParser(chat_file)
    messages = parser.parse()
    parser.save_json(output_file)
    
    # Print statistics
    print(f"\nStatistics:")
    print(f"  Text messages: {sum(1 for m in messages if m['type'] == 'text')}")
    print(f"  Media messages: {sum(1 for m in messages if m['type'] == 'media')}")
    print(f"  System messages: {sum(1 for m in messages if m['type'] == 'system')}")


if __name__ == '__main__':
    main()