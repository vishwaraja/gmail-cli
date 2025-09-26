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
@click.option('--help-detailed', is_flag=True, help='Show detailed help with examples')
def main(help_detailed):
    """Gmail CLI - A powerful command-line interface for Gmail
    
    A comprehensive Gmail management tool with support for:
    • Reading and sending emails
    • Managing drafts and threads
    • Configuring filters and settings
    • Downloading attachments
    • Label management
    • And much more!
    
    Get started with: gmail auth
    """
    if help_detailed:
        show_detailed_help()


def show_detailed_help():
    """Show comprehensive help with examples"""
    console.print(Panel.fit(
        "[bold blue]Gmail CLI - Complete Command Reference[/bold blue]\n\n"
        "[bold]🔐 Authentication:[/bold]\n"
        "  gmail auth                    # Authenticate with Gmail\n"
        "  gmail revoke                  # Revoke stored credentials\n\n"
        
        "[bold]📧 Basic Email Operations:[/bold]\n"
        "  gmail list                    # List recent emails\n"
        "  gmail list --max-results 20   # List 20 emails\n"
        "  gmail list --query 'is:unread' # List unread emails\n"
        "  gmail read <message-id>       # Read specific email\n"
        "  gmail send --to user@example.com --subject 'Hello' --body 'Hi!'\n"
        "  gmail search 'from:important@example.com' # Search emails\n"
        "  gmail mark <message-id> --read # Mark as read\n"
        "  gmail delete <message-id>     # Delete email\n\n"
        
        "[bold]📝 Draft Management:[/bold]\n"
        "  gmail drafts list             # List all drafts\n"
        "  gmail drafts create --to user@example.com --subject 'Draft' --body 'Content'\n"
        "  gmail drafts read <draft-id>  # Read specific draft\n"
        "  gmail drafts send <draft-id>  # Send draft\n"
        "  gmail drafts delete <draft-id> # Delete draft\n\n"
        
        "[bold]🧵 Thread Management:[/bold]\n"
        "  gmail threads list            # List message threads\n"
        "  gmail threads read <thread-id> # Read entire thread\n"
        "  gmail threads delete <thread-id> # Delete thread\n\n"
        
        "[bold]🏷️ Label Management:[/bold]\n"
        "  gmail labels                  # List all labels\n"
        "  gmail label create 'My Label' # Create new label\n"
        "  gmail label delete <label-id> # Delete label\n\n"
        
        "[bold]⚙️ Settings Management:[/bold]\n"
        "  gmail settings filters list   # List email filters\n"
        "  gmail settings forwarding list # List forwarding addresses\n"
        "  gmail settings sendas list    # List send-as aliases\n"
        "  gmail settings vacation status # Show vacation responder\n\n"
        
        "[bold]📎 Attachments:[/bold]\n"
        "  gmail download <message-id> <attachment-id> # Download attachment\n"
        "  gmail download <msg-id> <att-id> --filename file.pdf\n\n"
        
        "[bold]🔍 Search Examples:[/bold]\n"
        "  gmail search 'is:unread'      # Unread emails\n"
        "  gmail search 'from:boss@company.com' # From specific sender\n"
        "  gmail search 'has:attachment' # Emails with attachments\n"
        "  gmail search 'subject:meeting' # Subject contains 'meeting'\n"
        "  gmail search 'after:2024/01/01' # After specific date\n"
        "  gmail search 'label:important' # With specific label\n\n"
        
        "[bold]📤 Sending Examples:[/bold]\n"
        "  gmail send --to user@example.com --subject 'Hello' --body 'Hi there!'\n"
        "  gmail send --to user@example.com --cc cc@example.com --subject 'Meeting' --body 'Details'\n"
        "  gmail send --to user@example.com --subject 'Files' --body 'Attached' --attach file1.pdf --attach file2.jpg\n\n"
        
        "[bold]🐳 Docker Usage:[/bold]\n"
        "  ./docker-run.sh list          # List emails in Docker\n"
        "  ./docker-run.sh send --to user@example.com --subject 'Hello' --body 'Test'\n"
        "  ./docker-run.sh shell         # Open interactive shell\n\n"
        
        "[bold]💡 Tips:[/bold]\n"
        "• Use --help with any command for detailed options\n"
        "• Message/thread/draft IDs can be partial (first 8+ characters)\n"
        "• All commands support --confirm/-y to skip confirmations\n"
        "• Use quotes around search queries with spaces\n"
        "• Attachments are supported in send and draft commands\n\n"
        
        "[bold]🔗 More Information:[/bold]\n"
        "• GitHub: https://github.com/vishwaraja/gmail-cli\n"
        "• Gmail API: https://developers.google.com/gmail/api\n"
        "• Search Syntax: https://support.google.com/mail/answer/7190",
        title="📚 Gmail CLI Help",
        border_style="green"
    ))


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


