#!/usr/bin/env python3
"""
Pipeline Manager - Control and monitor the research pipeline
"""

import os
import sys
import subprocess
import signal
from pathlib import Path

def show_menu():
    """Show management menu"""
    print("\n" + "="*60)
    print("🎛️  RESEARCH PIPELINE MANAGER")
    print("="*60)
    print("\n1. Check pipeline status")
    print("2. Monitor progress (continuous)")
    print("3. Track costs")
    print("4. Pause pipeline")
    print("5. Resume pipeline")
    print("6. View recent logs")
    print("7. Exit")
    print("\nSelect option (1-7): ", end="")

def check_status():
    """Check if pipeline is running"""
    try:
        result = subprocess.run(['pgrep', '-f', 'run_parallel_research.py'], capture_output=True, text=True)
        if result.stdout.strip():
            pid = result.stdout.strip()
            print(f"\n✅ Pipeline is running (PID: {pid})")
            return pid
        else:
            print(f"\n⚠️  Pipeline is not running")
            return None
    except:
        print("\n❌ Error checking status")
        return None

def monitor_progress():
    """Run progress monitor"""
    subprocess.run([sys.executable, 'gtm-alpha-project/scripts/monitor_research_progress.py'])

def monitor_continuous():
    """Run continuous monitor"""
    subprocess.run([sys.executable, 'gtm-alpha-project/scripts/monitor_research_progress.py', '--continuous'])

def track_costs():
    """Track costs"""
    subprocess.run([sys.executable, 'gtm-alpha-project/scripts/track_costs.py'])

def pause_pipeline():
    """Pause the pipeline"""
    pid = check_status()
    if pid:
        try:
            os.kill(int(pid), signal.SIGSTOP)
            print("⏸️  Pipeline paused")
        except:
            print("❌ Error pausing pipeline")
    else:
        print("No pipeline to pause")

def resume_pipeline():
    """Resume the pipeline"""
    pid = check_status()
    if pid:
        try:
            os.kill(int(pid), signal.SIGCONT)
            print("▶️  Pipeline resumed")
        except:
            print("❌ Error resuming pipeline")
    else:
        print("No pipeline to resume. Start a new one with:")
        print("python3 gtm-alpha-project/scripts/run_parallel_research.py 331 10")

def view_logs():
    """View recent logs"""
    log_file = Path("gtm-alpha-project/outputs/research_pipeline.log")
    if log_file.exists():
        subprocess.run(['tail', '-n', '50', str(log_file)])
    else:
        print("No log file found")

def main():
    """Main menu loop"""
    while True:
        show_menu()
        try:
            choice = input().strip()
            
            if choice == '1':
                check_status()
                monitor_progress()
            elif choice == '2':
                monitor_continuous()
            elif choice == '3':
                track_costs()
            elif choice == '4':
                pause_pipeline()
            elif choice == '5':
                resume_pipeline()
            elif choice == '6':
                view_logs()
            elif choice == '7':
                print("\n👋 Goodbye!")
                break
            else:
                print("Invalid option")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()