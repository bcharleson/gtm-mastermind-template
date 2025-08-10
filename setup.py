#!/usr/bin/env python3
"""
Setup script for GTM Mastermind Template
"""

import os
import sys
import shutil
from pathlib import Path

def setup_project():
    """Setup a new GTM research project"""
    print("\n" + "="*60)
    print("🚀 GTM MASTERMIND SETUP")
    print("="*60)
    
    # Get project name
    project_name = input("\nEnter project name (e.g., 'gtm-acme-corp'): ").strip()
    if not project_name:
        print("❌ Project name required")
        return
    
    # Create project directory
    project_path = Path.cwd().parent / project_name
    if project_path.exists():
        overwrite = input(f"⚠️  {project_name} already exists. Overwrite? (y/N): ")
        if overwrite.lower() != 'y':
            return
        shutil.rmtree(project_path)
    
    # Copy template
    template_path = Path.cwd()
    shutil.copytree(template_path, project_path, ignore=shutil.ignore_patterns(
        '__pycache__', '*.pyc', '.git', 'venv', '*.log', 'outputs/*'
    ))
    
    print(f"✅ Created project: {project_path}")
    
    # Setup instructions
    print("\n📋 Next steps:")
    print(f"1. cd {project_path}")
    print("2. python3 -m venv venv")
    print("3. source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
    print("4. pip install -r requirements.txt")
    print("5. playwright install chromium")
    print("6. cp .env.example .env")
    print("7. Edit .env with your API keys")
    print("8. Add your company list to data/companies.csv")
    print("9. python scripts/quick_company_test.py  # Test setup")
    
    # Customize for specific industry?
    customize = input("\n🎯 Customize for specific industry? (y/N): ")
    if customize.lower() == 'y':
        print("\nAvailable industries:")
        industries = ["Construction", "Healthcare", "Manufacturing", "Financial Services", 
                     "Retail", "Technology", "Other"]
        for i, ind in enumerate(industries, 1):
            print(f"{i}. {ind}")
        
        choice = input("\nSelect industry (1-7): ")
        try:
            industry = industries[int(choice) - 1]
            
            # Update configuration
            config_file = project_path / "config" / "project_config.json"
            config = {
                "project_name": project_name,
                "industry": industry,
                "created": str(Path.cwd()),
                "template_version": "1.0.0"
            }
            
            import json
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"✅ Configured for {industry} industry")
        except:
            print("⚠️  Invalid selection, using generic configuration")
    
    print("\n✨ Setup complete!")
    print(f"📁 Your project is ready at: {project_path}")

if __name__ == "__main__":
    setup_project()