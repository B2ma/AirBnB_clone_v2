#!/usr/bin/python3
"""
distributes an archive to your web servers, using the function do_deploy
"""

from fabric.api import *
from datetime import datetime
import os

env.hosts = ['54.159.22.249', '54.173.9.57']
env.user = 'ubuntu'
env.use_ssh_config = True


def deploy():
    ''' Deploys archive '''
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)


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
    except:
        return False


def do_pack():
    """
    Generate a .tgz archive from the contents of the web_static folder.

    Returns:
        Archive path if generated successfully, otherwise None
    """
    try:
        local('mkdir -p versions')
        datetime_format = '%Y%m%d%H%M%S'
        archive_path = 'versions/web_static_{}.tgz'.format(
            datetime.now().strftime(datetime_format))
        local('tar -cvzf {} web_static'.format(archive_path))
        print('web_static packed: {} -> {}'.format(archive_path,
              os.path.getsize(archive_path)))
        return archive_path
    except:
        return None