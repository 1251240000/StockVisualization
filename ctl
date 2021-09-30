#!/usr/local/bin/python3

import sys
import os

args = sys.argv
uwsgi = os.path.join(os.path.dirname(sys.executable), 'uwsgi')

if len(args) <= 1:
    print('Usage: ctl [start|stop|reload|shell|migrate|update]')

elif args[1] == 'start':
    os.system('nohup %s --ini uwsgi.ini --pidfile uwsgi.pid -d uwsgi.log &' % uwsgi)

elif args[1] == 'stop':
    os.system('nohup %s --stop uwsgi.pid &' % uwsgi)

elif args[1] in ('reload', 'restart'):
    os.system('nohup %s --reload uwsgi.pid &' % uwsgi)

elif args[1] == 'migrate':
    os.system('%s manage.py makemigrations %s' % (sys.executable, ' '.join(args[2:])))
    os.system('%s manage.py migrate %s' % (sys.executable, ' '.join(args[2:])))

elif args[1] == 'shell':
    os.system('%s manage.py shell' % sys.executable)

elif args[1] == 'update':
    os.system('%s manage.py update_stock_list' % sys.executable)
    os.system('%s manage.py update_stock_top10' % sys.executable)
    os.system('%s manage.py update_stock_basic' % sys.executable)
