# GTM Mastermind Template

A scraping-first Go-To-Market (GTM) automation template for B2B teams. Collect data from the web using Crawl4AI, enrich or summarize with lightweight GPT-5 nano transforms, normalize with pandas/Polars, and ship results to a Clay table or n8n via webhook. Firecrawl and OpenAI Deep Research are optional add-ons.

## 🚀 Features

- **Parallel Web Scraping (Core)**: Crawl4AI with optional proxies for scale and resiliency
- **Lightweight AI Transforms**: GPT-5 nano for parsing/summarization/classification (optional)
- **Fallback Providers (Optional)**: Firecrawl when Crawl4AI is insufficient
- **Deep Research (Optional)**: OpenAI Deep Research if deeper analysis is required
- **Data Normalization**: Pandas/Polars pipelines for clean, tabular outputs
- **Webhook Delivery**: Send results to Clay or n8n via `WEBHOOK_URL`
- **Monitoring & Costs**: Real-time tracking and cost guardrails

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key (optional for GPT-5 nano transforms and/or Deep Research)
- Firecrawl API key (optional for fallback scraping)
- Proxy service (optional but recommended for scale)
- A `WEBHOOK_URL` (Clay table webhook or your n8n endpoint)

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
   - Start from `data/companies_template.csv` and add your rows
   - Recommended columns: Company Name, Website, Industry, LinkedIn URL, etc.
   - Set your `WEBHOOK_URL` in `.env` for Clay or n8n

## 🚦 Quick Start

1. **Test with a few companies**:
   ```bash
   python scripts/quick_company_test.py
   ```

2. **Run full scraping pipeline**:
   ```bash
   python scripts/run_parallel_research.py 10 5
   # Processes 10 companies in batches of 5
   ```

3. **Monitor progress**:
   ```bash
   python scripts/watch_results.py --continuous
   ```

## 📊 Scripts Overview

### Core Pipeline
- `run_parallel_research.py` - Main scraping pipeline orchestrator
- `parallel_company_research.py` - Core scraping + AI-transform logic
- `smart_scraping_workflow.py` - Crawl4AI-first strategy with optional fallbacks

### Monitoring & Delivery
- `watch_results.py` - Real-time result notifications
- `track_costs.py` - Cost tracking and projections
- `pipeline_manager.py` - Interactive pipeline control

### Testing & Utilities
- `quick_company_test.py` - Test with single company
- `test_proxy_scraping.py` - Verify proxy configuration

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

## 💰 Cost Estimates (Typical)

- **Web Scraping (Crawl4AI)**: Low cost, proxy-dependent
- **Firecrawl (Optional)**: Varies by plan/usage
- **AI Transforms (GPT-5 nano)**: Minimal
- **Deep Research (Optional)**: Higher, only if enabled

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

### 1. Modify Extraction Prompts
Edit `config/research_prompts.py` to control what to extract or summarize.

### 2. Add Industry-Specific Logic
Update `analyze_company_gtm_relevance()` in `parallel_company_research.py`.

### 3. Output Formats
Adapt CSV/JSON normalization (pandas/Polars) and markdown generation as needed.

### 4. Integration Points
- **Webhook Delivery**: Use `WEBHOOK_URL` (Clay table webhook or n8n)
- **CRM Export**: Extend CSV to match your CRM
- **Storage**: Extend `save_outputs()` to push to DB/S3

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