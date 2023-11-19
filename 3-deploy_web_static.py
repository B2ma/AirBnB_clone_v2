#!/usr/bin/python3
"""
distributes an archive to your web servers, using the function do_deploy
"""

from fabric.api import env, put, run, local
import os
from datetime import datetime

env.hosts = ['54.159.22.249', '54.173.9.57']
env.user = 'ubuntu'
env.use_ssh_config = True


def deploy():
    ''' Deploys archive '''
    archive_path = do_pack()
    if archive_path is None:
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
        print('Symbolic link created successfully.')
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
    local("mkdir -p versions")
    now = datetime.utcnow()
    archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
        now.year, now.month, now.day, now.hour, now.minute, now.second
    )

    archive_path = os.path.join("versions", archive_name)
    result = local("tar -czvf {} web_static".format(archive_path))

    if result.succeeded:
        print("Web static packed: {}".format(archive_path))
        return archive_path
    else:
        return None
