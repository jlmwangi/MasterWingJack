#!/usr/bin/python3

'''script that generates a .tgz archive from web_static folder'''

import datetime
from fabric import task
from invoke import run as local
#from fabric import Connection
import os

@task
def do_pack(c):
    '''pack contents into a .tgz archive'''
    day_time = datetime.datetime.now()
    today = day_time.strftime("%Y%m%d%H%M%S")
    name = f"web_static_{today}.tgz"

    try:
        c.run("mkdir -p versions")
        c.run("tar -cvzf versions/{} web_static/".format(name))
        file_path = ("versions/{}".format(name))
        file_size = os.path.getsize(file_path)
        print(f'web_static packed: versions/{name} -> {file_size}')
        return file_path
    except Exception:
        return None

@task
def do_deploy(c, archive_path):
    '''distributes an archive to the web servers'''
    if not os.path.exists(archive_path):
        return False

    try:
        filename = os.path.basename(archive_path)
        name = filename.replace('.tgz', '')
        print(f"Filename: {filename}, Release name: {name}")

        # upload archive to /tmp/ on web server
        print("Uploading to /tmp/")
        c.put(archive_path, '/tmp/')
        print("Upload complete")

        # create release directory
        print(f"Creating directory /data/web_static/releases/{name}")
        c.run(f'mkdir -p /data/web_static/releases/{name}')
        print("directory created")

        # extract archive
        print("Extracting archive")
        c.run(f'tar -xzf /tmp/{filename} -C /data/web_static/releases/{name}/')
        print("Extraction complete")

        # remove archive from tmp
        c.run(f'rm /tmp/{filename}')

        # move contents out of web_static folder
        print("Moving files")
        #c.run(f'rm -rf /data/web_static/releases/{name}/web_static')
        c.run(f'mv /data/web_static/releases/{name}/web_static/* /data/web_static/releases/{name}/')
        print("Files moved")

        # delete web_static folder
        c.run(f'rm -rf /data/web_static/releases/{name}/web_static')
        # remove old sym link
        c.run('rm -rf /data/web_static/current')

        # create new sym link
        c.run(f'ln -s /data/web_static/releases/{name} /data/web_static/current')
        print("Deployment complete")

        return True

    except Exception as e:
        print(f"ERROR: {e}")
        return False

@task
def deploy(c):
    """creates and distributes an archive"""
    filepath = do_pack(c)
    if filepath:
        return do_deploy(c, filepath)
    return False

@task
def do_clean(c, number=0):
    """deletes out of date archives"""
    number = int(number)
    if number < 1:
        number = 1

    #local clean up
    local_result = local("ls -1t versions").stdout.strip().split("\n")
    local_res_to_del = local_result[number:]

    for archive in local_res_to_del:
        local(f"rm -f versions/{archive}")
        print(f"deleted archive: versions/{archive}")

    # remote cleanup
    remote_res = c.run("ls -1t /data/web_static/releases").stdout.strip().split("\n")
    remote_res_to_del = [res for res in remote_res if res.startswith("web_static_")][number:]

    for release in remote_res_to_del:
        c.run(f"rm -rf /data/web_static/releases/{release}")
        print(f"Deleted remote release: /data/web_static/releases/{release}")

    print("Cleanup complete")
