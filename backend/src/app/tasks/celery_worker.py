from src.app.tasks.send_email import celery

if __name__ == "__main__":
    celery.worker_main(argv=["worker", "--pool=solo", "--loglevel=info"])
