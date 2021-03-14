### Initiate MySQL database, Superset database

1. log in to greene cluster, then `cd /home/$USER`
2. `git clone git@github.com:SMAPPNYU/internal-dashboard.git`
3. `cd /home/$USER/internal-dashboard`
4. modify `config.json`
5. run `./init.sh CONFIG_FILE` (do not forget to type the first dot, replace CONFIG_FILE with your config file)
6. if there is any error, please reach out to be zc1245@nyu.edu
7. now we can proceed to the user interface, connect with MySQL database, and create our first dashboard

### Connet to Superset (the visualization tool)

1. first log in greene cluster `ssh netID@log-1.nyu.cluster`
2. find the hostname HOST via `cat /home/$USER/decahose_visualization_setup/latest_hostname.txt`
3. log out greene `exit`
2. log in greene again with port forwarding, `ssh -L 8088:HOST:8088 netID@log-1.nyu.cluster`
2. open browser, visit http://localhost:8088/

### Create the first dashboard
1. when first visiting Superset, username and password is required
2. log in using the username and password defined in CONFIG_FILE
3. go to http://localhost:8088/databaseview/list/, click "+DATABASE", connect with the following string 
 > mysql://csmap_user:csmap@localhost:3306/tweet?read_default_file=~/.my.cnf
4. navigate to Chart page to create 20+ types of visualization: http://localhost:8088/chart/list/


#### sample MySQL queries

following are some sample MySQL querie to get started

count number of tweets per day
```
SELECT COUNT(*), yymmdd
FROM covid_tweet
GROUP BY yymmdd 
ORDER BY yymmdd 
```

top 10 tweets from users with the highest number of followers
```
SELECT text, user__followers_count, user__screen_name , user__name
FROM covid_tweet
WHERE user__followers_count > 10000
ORDER BY user__followers_count desc
LIMIT 10
```
