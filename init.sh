#!/bin/bash
# source /home/$USER/.bash_profile

module purge
module load jdk/1.8.0_271
module load anaconda3/2020.02
module load hadoop/3.3.0
module load spark/2.4.7
module load pyspark/2.4.7
module load mysql/8.0.22

pip install --user mysql-connector-python

cd /home/$USER/decahose_visualization_setup
python initialization.py --config_file $1
mysqld --initialize-insecure

echo 'creating table...'
nohup mysqld > my.log 2>&1 &
echo $! > save_pid.txt

sleep 10
mysql < /home/$USER/create_table.sql

kill -9 `cat save_pid.txt`
rm save_pid.txt
rm /home/$USER/create_table.sql

echo 'set up finish!'

# schedule update with crontab
# 0 22 * * * /home/$USER/decahose_visualization_setup/daily_update.sh $1
