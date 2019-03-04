#! /bin/sh

#

# pulseaudio initscript

#

### BEGIN INIT INFO

# Provides:          pulseaudio.sh

# Required-Start:    $local_fs $remote_fs

# Required-Stop:     $remote_fs

# Default-Start:     2 3 4 5

# Default-Stop:      0 1 6

# Short-Description: starts pulseaudio at startup

# Description:       starts pulseaudio at startup

### END INIT INFO

# This is needed for bluetooth audio

pulseaudio -D