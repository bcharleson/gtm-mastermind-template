# GTM Mastermind Template

A comprehensive Go-To-Market (GTM) research automation template for B2B companies. This template provides parallel web scraping, deep research integration, and comprehensive reporting capabilities.

## 🚀 Features

- **Parallel Web Scraping**: Uses Crawl4AI with proxy support for cost-effective data collection
- **Deep Research Integration**: OpenAI Deep Research API for comprehensive company analysis
- **Smart Cost Optimization**: Automatic fallback from cheap to premium scraping methods
- **Comprehensive Outputs**: Markdown reports, JSON data, and CSV exports
- **Real-time Monitoring**: Track progress, costs, and results as they come in

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key (for Deep Research)
- Firecrawl API key (optional, for fallback scraping)
- Proxy service (optional but recommended for scale)

## 🛠️ Setup

1. **Clone the template**:
   ```bash
   cp -r gtm-mastermind-template your-project-name
   cd your-project-name
   ```

2. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

4. **Configure environment**:
   ```bash
   cp env.example .env
   # Edit .env with your API keys and settings
   ```

5. **Prepare your data**:
   - Add your company list as a CSV file in `data/companies.csv`
   - Required columns: Company Name, Website
   - Optional columns: Industry, Revenue, Employees, LinkedIn URL, etc.

## 🚦 Quick Start

1. **Test with a few companies**:
   ```bash
   python scripts/quick_company_test.py
   ```

2. **Run full pipeline**:
   ```bash
   python scripts/run_parallel_research.py 10 5
   # Processes 10 companies in batches of 5
   ```

3. **Monitor progress**:
   ```bash
   python scripts/monitor_research_progress.py --continuous
   ```

## 📊 Scripts Overview

### Core Pipeline
- `run_parallel_research.py` - Main pipeline orchestrator
- `parallel_company_research.py` - Core research logic
- `smart_scraping_workflow.py` - Intelligent web scraping
- `deep_research_async.py` - OpenAI Deep Research integration

### Monitoring & Management
- `monitor_research_progress.py` - Track overall progress
- `track_deep_research.py` - Monitor research task status
- `track_costs.py` - Cost tracking and projections
- `watch_results.py` - Real-time result notifications
- `pipeline_manager.py` - Interactive pipeline control

### Testing & Demos
- `quick_company_test.py` - Test with single company
- `test_proxy_scraping.py` - Verify proxy configuration
- `demo_research_pipeline.py` - Demo with small batch

## 📁 Output Structure

```
outputs/
├── company_research/
│   ├── markdown/         # Detailed research reports
│   ├── json/            # Structured data
│   └── csv/             # Master spreadsheet
├── deep_research_tasks.json  # Task tracking
└── research_pipeline.log     # Detailed logs
```

## 💰 Cost Estimates

- **Web Scraping**: ~$0.001-0.01 per company
- **Deep Research**: ~$0.15-0.50 per company
- **Total**: ~$0.15-0.51 per company

## 🔧 Configuration

### Environment Variables (.env)

```bash
# OpenAI (Required for Deep Research)
OPENAI_API_KEY=your-key-here

# Web Scraping
FIRECRAWL_API_KEY=your-key-here
DEEPSEEK_API_KEY=your-key-here

# Proxy Configuration
CRAWL4AI_USE_PROXY=true
PROXY_TYPE=rotating
ROTATING_PROXY_URL=http://your-proxy:port
ROTATING_PROXY_USERNAME=username
ROTATING_PROXY_PASSWORD=password

# Cost Limits
OPENAI_COST_LIMIT_DAILY=50.00
SCRAPING_COST_LIMIT_DAILY=5.00
```

## 🎯 Customization Guide

### 1. Modify Research Prompts
Edit `config/research_prompts.py` to customize what information to extract.

### 2. Add Industry-Specific Logic
Update the `analyze_company_gtm_relevance()` method in `parallel_company_research.py`.

### 3. Custom Output Formats
Modify the `generate_markdown_report()` and `generate_json_output()` methods.

### 4. Integration Points
- **CRM Export**: Adapt `generate_master_csv()` for your CRM format
- **Webhook Notifications**: Add to `deep_research_async.py`
- **Database Storage**: Extend `save_outputs()` method

## 🚨 Troubleshooting

### Common Issues

1. **"Module not found" errors**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Proxy not working**:
   ```bash
   python scripts/test_proxy_scraping.py
   ```

3. **Deep Research tasks stuck**:
   ```bash
   python scripts/track_deep_research.py
   ```

## 📈 Scaling Tips

1. **Batch Size**: Adjust based on your API limits (default: 10)
2. **Proxy Rotation**: Essential for large-scale scraping
3. **Cost Management**: Set daily limits in .env
4. **Parallel Tasks**: OpenAI allows ~10 concurrent deep research tasks

## 🤝 Contributing

This is a template repository. Fork it and customize for your needs!

## 📄 License

MIT License - See LICENSE file for details