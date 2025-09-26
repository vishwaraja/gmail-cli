"""
Gmail Client - Core Gmail operations
"""

import base64
import email
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Dict, Optional, Any
from datetime import datetime
import re
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel

console = Console()


class GmailClient:
    """Main Gmail client for performing operations"""
    
    def __init__(self, service):
        self.service = service
    
    def list_messages(self, query: str = '', max_results: int = 10, label_ids: List[str] = None) -> List[Dict]:
        """
        List messages from Gmail
        
        Args:
            query: Gmail search query
            max_results: Maximum number of results to return
            label_ids: List of label IDs to filter by
            
        Returns:
            List of message metadata
        """
        try:
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results,
                labelIds=label_ids
            ).execute()
            
            messages = results.get('messages', [])
            return messages
        except Exception as e:
            console.print(f"[red]❌ Error listing messages: {e}[/red]")
            return []
    
    def get_message(self, message_id: str) -> Optional[Dict]:
        """
        Get full message details
        
        Args:
            message_id: Gmail message ID
            
        Returns:
            Message details or None if error
        """
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            return message
        except Exception as e:
            console.print(f"[red]❌ Error getting message: {e}[/red]")
            return None
    
    def get_message_content(self, message: Dict) -> Dict[str, Any]:
        """
        Extract readable content from Gmail message
        
        Args:
            message: Gmail message object
            
        Returns:
            Dictionary with parsed message content
        """
        payload = message.get('payload', {})
        headers = payload.get('headers', [])
        
        # Extract headers
        header_dict = {h['name'].lower(): h['value'] for h in headers}
        
        # Extract body
        body = self._extract_body(payload)
        
        # Extract attachments info
        attachments = self._extract_attachments(payload)
        
        return {
            'id': message['id'],
            'thread_id': message['threadId'],
            'subject': header_dict.get('subject', 'No Subject'),
            'from': header_dict.get('from', 'Unknown'),
            'to': header_dict.get('to', 'Unknown'),
            'date': header_dict.get('date', 'Unknown'),
            'body': body,
            'attachments': attachments,
            'labels': message.get('labelIds', [])
        }
    
    def _extract_body(self, payload: Dict) -> str:
        """Extract message body from payload"""
        body = ""
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data', '')
                    if data:
                        body = base64.urlsafe_b64decode(data).decode('utf-8')
                        break
                elif part['mimeType'] == 'text/html' and not body:
                    data = part['body'].get('data', '')
                    if data:
                        body = base64.urlsafe_b64decode(data).decode('utf-8')
        else:
            if payload['mimeType'] == 'text/plain':
                data = payload['body'].get('data', '')
                if data:
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
        
        return body
    
    def _extract_attachments(self, payload: Dict) -> List[Dict]:
        """Extract attachment information from payload"""
        attachments = []
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part.get('filename'):
                    attachments.append({
                        'filename': part['filename'],
                        'mime_type': part['mimeType'],
                        'size': part['body'].get('size', 0),
                        'attachment_id': part['body'].get('attachmentId')
                    })
        
        return attachments
    
    def send_message(self, to: str, subject: str, body: str, 
                    cc: str = None, bcc: str = None, 
                    attachments: List[str] = None) -> bool:
        """
        Send an email message
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body
            cc: CC recipients (comma-separated)
            bcc: BCC recipients (comma-separated)
            attachments: List of file paths to attach
            
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            # Create message
            message = MIMEMultipart()
            message['to'] = to
            message['subject'] = subject
            
            if cc:
                message['cc'] = cc
            if bcc:
                message['bcc'] = bcc
            
            # Add body
            message.attach(MIMEText(body, 'plain'))
            
            # Add attachments
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        with open(file_path, "rb") as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                        
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {os.path.basename(file_path)}'
                        )
                        message.attach(part)
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            # Send message
            send_message = self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            console.print(f"[green]✅ Message sent successfully! Message ID: {send_message['id']}[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Error sending message: {e}[/red]")
            return False
    
    def search_messages(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Search messages using Gmail search syntax
        
        Args:
            query: Gmail search query
            max_results: Maximum number of results
            
        Returns:
            List of matching messages
        """
        return self.list_messages(query=query, max_results=max_results)
    
    def get_labels(self) -> List[Dict]:
        """
        Get all Gmail labels
        
        Returns:
            List of label information
        """
        try:
            results = self.service.users().labels().list(userId='me').execute()
            labels = results.get('labels', [])
            return labels
        except Exception as e:
            console.print(f"[red]❌ Error getting labels: {e}[/red]")
            return []
    
    def mark_as_read(self, message_id: str) -> bool:
        """
        Mark a message as read
        
        Args:
            message_id: Gmail message ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            return True
        except Exception as e:
            console.print(f"[red]❌ Error marking message as read: {e}[/red]")
            return False
    
    def mark_as_unread(self, message_id: str) -> bool:
        """
        Mark a message as unread
        
        Args:
            message_id: Gmail message ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'addLabelIds': ['UNREAD']}
            ).execute()
            return True
        except Exception as e:
            console.print(f"[red]❌ Error marking message as unread: {e}[/red]")
            return False
    
    def delete_message(self, message_id: str) -> bool:
        """
        Delete a message
        
        Args:
            message_id: Gmail message ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.service.users().messages().delete(
                userId='me',
                id=message_id
            ).execute()
            console.print(f"[green]✅ Message deleted successfully[/green]")
            return True
        except Exception as e:
            console.print(f"[red]❌ Error deleting message: {e}[/red]")
            return False
