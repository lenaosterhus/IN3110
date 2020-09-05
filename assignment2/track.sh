#!/bin/bash


# Displaying error message to terminal and exit
function displayUsageError {
    echo "Usage: start [label] / stop / status"
}

# Writing argument to log file
function log {
    cat >> "$HOME/.local/share/$LOGFILE" <<- EOF
	$1
	EOF
}

# Find last task
# LOGFILE="/Users/Lena/.local/share/track.log" in .bashrc
function findLastTask {
    logfilePath="$HOME/.local/share/$LOGFILE"
    # Check if the file exists
    if [ -f "$logfilePath" ]; then
        # Find the last line with "LABEL"
        lastLABEL=$(cat $logfilePath | grep "LABEL" | tail -n1)
        # Find last task number, and optionally label
        lastTaskNo=$(echo $lastLABEL | cut -d" " -f5)
        lastTaskLabel=$(echo $lastLABEL | cut -d" " -f6)
    else
        echo "Creating: $logfilePath"
        touch $logfilePath
        lastTaskNo=0
    fi;
}

function printLog {
    task=""
    startTimeString=""
    endTimeString=""

    # Read lines in file
    cat "$HOME/.local/share/$LOGFILE" | while read line || [[ -n $line ]];
    do

        key=$(echo $line | cut -d" " -f1)

        case $key in
            START)
                startTimeString=${line:6}
                ;;
            LABEL)
                task=$(echo $line | cut -d" " -f5)
                ;;
            END)
                endTimeString=${line:4}
                ;;
            *)
                # Blank line between tasks logged

                # Epoc time
                startTimeSeconds=$(date -j -f "%a %b %e %H:%M:%S %Z %Y" "$startTimeString" "+%s")
                endTimeSeconds=$(date -j -f "%a %b %e %H:%M:%S %Z %Y" "$endTimeString" "+%s")

                diffEpocSeconds=$(($endTimeSeconds - $startTimeSeconds))
                # Hours
                diffHours=$(( $diffEpocSeconds / 60 / 60 ))
                # Minutes
                diffEpocSeconds=$(( $diffEpocSeconds - ($diffHours * 60 * 60) ))
                diffMins=$(( $diffEpocSeconds / 60 ))
                # Seconds
                diffSeconds=$(( $diffEpocSeconds - ($diffMins * 60) ))

                function formatDiff {
                    if [ $1 -lt 10 ]; then
                        newDiff="0$1"
                    else
                        newDiff=$1
                    fi
                }

                # Format to correct print output
                formatDiff $diffHours
                diffHours=$newDiff
                formatDiff $diffMins
                diffMins=$newDiff
                formatDiff $diffSeconds
                diffSeconds=$newDiff

                echo "Task $task: $diffHours:$diffMins:$diffSeconds"
                ;;
        esac

    done
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
    stat=$(cat "$HOME/.local/share/$LOGFILE" | tail -n1 | cut -d" " -f1)


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
        log)
            printLog
            ;;
        *)
            echo "$0: invalid option '$option'"
            displayUsageError
            ;;
    esac
    return
}
