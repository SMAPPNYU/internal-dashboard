#!/bin/bash
# source $HOME/.bash_profile

cd /home/$USER/internal-dashboard

# gracefully shut down all services
ssh `cat /home/$USER/internal-dashboard/latest_hostname.txt` 'singularity instance stop superset'
sleep 5

ssh `cat /home/$USER/internal-dashboard/latest_hostname.txt` 'singularity instance stop redis'
sleep 5

ssh `cat /home/$USER/internal-dashboard/latest_hostname.txt` 'singularity instance stop mysql'
sleep 15


# kill previous running job that hosts superset
squeue -u $USER | grep `cat /home/$USER/internal-dashboard/latest_hostname.txt | cut -d. -f1` | awk '{print $1}'| tail -n 1 | xargs scancel
# squeue -u $USER | awk '{print $1}'| tail -n 1 | xargs scancel
sleep 5

# save previous latest_hostname
mv /home/$USER/internal-dashboard/latest_hostname.txt /home/$USER/internal-dashboard/latest_hostname.txt.old

# clear latest_hostname.txt file
echo '' > latest_hostname.txt

# submit today's sbatch job
sbatch daily_update.sbatch $1

# identify the new hostname running the sbatch job
latest_hostname=''
trials=0

while [[ "$trials" -le 100 ]]; do
	if [[ $latest_hostname != *".nyu.cluster"* ]]
	then
      		#echo "\$latest_hostname is empty"
      		sleep 5
      		latest_hostname=`cat latest_hostname.txt`
		#echo $latest_hostname
		((trails=trails+1))
		#echo $trails
	else
      
		#echo "\$latest_hostname is NOT empty"
		break
	fi

done

echo "==============================================="
echo "========Important log in information =========="
echo "==============================================="
echo ""
echo "First log out Greene, then log in with the following command:"
echo "ssh -L 8088:$latest_hostname:8088 $USER@log-1.hpc.nyu.edu" 
echo ""
echo "Then open your browser, and visit http://localhost:8088"
echo "If there is any issue, you can contact Zhouhan Chen at zc1245@nyu.edu"
echo ""
echo "=============================================="


exit 0
# NOTE: port forwarding is optional, because each port can only be assigned to one user
# kill previous job listening to 30001
#lsof -i -P  | grep 30001 | awk 'NR > 1 {print $2}' |  xargs kill -9

# sleep for 3 seconds
#sleep 3

# launch a new ssh port forwarding job listenting to 30001
#ssh $latest_hostname -Nf  -o ServerAliveInterval=60 -L 30001:127.0.0.1:8088

