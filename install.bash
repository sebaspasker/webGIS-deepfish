#!/bin/bash

pip_exists=$(ls /bin/ /usr/bin/ | grep '^pip$' | wc -l)

if (( $pip_exists == 0 )); then
	echo "Pip probably don't exist. Continue?(y/n)"
	read ans
	[[ $ans == 'n' ]] && exit
fi

pip install -r dependencies.txt
