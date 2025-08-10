#!/usr/bin/env python3
"""
Parallel Company Research Pipeline
Combines existing scripts to process companies in parallel
Uses Smart Scraping
"""

import os
import sys
import csv
import json
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import polars as pl  # Using polars for faster data processing
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Add parent directory to path to import existing scripts
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import existing scripts
from smart_scraping_workflow import SmartScrapingWorkflow

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ParallelCompanyResearch:
    def __init__(self, csv_path: str, output_dir: str = "gtm-alpha-project/outputs/company_research"):
        self.csv_path = csv_path
        self.output_dir = Path(output_dir)
        
        # Create output directories
        for subdir in ['markdown', 'json', 'csv']:
            (self.output_dir / subdir).mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.scraper = SmartScrapingWorkflow()
        self.deep_researcher = None
        
        # Track active tasks
        self.active_tasks = {}
        self.completed_research = []
        
    def load_companies(self) -> List[Dict[str, Any]]:
        """Load companies from CSV"""
        companies = []
        
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                companies.append({
                    'company_name': row.get('Company Name', ''),
                    'website': row.get('Website', ''),
                    'founded_year': row.get('Founded Year', ''),
                    'revenue': row.get('Revenue (in 000s USD)', ''),
                    'revenue_range': row.get('Revenue Range (in USD)', ''),
                    'employees': row.get('Employees', ''),
                    'employee_range': row.get('Employee Range', ''),
                    'industry': row.get('Primary Industry', ''),
                    'sub_industry': row.get('Primary Sub-Industry', ''),
                    'ownership_type': row.get('Ownership Type', ''),
                    'business_model': row.get('Business Model', ''),
                    'linkedin_url': row.get('LinkedIn Company Profile URL', ''),
                    'facebook_url': row.get('Facebook Company Profile URL', ''),
                    'twitter_url': row.get('Twitter Company Profile URL', ''),
                    'address': row.get('Company Street Address', ''),
                    'city': row.get('Company City', ''),
                    'state': row.get('Company State', ''),
                    'zip_code': row.get('Company Zip Code', ''),
                    'country': row.get('Company Country', ''),
                    'zoominfo_id': row.get('ZoomInfo Company ID', '')
                })
        
        logger.info(f"Loaded {len(companies)} companies from CSV")
        return companies
    
    def clean_url(self, url: str) -> str:
        """Clean and normalize URL"""
        if not url:
            return ""
        
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        return url.rstrip('/')
    
    async def scrape_company_data(self, company: Dict[str, Any]) -> Dict[str, Any]:
        """Scrape company website and related pages"""
        logger.info(f"Scraping data for {company['company_name']}...")
        
        results = {
            'company': company,
            'scraping_results': {},
            'scraping_cost': 0.0
        }
        
        # Prepare extraction instructions
        extraction_prompt = f"""
        Extract comprehensive information about {company['company_name']}:
        1. Company overview and mission
        2. Products and services offered
        3. Technology stack and tools used (especially Procore, ACC, Primavera P6)
        4. Recent projects and achievements
        5. Leadership team and key executives
        6. News and announcements from the last 12 months
        7. Digital transformation initiatives
        8. Pain points or challenges mentioned
        9. Contact information
        """
        
        # Primary website
        website = self.clean_url(company.get('website', ''))
        if website:
            try:
                main_result = await self.scraper.scrape_url(website, extraction_prompt)
                if main_result['success']:
                    results['scraping_results']['main_site'] = main_result
                    results['scraping_cost'] += main_result.get('cost', 0)
                    
                    # Extract key data
                    if main_result.get('data', {}).get('extracted'):
                        extracted = main_result['data']['extracted']
                        results['scraping_results']['extracted_data'] = extracted
                        
            except Exception as e:
                logger.error(f"Error scraping {website}: {e}")
        
        # LinkedIn
        linkedin_url = company.get('linkedin_url', '')
        if linkedin_url and linkedin_url.startswith('http'):
            try:
                linkedin_result = await self.scraper.scrape_url(
                    linkedin_url, 
                    "Extract company size, recent posts, and employee count"
                )
                if linkedin_result['success']:
                    results['scraping_results']['linkedin'] = linkedin_result
                    results['scraping_cost'] += linkedin_result.get('cost', 0)
            except:
                pass
        
        return results
    
    def start_deep_research(self, company_name: str, company_data: Dict[str, Any]) -> Optional[str]:
        return None
    
    def save_active_tasks(self):
        return
    
    def check_research_status(self, task_id: str) -> Dict[str, Any]:
        return {"status": "disabled"}
    
    def generate_markdown_report(self, company: Dict[str, Any], research_data: Dict[str, Any]) -> str:
        """Generate detailed markdown report"""
        report = f"""# {company['company_name']}

## Company Overview
- **Founded:** {company.get('founded_year', 'N/A')}
- **Industry:** {company.get('industry', 'N/A')}
- **Sub-Industry:** {company.get('sub_industry', 'N/A')}
- **Revenue:** {company.get('revenue_range', 'N/A')}
- **Employees:** {company.get('employee_range', 'N/A')}
- **Ownership:** {company.get('ownership_type', 'N/A')}
- **Business Model:** {company.get('business_model', 'N/A')}
- **Website:** {company.get('website', 'N/A')}

## Location
- **Address:** {company.get('address', 'N/A')}
- **City:** {company.get('city', 'N/A')}, {company.get('state', 'N/A')}
- **Country:** {company.get('country', 'N/A')}

## Social Media
- **LinkedIn:** {company.get('linkedin_url', 'N/A')}
- **Twitter:** {company.get('twitter_url', 'N/A')}
"""
        
        # Add scraped data insights
        if research_data.get('scraping_results', {}).get('extracted_data'):
            extracted = research_data['scraping_results']['extracted_data']
            report += "\n## Web Intelligence\n"
            
            if isinstance(extracted, dict):
                for key, value in extracted.items():
                    if value:
                        report += f"\n### {key.replace('_', ' ').title()}\n{value}\n"
        
        # Deep research removed from template
        
        # Add metadata
        report += f"""
## Research Metadata
- **Research Date:** {datetime.now().strftime('%Y-%m-%d')}
- **Web Scraping Cost:** ${research_data.get('scraping_cost', 0):.4f}
- **Deep Research Cost:** $0.00
- **Total Cost:** ${research_data.get('scraping_cost', 0):.2f}
"""
        
        return report
    
    def generate_json_output(self, company: Dict[str, Any], research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate structured JSON output"""
        return {
            "companyName": company['company_name'],
            "companyData": company,
            "webIntelligence": research_data.get('scraping_results', {}),
            "deepResearchResults": {},
            "researchMetadata": {
                "researchDate": datetime.now().isoformat(),
                "scrapingCost": research_data.get('scraping_cost', 0),
                "deepResearchCost": 0,
                "totalCost": research_data.get('scraping_cost', 0)
            }
        }
    
    def save_outputs(self, company: Dict[str, Any], research_data: Dict[str, Any]):
        """Save all output formats"""
        safe_name = company['company_name'].replace(' ', '_').replace('/', '_')
        
        # Save Markdown
        markdown_content = self.generate_markdown_report(company, research_data)
        markdown_path = self.output_dir / 'markdown' / f"{safe_name}.md"
        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        # Save JSON
        json_content = self.generate_json_output(company, research_data)
        json_path = self.output_dir / 'json' / f"{safe_name}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_content, f, indent=2)
        
        logger.info(f"Saved outputs for {company['company_name']}")
    
    async def process_company_batch(self, companies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process a batch of companies in parallel"""
        results = []
        
        # Phase 1: Scrape all companies in parallel
        logger.info(f"Phase 1: Scraping {len(companies)} companies...")
        scraping_tasks = [self.scrape_company_data(company) for company in companies]
        scraping_results = await asyncio.gather(*scraping_tasks)
        
        # Phase 2: Start deep research for each company
        logger.info(f"Phase 2: Deep research disabled; skipping")
        for scraped_data in scraping_results:
            company = scraped_data['company']
            results.append(scraped_data)
        
        return results
    
    async def wait_for_deep_research(self, results: List[Dict[str, Any]], timeout: int = 1800):
        return results
    
    def generate_master_csv(self, all_results: List[Dict[str, Any]]):
        """Generate master CSV with all results"""
        rows = []
        
        for result in all_results:
            company = result['company']
            
            # Extract key intelligence
            extracted = result.get('scraping_results', {}).get('extracted_data', {})
            deep_research = {}
            
            row = {
                'Company Name': company['company_name'],
                'Website': company.get('website', ''),
                'Founded Year': company.get('founded_year', ''),
                'Revenue Range': company.get('revenue_range', ''),
                'Employee Range': company.get('employee_range', ''),
                'Industry': company.get('industry', ''),
                'Sub-Industry': company.get('sub_industry', ''),
                'Ownership Type': company.get('ownership_type', ''),
                'LinkedIn URL': company.get('linkedin_url', ''),
                'City': company.get('city', ''),
                'State': company.get('state', ''),
                'Country': company.get('country', ''),
                
                # Scraped intelligence
                'Technology Stack': str(extracted.get('technology_stack', ''))[:500] if isinstance(extracted, dict) else '',
                'Recent News': str(extracted.get('recent_news', ''))[:500] if isinstance(extracted, dict) else '',
                'Digital Initiatives': str(extracted.get('digital_initiatives', ''))[:500] if isinstance(extracted, dict) else '',
                
                # Deep research status
                'Deep Research Status': 'disabled',
                'Deep Research Summary': '',
                
                # Costs
                'Web Scraping Cost': f"${result.get('scraping_cost', 0):.4f}",
                'Deep Research Cost': f"$0.00",
                'Total Research Cost': f"${result.get('scraping_cost', 0):.2f}",
                
                'Research Date': datetime.now().strftime('%Y-%m-%d')
            }
            
            rows.append(row)
        
        # Save CSV using Polars (faster than pandas)
        csv_path = self.output_dir / 'csv' / f'master_research_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
        if rows:
            # Convert to Polars DataFrame and save
            df = pl.DataFrame(rows)
            df.write_csv(csv_path)
            logger.info(f"Generated master CSV with Polars: {csv_path}")
            logger.info(f"CSV contains {len(df)} rows and {len(df.columns)} columns")
    
    async def run_research_pipeline(self, limit: Optional[int] = None, batch_size: int = 10):
        """Run the complete research pipeline"""
        # Load companies
        companies = self.load_companies()
        
        if limit:
            companies = companies[:limit]
            logger.info(f"Processing first {limit} companies")
        
        all_results = []
        
        # Process in batches
        for i in range(0, len(companies), batch_size):
            batch = companies[i:i + batch_size]
            logger.info(f"\n{'='*60}")
            logger.info(f"Processing batch {i//batch_size + 1} ({len(batch)} companies)")
            logger.info(f"{'='*60}")
            
            # Process batch
            batch_results = await self.process_company_batch(batch)
            
            completed_results = await self.wait_for_deep_research(batch_results)
            
            all_results.extend(completed_results)
            
            # Save progress
            self.generate_master_csv(all_results)
            
            # Print cost summary
            total_scraping = sum(r.get('scraping_cost', 0) for r in all_results)
            total_deep_research = 0.0
            
            logger.info(f"""
💰 Cost Summary:
- Web Scraping: ${total_scraping:.2f}
- Deep Research: ${total_deep_research:.2f}
- Total: ${total_scraping + total_deep_research:.2f}
- Companies Processed: {len(all_results)}
""")
        
        logger.info(f"\n✅ Research pipeline complete! Processed {len(all_results)} companies")
        return all_results


async def main():
    """Main execution"""
    csv_path = "data/raw/2025-07-07/331_070725_COMPANY.csv"
    
    pipeline = ParallelCompanyResearch(csv_path)
    
    # Process first 10 companies as a test
    await pipeline.run_research_pipeline(limit=10, batch_size=5)


if __name__ == "__main__":
    asyncio.run(main())