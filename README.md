What it does:
1. Creates a .tar.gz package containing web application.
2. Removes existing site files on server.
3. Copies package to site directory on server.
4. Extracts package files to site directory on server.
5. Restarts server's web process responsible for hosting application.


### Requirements

- Python 3
- Private SSH Key

### Installation

```
pip install -r ./requirements.txt
```

### Script Configuration

- **package_name** - tar.gz archive created to transfer deliverables. This can be whatever you want so long as it ends with the .tar.gz extention.

- **local_path** - Path to the deliverables that need to be added to the package.

- **local_pk_path** - Path to the private key which can be used to access the server via SSH.

- **server_ip** - Server ip address or host name.

- **server_user** - User configured on the server that will run SSH commands for deployment.

- **server_site_path** - Where the site is on the server.

- **service_name** - Name of the systemd service. Not needed if a service does not need restarted after deployment.

### Server configuration

- Connecting user must have access to run `sudo systemctl restart my-web-process.service` without entering sudo password.
  - This can be configured through the `visudo` tool, which edits the `/etc/sudoers` file.
  - i.e. Add line to the end: `webuser ALL=NOPASSWD: /bin/systemctl restart my-kestrel-app.service`
  - This is only needed if your service needs to be restarted after copying new files (i.e. .NET core needs to load fresh dll's). If this is not needed, you can remove this step from the deploy script.