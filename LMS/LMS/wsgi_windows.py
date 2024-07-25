"""
WSGI config for LMS project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
import sys
import site


os.environ["DJANGO_SETTINGS_MODULE"] = "LMS.settings"
           
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LMS.settings')
os.environ['HTTPS'] = "on"
sys.path.append('C:/Users/user/Desktop/NGANACONDA/Projects/lms-web/LMS/LMS')
sys.path.append('C:/Users/user/Desktop/NGANACONDA/Projects/lms-web/LMS')
sys.path.append('C:/Users/user/Desktop/NGANACONDA/Projects/lms-web/LMS/core')
sys.path.append('C:/Users/user/Desktop/NGANACONDA/Projects/lms-web/venv/Lib/site-packages')
application = get_wsgi_application()
