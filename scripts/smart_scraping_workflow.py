#!/usr/bin/env python3
"""
Smart Scraping Workflow
Automatically chooses between Crawl4AI (with DeepSeek/Grok) and Firecrawl
Includes proxy rotation for large-scale scraping
"""

import os
import json
import asyncio
import random
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dotenv import load_dotenv
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy, JsonCssExtractionStrategy
from firecrawl import FirecrawlApp
import httpx
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SmartScrapingWorkflow:
    """
    Intelligent scraping that starts with Crawl4AI (cheap) 
    and falls back to Firecrawl (reliable) when needed
    """
    
    def __init__(self):
        # Initialize Firecrawl
        self.firecrawl = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))
        
        # LLM provider configuration
        self.llm_provider = os.getenv('CRAWL4AI_LLM_PROVIDER', 'deepseek')
        self.use_proxy = os.getenv('CRAWL4AI_USE_PROXY', 'false').lower() == 'true'
        
        # Cost tracking
        self.costs = {
            'crawl4ai': 0.0,
            'firecrawl': 0.0,
            'total_pages': 0
        }
        
        # Proxy pool
        self.proxy_pool = []
        if self.use_proxy:
            self._load_proxy_pool()
    
    def _load_proxy_pool(self):
        """Load proxy configuration"""
        proxy_type = os.getenv('PROXY_TYPE', 'single')
        
        if proxy_type == 'single':
            # Static proxy
            if os.getenv('PROXY_URL'):
                self.proxy_pool.append({
                    'url': os.getenv('PROXY_URL'),
                    'username': os.getenv('PROXY_USERNAME'),
                    'password': os.getenv('PROXY_PASSWORD')
                })
                logger.info(f"Loaded single proxy")
        
        elif proxy_type == 'rotating':
            # Rotating proxy configuration
            rotating_url = os.getenv('ROTATING_PROXY_URL')
            if rotating_url:
                self.proxy_pool.append({
                    'url': rotating_url,
                    'username': os.getenv('ROTATING_PROXY_USERNAME'),
                    'password': os.getenv('ROTATING_PROXY_PASSWORD'),
                    'type': 'rotating'
                })
                logger.info(f"Loaded rotating proxy: {rotating_url}")
    
    def _get_proxy(self) -> Optional[Dict]:
        """Get a proxy from the pool"""
        if not self.proxy_pool:
            return None
        return random.choice(self.proxy_pool)
    
    def _get_llm_config(self) -> Tuple[str, str, str]:
        """Get LLM configuration based on provider"""
        if self.llm_provider == 'deepseek':
            return (
                'deepseek',
                os.getenv('DEEPSEEK_API_KEY'),
                os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')
            )
        elif self.llm_provider == 'grok':
            return (
                'grok',
                os.getenv('GROK_API_KEY'),
                os.getenv('GROK_MODEL', 'grok-3-mini')
            )
        else:
            return (
                'openai',
                os.getenv('OPENAI_API_KEY'),
                os.getenv('OPENAI_MODEL', 'gpt-5-nano')
            )
    
    async def scrape_url(self, url: str, extraction_instructions: str = None) -> Dict:
        """
        Smart scraping that tries Crawl4AI first, then Firecrawl
        
        Args:
            url: URL to scrape
            extraction_instructions: What to extract from the page
            
        Returns:
            Scraped data with source information
        """
        logger.info(f"Smart scraping: {url}")
        
        # Step 1: Try Crawl4AI (cheapest option)
        crawl4ai_result = await self._try_crawl4ai(url, extraction_instructions)
        
        if crawl4ai_result and crawl4ai_result.get('success'):
            logger.info("✅ Crawl4AI succeeded")
            return crawl4ai_result
        
        logger.warning("⚠️ Crawl4AI failed, trying Firecrawl...")
        
        # Step 2: Fallback to Firecrawl
        firecrawl_result = await self._try_firecrawl(url, extraction_instructions)
        
        if firecrawl_result and firecrawl_result.get('success'):
            logger.info("✅ Firecrawl succeeded")
            return firecrawl_result
        
        logger.error("❌ Both scrapers failed")
        return {
            'success': False,
            'error': 'Both Crawl4AI and Firecrawl failed',
            'url': url
        }
    
    async def _try_crawl4ai(self, url: str, extraction_instructions: str = None) -> Dict:
        """Try scraping with Crawl4AI using cheap LLMs"""
        try:
            # Get LLM configuration
            provider, api_key, model = self._get_llm_config()
            
            # Get proxy if enabled
            proxy = self._get_proxy() if self.use_proxy else None
            
            # Configure browser with proxy
            browser_config = {
                'headless': True,
                'viewport': {'width': 1920, 'height': 1080}
            }
            
            if proxy:
                browser_config['proxy'] = {
                    'server': proxy['url'],
                    'username': proxy.get('username'),
                    'password': proxy.get('password')
                }
            
            async with AsyncWebCrawler(**browser_config) as crawler:
                # First, run a basic crawl to collect page content
                result = await crawler.arun(url=url)
                
                if result.success:
                    # Optional: Run LLM extraction with OpenAI (GPT-5 nano) if configured
                    extracted_json = None
                    if provider == 'openai' and api_key:
                        try:
                            instruction = extraction_instructions or (
                                """
                                Extract concise business intelligence:
                                - company_description (1-2 sentences)
                                - products_services (bullet list)
                                - leadership (C-suite names and titles if present)
                                - technology_mentions (keywords like Procore, P6, Autodesk, Oracle, AI, cloud)
                                - recent_news (last 12 months)
                                Return valid JSON with these keys.
                                """
                            )
                            llm_strategy = LLMExtractionStrategy(
                                provider='openai',
                                api_token=api_key,
                                model=model,
                                instruction=instruction
                            )
                            llm_result = await crawler.arun(url=url, extraction_strategy=llm_strategy)
                            if llm_result.success and llm_result.extracted_content:
                                extracted_json = json.loads(llm_result.extracted_content)
                        except Exception as llm_err:
                            logger.debug(f"LLM extraction skipped: {str(llm_err)}")

                    # Track costs (approximate)
                    estimated_tokens = len(result.markdown) / 4 if result.markdown else 0
                    if provider == 'deepseek':
                        cost = (estimated_tokens / 1_000_000) * 0.14
                    elif provider == 'grok':
                        cost = (estimated_tokens / 1_000_000) * 0.10  # Estimate
                    else:
                        # Default to inexpensive GPT-5 nano pricing; allow override via env
                        openai_nano_cost_per_m = float(os.getenv('OPENAI_NANO_COST_PER_M', '0.5'))
                        cost = (estimated_tokens / 1_000_000) * openai_nano_cost_per_m
                    
                    self.costs['crawl4ai'] += cost
                    self.costs['total_pages'] += 1
                    
                    return {
                        'success': True,
                        'source': 'crawl4ai',
                        'provider': provider,
                        'model': model,
                        'cost': cost,
                        'data': {
                            'markdown': result.markdown,
                            'extracted': extracted_json or (json.loads(result.extracted_content) if result.extracted_content else None),
                            'links': result.links,
                            'images': result.images if hasattr(result, 'images') else []
                        },
                        'proxy_used': proxy['url'] if proxy else None
                    }
                
        except Exception as e:
            logger.error(f"Crawl4AI error: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    async def _try_firecrawl(self, url: str, extraction_instructions: str = None) -> Dict:
        """Try scraping with Firecrawl as fallback"""
        try:
            # Updated Firecrawl v2 params
            params = {
                'formats': ['markdown'],
                'onlyMainContent': True
            }
            
            if extraction_instructions:
                params['extract'] = {
                    'prompt': extraction_instructions
                }
            
            # Firecrawl v2 API format
            result = self.firecrawl.scrape_url(url, **params)
            
            if result:
                # Track costs ($0.01 per page)
                cost = 0.01
                self.costs['firecrawl'] += cost
                self.costs['total_pages'] += 1
                
                return {
                    'success': True,
                    'source': 'firecrawl',
                    'cost': cost,
                    'data': result
                }
                
        except Exception as e:
            logger.error(f"Firecrawl error: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    async def bulk_scrape(self, urls: List[str], extraction_instructions: str = None) -> Dict:
        """
        Bulk scraping with intelligent routing
        
        Args:
            urls: List of URLs to scrape
            extraction_instructions: What to extract
            
        Returns:
            Results and cost analysis
        """
        logger.info(f"Starting bulk scrape of {len(urls)} URLs")
        
        results = []
        failed_urls = []
        
        for i, url in enumerate(urls):
            logger.info(f"Processing {i+1}/{len(urls)}: {url}")
            
            result = await self.scrape_url(url, extraction_instructions)
            
            if result['success']:
                results.append(result)
            else:
                failed_urls.append(url)
            
            # Rate limiting
            await asyncio.sleep(1)
            
            # Progress update every 10 URLs
            if (i + 1) % 10 == 0:
                self._print_cost_summary()
        
        # Final summary
        summary = {
            'total_urls': len(urls),
            'successful': len(results),
            'failed': len(failed_urls),
            'failed_urls': failed_urls,
            'costs': self.costs,
            'results': results,
            'recommendations': self._generate_recommendations()
        }
        
        return summary
    
    def _print_cost_summary(self):
        """Print current cost summary"""
        total_cost = self.costs['crawl4ai'] + self.costs['firecrawl']
        logger.info(f"""
        💰 Cost Summary:
        - Crawl4AI: ${self.costs['crawl4ai']:.4f}
        - Firecrawl: ${self.costs['firecrawl']:.2f}
        - Total: ${total_cost:.2f}
        - Pages processed: {self.costs['total_pages']}
        - Average cost per page: ${total_cost / max(self.costs['total_pages'], 1):.4f}
        """)
    
    def _generate_recommendations(self) -> Dict:
        """Generate recommendations based on scraping results"""
        total_cost = self.costs['crawl4ai'] + self.costs['firecrawl']
        avg_cost = total_cost / max(self.costs['total_pages'], 1)
        
        recommendations = {
            'cost_analysis': {
                'total_cost': total_cost,
                'average_per_page': avg_cost,
                'crawl4ai_percentage': (self.costs['crawl4ai'] / max(total_cost, 0.01)) * 100
            }
        }
        
        if self.costs['firecrawl'] > self.costs['crawl4ai'] * 10:
            recommendations['suggestion'] = "Consider investigating why Crawl4AI is failing. Maybe need better proxies?"
        elif avg_cost < 0.001:
            recommendations['suggestion'] = "Excellent cost efficiency! Crawl4AI is working well."
        else:
            recommendations['suggestion'] = "Good balance between cost and reliability."
        
        return recommendations


async def main():
    """Example usage of smart scraping workflow"""
    
    scraper = SmartScrapingWorkflow()
    
    # Example 1: Single URL with extraction
    print("📊 Example 1: Smart scraping with extraction")
    
    extraction_prompt = """
    Extract the following information:
    1. Company name and description
    2. Main products or services
    3. Recent news or announcements
    4. Technology stack mentioned
    5. Contact information
    """
    
    result = await scraper.scrape_url(
        "https://example.com",
        extraction_prompt
    )
    
    print(f"Source: {result.get('source')}")
    print(f"Cost: ${result.get('cost', 0):.4f}")
    print(f"Success: {result.get('success')}")
    
    # Example 2: Bulk scraping
    print("\n📊 Example 2: Bulk scraping")
    
    urls = [
        "https://example.com",
        "https://example.com/about",
        "https://example.com/products",
        "https://example.com/contact",
        "https://example.com/blog"
    ]
    
    bulk_results = await scraper.bulk_scrape(urls)
    
    print(f"\nBulk Scraping Summary:")
    print(f"- Total URLs: {bulk_results['total_urls']}")
    print(f"- Successful: {bulk_results['successful']}")
    print(f"- Failed: {len(bulk_results['failed_urls'])}")
    print(f"- Total Cost: ${bulk_results['costs']['crawl4ai'] + bulk_results['costs']['firecrawl']:.2f}")
    print(f"- Recommendation: {bulk_results['recommendations']['suggestion']}")


if __name__ == "__main__":
    asyncio.run(main())