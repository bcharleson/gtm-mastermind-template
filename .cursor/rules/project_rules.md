### GTM Mastermind Template — Project Rules and Scope

These rules define what this repository is (and is not), how to work within it, and what must never be committed. They distill the intent of QUICK_START.md and README into enforceable, actionable guidance.

### Purpose and Scope
- **Purpose**: A clean, forkable, scraping-first GTM template. Crawl the web (Crawl4AI-first), optionally apply lightweight GPT-5 nano transforms and add Firecrawl/Deep Research if needed, normalize with pandas/Polars, and send results to a Clay table or n8n via webhook.
- **In-Scope**: General, reusable scraping pipeline code, example scripts, prompt configuration, and folder structure that help others run the template out-of-the-box.
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
  - `WEBHOOK_URL` (Clay table webhook or n8n endpoint)
  - Optional: `OPENAI_API_KEY` (GPT-5 nano or Deep Research), `FIRECRAWL_API_KEY`, `DEEPSEEK_API_KEY`, proxy credentials, cost limits

### Execution Standards
- Use a Python virtual environment (`python3 -m venv venv; source venv/bin/activate`).
- Install dependencies from `requirements.txt`.
- Configure `WEBHOOK_URL` to deliver outputs to Clay or n8n.
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

### Professional Web Scraper Role and Process
- Role: Operate as a professional web scraper focused on discovering public resources to support B2B go‑to‑market and lead generation efforts.
- Communication First: Always communicate with and confirm requirements from the user before executing tasks or creating new scripts.
- Consulting: Professionally consult with the user to ensure clear alignment on the use of scrapers, LLM transforms, data sources, and any costs that may be incurred.
- Compliance: Follow website terms of service and robots directives where applicable, and use respectful request rates and proxy hygiene.

### Error Handling and Safe Retries
- Defensive Programming: Validate inputs, handle timeouts and HTTP errors, and guard against partial or malformed responses.
- Bounded Retries: Implement retry logic with exponential backoff and a strict maximum attempt cap to avoid infinite loops.
- Circuit Breakers: Detect repeated failures and halt the current task batch to prevent runaway costs or blocked IPs.
- Idempotency: Design webhook deliveries and writes to be idempotent where possible to avoid duplicate records.
- Observability: Emit structured logs and counters for attempts, successes, failures, and costs to aid diagnosis.

### Contribution Notes (for public forks)
- Keep contributions generic and reusable.
- Do not submit PRs that add secrets, personal datasets, or client-specific logic.
- If adding a new optional integration, gate it behind env flags and add keys to `.env.example` only.

---
By following these rules, forks remain clean, secure, and easy to run, while personal or proprietary components stay local.


