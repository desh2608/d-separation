#!/bin/bash

graph_file='dag.txt'

# Check and install required packages
required_packages='numpy argparse copy'

for package in ${required_packages}; do
	if [[ $(python3 -c "import $package") -ne 0 ]]; then
		pip3 install --user $package
	fi 
done

# Run for given problems
# Part (a)
source=61
target=68
given='4 19 90'

python3 dsep.py -f $graph_file -s $source \
	-t $target -g $given

# Part (b)
source=55
target=27
given='4 8 9 12 29 32 40 44 45 48 50 52'

python3 dsep.py -f $graph_file -s $source \
	-t $target -g $given