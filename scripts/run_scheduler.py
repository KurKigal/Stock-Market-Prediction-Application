import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scraper.scheduler import start_scheduler

if __name__ == "__main__":
    print("Starting data update scheduler...")
    start_scheduler()