
# cheat and hard-code the path.
PROJECT_ROOT=/home/brian/webapps/oebfare

# activate the oebfare virtualenv
source /home/brian/.virtualenv/oebfare/bin/activate

cd $PROJECT_ROOT
python manage.py send_mail >> $PROJECT_ROOT/logs/cron_mail.log 2>&1
