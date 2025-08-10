#!/usr/bin/env python3
"""
Test proxy configuration with web scraping
"""

import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from smart_scraping_workflow import SmartScrapingWorkflow

async def test_proxy():
    """Test proxy configuration"""
    print("\n" + "="*60)
    print("🔧 PROXY CONFIGURATION TEST")
    print("="*60)
    
    # Check proxy settings
    proxy_enabled = os.getenv('CRAWL4AI_USE_PROXY', 'false').lower() == 'true'
    proxy_type = os.getenv('PROXY_TYPE', 'none')
    proxy_url = os.getenv('ROTATING_PROXY_URL', 'Not set')
    
    print(f"\n📋 Proxy Configuration:")
    print(f"  - Proxy Enabled: {proxy_enabled}")
    print(f"  - Proxy Type: {proxy_type}")
    print(f"  - Proxy URL: {proxy_url}")
    print(f"  - Proxy Username: {'Set' if os.getenv('ROTATING_PROXY_USERNAME') else 'Not set'}")
    
    if not proxy_enabled:
        print("\n⚠️  Proxy is not enabled. Set CRAWL4AI_USE_PROXY=true in .env")
        return
    
    # Initialize scraper
    scraper = SmartScrapingWorkflow()
    
    # Test URLs
    test_urls = [
        "https://httpbin.org/ip",  # Shows your IP
        "https://www.example.com"   # Simple test page
    ]
    
    print("\n🌐 Testing proxy with web scraping...")
    
    for url in test_urls:
        print(f"\n📍 Testing: {url}")
        result = await scraper.scrape_url(url)
        
        if result['success']:
            print(f"  ✅ Success! Method: {result['source']}")
            print(f"  💰 Cost: ${result['cost']:.4f}")
            
            # Show IP if httpbin
            if 'httpbin.org/ip' in url and result.get('data'):
                if result['source'] == 'crawl4ai':
                    content = result['data'].get('markdown', '')
                    print(f"  🌍 Response (first 200 chars):\n{content[:200]}")
                elif result['source'] == 'firecrawl':
                    content = result['data'].get('markdown', '')
                    print(f"  🌍 Response (first 200 chars):\n{content[:200]}")
        else:
            print(f"  ❌ Failed: {result.get('error', 'Unknown error')}")
    
    print("\n" + "="*60)
    print("✨ Proxy test complete!")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(test_proxy())