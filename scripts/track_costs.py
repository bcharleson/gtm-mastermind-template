#!/usr/bin/env python3
"""
Track costs for the research pipeline
"""

import json
import glob
from pathlib import Path
from datetime import datetime

def calculate_costs():
    """Calculate total costs from completed research"""
    output_dir = Path("gtm-alpha-project/outputs/company_research")
    
    print("\n" + "="*60)
    print("💰 RESEARCH COST TRACKER")
    print("="*60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Collect costs from JSON files
    json_files = list(output_dir.glob("json/*.json"))
    
    total_scraping_cost = 0
    total_research_cost = 0
    companies_processed = []
    
    for json_file in json_files:
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            metadata = data.get('researchMetadata', {})
            scraping = metadata.get('scrapingCost', 0)
            research = metadata.get('deepResearchCost', 0)
            
            total_scraping_cost += scraping
            total_research_cost += research
            
            companies_processed.append({
                'name': data.get('companyName', 'Unknown'),
                'scraping': scraping,
                'research': research,
                'total': scraping + research
            })
        except:
            pass
    
    # Sort by total cost
    companies_processed.sort(key=lambda x: x['total'], reverse=True)
    
    print(f"\n📊 Summary:")
    print(f"  - Companies processed: {len(companies_processed)}")
    print(f"  - Total scraping cost: ${total_scraping_cost:.4f}")
    print(f"  - Total research cost: ${total_research_cost:.2f}")
    print(f"  - Total cost: ${total_scraping_cost + total_research_cost:.2f}")
    print(f"  - Average cost per company: ${(total_scraping_cost + total_research_cost) / max(len(companies_processed), 1):.2f}")
    
    # Projection for all 331 companies
    if len(companies_processed) > 0:
        avg_cost = (total_scraping_cost + total_research_cost) / len(companies_processed)
        projected_total = avg_cost * 331
        print(f"\n💵 Projected cost for all 331 companies: ${projected_total:.2f}")
    
    # Show top 5 most expensive
    if companies_processed:
        print(f"\n🏢 Top 5 Most Expensive Companies:")
        for i, company in enumerate(companies_processed[:5], 1):
            print(f"  {i}. {company['name']}: ${company['total']:.2f}")
    
    # Daily limit check
    daily_limit = 40.00  # From .env
    if total_research_cost > daily_limit * 0.8:
        print(f"\n⚠️  WARNING: Approaching daily cost limit (${daily_limit})")
        print(f"   Current: ${total_research_cost:.2f} ({(total_research_cost/daily_limit)*100:.1f}%)")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    calculate_costs()