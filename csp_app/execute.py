from apscheduler.schedulers.background import BackgroundScheduler
# from pytz import timezone
from pytz import utc

scheduler = BackgroundScheduler()
scheduler.configure(timezone=utc)
# def print_lol():
#     print("lol")
from csp_app import scheduler_jobs
# scheduler.add_job(print_lol, 'interval', seconds=2)
scheduler.add_job(scheduler_jobs.RemindVendor, 'interval', hours=2)
scheduler.add_job(scheduler_jobs.DocumentReminder, 'interval', hours=2)
scheduler.add_job(scheduler_jobs.confirmJoining, 'interval', hours=24)




scheduler.start()
