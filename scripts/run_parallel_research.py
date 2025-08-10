#!/usr/bin/env python3
"""
Run parallel company research with all features enabled
- Proxy-enabled web scraping
- Parallel processing
- Comprehensive outputs
"""

import asyncio
import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from parallel_company_research import ParallelCompanyResearch

async def main():
    """Run the complete research pipeline"""
    print("\n" + "="*80)
    print("🚀 PARALLEL COMPANY RESEARCH PIPELINE")
    print("="*80)
    print(f"\n📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Configuration summary
    print("\n📋 Configuration:")
    print(f"  ✅ OpenAI API (LLM extraction): {'Configured' if os.getenv('OPENAI_API_KEY') else '❌ Missing'}")
    print(f"  ✅ Firecrawl API: {'Configured' if os.getenv('FIRECRAWL_API_KEY') else '❌ Missing'}")
    print(f"  ✅ Proxy: {'Enabled (ZenRows)' if os.getenv('CRAWL4AI_USE_PROXY') == 'true' else '❌ Disabled'}")
    print(f"  ✅ DeepSeek API: {'Configured' if os.getenv('DEEPSEEK_API_KEY') else '⚠️  Not configured'}")
    
    # Initialize pipeline
    csv_path = "data/raw/2025-07-07/331_070725_COMPANY.csv"
    pipeline = ParallelCompanyResearch(csv_path)
    
    # Get parameters from command line or use defaults
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    batch_size = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    print(f"\n📊 Processing Configuration:")
    print(f"  - Companies to process: {limit}")
    print(f"  - Batch size: {batch_size}")
    print(f"  - Output directory: {pipeline.output_dir}")
    
    print("\n" + "-"*80)
    print("Starting research pipeline...")
    print("-"*80)
    
    try:
        # Run the pipeline
        results = await pipeline.run_research_pipeline(limit=limit, batch_size=batch_size)
        
        print("\n" + "="*80)
        print("✅ RESEARCH PIPELINE COMPLETE!")
        print("="*80)
        
        # Summary statistics
        total_companies = len(results)
        successful_scrapes = sum(1 for r in results if r.get('scraping_cost', 0) > 0)
        
        total_scraping_cost = sum(r.get('scraping_cost', 0) for r in results)
        
        print(f"\n📈 Summary Statistics:")
        print(f"  - Total companies processed: {total_companies}")
        print(f"  - Successful web scrapes: {successful_scrapes}/{total_companies}")
        print(f"\n💰 Cost Summary:")
        print(f"  - Web scraping cost: ${total_scraping_cost:.4f}")
        print(f"  - Total cost: ${total_scraping_cost:.2f}")
        
        # Output locations
        print(f"\n📁 Output Files:")
        print(f"  - Markdown reports: {pipeline.output_dir}/markdown/")
        print(f"  - JSON data: {pipeline.output_dir}/json/")
        print(f"  - Master CSV: {pipeline.output_dir}/csv/")
        
        # Show sample companies
        print(f"\n🏢 Sample Companies Processed:")
        for i, result in enumerate(results[:5], 1):
            company = result['company']
            print(f"  {i}. {company['company_name']} - {company['industry']}")
        
        if len(results) > 5:
            print(f"  ... and {len(results) - 5} more")
        
        print("\n✨ Research pipeline complete!")
        print(f"📊 Check the output directory for detailed reports")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Pipeline interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Pipeline error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Run with command line args: python run_parallel_research.py [limit] [batch_size]
    # Example: python run_parallel_research.py 20 5
    asyncio.run(main())