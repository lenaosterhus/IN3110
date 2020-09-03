#!/bin/bash


function move {

	# Checking that at least two arguments were provided
	if [ $# -lt 2 ]; then
		echo "Usage: source destination [file type (*.txt *.dat ...)]"
		return
	fi


	src=$1
	dst=$2

	# Checking that arguments are directories
	if ! [ -d $src ]; then
		echo "$src is not a directory"
		return
	fi
	if ! [ -d $dst ]; then
		echo "$dst is not a directory"
		return
	fi

	# Files that are to be moved
	# 2.1a
	if [ $# == 3 ]; then
	    files=$(ls "${src}/$3")
	    # Bash will print "No such file or directory" if no files with file extention
	else
	    files=$(ls $src)
	fi

	# Moving files
	for file in $files
	    do
	        echo "Moving $file"
	        mv $src"/"$file $dst
	    done
}
