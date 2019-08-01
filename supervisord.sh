#!/bin/bash

cat <<EOT > /etc/supervisord.conf

[supervisord]
nodaemon=true

[program:app]
command=flask run --host=0.0.0.0
autorestart=true
startsecs=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0

EOT

exec /usr/bin/supervisord
