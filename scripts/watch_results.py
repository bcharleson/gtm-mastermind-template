#!/usr/bin/env python3
"""
Watch for new research results as they complete
"""

import os
import time
import json
from pathlib import Path
from datetime import datetime

class ResultWatcher:
    def __init__(self):
        self.output_dir = Path("gtm-alpha-project/outputs/company_research")
        self.seen_files = set()
        
        # Initialize with existing files
        for f in self.output_dir.glob("json/*.json"):
            self.seen_files.add(f.name)
    
    def check_new_results(self):
        """Check for newly completed research"""
        new_results = []
        
        for json_file in self.output_dir.glob("json/*.json"):
            if json_file.name not in self.seen_files:
                try:
                    with open(json_file, 'r') as f:
                        data = json.load(f)
                    
                    # Deep research removed in template; mark JSON seen without processing
                    self.seen_files.add(json_file.name)
                except:
                    pass
        
        return new_results
    
    def display_result_summary(self, result):
        """Display a summary of a new result"""
        print(f"\n{'='*60}")
        print(f"🎉 NEW RESEARCH COMPLETED: {result['company']}")
        print(f"{'='*60}")
        print(f"📄 Report length: {result['report_length']:,} characters")
        print(f"🔗 Citations: {result['citations']}")
        print(f"💰 Cost: ${result['cost']:.2f}")
        print(f"📁 File: {result['file']}")
        
        # Show preview of the markdown report
        markdown_file = self.output_dir / 'markdown' / result['file'].replace('.json', '.md')
        if markdown_file.exists():
            print(f"\n📝 Report Preview:")
            print("-" * 60)
            with open(markdown_file, 'r') as f:
                content = f.read()
                # Show first 500 chars
                preview = content[:500] + "..." if len(content) > 500 else content
                print(preview)
    
    def watch_continuous(self):
        """Continuously watch for new results"""
        print("\n" + "="*60)
        print("👀 WATCHING FOR NEW RESEARCH RESULTS")
        print("="*60)
        print(f"Monitoring: {self.output_dir}")
        print("Press Ctrl+C to stop\n")
        
        check_count = 0
        
        try:
            while True:
                new_results = self.check_new_results()
                
                if new_results:
                    for result in new_results:
                        self.display_result_summary(result)
                        print(f"\n✨ Total completed: {len(self.seen_files)}")
                else:
                    check_count += 1
                    if check_count % 12 == 0:  # Every minute
                        print(f"⏳ {datetime.now().strftime('%H:%M:%S')} - Still watching... ({len(self.seen_files)} completed so far)")
                
                time.sleep(5)  # Check every 5 seconds
                
        except KeyboardInterrupt:
            print("\n\n✋ Stopped watching")
            print(f"📊 Final count: {len(self.seen_files)} companies with completed research")

if __name__ == "__main__":
    watcher = ResultWatcher()
    watcher.watch_continuous()