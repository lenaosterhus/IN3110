#!/bin/bash -x

# Checking that two arguments were provided
if [ $# -lt 2 ]; then
	echo "Usage: Source & destination. Option: file type (*.txt *.dat ...)"
	exit
fi

function checkDirectory {
    # Checks if argument is a directory

	if ! [ -d $1 ]; then
        echo "$1 is not a directory"
        exit
    fi
}

src=$1
dst=$2

# Checking that arguments are directories
checkDirectory $src
checkDirectory $dst

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
