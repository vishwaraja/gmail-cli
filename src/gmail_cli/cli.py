"""
Gmail CLI - Command Line Interface
"""

import os
import sys
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing import List, Optional

from .auth import GmailAuthenticator
from .gmail_client import GmailClient

console = Console()


@click.group()
@click.version_option(version="1.0.0", prog_name="Gmail CLI")
def main():
    """Gmail CLI - A powerful command-line interface for Gmail"""
    pass


@main.command()
@click.option('--max-results', '-n', default=10, help='Maximum number of messages to display')
@click.option('--query', '-q', default='', help='Gmail search query')
@click.option('--label', '-l', help='Filter by label')
def list(max_results: int, query: str, label: Optional[str]):
    """List recent emails"""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Connecting to Gmail...", total=None)
            
            # Authenticate
            auth = GmailAuthenticator()
            if not auth.authenticate():
                console.print("[red]❌ Authentication failed![/red]")
                sys.exit(1)
            
            # Get service and client
            service = auth.get_service()
            client = GmailClient(service)
            
            progress.update(task, description="Fetching messages...")
            
            # Get messages
            label_ids = [label] if label else None
            messages = client.list_messages(query=query, max_results=max_results, label_ids=label_ids)
            
            if not messages:
                console.print("[yellow]No messages found.[/yellow]")
                return
            
            # Display messages
            table = Table(title="📧 Recent Emails")
            table.add_column("ID", style="cyan", no_wrap=True)
            table.add_column("From", style="magenta")
            table.add_column("Subject", style="green")
            table.add_column("Date", style="blue")
            table.add_column("Labels", style="yellow")
            
            for msg in messages[:max_results]:
                message_details = client.get_message(msg['id'])
                if message_details:
                    content = client.get_message_content(message_details)
                    
                    # Truncate long subjects
                    subject = content['subject'][:50] + "..." if len(content['subject']) > 50 else content['subject']
                    
                    # Format labels
                    labels = ", ".join(content['labels'][:3])  # Show first 3 labels
                    if len(content['labels']) > 3:
                        labels += "..."
                    
                    table.add_row(
                        msg['id'][:8] + "...",
                        content['from'],
                        subject,
                        content['date'][:16],  # Truncate date
                        labels
                    )
            
            console.print(table)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


@main.command()
@click.argument('message_id')
def read(message_id: str):
    """Read a specific email by ID"""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Fetching message...", total=None)
            
            # Authenticate
            auth = GmailAuthenticator()
            if not auth.authenticate():
                console.print("[red]❌ Authentication failed![/red]")
                sys.exit(1)
            
            # Get service and client
            service = auth.get_service()
            client = GmailClient(service)
            
            # Get message
            message = client.get_message(message_id)
            if not message:
                console.print("[red]❌ Message not found![/red]")
                return
            
            content = client.get_message_content(message)
            
            # Display message
            panel = Panel.fit(
                f"[bold]From:[/bold] {content['from']}\n"
                f"[bold]To:[/bold] {content['to']}\n"
                f"[bold]Subject:[/bold] {content['subject']}\n"
                f"[bold]Date:[/bold] {content['date']}\n"
                f"[bold]Labels:[/bold] {', '.join(content['labels'])}\n\n"
                f"[bold]Body:[/bold]\n{content['body']}",
                title="📧 Email Content",
                border_style="blue"
            )
            
            console.print(panel)
            
            # Mark as read
            if 'UNREAD' in content['labels']:
                if Confirm.ask("Mark this message as read?"):
                    client.mark_as_read(message_id)
                    console.print("[green]✅ Message marked as read[/green]")
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


@main.command()
@click.option('--to', '-t', required=True, help='Recipient email address')
@click.option('--subject', '-s', required=True, help='Email subject')
@click.option('--body', '-b', help='Email body (will prompt if not provided)')
@click.option('--cc', help='CC recipients (comma-separated)')
@click.option('--bcc', help='BCC recipients (comma-separated)')
@click.option('--attach', '-a', multiple=True, help='File paths to attach')
def send(to: str, subject: str, body: Optional[str], cc: Optional[str], 
         bcc: Optional[str], attach: List[str]):
    """Send an email"""
    try:
        # Get body if not provided
        if not body:
            body = Prompt.ask("Enter email body")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Sending email...", total=None)
            
            # Authenticate
            auth = GmailAuthenticator()
            if not auth.authenticate():
                console.print("[red]❌ Authentication failed![/red]")
                sys.exit(1)
            
            # Get service and client
            service = auth.get_service()
            client = GmailClient(service)
            
            # Send message
            success = client.send_message(
                to=to,
                subject=subject,
                body=body,
                cc=cc,
                bcc=bcc,
                attachments=list(attach) if attach else None
            )
            
            if success:
                console.print("[green]✅ Email sent successfully![/green]")
            else:
                console.print("[red]❌ Failed to send email[/red]")
                sys.exit(1)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


