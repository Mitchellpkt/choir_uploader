#!/bin/bash

#####################
## OPERATOR AWARE 
## MitchellPKT@pm.me
## Run this once
#####################

sudo apt update
sudo apt upgrade

#####################
# Install pip
echo pip incoming...
#sudo apt-get install python-pip
sudo apt-get install python3-pip

#####################
# Install anaconda
wget https://repo.anaconda.com/archive/Anaconda3-5.2.0-Linux-x86_64.sh
chmod +777 Anaconda3-5.2.0-Linux-x86_64.sh
bash Anaconda3-5.2.0-Linux-x86_64.sh
rm Anaconda3-5.2.0-Linux-x86_64.sh
## go through the install
cd ~/anaconda3/bin
./conda update anaconda # may need to adjust the path
echo If conda not recognized, add anaconda bin to path
echo ... learned hard way: append not replace. *cough*
echo you may be able to skip this. 
## Export path if needed
# e.g. export path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/home/pwn_me_user/anaconda3/bin"
./conda create -n insight python=3 # I added ./ more recently
source activate insight
conda install flask

#####################
# Install anaconda
# echo flask incoming...
# sudo apt install python3-flask

#####################
# Install net-tools 
echo snag net-tools
sudo apt install net-tools # for ifconfig


