#!/usr/bin/env python
# coding: utf-8

# In[63]:


# NOTE: only run this jupyter notebbook once, afterwards

# A step-by-step guide to set up visualization dashboard to HPC

# step 1: configure mysql
# step 2: configure superset
# step 3: load data into mysql
# step 4: connect superset with mysql
# step 5: write sql query and build your own dashboards!


# In[68]:


import os.path
from os import path
from pprint import pprint
import subprocess
import json
import time
import argparse

parser = argparse.ArgumentParser(description='init a new table.')
parser.add_argument('--config_file', type=str, default='config.json', help='path to config file')
args = parser.parse_args()

CONFIG = json.load(open(args.config, 'r'))

# Get environment variables
USER = os.getenv('USER')

#####################################
##### TODO: change password !    ####
#####################################
DASHBOARD_USER = CONFIG['DASHBOARD_USER_NAME']
DASHBOARD_USER_PASSWORD = CONFIG['DASHBOARD_USER_PASSWORD']
ROOT_PASSWORD = CONFIG['DASHBOARD_USER_PASSWORD']
#####################################
# TODO: change dashboard directory if you want, otherwise 
#       no need to modify the line below

# DASHBOARD_DIRECTORY will store all data related to this dashboard project
DASHBOARD_DIRECTORY = '/scratch/{}/{}'.format(USER, CONFIG['DASHBOARD_DIRECTORY_PREFIX'])
#####################################

print('Auto dashboard setup........')
print('Welcome -- {}'.format(USER))

# create dashboard directory if not exists
if not os.path.exists(DASHBOARD_DIRECTORY):
    print('create {}'.format(DASHBOARD_DIRECTORY))
    os.makedirs(DASHBOARD_DIRECTORY)
else:
    print('{} exists'.format(DASHBOARD_DIRECTORY))
    
if not os.path.exists(DASHBOARD_DIRECTORY + '/mysql'):
    print('create {}'.format(DASHBOARD_DIRECTORY + '/mysql'))
    os.makedirs(DASHBOARD_DIRECTORY + '/mysql')
else:
    print('{} exists'.format(DASHBOARD_DIRECTORY + '/mysql'))
    
if not os.path.exists(DASHBOARD_DIRECTORY + '/mysql/run'):
    os.makedirs(DASHBOARD_DIRECTORY + '/mysql/run')
if not os.path.exists(DASHBOARD_DIRECTORY + '/mysql/var'):
    os.makedirs(DASHBOARD_DIRECTORY + '/mysql/var')
if not os.path.exists(DASHBOARD_DIRECTORY + '/mysql/tmp'):
    os.makedirs(DASHBOARD_DIRECTORY + '/mysql/tmp')

if not os.path.exists(DASHBOARD_DIRECTORY + '/superset-data'):
    os.makedirs(DASHBOARD_DIRECTORY + '/superset-data')

if not os.path.exists(DASHBOARD_DIRECTORY + '/redis-data'):
    os.makedirs(DASHBOARD_DIRECTORY + '/redis-data')

MYSQL_CONFIG_FILE = "/home/{}/.my.cnf".format(USER)
MYSQL_INIT_FILE = "/home/{}/.mysqlrootpw".format(USER)

MYSQL_CONFIG = """
[mysqld]
init-file=/home/{user}/.mysqlrootpw
datadir={dashboard}/mysql/run/
tmpdir={dashboard}/mysql/tmp/

# General #
default-storage-engine = InnoDB
port                   = 3306
socket                 = {dashboard}/mysql/run/mysqld.sock
key-buffer-size        = 256M
innodb_buffer_pool_size = 20GB
innodb_parallel_read_threads = 32

[client]
user='{dashboard_user}'
password='{dashboard_user_password}'
port = 3306
socket = {dashboard}/mysql/run/mysqld.sock
""".format(**{'dashboard_user': DASHBOARD_USER,
            'dashboard_user_password': DASHBOARD_USER_PASSWORD,
            'user': USER,
            'dashboard': DASHBOARD_DIRECTORY
           })

