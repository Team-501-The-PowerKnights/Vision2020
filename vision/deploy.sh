#!/bin/bash
### deploys vision code to the raspberry pi (tinkerboard)
### must be run from the root of the vision repository

hostname="raspberrypi.local"
home="/home/pi"
user="pi"

if [ -f util/.ssh/id_rsa.pub ]; then
   echo "Vision public key found."
   list=$(find $PWD -type f | grep -vE ".idea|.git|__pycache__")
   dirs=$(find . -type d |grep -vE ".git|.idea|__pycache__"| sed 's/^\.$//g; s/\.\///g')
   pwd=$(pwd)
   cd ..
   # base="linaro@tinkerboard.local:/home/linaro"
   base=$user@$hostname:$home
   echo $base

   echo "Creating remote directories..."
   for directory in $dirs;
      do
         ssh -i $pwd/util/.ssh/id_rsa $user@$hostname "mkdir -p $home/$directory"
         if [ $? -eq 0 ]; then
            echo "Created $directory"
         else
            echo "ERROR: Could not create remote directory \"$directory\". Deploy failed."
            exit
         fi
      done

   echo "Deploying code..."
   for file in $list;
      do
         #echo $pwd
         #echo $file
         next_dir=$(sed -e 's,'"$pwd"',,g' <<<"$file")
         destination=$base$next_dir
         scp -q -r -i $pwd/util/.ssh/id_rsa $file $destination;
         if [ $? -eq 0 ]; then
            code="good"
            echo "Deployed $next_dir"
         elif [ $? -eq 4 ]; then
            code="connect"
            echo "ERROR: Could not deploy $next_dir"
            break
         else
            code="fail"
            echo "ERROR: Could not deploy $next_dir"
            break
         fi
      done
   if [ "$code" = "connect" ]; then
      echo -e "Cannot connect. Deploy failed.\a"
   elif [ "$code" = "fail" ]; then
      echo -e "Deploy failed.\a"
   elif [ "$code" = "good" ]; then
      echo "Successfully Deployed Vision Code."
   fi
else
   echo "Vision public key not found. Are you in the root of the vision repository?"
fi
