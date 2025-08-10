# GTM Mastermind Quick Start - 5 Minute Setup

## 🎯 What This Is

GTM Mastermind is your template for building AI-powered sales intelligence systems. It automates account research using OpenAI's Deep Research API and provides your sales team with actionable insights.

## 🚀 Fastest Setup (< 5 minutes)

### 1. Run Setup Script
```bash
cd gtm-mastermind-template/
./setup_new_client.sh
```

Enter when prompted:
- Client name (e.g., "Acme Corp")
- Industry (e.g., "SaaS")
- Product name (e.g., "Acme Analytics")
- Project folder name (e.g., "acme-gtm-alpha")

### 2. Add Your Data
```bash
cd ../[your-project-folder]/data/

# Add your CSV file with target accounts:
# Must have columns: company_name, domain, industry
```

### 3. Configure API Keys
```bash
# Edit .env file
nano .env

# Add at minimum:
OPENAI_API_KEY=sk-...
```

### 4. Install & Run
```bash
# Set up Python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Copy env example and add your keys
cp env.example .env
nano .env

# Test with one company
python scripts/quick_company_test.py
```

## 📁 What Goes Where

```
your-project/
├── data/           # PUT YOUR CSV FILES HERE
│   └── target_accounts.csv
├── scripts/        # YOUR PYTHON SCRIPTS GO HERE
│   └── deep_research.py
├── outputs/        # REPORTS WILL BE SAVED HERE
│   └── research_results/
└── config/         # CUSTOMIZE PROMPTS HERE
    └── research_prompts.py
```

## ✅ You're Ready When...

1. ✅ Your target accounts CSV is in /data
2. ✅ Your OpenAI API key is in .env
3. ✅ Python environment is activated
4. ✅ `python scripts/quick_company_test.py` runs successfully

## 🏃‍♂️ First Test

```python
# Quick test script
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

# Test API connection
response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=[{"role": "user", "content": "Hello"}]
)
print("✅ API Connected!" if response else "❌ API Error")
```

## 🆘 Need Help?

1. Check README.md for detailed instructions
2. Review docs/TEMPLATE_INSTRUCTIONS.md
3. Look at example files in /data and /scripts

## 🎉 Next Steps

1. Customize prompts in `config/research_prompts.py`
2. Run research on your first account
3. Show results to your client
4. Scale to full account list

---
**Remember:** Start with 5 accounts, validate results, then scale up!