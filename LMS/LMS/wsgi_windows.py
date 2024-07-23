"""
WSGI config for Dice project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
import sys
import site


os.environ["DJANGO_SETTINGS_MODULE"] = "Dice.settings"
           
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Dice.settings')
os.environ['HTTPS'] = "on"
sys.path.append('C:/Users/user/Desktop/NGANACONDA/Projects/dicegame-web/Dice/Dice')
sys.path.append('C:/Users/user/Desktop/NGANACONDA/Projects/dicegame-web/Dice')
sys.path.append('C:/Users/user/Desktop/NGANACONDA/Projects/dicegame-web/Dice/core')
sys.path.append('C:/Users/user/Desktop/NGANACONDA/Projects/dicegame-web/venv/Lib/site-packages')
application = get_wsgi_application()
