#!/usr/bin/env python3
"""
Simple test script for Gmail CLI
Run this to test basic functionality without full CLI
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gmail_cli.auth import GmailAuthenticator
from gmail_cli.gmail_client import GmailClient

def test_authentication():
    """Test Gmail API authentication"""
    print("🔐 Testing Gmail API Authentication...")
    
    auth = GmailAuthenticator()
    if auth.authenticate():
        print("✅ Authentication successful!")
        return auth.get_service()
    else:
        print("❌ Authentication failed!")
        return None

def test_basic_operations(service):
    """Test basic Gmail operations"""
    print("\n📧 Testing basic Gmail operations...")
    
    client = GmailClient(service)
    
    # Test getting labels
    print("📋 Testing label retrieval...")
    labels = client.get_labels()
    print(f"✅ Found {len(labels)} labels")
    
    # Test listing messages
    print("📬 Testing message listing...")
    messages = client.list_messages(max_results=5)
    print(f"✅ Found {len(messages)} recent messages")
    
    if messages:
        # Test getting message details
        print("📖 Testing message details...")
        message_id = messages[0]['id']
        message = client.get_message(message_id)
        if message:
            content = client.get_message_content(message)
            print(f"✅ Retrieved message: {content['subject'][:50]}...")
    
    return True

def main():
    """Main test function"""
    print("🚀 Gmail CLI Test Suite")
    print("=" * 50)
    
    # Test authentication
    service = test_authentication()
    if not service:
        print("\n❌ Cannot proceed without authentication")
        print("Please ensure you have:")
        print("1. credentials.json file in the project directory")
        print("2. Gmail API enabled in Google Cloud Console")
        print("3. Valid OAuth2 credentials")
        return False
    
    # Test basic operations
    try:
        test_basic_operations(service)
        print("\n🎉 All tests passed!")
        return True
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
