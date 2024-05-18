from fabric.api import env, local, put, run
from datetime import datetime
import os

env.hosts = ['<IP web-01>', '<IP web-02>']  # replace with your actual server IPs

def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""
    if not os.path.exists("versions"):
        os.makedirs("versions")
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "web_static_{}.tgz".format(timestamp)
    archive_path = "versions/{}".format(archive_name)
    
    print("Packing web_static to {}".format(archive_path))
    result = local("tar -cvzf {} web_static".format(archive_path))
    
    if result.succeeded:
        return archive_path
    else:
        return None

def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.
    Args:
        archive_path (str): The path to the archive to be deployed.
    Returns:
        bool: True if all operations are successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    archive_file = os.path.basename(archive_path)
    base_name = os.path.splitext(archive_file)[0]
    release_folder = f"/data/web_static/releases/{base_name}/"

    try:
        put(archive_path, f"/tmp/{archive_file}")
        run(f"mkdir -p {release_folder}")
        run(f"tar -xzf /tmp/{archive_file} -C {release_folder}")
        run(f"rm /tmp/{archive_file}")
        run(f"mv {release_folder}web_static/* {release_folder}")
        run(f"rm -rf {release_folder}web_static")
        run("rm -rf /data/web_static/current")
        run(f"ln -s {release_folder} /data/web_static/current")
        print("New version deployed!")
        return True
    except:
        return False

def deploy():
    """
    Full deployment: packs and deploys the archive to the web servers.
    Returns:
        bool: True if all operations are successful, False otherwise.
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)

