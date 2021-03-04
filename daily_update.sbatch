#!/bin/bash
#SBATCH --job-name=cpu_jupyter
#SBATCH --nodes=1
#SBATCH --cpus-per-task=20
#SBATCH --mem=40GB
#SBATCH --time=26:00:00

module purge

jupyter_dir=/home/$USER/
cd $jupyter_dir

port=$(shuf -i 6000-9999 -n 1)
/usr/bin/ssh -N -f -R $port:localhost:$port log-0
/usr/bin/ssh -N -f -R $port:localhost:$port log-1
/usr/bin/ssh -N -f -R $port:localhost:$port log-2
/usr/bin/ssh -N -f -R $port:localhost:$port log-3
cat<<EOF
Jupyter server is running on: $(hostname)
Job starts at: $(date)
Step 1 :
If you are working in NYU campus, please open an iTerm window, run command
ssh -L $port:localhost:$port greene
If you are working off campus, you should already have ssh tunneling setup through HPC bastion host, 
that you can directly login to prince with command
ssh $USER@greene
Please open an iTerm window, run command
ssh -L $port:localhost:$port $USER@greene
Step 2:
Keep the iTerm windows in the previouse step open. Now open browser, find the line with
The Jupyter Notebook is running at:
the URL is something: http://localhost:${jupyter_port}/?token=XXXXXXXX
you should be able to connect to jupyter notebook running remotly on prince compute node with above url
EOF
unset XDG_RUNTIME_DIR
if [ "$SLURM_JOBTMP" != "" ]; then
    export XDG_RUNTIME_DIR=$SLURM_JOBTMP
fi

# write hostname to a globally shared files
echo $(hostname) > /home/$USER/latest_hostname.txt

cd /scratch/$USER
singularity instance start --bind ${PWD}/redis-data:/data docker://redis redis redis-server
singularity exec instance://redis nohup redis-server &
singularity instance start --bind ${HOME} --bind ${PWD}/mysql/var/lib/mysql/:/var/lib/mysql --bind ${PWD}/mysql/run/mysqld:/run/mysqld ./mysql-8.0.22.sif mysql && singularity run instance://mysql
singularity instance start --bind ${PWD}/superset-data:/var/lib/superset --bind ${PWD}/superset_config.py:/etc/superset/superset_config.py  docker://amancevice/superset superset
singularity exec instance://superset nohup superset run -p 8088 --host=0.0.0.0 --with-threads --reload --debugger &

echo 'Waiting for all instances to start...'
sleep 30

cd /home/$USER/decahose_visualization_setup/

# TODO: add CONFIG_FILE as an additional argument, e.g.: NB_ARGS=some_args
CONFIG_FILE=$1 nohup /share/apps/anaconda3/2020.02/bin/jupyter nbconvert --to notebook --inplace --ExecutePreprocessor.timeout=7200 --execute daily_update.ipynb &
#nohup /share/apps/anaconda3/2020.02/bin/jupyter nbconvert --to notebook --inplace --ExecutePreprocessor.timeout=20000 --execute selenium_crawl_page.ipynb &


cd /home/$USER
/share/apps/anaconda3/2020.02/bin/jupyter lab --no-browser --port $port


:'
Read the docs for this script here:
https://github.com/SMAPPNYU/smapputil#cpu-jupyter
Updated: 2017-04-21
Author @yinleon @yvan

Last Updated: 2021-03-06
Author @zhouhanchen
'

