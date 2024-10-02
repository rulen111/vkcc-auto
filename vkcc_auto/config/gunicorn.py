import multiprocessing
import os

bind = os.getenv("WEB_BIND", "0.0.0.0:8000")

workers = int(os.getenv("WEB_CONCURRENCY", 4))
threads = int(os.getenv("PYTHON_MAX_THREADS", 1))