@main.command()
@click.argument('query')
@click.option('--max-results', '-n', default=10, help='Maximum number of results')
def search(query: str, max_results: int):
    """Search emails using Gmail search syntax"""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Searching emails...", total=None)
            
            # Authenticate
            auth = GmailAuthenticator()
            if not auth.authenticate():
                console.print("[red]❌ Authentication failed![/red]")
                sys.exit(1)
            
            # Get service and client
            service = auth.get_service()
            client = GmailClient(service)
            
            # Search messages
            messages = client.search_messages(query, max_results)
            
            if not messages:
                console.print("[yellow]No messages found matching your search.[/yellow]")
                return
            
            # Display results
            table = Table(title=f"🔍 Search Results for: '{query}'")
            table.add_column("ID", style="cyan", no_wrap=True)
            table.add_column("From", style="magenta")
            table.add_column("Subject", style="green")
            table.add_column("Date", style="blue")
            
            for msg in messages:
                message_details = client.get_message(msg['id'])
                if message_details:
                    content = client.get_message_content(message_details)
                    
                    # Truncate long subjects
                    subject = content['subject'][:50] + "..." if len(content['subject']) > 50 else content['subject']
                    
                    table.add_row(
                        msg['id'][:8] + "...",
                        content['from'],
                        subject,
                        content['date'][:16]
                    )
            
            console.print(table)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


@main.command()
def labels():
    """List all Gmail labels"""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Fetching labels...", total=None)
            
            # Authenticate
            auth = GmailAuthenticator()
            if not auth.authenticate():
                console.print("[red]❌ Authentication failed![/red]")
                sys.exit(1)
            
            # Get service and client
            service = auth.get_service()
            client = GmailClient(service)
            
            # Get labels
            labels = client.get_labels()
            
            if not labels:
                console.print("[yellow]No labels found.[/yellow]")
                return
            
            # Display labels
            table = Table(title="🏷️  Gmail Labels")
            table.add_column("Name", style="green")
            table.add_column("ID", style="cyan")
            table.add_column("Type", style="blue")
            table.add_column("Messages", style="yellow")
            table.add_column("Unread", style="red")
            
            for label in labels:
                table.add_row(
                    label.get('name', 'Unknown'),
                    label.get('id', 'Unknown'),
                    label.get('type', 'Unknown'),
                    str(label.get('messagesTotal', 0)),
                    str(label.get('messagesUnread', 0))
                )
            
            console.print(table)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


@main.command()
@click.argument('message_id')
@click.option('--read/--unread', default=True, help='Mark as read or unread')
def mark(message_id: str, read: bool):
    """Mark a message as read or unread"""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Updating message...", total=None)
            
            # Authenticate
            auth = GmailAuthenticator()
            if not auth.authenticate():
                console.print("[red]❌ Authentication failed![/red]")
                sys.exit(1)
            
            # Get service and client
            service = auth.get_service()
            client = GmailClient(service)
            
            # Mark message
            if read:
                success = client.mark_as_read(message_id)
                status = "read"
            else:
                success = client.mark_as_unread(message_id)
                status = "unread"
            
            if success:
                console.print(f"[green]✅ Message marked as {status}[/green]")
            else:
                console.print(f"[red]❌ Failed to mark message as {status}[/red]")
                sys.exit(1)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


@main.command()
@click.argument('message_id')
@click.option('--confirm', '-y', is_flag=True, help='Skip confirmation prompt')
def delete(message_id: str, confirm: bool):
    """Delete a message"""
    try:
        if not confirm:
            if not Confirm.ask(f"Are you sure you want to delete message {message_id}?"):
                console.print("[yellow]Operation cancelled.[/yellow]")
                return
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Deleting message...", total=None)
            
            # Authenticate
            auth = GmailAuthenticator()
            if not auth.authenticate():
                console.print("[red]❌ Authentication failed![/red]")
                sys.exit(1)
            
            # Get service and client
            service = auth.get_service()
            client = GmailClient(service)
            
            # Delete message
            success = client.delete_message(message_id)
            
            if not success:
                console.print("[red]❌ Failed to delete message[/red]")
                sys.exit(1)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


@main.command()
def auth():
    """Manage authentication"""
    try:
        auth = GmailAuthenticator()
        
        console.print(Panel.fit(
            "[bold]Gmail CLI Authentication[/bold]\n\n"
            "This tool will help you authenticate with Gmail API.\n"
            "You'll need to:\n"
            "1. Create a Google Cloud Project\n"
            "2. Enable Gmail API\n"
            "3. Create OAuth2 credentials\n"
            "4. Download credentials.json\n\n"
            "For detailed instructions, visit:\n"
            "https://developers.google.com/gmail/api/quickstart/python",
            title="🔐 Authentication Setup",
            border_style="blue"
        ))
        
        if Confirm.ask("Do you want to authenticate now?"):
            if auth.authenticate():
                console.print("[green]✅ Authentication successful![/green]")
            else:
                console.print("[red]❌ Authentication failed![/red]")
                sys.exit(1)
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


@main.command()
def revoke():
    """Revoke stored credentials"""
    try:
        auth = GmailAuthenticator()
        
        if Confirm.ask("Are you sure you want to revoke stored credentials?"):
            if auth.revoke_credentials():
                console.print("[green]✅ Credentials revoked successfully![/green]")
            else:
                console.print("[red]❌ Failed to revoke credentials[/red]")
                sys.exit(1)
        else:
            console.print("[yellow]Operation cancelled.[/yellow]")
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


if __name__ == '__main__':
    main()
