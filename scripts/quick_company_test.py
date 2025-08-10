#!/usr/bin/env python3
"""
Quick test with one company
"""

import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from parallel_company_research import ParallelCompanyResearch

async def quick_test():
    """Test with just IBM"""
    print("\n🚀 Quick Company Research Test")
    print("="*60)
    
    # Initialize pipeline
    csv_path = "data/raw/2025-07-07/331_070725_COMPANY.csv"
    pipeline = ParallelCompanyResearch(csv_path)
    
    # Load companies
    companies = pipeline.load_companies()
    print(f"✅ Loaded {len(companies)} companies")
    
    # Test with just IBM
    test_company = companies[0]  # IBM
    print(f"\n🏢 Testing with: {test_company['company_name']}")
    print(f"  - Industry: {test_company['industry']}")
    print(f"  - Website: {test_company['website']}")
    
    # Scrape company data
    print("\n📊 Scraping company website...")
    scrape_result = await pipeline.scrape_company_data(test_company)
    
    print(f"\n✅ Scraping complete!")
    print(f"  - Cost: ${scrape_result['scraping_cost']:.4f}")
    print(f"  - Main site scraped: {'Yes' if 'main_site' in scrape_result['scraping_results'] else 'No'}")
    print(f"  - LinkedIn scraped: {'Yes' if 'linkedin' in scrape_result['scraping_results'] else 'No'}")
    
    # Save outputs
    pipeline.save_outputs(test_company, scrape_result)
    print(f"\n📁 Outputs saved to: {pipeline.output_dir}")
    
    # Show markdown preview
    safe_name = test_company['company_name'].replace(' ', '_').replace('/', '_')
    markdown_path = pipeline.output_dir / 'markdown' / f"{safe_name}.md"
    
    if markdown_path.exists():
        print(f"\n📄 Markdown Report Preview:")
        print("-"*60)
        with open(markdown_path, 'r') as f:
            content = f.read()
            print(content[:800] + "..." if len(content) > 800 else content)

if __name__ == "__main__":
    asyncio.run(quick_test())