# ==================== DRAFTS COMMANDS ====================

@main.group()
def drafts():
    """Manage draft messages"""
    pass


@drafts.command('list')
@click.option('--max-results', '-n', default=10, help='Maximum number of drafts to display')
def drafts_list(max_results: int):
    """List draft messages"""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Fetching drafts...", total=None)
            
            # Authenticate
            auth = GmailAuthenticator()
            if not auth.authenticate():
                console.print("[red]❌ Authentication failed![/red]")
                sys.exit(1)
            
            # Get service and client
            service = auth.get_service()
            client = GmailClient(service)
            
            # Get drafts
            drafts = client.list_drafts(max_results)
            
            if not drafts:
                console.print("[yellow]No drafts found.[/yellow]")
                return
            
            # Display drafts
            table = Table(title="📝 Draft Messages")
            table.add_column("ID", style="cyan", no_wrap=True)
            table.add_column("Subject", style="green")
            table.add_column("To", style="magenta")
            table.add_column("Date", style="blue")
            
            for draft in drafts[:max_results]:
                draft_details = client.get_draft(draft['id'])
                if draft_details:
                    content = client.get_message_content(draft_details['message'])
                    
                    # Truncate long subjects
                    subject = content['subject'][:50] + "..." if len(content['subject']) > 50 else content['subject']
                    
                    table.add_row(
                        draft['id'][:8] + "...",
                        subject,
                        content['to'],
                        content['date'][:16]
                    )
            
            console.print(table)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


@drafts.command('create')
@click.option('--to', '-t', required=True, help='Recipient email address')
@click.option('--subject', '-s', required=True, help='Email subject')
@click.option('--body', '-b', help='Email body (will prompt if not provided)')
@click.option('--cc', help='CC recipients (comma-separated)')
@click.option('--bcc', help='BCC recipients (comma-separated)')
@click.option('--attach', '-a', multiple=True, help='File paths to attach')
def drafts_create(to: str, subject: str, body: Optional[str], cc: Optional[str], 
                 bcc: Optional[str], attach: List[str]):
    """Create a draft message"""
    try:
        # Get body if not provided
        if not body:
            body = Prompt.ask("Enter email body")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Creating draft...", total=None)
            
            # Authenticate
            auth = GmailAuthenticator()
            if not auth.authenticate():
                console.print("[red]❌ Authentication failed![/red]")
                sys.exit(1)
            
            # Get service and client
            service = auth.get_service()
            client = GmailClient(service)
            
            # Create draft
            draft_id = client.create_draft(
                to=to,
                subject=subject,
                body=body,
                cc=cc,
                bcc=bcc,
                attachments=list(attach) if attach else None
            )
            
            if draft_id:
                console.print("[green]✅ Draft created successfully![/green]")
            else:
                console.print("[red]❌ Failed to create draft[/red]")
                sys.exit(1)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


@drafts.command('read')
@click.argument('draft_id')
def drafts_read(draft_id: str):
    """Read a specific draft by ID"""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Fetching draft...", total=None)
            
            # Authenticate
            auth = GmailAuthenticator()
            if not auth.authenticate():
                console.print("[red]❌ Authentication failed![/red]")
                sys.exit(1)
            
            # Get service and client
            service = auth.get_service()
            client = GmailClient(service)
            
            # Get draft
            draft = client.get_draft(draft_id)
            if not draft:
                console.print("[red]❌ Draft not found![/red]")
                return
            
            content = client.get_message_content(draft['message'])
            
            # Display draft
            panel = Panel.fit(
                f"[bold]From:[/bold] {content['from']}\n"
                f"[bold]To:[/bold] {content['to']}\n"
                f"[bold]Subject:[/bold] {content['subject']}\n"
                f"[bold]Date:[/bold] {content['date']}\n\n"
                f"[bold]Body:[/bold]\n{content['body']}",
                title="📝 Draft Content",
                border_style="blue"
            )
            
            console.print(panel)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


