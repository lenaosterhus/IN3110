#!/bin/bash


# Displaying error message to terminal and exit
function displayUsageError {
    echo "Usage: start [label] / stop / status"
}

# Writing argument to log file
function log {
    cat >> $LOGFILE <<- EOF
	$1
	EOF
}

# Find last task
# LOGFILE="/Users/Lena/.local/share/track.log" in .bashrc
function findLastTask {
    if [ -f "$LOGFILE" ]; then
        # Find the last line with "LABEL"
        lastLABEL=$(cat $LOGFILE | grep "LABEL" | tail -n1)
        # Find last task number, and optionally label
        lastTaskNo=$(echo $lastLABEL | cut -d" " -f5)
        lastTaskLabel=$(echo $lastLABEL | cut -d" " -f6)
    else
        echo "Creating: $LOGFILE"
        touch $LOGFILE
        lastTaskNo=0
    fi;
}

function track {

    # Checking that at least one argument was provided
    if [ $# -lt 1 ]; then
    	displayUsageError
        return
    fi


    option=$1

    findLastTask
    # Retrieve the first word in the last log
    # LABEL = task running
    # END = no task is running
    stat=$(cat $LOGFILE | tail -n1 | cut -d" " -f1)


    case $option in

        start)
            # Error message if already running
            if [ "$stat" == "LABEL" ]; then
                echo "ERROR: Already running"
            # Log task if not already running
            else
                log "START $(date)"

                label=$2
                declare -i last=$lastTaskNo
                lastTaskNo=$((++last))

                log "LABEL This is task $lastTaskNo $label"
            fi ;;

        stop)
            # Stop task if running
            if [ "$stat" == "LABEL" ]; then
                log "END $(date)"
                log ""
            fi ;;

        status)
            if [ "$stat" == "LABEL" ]; then
                echo "Currently tracking task $lastTaskNo $lastTaskLabel"
            else
                echo "No active task"
            fi ;;
        *)
            echo "$0: invalid option '$option'"
            displayUsageError ;;
    esac
    return
}
