CSMaP Internal Dashboard
=========

A modern dashboard to explore and visualize tweets related to a topic of interest.

[**Why use this dashboard**](#why-use-this-dashboard) |
[**What questions can be answered**](#what-questions-can-be-answered) |
[**Installation and Configuration**](#installation-and-configuration) |
[**Example MySQL queries**](#example-mysql-queries) |
[**Resources**](#resources) |

![Sample dashboard layout](/img/decahose-covid-tweet-dashboard-example.png)

## Why use this dashboard?

If you're studying social networks, chances are you might want to collect and visualize tweets related to a certain topic. Fortunately, CSMaP has access to Decahose, a 10% sample of all tweets!

With minimal configuration, this repository first loads tweets related to a given keyword(s) from Decahose to a local MySQL database. It then sets up a dashboard using [Superset](https://superset.apache.org/). Users can then write custom SQL queries, create a variety of charts, and group charts together into a dashboard.

## What questions can be answered?
 - How many tweets are related to a topic (e.g.: BLM, vaccine, election...)?
 - Who are sharing those tweets; when and where do they post?
 - What hashtags/urls are co-shared?
 - Is the topic gaining or losing popularity? What is the trend?
 - ...

Since new tweets are added every day, the system also schedules a background job that loads new tweets every 24 hours. The overall system architecture is shown below.

![System architecture](img/system-architecture.png)


## Installation and Configuration

##### Step 1: Initiate MySQL database and Superset
1. Log in HPC, then `cd /home/$USER`
2. `git clone git@github.com:SMAPPNYU/internal-dashboard.git`
3. `cd /home/$USER/internal-dashboard` (do not rename the directory)
4. Modify `config.json`, change `KEYWORD` or `TABLE_NAME`. Leave other configurations as they are. Note: `KEYWORD` needs at least 2 words. 
5. `./init.sh config.json` (do not forget to type the first dot)
6. We are ready to create our first dashboard (go to Step 2-a)

__Tip: if you want to track other keywords, please create another config file (e.g.: config-vaccine.json, and issue `./init.sh config-vaccine.json`)__

##### Step 2-a: Connect to a _new_ Superset dashboard

1. Inside HPC log-in node, run command: `source $HOME/.bash_profile; cd /home/$USER/internal-dashboard && ./daily_update.sh config.json`
2. Wait until the script finishes, follow instructions printed on the console (stdout)
3. After re-connecting to HPC, proceed to Step 3

##### Step 2-b: Connect to an _existing_ Superset dashboard
1. `./init.sh config.json` schedule a background job that loads new tweets and hosts a new Dashboard on a new IP address every 24 hours.
2. To connect to a dashboard from a running job, find the hostname YOUR_HOSTNAME via `cat /home/$USER/decahose_visualization_setup/latest_hostname.txt`
3. Log out HPC `exit`
4. Log in HPC again with port forwarding, `ssh -L 8088:YOUR_HOSTNAME:8088 YOUR_NETID@log-1.nyu.cluster` (change `YOUR_HOSTNAME` and `YOUR_NETID`)
5. Proceed to Step 3

__Tip: Inside the same HPC log-in node as Step 1, run `crontab -e`. You can delete the scheduled job if you prefer.__

##### Step 3: Create your first dashboard
1. Open browser, visit http://localhost:8088/
2. Enter default username (__`admin`__) and password (__`admin`__). Update the password for enhanced security.
3. Go to http://localhost:8088/databaseview/list/, click "+DATABASE", connect with the following string 
 > mysql+pymysql://csmap_user:csmap@localhost:3306/tweet?read_default_file=~/.my.cnf
4. Once we connect to the database, add a dataset
5. Navigate to Chart page to create 20+ types of visualization: http://localhost:8088/chart/list/

## Example MySQL queries

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

## Resources
* [Superset documentation](https://github.com/apache/superset/blob/master/README.md)
* [MySQL tutorial](https://www.tutorialspoint.com/mysql/mysql-introduction.htm)
* [About Twitter Decahose](https://developer.twitter.com/en/docs/twitter-api/enterprise/decahose-api/overview/decahose)
* [NYU HPC](https://sites.google.com/a/nyu.edu/nyu-hpc/systems/greene-cluster)

_Note: If you encounter any problem during the set up, please contact Zhouhan, email: zc1245@nyu.edu_