@drafts.command('send')
@click.argument('draft_id')
def drafts_send(draft_id: str):
    """Send a draft message"""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Sending draft...", total=None)
            
            # Authenticate
            auth = GmailAuthenticator()
            if not auth.authenticate():
                console.print("[red]❌ Authentication failed![/red]")
                sys.exit(1)
            
            # Get service and client
            service = auth.get_service()
            client = GmailClient(service)
            
            # Send draft
            success = client.send_draft(draft_id)
            
            if not success:
                console.print("[red]❌ Failed to send draft[/red]")
                sys.exit(1)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


@drafts.command('delete')
@click.argument('draft_id')
@click.option('--confirm', '-y', is_flag=True, help='Skip confirmation prompt')
def drafts_delete(draft_id: str, confirm: bool):
    """Delete a draft message"""
    try:
        if not confirm:
            if not Confirm.ask(f"Are you sure you want to delete draft {draft_id}?"):
                console.print("[yellow]Operation cancelled.[/yellow]")
                return
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Deleting draft...", total=None)
            
            # Authenticate
            auth = GmailAuthenticator()
            if not auth.authenticate():
                console.print("[red]❌ Authentication failed![/red]")
                sys.exit(1)
            
            # Get service and client
            service = auth.get_service()
            client = GmailClient(service)
            
            # Delete draft
            success = client.delete_draft(draft_id)
            
            if not success:
                console.print("[red]❌ Failed to delete draft[/red]")
                sys.exit(1)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


# ==================== THREADS COMMANDS ====================

@main.group()
def threads():
    """Manage message threads"""
    pass


@threads.command('list')
@click.option('--max-results', '-n', default=10, help='Maximum number of threads to display')
@click.option('--query', '-q', default='', help='Gmail search query')
@click.option('--label', '-l', help='Filter by label')
def threads_list(max_results: int, query: str, label: Optional[str]):
    """List message threads"""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Fetching threads...", total=None)
            
            # Authenticate
            auth = GmailAuthenticator()
            if not auth.authenticate():
                console.print("[red]❌ Authentication failed![/red]")
                sys.exit(1)
            
            # Get service and client
            service = auth.get_service()
            client = GmailClient(service)
            
            # Get threads
            label_ids = [label] if label else None
            threads = client.list_threads(query=query, max_results=max_results, label_ids=label_ids)
            
            if not threads:
                console.print("[yellow]No threads found.[/yellow]")
                return
            
            # Display threads
            table = Table(title="🧵 Message Threads")
            table.add_column("ID", style="cyan", no_wrap=True)
            table.add_column("Subject", style="green")
            table.add_column("Messages", style="yellow")
            table.add_column("Labels", style="blue")
            
            for thread in threads[:max_results]:
                thread_details = client.get_thread(thread['id'])
                if thread_details:
                    # Get first message for subject
                    first_message = thread_details['messages'][0]
                    content = client.get_message_content(first_message)
                    
                    # Truncate long subjects
                    subject = content['subject'][:50] + "..." if len(content['subject']) > 50 else content['subject']
                    
                    # Format labels
                    labels = ", ".join(thread_details.get('labelIds', [])[:3])
                    if len(thread_details.get('labelIds', [])) > 3:
                        labels += "..."
                    
                    table.add_row(
                        thread['id'][:8] + "...",
                        subject,
                        str(len(thread_details['messages'])),
                        labels
                    )
            
            console.print(table)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


@threads.command('read')
@click.argument('thread_id')
def threads_read(thread_id: str):
    """Read a specific thread by ID"""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Fetching thread...", total=None)
            
            # Authenticate
            auth = GmailAuthenticator()
            if not auth.authenticate():
                console.print("[red]❌ Authentication failed![/red]")
                sys.exit(1)
            
            # Get service and client
            service = auth.get_service()
            client = GmailClient(service)
            
            # Get thread
            thread = client.get_thread(thread_id)
            if not thread:
                console.print("[red]❌ Thread not found![/red]")
                return
            
            # Display thread
            console.print(f"[bold]🧵 Thread: {thread_id}[/bold]")
            console.print(f"[bold]Messages:[/bold] {len(thread['messages'])}")
            console.print(f"[bold]Labels:[/bold] {', '.join(thread.get('labelIds', []))}")
            console.print()
            
            for i, message in enumerate(thread['messages'], 1):
                content = client.get_message_content(message)
                
                panel = Panel.fit(
                    f"[bold]Message {i}:[/bold]\n"
                    f"[bold]From:[/bold] {content['from']}\n"
                    f"[bold]To:[/bold] {content['to']}\n"
                    f"[bold]Subject:[/bold] {content['subject']}\n"
                    f"[bold]Date:[/bold] {content['date']}\n\n"
                    f"[bold]Body:[/bold]\n{content['body']}",
                    title=f"📧 Message {i}",
                    border_style="blue"
                )
                
                console.print(panel)
                console.print()
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


