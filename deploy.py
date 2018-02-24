import os
import tarfile
import paramiko
from scp import SCPClient

package_name = "package.tar.gz"
local_path = "./MyApp/bin/Release/netcoreapp2.0/publish/"
local_pk_path = "C:/Users/Brandon/Desktop/id_rsa"
server_ip = "123.456.789.101"
server_user = "webuser"
server_site_path = "/home/webuser/my_site/"
service_name = "kestrel-myapp.service"

def remove_pkg_if_exists():
    print("removing any existing local package")
    try:
        os.remove(package_name)
    except OSError:
        pass

def print_output(stdout, stderr):
    out = stdout.read()
    err = stderr.read()
    if out != b'':
        print("Output")
        print(out)
    if err != b'':
        print( "Errors")
        print (err)

def make_tarfile(output_filename, source_dir):
    print('creating package archive')
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

def ssh_to_server(ip, user, pk_path):
    print("connecting to server")
    pk = paramiko.RSAKey.from_private_key_file(pk_path)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect( hostname = ip, username = user, pkey = pk )
    return ssh

def remove_existing_site_files(ssh, site_path):
    print('removing existing site files')
    _, stdout, stderr = ssh.exec_command("rm -rf " + site_path + "*")
    print_output(stdout, stderr)

def copy_package_to(ssh, pkg, path):
    print('copying package to server')
    scp = SCPClient(ssh.get_transport())
    scp.put(pkg, path)

def extract_package_files(ssh, site_path, pkg_name):
    print('extracting package on server')
    cmd = "cd " + site_path + "; tar -xzf ./" + pkg_name + "; rm ./" + pkg_name
    _, stdout, stderr = ssh.exec_command(cmd)
    print_output(stdout, stderr)

def restart_web_process(svc_name):
    print('restarting web process')
    cmd = "sudo systemctl restart " + svc_name
    _, stdout, stderr = ssh.exec_command(cmd)
    print_output(stdout, stderr)

remove_pkg_if_exists()
make_tarfile(package_name, local_path)
ssh = ssh_to_server(server_ip, server_user, local_pk_path)
remove_existing_site_files(ssh, server_site_path)
copy_package_to(ssh, package_name, server_site_path + package_name)
extract_package_files(ssh, server_site_path, package_name)
restart_web_process(service_name)

ssh.close()





