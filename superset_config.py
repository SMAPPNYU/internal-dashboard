import os

MAPBOX_API_KEY = os.getenv('MAPBOX_API_KEY', 'pk.eyJ1IjoiMTUzNDU5OTUzIiwiYSI6ImNraHc2a25lZzFvbngyeG5wYWdiMmMzcHMifQ.JZVq1cP_pvRUIibzovh7jg')
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