@threads.command('delete')
@click.argument('thread_id')
@click.option('--confirm', '-y', is_flag=True, help='Skip confirmation prompt')
def threads_delete(thread_id: str, confirm: bool):
    """Delete a thread"""
    try:
        if not confirm:
            if not Confirm.ask(f"Are you sure you want to delete thread {thread_id}?"):
                console.print("[yellow]Operation cancelled.[/yellow]")
                return
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Deleting thread...", total=None)
            
            # Authenticate
            auth = GmailAuthenticator()
            if not auth.authenticate():
                console.print("[red]❌ Authentication failed![/red]")
                sys.exit(1)
            
            # Get service and client
            service = auth.get_service()
            client = GmailClient(service)
            
            # Delete thread
            success = client.delete_thread(thread_id)
            
            if not success:
                console.print("[red]❌ Failed to delete thread[/red]")
                sys.exit(1)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


# ==================== SETTINGS COMMANDS ====================

@main.group()
def settings():
    """Manage Gmail settings"""
    pass


@settings.group()
def filters():
    """Manage email filters"""
    pass


@filters.command('list')
def filters_list():
    """List all email filters"""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Fetching filters...", total=None)
            
            # Authenticate
            auth = GmailAuthenticator()
            if not auth.authenticate():
                console.print("[red]❌ Authentication failed![/red]")
                sys.exit(1)
            
            # Get service and client
            service = auth.get_service()
            client = GmailClient(service)
            
            # Get filters
            filters = client.get_filters()
            
            if not filters:
                console.print("[yellow]No filters found.[/yellow]")
                return
            
            # Display filters
            table = Table(title="🔍 Email Filters")
            table.add_column("ID", style="cyan", no_wrap=True)
            table.add_column("Criteria", style="green")
            table.add_column("Action", style="blue")
            
            for filter_item in filters:
                criteria = filter_item.get('criteria', {})
                action = filter_item.get('action', {})
                
                # Format criteria
                criteria_str = ", ".join([f"{k}: {v}" for k, v in criteria.items()])
                if len(criteria_str) > 50:
                    criteria_str = criteria_str[:50] + "..."
                
                # Format action
                action_str = ", ".join([f"{k}: {v}" for k, v in action.items()])
                if len(action_str) > 50:
                    action_str = action_str[:50] + "..."
                
                table.add_row(
                    filter_item.get('id', 'Unknown')[:8] + "...",
                    criteria_str,
                    action_str
                )
            
            console.print(table)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


@settings.group()
def forwarding():
    """Manage email forwarding"""
    pass


@forwarding.command('list')
def forwarding_list():
    """List forwarding addresses"""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Fetching forwarding addresses...", total=None)
            
            # Authenticate
            auth = GmailAuthenticator()
            if not auth.authenticate():
                console.print("[red]❌ Authentication failed![/red]")
                sys.exit(1)
            
            # Get service and client
            service = auth.get_service()
            client = GmailClient(service)
            
            # Get forwarding addresses
            addresses = client.get_forwarding_addresses()
            
            if not addresses:
                console.print("[yellow]No forwarding addresses found.[/yellow]")
                return
            
            # Display forwarding addresses
            table = Table(title="📧 Forwarding Addresses")
            table.add_column("Email", style="green")
            table.add_column("Verification Status", style="blue")
            
            for address in addresses:
                table.add_row(
                    address.get('forwardingEmail', 'Unknown'),
                    address.get('verificationStatus', 'Unknown')
                )
            
            console.print(table)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


@settings.group()
def sendas():
    """Manage send-as aliases"""
    pass


@sendas.command('list')
def sendas_list():
    """List send-as aliases"""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Fetching send-as aliases...", total=None)
            
            # Authenticate
            auth = GmailAuthenticator()
            if not auth.authenticate():
                console.print("[red]❌ Authentication failed![/red]")
                sys.exit(1)
            
            # Get service and client
            service = auth.get_service()
            client = GmailClient(service)
            
            # Get send-as aliases
            aliases = client.get_send_as_aliases()
            
            if not aliases:
                console.print("[yellow]No send-as aliases found.[/yellow]")
                return
            
            # Display send-as aliases
            table = Table(title="📤 Send-As Aliases")
            table.add_column("Email", style="green")
            table.add_column("Display Name", style="blue")
            table.add_column("Primary", style="yellow")
            table.add_column("Verification", style="cyan")
            
            for alias in aliases:
                table.add_row(
                    alias.get('sendAsEmail', 'Unknown'),
                    alias.get('displayName', 'None'),
                    "Yes" if alias.get('isPrimary', False) else "No",
                    alias.get('verificationStatus', 'Unknown')
                )
            
            console.print(table)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


