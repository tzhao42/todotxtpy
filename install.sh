#!/bin/bash

mkdir ~/bin
mkdir ~/todo
touch ~/todo/config
touch ~/todo/todo.txt
touch ~/todo/done.txt

cd /tmp
git clone git@github.com:tzhao42/todotxtpy.git
mv /tmp/todotxtpy/todotxtpy/todotxt.py ~/bin

echo 'export PATH="/home/$USER/bin:$PATH"' >> ~/.bashrc
echo 'alias t="todotxt.py"' >> ~/.bash_aliases

