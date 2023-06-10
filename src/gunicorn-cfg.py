# -*- encoding: utf-8 -*-
import os
workers = 1
accesslog = '-'
loglevel = 'debug' if (os.getenv('DEBUG', 'False') == 'True') else 'info'
capture_output = True
enable_stdio_inheritance = True
bind = "0.0.0.0:5000"
