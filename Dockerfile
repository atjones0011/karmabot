FROM ubuntu:14.04

# Install Linux Packages
RUN apt-get update -qq && apt-get install -y python python-pip python-dev wget

# Install Python Packages
RUN pip install redis slackclient

# Install Redis
RUN \
  cd /tmp && \
  wget http://download.redis.io/releases/redis-3.0.6.tar.gz && \
  tar xvzf redis-3.0.6.tar.gz && \
  cd redis-3.0.6 && \
  make && \
  make install && \
  rm -rf /tmp/redis-3.0.6.tar.gz

RUN mkdir /etc/redis

# Launch Redis Server in Background
#
# This does not work. Need to use Docker Compose or figure out another way
#
CMD ["redis-server", "--daemonize", "yes", "--dir", "/etc/redis", "--dbfilename", "dump.rdb"]

# Add src files
ADD . /src

# Launch Karmabot
ENTRYPOINT ["python", "/src/karmabot.py"]