from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""
    # Create the versions directory if it does not exist
    if not os.path.exists("versions"):
        os.makedirs("versions")
    
    # Create a timestamp for the archive name
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # Define the archive name and path
    archive_name = "web_static_{}.tgz".format(timestamp)
    archive_path = "versions/{}".format(archive_name)
    
    # Pack the contents of web_static into the archive
    print("Packing web_static to {}".format(archive_path))
    result = local("tar -cvzf {} web_static".format(archive_path))
    
    # Check if the archive was created successfully
    if result.succeeded:
        return archive_path
    else:
        return None

