# Karmabot
A Slack bot integration for giving and receiving points to teammates

### Using Karmabot
Coming soon.

### Installation
The data for Karmabot is stored in Redis. The below commands will launch a Redis server as a background process and persists the data to disk in case the Redis server needs to be restarted.

    $ mkdir /etc/redis
    $ redis-server --daemonize yes --dir /etc/redis --dbfilename dump.rdb

This tool requires the Python packages redis and slackclient. Run pip install on the requirements file to install the packages.

    $ pip install -r requirements.txt

In Slack, you must create a new bot user for your team. This can be done [here](http://my.slack.com/services/new/hubot). Take note of the API Token that is generated when you create your user. This will be used in the next step.

With the prerequisites covered, you can now run Karmabot with the following command.

    $ python karmabot.py <API_TOKEN>
