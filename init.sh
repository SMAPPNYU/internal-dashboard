#!/bin/bash

source ~/.bash_profile
source ~/.bashrc

module purge
module load jdk/1.8.0_271
module load anaconda3/2020.02
module load hadoop/3.3.0
module load spark/2.4.7
module load pyspark/2.4.7
module load mysql/8.0.22

pip install --user mysql-connector-python
pip install --user pymysql
pip install --user SQLAlchemy

# NOTE: By default Superset uses mysqlclient to connect to Mysql, but the library might not be compatible with python3
# NOTT: If you use mysqlclient, your connection string should be mysql://
#       if use pymysql, connection string should be mysql+pymysql://
# pip install mysqlclient

cd /home/$USER/internal-dashboard
python initialization.py --config_file $1

echo 'start mysqld, creat database and table...'
nohup mysqld > my.log 2>&1 &
echo $! > save_pid.txt

sleep 10
mysql < /home/$USER/create_table.sql

kill -9 `cat save_pid.txt`
rm save_pid.txt
rm /home/$USER/create_table.sql

# schedule update with crontab
# 0 22 * * * /home/$USER/internal-dashboard/daily_update.sh $1

firstString=$1
secondString="_add_to_crontab.txt"
FILE="${firstString/.json/$secondString}"
if test -f "$FILE"; then
    echo "$FILE exists."
    echo "No need to update crontab"
else 
    echo "update crontab..."	 
    echo "update crontab" > $FILE
    echo `date` >> $FILE
    (crontab -l ; echo "0 22 * * * source $HOME/.bash_profile; cd /home/$USER/internal-dashboard && ./daily_update.sh $1") | crontab
fi

echo "==============================================="
echo "======== Important Info              =========="
echo "==============================================="
echo ""
echo "init.sh has finished, please follow the next step from https://github.com/SMAPPNYU/internal-dashboard"
echo ""
echo "a new job is added to crontab. the job kills current dashboard instance (if there is one), loads new tweets, and starts a new dashboard instance evey 24 hours"
echo "use [crontab -e] to modify or delete the job"
echo ""
echo "=============================================="

exit 0
