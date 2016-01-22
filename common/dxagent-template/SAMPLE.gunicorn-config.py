# Gunicorn configuration file.
import multiprocessing

#
# Server socket
#
#   bind - The socket to bind.
#
#       A string of the form: 'HOST', 'HOST:PORT', 'unix:PATH'.
#       Multiple addresses can be bound.
#
#   backlog - The number of pending connections. 
#       
#       This refers to the number of clients that can be waiting to be served. Exceeding this number results in the client
#       getting an error when attempting to connect. It should only affect servers under significant load.
#
#       Must be a positive integer. Generally set in the 64-2048
#       range.
#

bind = '0.0.0.0:8443'
backlog = 2048

#
# Worker processes
#
#   workers - The number of worker processes for handling requests.
#
#       A positive integer generally in the 2-4 x $(NUM_CORES) range. You'll want to vary this a bit to find the best
#       for your particular application's work load. By default, the value of the WEB_CONCURRENCY environment variable. 
#       If it is not defined, the default is 1.
#
#   worker_class - The type of workers to use. 
#
#       The default async class should handle most 'normal' types of work loads. You'll want to read http://gunicorn/deployment.hml
#       for information on when you might want to choose one of the other worker classes.
#
#       An string referring to a 'gunicorn.workers' entry point  or a python path to a subclass of
#       gunicorn.workers.base.Worker. The default provided values are:
#
#           egg:gunicorn#sync
#           egg:gunicorn#eventlet   - Requires eventlet >= 0.9.7
#           egg:gunicorn#gevent     - Requires gevent >= 0.12.2 (?)
#           egg:gunicorn#tornado    - Requires tornado >= 0.2
#
#   worker_connections - The maximum number of simultaneous clients.
#
#       This setting only affects the Eventlet and Gevent worker types.
#       A positive integer generally set to around 1000.
#
#   timeout - Workers silent for more than this many seconds are killed and restarted.
#
#       Generally set to thirty seconds. Only set this noticeably higher if you're sure of
#       the repercussions for sync workers. For the non sync workers it just means that the worker
#       process is still communicating and is not tied to the length of time required to handle a single request.
#
#   keepalive -  The number of seconds to wait for requests on a Keep-Alive connection. 
#
#       Generally set in the 1-5 seconds range.
#

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 300
keepalive = 2

#
#   spew - Install a trace function that spews every line of Python that is executed when running the server.
# 
#       This is the nuclear option.
#
#       True or False
#

spew = False

#
# Server mechanics
#
#   daemon - Daemonize the Gunicorn process.
#
#       Detach the main Gunicorn process from the controlling terminal with a standard fork/fork sequence.
#
#       True or False
#
#   pidfile - A filename to use for the PID file.
#
#       If not set, no PID file will be written.
#
#   user - Switch worker processes to run as this user.
#
#       A valid user id (as an integer) or the name of a user that can be retrieved with a call to pwd.getpwnam(value)
#       or None to not change the worker process user.
#
#   group - Switch worker process to run as this group.
#
#       A valid group id (as an integer) or the name of a user that can be retrieved with a call to pwd.getgrnam(value) or None
#       to change the worker processes group.
#
#   umask - A mask for file permissions written by Gunicorn. 
#       Note that this affects unix socket permissions.
#
#       A valid value for the os.umask(mode) call or a string compatible with int(value, 0) (0 means Python guesses
#       the base, so values like "0", "0xFF", "0022" are valid for decimal, hex, and octal representations)
#
#   tmp_upload_dir - Directory to store temporary request data as they are read.
#
#       This may disappear in the near future.
#       This path should be writable by the process permissions set for Gunicorn workers. 
#       If not specified, Gunicorn will choose a system generated temporary directory.
#

daemon = False
pidfile = "./gunicorn.pid"
umask = 0
user = None
group = None
tmp_upload_dir = None

#
#   Logging
#
#   logconfig - The log config file to use. Gunicorn uses the standard Python logging modules's Configuration file format
#


logconfig = 'gunicorn-logging.conf'


#
#   SSL
#
#   keyfile - SSL Key file
#   certfile - SSL certificate file
#   ssl_version - version of SSL
#   cert_reqs - Whether client certificate is required. Set to 2 to require client certificate and validation
#   ca_certs - CA certificates file
#   do_handshake_on_connect = Whether to perform SSL handshake on socket connect
#


keyfile = './openssl-ca/out/__SERVER__.key'
certfile = './openssl-ca/out/__SERVER__.pem'
ssl_version = 3
cert_reqs = 2
ca_certs = './openssl-ca/CA/certs/ca.pem'
do_handshake_on_connect = True

#
# Process naming
#
#   proc_name - A base to use with setproctitle for process naming.
#
#       This affects things like ps and top. If you are going to be running more than one instance of Gunicorn 
#       you will probably want to set a name to tell them apart. This requires that you install the setproctitle module.
#
#       It defaults to 'gunicorn'.
#

proc_name = None

#
# Server hooks
#
#   post_fork - Called just after a worker has been forked.
#
#       A callable that takes a server and worker instance as arguments.
#
#   pre_fork - Called just prior to forking the worker subprocess.
#
#       A callable that accepts the same arguments as after_fork
#
#   pre_exec - Called just prior to forking off a secondary master process during things like config reloading.
#
#       A callable that takes a server instance as the sole argument.
#

def post_fork(server, worker):
    server.log.info("Worker process spawned. Pid is: %s", worker.pid)

def pre_fork(server, worker):
    pass

def pre_exec(server):
    server.log.info("Forked child process, re-executing.")

def when_ready(server):
    server.log.info("Server is ready. Spawning worker processes")

def worker_int(worker):
    worker.log.info("Worker process received INT or QUIT signal")

def worker_abort(worker):
    worker.log.info("Worker process received SIGABRT signal")