MYSQL_INIT = """
SET sql_mode = '';
ALTER USER 'root'@'localhost' IDENTIFIED BY '{root_password}';
CREATE USER IF NOT EXISTS '{dashboard_user}'@'localhost' IDENTIFIED BY '{dashboard_user_password}';
CREATE USER IF NOT EXISTS '{dashboard_user}'@'127.0.0.1' IDENTIFIED BY '{dashboard_user_password}';
CREATE USER IF NOT EXISTS '{dashboard_user}'@'::1' IDENTIFIED BY '{dashboard_user_password}';
GRANT ALL PRIVILEGES ON *.* TO '{dashboard_user}'@'localhost' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO '{dashboard_user}'@'127.0.0.1' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO '{dashboard_user}'@'::1' WITH GRANT OPTION;
FLUSH PRIVILEGES;
""".format(**{'dashboard_user': DASHBOARD_USER,
            'dashboard_user_password': DASHBOARD_USER_PASSWORD,
            'root_password': ROOT_PASSWORD
           })

if path.exists(MYSQL_CONFIG_FILE):
    print('[WARNING] {} already exists!'.format(MYSQL_CONFIG_FILE))
else:
    cmd = """cat >{} <<EOL
    {}
    """.format(MYSQL_CONFIG_FILE, MYSQL_CONFIG)

    print('create mysql config file {}'.format(MYSQL_CONFIG_FILE))
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    
if path.exists(MYSQL_INIT_FILE):
    print('[WARNING] {} already exists!'.format(MYSQL_INIT_FILE))
else:    
    cmd = """cat >{} <<EOL
    {}
    """.format(MYSQL_INIT_FILE, MYSQL_INIT)
    print('create mysql init file {}'.format(MYSQL_INIT_FILE))
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)


SUPERSET_CONFIG = """
import os
MAPBOX_API_KEY = os.getenv('MAPBOX_API_KEY')
CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 60 * 60 * 12, # 1 day default (in secs)
    #'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'superset_',
    'CACHE_REDIS_HOST': 'redis',
    'CACHE_REDIS_PORT': 6379,
    'CACHE_REDIS_DB': 1,
    'CACHE_REDIS_URL': 'redis://localhost:6379/1'}

DATA_CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 60 * 60 * 24, # 1 day default (in secs)
    'CACHE_KEY_PREFIX': 'superset_results',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0',
}

SQLALCHEMY_DATABASE_URI = 'sqlite:////var/lib/superset/superset.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = 'thisISaSECRET_1234'
PUBLIC_ROLE_LIKE_GAMMA = True
"""


# In[71]:


# cmd = 'mysqld --initialize-insecure'
# proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

# time.sleep(3)


# cmd = 'mysql < {}'.format('{}/create_table.sql'.format(DASHBOARD_DIRECTORY))
# proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
# print(proc.communicate()[0])


# In[75]:


