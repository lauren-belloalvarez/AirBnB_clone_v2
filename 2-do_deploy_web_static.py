from fabric.api import env, put, run
import os

# Define the list of hosts
env.hosts = ['<IP web-01>', '<IP web-02>']  # replace with your actual server IPs

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

    # Extract the file name and the base name without the extension
    archive_file = os.path.basename(archive_path)
    base_name = os.path.splitext(archive_file)[0]
    
    # Define the full path for deployment
    release_folder = f"/data/web_static/releases/{base_name}/"

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, f"/tmp/{archive_file}")

        # Create the release directory
        run(f"mkdir -p {release_folder}")

        # Uncompress the archive to the release folder
        run(f"tar -xzf /tmp/{archive_file} -C {release_folder}")

        # Remove the uploaded archive from the web server
        run(f"rm /tmp/{archive_file}")

        # Move the contents of the web_static folder to the release folder
        run(f"mv {release_folder}web_static/* {release_folder}")

        # Remove the now empty web_static folder
        run(f"rm -rf {release_folder}web_static")

        # Delete the symbolic link /data/web_static/current
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link to the new version of your code
        run(f"ln -s {release_folder} /data/web_static/current")

        print("New version deployed!")
        return True
    except:
        return False

