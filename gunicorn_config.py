"""
Gunicorn configuration file for Django movie website
"""

import multiprocessing

# Bind to the socket
bind = "unix:/home/ubuntu/WEBSITE/movies.sock"

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gthread"
threads = 2

# Logging
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"

# Process naming
proc_name = "movies_gunicorn"

# Timeout settings
timeout = 120
keepalive = 5

# Security settings
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Server mechanics
user = "ubuntu"
group = "www-data"
umask = 0o007
reload = True

# Django settings
raw_env = [
    "DJANGO_SETTINGS_MODULE=movies.movies.production",
]