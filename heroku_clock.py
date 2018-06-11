from apscheduler.schedulers.background import BlockingScheduler
from scraper.collector import collect_all_pages, collect_new_data

from pathlib import Path
home = Path.home()

sched = BlockingScheduler()

def job_function():
	collect_all_pages()
	collect_new_data();

sched.add_job(job_function,'cron', day_of_week='mon-sun', hour=11, minute=1)

sched.start()