
# cheat and hard-code the path.
PROJECT_ROOT=/home/brian/webapps/oebfare

# activate the oebfare virtualenv
source /home/oebfare/.virtualenv/oebfare/bin/activate

cd $PROJECT_ROOT
python manage.py retry_deferred >> $PROJECT_ROOT/logs/cron_mail.log 2>&1