CREATE_TABLE_SQL = """
CREATE DATABASE IF NOT EXISTS {};
USE {};
CREATE TABLE IF NOT EXISTS {} (
  tweet_id VARCHAR(100), 
  tweet_timestamp timestamp, 
  created_at VARCHAR(100), 
  is_deleted BIGINT, 
  text TEXT(1024), 
  full_text TEXT(1024), 
  orig_user_id VARCHAR(100), 
  source TEXT(1024), 
  truncated TEXT(1024),
  in_reply_to_status_id TEXT(1024), 
  in_reply_to_user_id TEXT(1024), 
  in_reply_to_screen_name TEXT(1024), 
  coordinates TEXT(1024), 
  quote_count BIGINT, 
  reply_count BIGINT, 
  retweet_count BIGINT, 
  favorite_count BIGINT, 
  lang TEXT(1024), 
  user__id VARCHAR(100), 
  user__name VARCHAR(100), 
  user__screen_name VARCHAR(100), 
  user__location TEXT(1024),
  user__derived_location_country1 TEXT(1024), 
  user__derived_location_country_code1 TEXT(1024), 
  user__derived_location_region1 TEXT(1024), 
  user__derived_location_sub_region1 TEXT(1024), 
  user__derived_location_locality1 TEXT(1024), 
  user__derived_location_full_name1 TEXT(1024), 
  user__derived_location_geo1 TEXT(1024), 
  user__url TEXT(1024), 
  user__description TEXT(1024), 
  user__followers_count BIGINT, 
  user__friends_count BIGINT, 
  user__listed_count BIGINT, 
  user__favorites_count BIGINT, 
  user__statuses_count BIGINT, 
  user__created_at TEXT(1024), 
  entities__hashtags TEXT(1024), 
  entities__urls TEXT(1024), 
  entities__expanded_urls TEXT(1024), 
  entities__user_mentions__id TEXT(1024), 
  entities__user_mentions__name TEXT(1024), 
  entities__user_mentions__screen_name TEXT(1024), 
  entities__symbols TEXT(1024), 
  entities__entities_polls TEXT(1024), 
  entities__media__media_urls TEXT(1024), 
  entities__media__urls TEXT(1024), 
  entities__media__display_urls TEXT(1024), 
  entities__media__expanded_urls TEXT(1024), 
  entities__media__types TEXT(1024), 
  extended_entities__media_urls TEXT(1024), 
  extended_entities__urls TEXT(1024), 
  extended_entities__display_urls TEXT(1024), 
  extended_entities__expanded_urls TEXT(1024), 
  extended_entities__types TEXT(1024), 
  quoted__created_at TEXT(1024), 
  quoted__id TEXT(1024), 
  quoted__text TEXT(1024), 
  quoted__full_text TEXT(1024), 
  quoted__in_reply_to_status_id TEXT(1024), 
  quoted__in_reply_to_user_id TEXT(1024), 
  quoted__in_reply_to_screen_name TEXT(1024), 
  quoted__quote_count BIGINT, 
  quoted__reply_count BIGINT, 
  quoted__retweet_count BIGINT, 
  quoted__favorite_count BIGINT, 
  quoted__lang TEXT(1024), 
  quoted__user__id TEXT(1024), 
  quoted__user__name TEXT(1024), 
  quoted__user__screen_name TEXT(1024), 
  quoted__user__location TEXT(1024), 
  quoted__user__url TEXT(1024), 
  quoted__user__description TEXT(1024), 
  quoted__user__followers_count BIGINT, 
  quoted__user__friends_count BIGINT, 
  quoted__user__listed_count BIGINT, 
  quoted__user__favorites_count BIGINT, 
  quoted__user__statuses_count BIGINT, 
  quoted__user__created_at TEXT(1024), 
  retweeted__created_at TEXT(1024), 
  retweeted__id TEXT(1024), 
  retweeted__text TEXT(1024), 
  retweeted__full_text TEXT(1024), 
  retweeted__in_reply_to_status_id TEXT(1024), 
  retweeted__in_reply_to_user_id TEXT(1024), 
  retweeted__in_reply_to_screen_name TEXT(1024), 
  retweeted__quote_count BIGINT, 
  retweeted__reply_count BIGINT, 
  retweeted__retweet_count BIGINT, 
  retweeted__favorite_count BIGINT, 
  retweeted__lang TEXT(1024), 
  retweeted__user__id TEXT(1024), 
  retweeted__user__name TEXT(1024), 
  retweeted__user__screen_name TEXT(1024), 
  retweeted__user__location TEXT(1024), 
  retweeted__user__url TEXT(1024), 
  retweeted__user__description TEXT(1024), 
  retweeted__user__followers_count BIGINT, 
  retweeted__user__friends_count BIGINT, 
  retweeted__user__listed_count BIGINT, 
  retweeted__user__favorites_count BIGINT, 
  retweeted__user__statuses_count BIGINT, 
  retweeted__user__created_at TEXT(1024), 
  when_created timestamp,
    label_1 FLOAT,
    label_2 FLOAT,
    label_3 FLOAT,
    label_4 FLOAT,
    label_5 FLOAT,
    reserved_1 TEXT(20),
    reserved_2 TEXT(20),
    reserved_3 TEXT(20),
    reserved_4 TEXT(20),
    reserved_5 TEXT(20),
    yymmdd VARCHAR(10)
  ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC;
""".format(CONFIG['DATABASE_NAME'], 
           CONFIG['DATABASE_NAME'],
           CONFIG['TABLE_NAME'])

if not os.path.exists('/home/{}/create_table.sql'.format(USER)):
    cmd = """cat >{} <<EOL
    {}
    """.format('/home/{}/create_table.sql'.format(USER), CREATE_TABLE_SQL)
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
else:
    print('create_table.sql already exists')

print('auto setup finish')


