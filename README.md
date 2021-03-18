### How can this dashboard benefit my research?

If your study social networks, chances are you might want to collect and visualize tweets related to a certain topic. Fortunately, CSMaP has access to Decahose, a 10% sample of all tweets.

With minimal configuration, this repository first loads tweets related to a given keyword(s) from Decahose to a local MySQL database. It then sets up a dashboard using [Superset](https://superset.apache.org/). Users can then write custom SQL queries, create a variety of charts, and group charts together into a dashboard.

Since new tweets are added every day, the system also schedules a background job that loads new tweets every 24 hours. The overall systetm architecture is shown below.

This repository is intended as a starting point, so be creative. 

_Note: If you encounter any problem during the set up, please contact Zhouhan, email: zc1245@nyu.edu_
![System architecture](img/system-architecture.png)


### Initiate MySQL database and Superset

1. Log in HPC, then `cd /home/$USER`
2. `git clone git@github.com:SMAPPNYU/internal-dashboard.git`
3. `cd /home/$USER/internal-dashboard`
4. Modify `config.json`, change keyword. You can leave other configurations as default. 
5. `./init.sh config.json` (do not forget to type the first dot)
6. Now we are ready to create our first dashboard

### Connect to Superset (our dashboard tool)

1. The above steps schedule a background job that loads new tweets and updates Dashboard IP address every 24 hours. To create a dashboard instantly, we can run this command: `source $HOME/.bash_profile; cd /home/$USER/internal-dashboard && ./daily_update.sh config.json`
2. Wait for a while, instructions to re-connect to HPC should be printed on the console (stdout)

3. Alternatively, if we want to connect to a dashboard when a schduled job is running, we can find the hostname HOST via `cat /home/$USER/decahose_visualization_setup/latest_hostname.txt`
4. Then log out HPC `exit`
5. Log in HPC again with port forwarding, `ssh -L 8088:HOST:8088 netID@log-1.nyu.cluster`

### Create the first dashboard
1. Open browser, visit http://localhost:8088/
2. Enter default username (`admin`) and password (`admin`). Update the password for enhanced security.
3. Go to http://localhost:8088/databaseview/list/, click "+DATABASE", connect with the following string 
 > mysql://csmap_user:csmap@localhost:3306/tweet?read_default_file=~/.my.cnf
4. Navigate to Chart page to create 20+ types of visualization: http://localhost:8088/chart/list/

#### sample MySQL queries

Following are some MySQL queries to get started

- count number of tweets per day
```
SELECT COUNT(*), yymmdd
FROM covid_tweet
GROUP BY yymmdd 
ORDER BY yymmdd 
```

- top 10 tweets from users with the highest number of followers
```
SELECT text, user__followers_count, user__screen_name , user__name
FROM covid_tweet
WHERE user__followers_count > 10000
ORDER BY user__followers_count desc
LIMIT 10
```

#### An example dashboard that visualizes tweets containing "COVID" related keywords
![Sample dashboard layout](/img/decahose-covid-tweet-dashboard-example.png)





