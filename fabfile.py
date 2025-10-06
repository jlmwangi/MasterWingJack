#!/usr/bin/python3

# Fabfile to:
#    - update the remote system(s) 
#    - download and install an application

# Import Fabric's API module
from fabric import task, Connection


#env.hosts = [
 #   'server.domain.tld',
  # 'ip.add.rr.ess
  # 'server2.domain.tld',
#]
# Set the username
#env.user   = "root"

# Set the password [NOT RECOMMENDED]
# env.password = "passwd"

@task
def update_upgrade(c):
    """
        Update the default OS installation's
        basic default tools.
                                            """
    c.run("aptitude    update")
    c.run("aptitude -y upgrade")

@task
def install_memcached(c):
    """ Download and install memcached. """
    c.run("aptitude install -y memcached")

@task
def update_install(c):

    # Update
    update_upgrade(c)
    
    # Install
    install_memcached(c)
