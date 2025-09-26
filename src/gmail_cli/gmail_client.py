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
    
    # ==================== DRAFTS API ====================
    
    def create_draft(self, to: str, subject: str, body: str, 
                    cc: str = None, bcc: str = None, 
                    attachments: List[str] = None) -> Optional[str]:
        """
        Create a draft message
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body
            cc: CC recipients (comma-separated)
            bcc: BCC recipients (comma-separated)
            attachments: List of file paths to attach
            
        Returns:
            Draft ID if successful, None otherwise
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
            
            # Create draft
            draft = self.service.users().drafts().create(
                userId='me',
                body={'message': {'raw': raw_message}}
            ).execute()
            
            console.print(f"[green]✅ Draft created successfully! Draft ID: {draft['id']}[/green]")
            return draft['id']
            
        except Exception as e:
            console.print(f"[red]❌ Error creating draft: {e}[/red]")
            return None
    
    def list_drafts(self, max_results: int = 10) -> List[Dict]:
        """
        List draft messages
        
        Args:
            max_results: Maximum number of drafts to return
            
        Returns:
            List of draft metadata
        """
        try:
            results = self.service.users().drafts().list(
                userId='me',
                maxResults=max_results
            ).execute()
            
            drafts = results.get('drafts', [])
            return drafts
        except Exception as e:
            console.print(f"[red]❌ Error listing drafts: {e}[/red]")
            return []
    
    def get_draft(self, draft_id: str) -> Optional[Dict]:
        """
        Get full draft details
        
        Args:
            draft_id: Gmail draft ID
            
        Returns:
            Draft details or None if error
        """
        try:
            draft = self.service.users().drafts().get(
                userId='me',
                id=draft_id,
                format='full'
            ).execute()
            return draft
        except Exception as e:
            console.print(f"[red]❌ Error getting draft: {e}[/red]")
            return None
    
    def update_draft(self, draft_id: str, to: str, subject: str, body: str,
                    cc: str = None, bcc: str = None, 
                    attachments: List[str] = None) -> bool:
        """
        Update a draft message
        
        Args:
            draft_id: Gmail draft ID
            to: Recipient email address
            subject: Email subject
            body: Email body
            cc: CC recipients (comma-separated)
            bcc: BCC recipients (comma-separated)
            attachments: List of file paths to attach
            
        Returns:
            True if successful, False otherwise
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
            
            # Update draft
            self.service.users().drafts().update(
                userId='me',
                id=draft_id,
                body={'message': {'raw': raw_message}}
            ).execute()
            
            console.print(f"[green]✅ Draft updated successfully![/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Error updating draft: {e}[/red]")
            return False
    
    def delete_draft(self, draft_id: str) -> bool:
        """
        Delete a draft message
        
        Args:
            draft_id: Gmail draft ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.service.users().drafts().delete(
                userId='me',
                id=draft_id
            ).execute()
            console.print(f"[green]✅ Draft deleted successfully[/green]")
            return True
        except Exception as e:
            console.print(f"[red]❌ Error deleting draft: {e}[/red]")
            return False
    
    def send_draft(self, draft_id: str) -> bool:
        """
        Send a draft message
        
        Args:
            draft_id: Gmail draft ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            result = self.service.users().drafts().send(
                userId='me',
                body={'id': draft_id}
            ).execute()
            
            console.print(f"[green]✅ Draft sent successfully! Message ID: {result['id']}[/green]")
            return True
        except Exception as e:
            console.print(f"[red]❌ Error sending draft: {e}[/red]")
            return False
    
    # ==================== THREADS API ====================
    
    def list_threads(self, query: str = '', max_results: int = 10, label_ids: List[str] = None) -> List[Dict]:
        """
        List message threads from Gmail
        
        Args:
            query: Gmail search query
            max_results: Maximum number of results to return
            label_ids: List of label IDs to filter by
            
        Returns:
            List of thread metadata
        """
        try:
            results = self.service.users().threads().list(
                userId='me',
                q=query,
                maxResults=max_results,
                labelIds=label_ids
            ).execute()
            
            threads = results.get('threads', [])
            return threads
        except Exception as e:
            console.print(f"[red]❌ Error listing threads: {e}[/red]")
            return []
    
    def get_thread(self, thread_id: str) -> Optional[Dict]:
        """
        Get full thread details
        
        Args:
            thread_id: Gmail thread ID
            
        Returns:
            Thread details or None if error
        """
        try:
            thread = self.service.users().threads().get(
                userId='me',
                id=thread_id,
                format='full'
            ).execute()
            return thread
        except Exception as e:
            console.print(f"[red]❌ Error getting thread: {e}[/red]")
            return None
    
    def delete_thread(self, thread_id: str) -> bool:
        """
        Delete a thread
        
        Args:
            thread_id: Gmail thread ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.service.users().threads().delete(
                userId='me',
                id=thread_id
            ).execute()
            console.print(f"[green]✅ Thread deleted successfully[/green]")
            return True
        except Exception as e:
            console.print(f"[red]❌ Error deleting thread: {e}[/red]")
            return False
    
    def modify_thread(self, thread_id: str, add_label_ids: List[str] = None, 
                     remove_label_ids: List[str] = None) -> bool:
        """
        Modify thread labels
        
        Args:
            thread_id: Gmail thread ID
            add_label_ids: List of label IDs to add
            remove_label_ids: List of label IDs to remove
            
        Returns:
            True if successful, False otherwise
        """
        try:
            body = {}
            if add_label_ids:
                body['addLabelIds'] = add_label_ids
            if remove_label_ids:
                body['removeLabelIds'] = remove_label_ids
            
            self.service.users().threads().modify(
                userId='me',
                id=thread_id,
                body=body
            ).execute()
            
            console.print(f"[green]✅ Thread modified successfully[/green]")
            return True
        except Exception as e:
            console.print(f"[red]❌ Error modifying thread: {e}[/red]")
            return False
    
    # ==================== SETTINGS API ====================
    
    def get_filters(self) -> List[Dict]:
        """
        Get all Gmail filters
        
        Returns:
            List of filter information
        """
        try:
            results = self.service.users().settings().filters().list(userId='me').execute()
            filters = results.get('filter', [])
            return filters
        except Exception as e:
            console.print(f"[red]❌ Error getting filters: {e}[/red]")
            return []
    
    def create_filter(self, criteria: Dict, action: Dict) -> Optional[str]:
        """
        Create a new Gmail filter
        
        Args:
            criteria: Filter criteria (from, to, subject, etc.)
            action: Filter action (addLabelIds, removeLabelIds, etc.)
            
        Returns:
            Filter ID if successful, None otherwise
        """
        try:
            filter_body = {
                'criteria': criteria,
                'action': action
            }
            
            result = self.service.users().settings().filters().create(
                userId='me',
                body=filter_body
            ).execute()
            
            console.print(f"[green]✅ Filter created successfully! Filter ID: {result['id']}[/green]")
            return result['id']
        except Exception as e:
            console.print(f"[red]❌ Error creating filter: {e}[/red]")
            return None
    
    def delete_filter(self, filter_id: str) -> bool:
        """
        Delete a Gmail filter
        
        Args:
            filter_id: Gmail filter ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.service.users().settings().filters().delete(
                userId='me',
                id=filter_id
            ).execute()
            console.print(f"[green]✅ Filter deleted successfully[/green]")
            return True
        except Exception as e:
            console.print(f"[red]❌ Error deleting filter: {e}[/red]")
            return False
    
    def get_forwarding_addresses(self) -> List[Dict]:
        """
        Get all forwarding addresses
        
        Returns:
            List of forwarding address information
        """
        try:
            results = self.service.users().settings().forwardingAddresses().list(userId='me').execute()
            addresses = results.get('forwardingAddresses', [])
            return addresses
        except Exception as e:
            console.print(f"[red]❌ Error getting forwarding addresses: {e}[/red]")
            return []
    
    def create_forwarding_address(self, email: str) -> Optional[str]:
        """
        Create a forwarding address
        
        Args:
            email: Email address to forward to
            
        Returns:
            Forwarding address ID if successful, None otherwise
        """
        try:
            result = self.service.users().settings().forwardingAddresses().create(
                userId='me',
                body={'forwardingEmail': email}
            ).execute()
            
            console.print(f"[green]✅ Forwarding address created successfully! ID: {result['forwardingEmail']}[/green]")
            return result['forwardingEmail']
        except Exception as e:
            console.print(f"[red]❌ Error creating forwarding address: {e}[/red]")
            return None
    
    def get_send_as_aliases(self) -> List[Dict]:
        """
        Get all send-as aliases
        
        Returns:
            List of send-as alias information
        """
        try:
            results = self.service.users().settings().sendAs().list(userId='me').execute()
            aliases = results.get('sendAs', [])
            return aliases
        except Exception as e:
            console.print(f"[red]❌ Error getting send-as aliases: {e}[/red]")
            return []
    
    def create_send_as_alias(self, send_as_email: str, display_name: str = None) -> bool:
        """
        Create a send-as alias
        
        Args:
            send_as_email: Email address to send as
            display_name: Display name for the alias
            
        Returns:
            True if successful, False otherwise
        """
        try:
            body = {'sendAsEmail': send_as_email}
            if display_name:
                body['displayName'] = display_name
            
            self.service.users().settings().sendAs().create(
                userId='me',
                body=body
            ).execute()
            
            console.print(f"[green]✅ Send-as alias created successfully![/green]")
            return True
        except Exception as e:
            console.print(f"[red]❌ Error creating send-as alias: {e}[/red]")
            return False
    
    def get_vacation_settings(self) -> Optional[Dict]:
        """
        Get vacation responder settings
        
        Returns:
            Vacation settings or None if error
        """
        try:
            result = self.service.users().settings().getVacation(userId='me').execute()
            return result
        except Exception as e:
            console.print(f"[red]❌ Error getting vacation settings: {e}[/red]")
            return None
    
    def update_vacation_settings(self, enable: bool, subject: str = None, 
                               message: str = None, start_time: str = None, 
                               end_time: str = None) -> bool:
        """
        Update vacation responder settings
        
        Args:
            enable: Whether to enable vacation responder
            subject: Vacation responder subject
            message: Vacation responder message
            start_time: Start time (RFC 3339 format)
            end_time: End time (RFC 3339 format)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            body = {'enableAutoReply': enable}
            if subject:
                body['responseSubject'] = subject
            if message:
                body['responseBodyPlainText'] = message
            if start_time:
                body['restrictToContacts'] = False
                body['restrictToDomain'] = False
            if end_time:
                body['endTime'] = end_time
            
            self.service.users().settings().updateVacation(
                userId='me',
                body=body
            ).execute()
            
            console.print(f"[green]✅ Vacation settings updated successfully![/green]")
            return True
        except Exception as e:
            console.print(f"[red]❌ Error updating vacation settings: {e}[/red]")
            return False
    
    def get_delegates(self) -> List[Dict]:
        """
        Get all delegates
        
        Returns:
            List of delegate information
        """
        try:
            results = self.service.users().settings().delegates().list(userId='me').execute()
            delegates = results.get('delegates', [])
            return delegates
        except Exception as e:
            console.print(f"[red]❌ Error getting delegates: {e}[/red]")
            return []
    
    def create_delegate(self, delegate_email: str) -> bool:
        """
        Create a delegate
        
        Args:
            delegate_email: Email address of the delegate
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.service.users().settings().delegates().create(
                userId='me',
                body={'delegateEmail': delegate_email}
            ).execute()
            
            console.print(f"[green]✅ Delegate created successfully![/green]")
            return True
        except Exception as e:
            console.print(f"[red]❌ Error creating delegate: {e}[/red]")
            return False
    
    def delete_delegate(self, delegate_email: str) -> bool:
        """
        Delete a delegate
        
        Args:
            delegate_email: Email address of the delegate
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.service.users().settings().delegates().delete(
                userId='me',
                delegateEmail=delegate_email
            ).execute()
            
            console.print(f"[green]✅ Delegate deleted successfully![/green]")
            return True
        except Exception as e:
            console.print(f"[red]❌ Error deleting delegate: {e}[/red]")
            return False
    
    # ==================== HISTORY API ====================
    
    def get_history(self, start_history_id: str, max_results: int = 10) -> List[Dict]:
        """
        Get mailbox history
        
        Args:
            start_history_id: Starting history ID
            max_results: Maximum number of results to return
            
        Returns:
            List of history records
        """
        try:
            results = self.service.users().history().list(
                userId='me',
                startHistoryId=start_history_id,
                maxResults=max_results
            ).execute()
            
            history = results.get('history', [])
            return history
        except Exception as e:
            console.print(f"[red]❌ Error getting history: {e}[/red]")
            return []
    
    # ==================== ATTACHMENTS API ====================
    
    def download_attachment(self, message_id: str, attachment_id: str, 
                          filename: str = None) -> bool:
        """
        Download a message attachment
        
        Args:
            message_id: Gmail message ID
            attachment_id: Attachment ID
            filename: Local filename to save to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            attachment = self.service.users().messages().attachments().get(
                userId='me',
                messageId=message_id,
                id=attachment_id
            ).execute()
            
            # Decode the attachment data
            file_data = base64.urlsafe_b64decode(attachment['data'])
            
            # Save to file
            if not filename:
                filename = f"attachment_{attachment_id}"
            
            with open(filename, 'wb') as f:
                f.write(file_data)
            
            console.print(f"[green]✅ Attachment downloaded successfully: {filename}[/green]")
            return True
        except Exception as e:
            console.print(f"[red]❌ Error downloading attachment: {e}[/red]")
            return False
    
    # ==================== LABEL MANAGEMENT ====================
    
    def create_label(self, name: str, label_list_visibility: str = 'labelShow',
                    message_list_visibility: str = 'show') -> Optional[str]:
        """
        Create a new label
        
        Args:
            name: Label name
            label_list_visibility: Label list visibility
            message_list_visibility: Message list visibility
            
        Returns:
            Label ID if successful, None otherwise
        """
        try:
            label_body = {
                'name': name,
                'labelListVisibility': label_list_visibility,
                'messageListVisibility': message_list_visibility
            }
            
            result = self.service.users().labels().create(
                userId='me',
                body=label_body
            ).execute()
            
            console.print(f"[green]✅ Label created successfully! Label ID: {result['id']}[/green]")
            return result['id']
        except Exception as e:
            console.print(f"[red]❌ Error creating label: {e}[/red]")
            return None
    
    def update_label(self, label_id: str, name: str = None, 
                    label_list_visibility: str = None,
                    message_list_visibility: str = None) -> bool:
        """
        Update a label
        
        Args:
            label_id: Label ID
            name: New label name
            label_list_visibility: New label list visibility
            message_list_visibility: New message list visibility
            
        Returns:
            True if successful, False otherwise
        """
        try:
            body = {}
            if name:
                body['name'] = name
            if label_list_visibility:
                body['labelListVisibility'] = label_list_visibility
            if message_list_visibility:
                body['messageListVisibility'] = message_list_visibility
            
            self.service.users().labels().update(
                userId='me',
                id=label_id,
                body=body
            ).execute()
            
            console.print(f"[green]✅ Label updated successfully![/green]")
            return True
        except Exception as e:
            console.print(f"[red]❌ Error updating label: {e}[/red]")
            return False
    
    def delete_label(self, label_id: str) -> bool:
        """
        Delete a label
        
        Args:
            label_id: Label ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.service.users().labels().delete(
                userId='me',
                id=label_id
            ).execute()
            
            console.print(f"[green]✅ Label deleted successfully[/green]")
            return True
        except Exception as e:
            console.print(f"[red]❌ Error deleting label: {e}[/red]")
            return False
