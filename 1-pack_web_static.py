#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of
the web_static folder of your AirBnB Clone repo, using the function do_pack
"""
from fabric.api import local
from datetime import datetime
import os

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
