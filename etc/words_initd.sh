#!/bin/bash
# Start/stop words application
#
#set -e -u -x

NAME=words
APP=words
RUNDIR=/home/steder/Words/current
TWISTD=/usr/local/bin/twistd
PID=/var/run/$NAME.pid
LOGFILE=/var/log/$NAME/$NAME.log
DESCRIPTION="Twistd Service"
TB_UID=`id -u steder`
TB_GID=`id -g steder`

test -f $TWISTD || exit 0

. /lib/lsb/init-functions

case "$1" in
	start)	log_daemon_msg "Starting $DESCRIPTION" "$NAME"
		start-stop-daemon --start --verbose --chdir $RUNDIR --pidfile $PID --name $NAME --startas $TWISTD -- --logfile="$LOGFILE" --rundir="$RUNDIR" --pidfile="$PID" --uid=$TB_UID --gid=$TB_GID $APP
		log_end_msg $?
		;;
	stop)	log_daemon_msg "Stopping $DESCRIPTION" "$NAME"
		start-stop-daemon --stop --verbose --oknodo --pidfile $PID
		log_end_msg $?
		;;
	restart) log_daemon_msg "Restarting $DESCRIPTION" "$NAME"
		$0 stop
		$0 start
		log_end_msg $?
		;;
*)		log_action_msg "Usage: /etc/init.d/$NAME {start|stop|restart}"
		exit 2
		;;
esac
exit 0