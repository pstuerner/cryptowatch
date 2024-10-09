import typer
from apscheduler.schedulers.blocking import BlockingScheduler
from backend.rss.watch import RSSWatcher

app = typer.Typer()

@app.command()
def dummy():
    return True

@app.command()
def run():
    watcher = RSSWatcher()
    watcher.run()

    scheduler = BlockingScheduler()
    scheduler.add_job(watcher.run, 'interval', minutes=5)
    
    try:
        print("Started ...")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")

if __name__ == "__main__":
    app()