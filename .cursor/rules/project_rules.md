### GTM Mastermind Template — Project Rules and Scope

These rules define what this repository is (and is not), how to work within it, and what must never be committed. They distill the intent of QUICK_START.md and README into enforceable, actionable guidance.

### Purpose and Scope
- **Purpose**: A clean, forkable template for building AI-powered B2B research pipelines using OpenAI Deep Research plus cost-effective scraping fallbacks.
- **In-Scope**: General, reusable pipeline code, example scripts, prompt configuration, and folder structure that help others run the template out-of-the-box.
- **Out-of-Scope**: Any personal, client-specific, or proprietary scrapers, datasets, or secrets.

### Directory Contract
- `config/`: Public, templated prompt config. May be customized but should remain generic.
- `data/`: Only example/template files belong in version control. Real datasets must not be committed.
  - Allowed: `data/companies_template.csv`
  - Disallowed: Any other CSVs (these are ignored by default)
- `scripts/`: General-purpose, reusable scripts only. Domain- or client-specific scrapers must stay local and are ignored by default (see Exclusions).
- `outputs/`: Generated artifacts only; never commit. Contains logs, jsonl, markdown, csv results.
- `demo/outputs/`: Generated demo outputs; never commit.

### Secrets and Environment
- Never commit secrets. Use `.env` locally and do not version it.
- The template ships with `.env.example`. Forkers copy it to `.env` and fill values.
- Required keys (see README for details):
  - `OPENAI_API_KEY`
  - Optional: `FIRECRAWL_API_KEY`, `DEEPSEEK_API_KEY`, proxy credentials, cost limits

### Execution Standards
- Use a Python virtual environment (`python3 -m venv venv; source venv/bin/activate`).
- Install dependencies from `requirements.txt`.
- Run general-purpose scripts only (see next section).

### Scripts Policy
- Allowed (template/general purpose):
  - Research orchestration, parallelization, monitoring, cost tracking, data cleaners, safe CSV creators, quick tests, and generic scraping workflow helpers.
  - Examples: `run_parallel_research.py`, `parallel_company_research.py`, `smart_scraping_workflow.py`, `quick_company_test.py`, `track_costs.py`, `watch_results.py`, etc.
- Excluded (personal or domain-specific; kept local only and ignored by git):
  - `scripts/dental_us_scrape_to_clay.py`
  - `scripts/hvac_pool_scrape_to_clay.py`
  - `scripts/enterprise_dev_to_clay.py`
  - Any new client- or niche-specific scrapers should follow the same pattern: keep locally and add to `.gitignore`.

### Data and Outputs Policy
- Data: Only include small, safe templates (e.g., `data/companies_template.csv`). Real datasets are local-only.
- Outputs: Never commit results, logs, or transient state under `outputs/` or `demo/outputs/`.

### Quality and Safety
- Prefer simple, readable solutions and avoid duplication.
- Add error handling around network and API operations. Respect cost limits via environment variables.
- Avoid hardcoding magic numbers; prefer named constants.
- Treat proxies and scraping as optional fallbacks; keep the default template functional with just an OpenAI key.

### Contribution Notes (for public forks)
- Keep contributions generic and reusable.
- Do not submit PRs that add secrets, personal datasets, or client-specific logic.
- If adding a new optional integration, gate it behind env flags and add keys to `.env.example` only.

---
By following these rules, forks remain clean, secure, and easy to run, while personal or proprietary components stay local.


