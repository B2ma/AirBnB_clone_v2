#!/usr/bin/python3
"""
distributes an archive to your web servers, using the function do_deploy
"""

from fabric.api import env, put, run
import os
from datetime import datetime

env.hosts = ['54.159.22.249', '54.173.9.57']
env.user = 'ubuntu'


def do_deploy(archive_path):
    '''
    Distributes an archive to web servers
    '''
    if not os.path.exists(archive_path):
        return False
    file_name = archive_path.split('/')[1]
    file_path = '/data/web_static/releases/'
    releases_path = file_path + file_name[:-4]
    try:
        put(archive_path, '/tmp/')
        run('mkdir -p {}'.format(releases_path))
        run('tar -xzf /tmp/{} -C {}'.format(file_name, releases_path))
        run('rm /tmp/{}'.format(file_name))
        run('mv {}/web_static/* {}/'.format(releases_path, releases_path))
        run('rm -rf {}/web_static'.format(releases_path))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(releases_path))
        print('New version deployed!')
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