@settings.group()
def vacation():
    """Manage vacation responder"""
    pass


@vacation.command('status')
def vacation_status():
    """Show vacation responder status"""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Fetching vacation settings...", total=None)
            
            # Authenticate
            auth = GmailAuthenticator()
            if not auth.authenticate():
                console.print("[red]❌ Authentication failed![/red]")
                sys.exit(1)
            
            # Get service and client
            service = auth.get_service()
            client = GmailClient(service)
            
            # Get vacation settings
            settings = client.get_vacation_settings()
            
            if not settings:
                console.print("[yellow]No vacation settings found.[/yellow]")
                return
            
            # Display vacation settings
            panel = Panel.fit(
                f"[bold]Enabled:[/bold] {settings.get('enableAutoReply', False)}\n"
                f"[bold]Subject:[/bold] {settings.get('responseSubject', 'None')}\n"
                f"[bold]Message:[/bold] {settings.get('responseBodyPlainText', 'None')}\n"
                f"[bold]Start Time:[/bold] {settings.get('startTime', 'None')}\n"
                f"[bold]End Time:[/bold] {settings.get('endTime', 'None')}",
                title="🏖️ Vacation Responder",
                border_style="blue"
            )
            
            console.print(panel)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


# ==================== ATTACHMENTS COMMANDS ====================

@main.command()
@click.argument('message_id')
@click.argument('attachment_id')
@click.option('--filename', '-f', help='Local filename to save to')
def download(message_id: str, attachment_id: str, filename: Optional[str]):
    """Download a message attachment"""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Downloading attachment...", total=None)
            
            # Authenticate
            auth = GmailAuthenticator()
            if not auth.authenticate():
                console.print("[red]❌ Authentication failed![/red]")
                sys.exit(1)
            
            # Get service and client
            service = auth.get_service()
            client = GmailClient(service)
            
            # Download attachment
            success = client.download_attachment(message_id, attachment_id, filename)
            
            if not success:
                console.print("[red]❌ Failed to download attachment[/red]")
                sys.exit(1)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


# ==================== LABEL MANAGEMENT COMMANDS ====================

@main.group()
def label():
    """Manage Gmail labels"""
    pass


@label.command('create')
@click.argument('name')
@click.option('--label-visibility', default='labelShow', 
              type=click.Choice(['labelShow', 'labelHide']),
              help='Label list visibility')
@click.option('--message-visibility', default='show',
              type=click.Choice(['show', 'hide']),
              help='Message list visibility')
def label_create(name: str, label_visibility: str, message_visibility: str):
    """Create a new label"""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Creating label...", total=None)
            
            # Authenticate
            auth = GmailAuthenticator()
            if not auth.authenticate():
                console.print("[red]❌ Authentication failed![/red]")
                sys.exit(1)
            
            # Get service and client
            service = auth.get_service()
            client = GmailClient(service)
            
            # Create label
            label_id = client.create_label(name, label_visibility, message_visibility)
            
            if not label_id:
                console.print("[red]❌ Failed to create label[/red]")
                sys.exit(1)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


@label.command('delete')
@click.argument('label_id')
@click.option('--confirm', '-y', is_flag=True, help='Skip confirmation prompt')
def label_delete(label_id: str, confirm: bool):
    """Delete a label"""
    try:
        if not confirm:
            if not Confirm.ask(f"Are you sure you want to delete label {label_id}?"):
                console.print("[yellow]Operation cancelled.[/yellow]")
                return
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Deleting label...", total=None)
            
            # Authenticate
            auth = GmailAuthenticator()
            if not auth.authenticate():
                console.print("[red]❌ Authentication failed![/red]")
                sys.exit(1)
            
            # Get service and client
            service = auth.get_service()
            client = GmailClient(service)
            
            # Delete label
            success = client.delete_label(label_id)
            
            if not success:
                console.print("[red]❌ Failed to delete label[/red]")
                sys.exit(1)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")


if __name__ == '__main__':
    main()
