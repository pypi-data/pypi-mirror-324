import sys, os, io, subprocess, threading, socket, psutil, json, time, requests, platform, tempfile
import django
from django.core.management import call_command

thread_failed = False
thread_error_msg = None

# **********************************************************************************************************************
def set_environment_variable(name, value):
    try:
        os.environ[name] = value
    except Exception as e:
        print(f"Error setting environment variable '{name}': {e}")

def set_environment_variable_persist(name, value):
    try:
        subprocess.run(['setx', name, value])
        # print(f"Environment variable '{name}' set to '{value}'")
    except Exception as e:
        # print(f"Error setting environment variable '{name}': {e}")
        pass

def find_process_by_port(port):
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            for conn in proc.connections():
                if conn.laddr.port == port:
                    return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None

def is_port_available(port:int) -> bool:
    return is_port_available_fast(port)

def is_port_available_fast(port:int) -> bool:
    try:
        # Create a socket object
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Try to connect to the specified port
            s.bind(("localhost", port))
            return True
    except socket.error:
        return False

def is_port_available_slow(port: int) -> bool:
    """
    Check if a given port is available by attempting to connect
    and using system tools for a more robust check.

    Args:
        port (int): The port number to check.

    Returns:
        bool: True if the port is available, False otherwise.
    """
    # Python socket-based check
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", port))
        # If connection succeeds, the port is in use
        return False
    except socket.error:
        # Connection failed; port might be free
        pass

    # Additional system-level check
    try:
        os_type = platform.system().lower()
        if os_type == "windows":
            cmd = ["netstat", "-ano"]
        elif os_type in ["linux", "darwin"]:  # darwin is macOS
            cmd = ["netstat", "-tuln"]
        else:
            raise RuntimeError("Unsupported OS for netstat check")

        # Execute netstat and filter for the port
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
        if result.returncode == 0:
            output = result.stdout
            # Look for the port in the output
            if f":{port}" in output:
                return False  # Port is in use
        else:
            print("Error running netstat:", result.stderr)
    except Exception as e:
        print("Error during system-level port check:", str(e))

    # If no issues detected, port is available
    return True

def is_port_busy(port:int) -> bool:
    return not is_port_available(port)
    
def generate_port() -> int:
    port = 8664
    while not is_port_available(port):
        port += 1

    return port

def generate_asgi_port() -> int:
    port = 5664
    while not is_port_available(port):
        port += 1

    return port

# **********************************************************************************************************************

def set_spartaqube_shortcut():
    '''
    Set spartaqube exec to env
    '''
    current_path = os.path.dirname(__file__)
    base_path = os.path.dirname(current_path)
    spartaqube_exec = os.path.join(base_path, 'cli/spartaqube')
    set_environment_variable_persist('spartaqube', spartaqube_exec)

def db_make_migrations_migrate():
    '''
    
    '''
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    new_stdout, new_stderr = io.StringIO(), io.StringIO()
    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = new_stdout, new_stderr
    try:
        call_command('makemigrations')
        call_command('migrate')
    finally:
        # Reset stdout and stderr to their original values    
        sys.stdout, sys.stderr = old_stdout, old_stderr
        
def create_public_user():
    '''
    Public user
    '''
    current_path = os.path.dirname(__file__)
    base_project = os.path.dirname(current_path)
    sys.path.insert(0, os.path.join(base_project, '/project/management'))
    from project.management.commands.createpublicuser import Command as CommandCreatePublicUser
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    CommandCreatePublicUser().handle()

def create_admin_user():
    '''
    Admin user
    '''
    current_path = os.path.dirname(__file__)
    base_project = os.path.dirname(current_path)
    sys.path.insert(0, os.path.join(base_project, '/project/management'))
    from project.management.commands.createadminuser import Command as CommandCreateAdminUser
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    CommandCreateAdminUser().handle()

def get_last_or_default_wsgi_port() -> int:
    try:
        current_path = os.path.dirname(__file__)
        with open(os.path.join(current_path, 'app_data.json'), "r") as json_file:
            loaded_data_dict = json.load(json_file)
        
        wsgi_port = int(loaded_data_dict['default_port'])
    except:
        wsgi_port = 8664

    return wsgi_port
    
def get_last_or_default_asgi_port() -> int:
    try:
        current_path = os.path.dirname(__file__)
        with open(os.path.join(current_path, 'app_data_asgi.json'), "r") as json_file:
            loaded_data_dict = json.load(json_file)
        
        asgi_port = int(loaded_data_dict['default_port'])
        # if default_asgi_port == get_last_or_default_asgi_port(): # Should not be tolerated if using the API (we do not rely on the django server for prod (API based))
            # asgi_port = 5664
        # else:
            # asgi_port = default_asgi_port
    except:
        asgi_port = 5664

    return asgi_port

def generate_free_wsgi_port(wsgi_port:int=None) -> int:
    if wsgi_port is None:
        wsgi_port = get_last_or_default_wsgi_port()    
    while is_port_busy(wsgi_port):
        wsgi_port += 1
    return wsgi_port

def generate_free_asgi_port(asgi_port:int=None, different_than=None) -> int:
    if asgi_port is None:
        asgi_port = get_last_or_default_asgi_port()    
    while is_port_busy(asgi_port) or asgi_port == different_than:
        asgi_port += 1
    return asgi_port

def is_server_live(url):
    '''
    Ping the server to check if it's live
    '''
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except requests.ConnectionError:
        return False
    return False

def erase_line():
    sys.stdout.write('\r')
    sys.stdout.write(' ' * 80)
    sys.stdout.write('\r')
    sys.stdout.flush()

def get_platform() -> str:
    system = platform.system()
    if system == 'Windows':
        return 'windows'
    elif system == 'Linux':
        return 'linux'
    elif system == 'Darwin':
        return 'mac'
    else:
        return None

def start_asgi_server(asgi_port=None, silent=False, is_blocking=True):
    '''
    runserver asgi server
    '''

    def thread_job(stderr_file_path):
        global thread_failed, thread_error_msg
        current_path = os.path.dirname(__file__)
        base_path = os.path.dirname(current_path)
        server_req = f"daphne -b=0.0.0.0 --port={asgi_port} spartaqube_app.asgi:application &"
        # print("server_req")
        # print(server_req)
        with open(stderr_file_path, 'w') as stderr_file:
            process = subprocess.Popen(
                server_req, 
                stdout=subprocess.PIPE, 
                stderr=stderr_file,
                # stderr=subprocess.PIPE, 
                shell=True,
                cwd=base_path,
            )
            if is_blocking:
                process.communicate() # This line is important to block the terminal running spartaqube

    # Create a temporary file to hold the stderr output
    stderr_file = tempfile.NamedTemporaryFile(delete=False)
    stderr_file_path = stderr_file.name
    stderr_file.close()

    t_awsgi = threading.Thread(target=thread_job, args=(stderr_file_path, ))
    t_awsgi.start()
    # thread_job()
    
    i = 0
    while True:
        if not silent:
            # animation
            if i > 3:
                i = 0
            erase_line()
            sys.stdout.write(f'\rWaiting for asgi server application{i*"."}')
            sys.stdout.flush()
            i += 1

        # Check if the stderr file has any content
        with open(stderr_file_path, 'r') as f:
            stderr_output = f.read()
            if stderr_output is not None:
                if len(stderr_output) > 0:
                    global thread_failed, thread_error_msg
                    thread_failed = True
                    thread_error_msg = stderr_output
                    print("stderr_output")
                    print(stderr_output)
        
        if is_port_available(asgi_port):
            break
        
        if thread_failed:  # Check if thread is alive or if it failed
            print("\nThread crashed or command failed. Exiting loop.")
            raise Exception(thread_error_msg)
            # break

        time.sleep(1)  # Wait for a second before pinging again

    # Clean up the temporary file
    try:
        os.unlink(stderr_file_path)
    except:
        pass
    
    if not silent:
        erase_line()
    
    app_data_dict = {'default_port': asgi_port}
    current_path = os.path.dirname(__file__)
    with open(os.path.join(current_path, "app_data_asgi.json"), "w") as json_file:
        json.dump(app_data_dict, json_file)

def start_server(port, silent=False, is_blocking=True):
    '''
    runserver at port
    '''
    def thread_job_wsgi(stderr_file_path):
        global thread_failed, thread_error_msg
        current_path = os.path.dirname(__file__)
        base_path = os.path.dirname(current_path)
        # f"python manage.py runserver 0.0.0.0:{port} &"
        # waitress-serve --threads=4 --port=8000 your_project.wsgi:application
        # gunicorn --workers 4 your_project.wsgi:application
        dev_server = f"python {os.path.join(base_path, 'manage.py')} runserver 0.0.0.0:{port}"
        gunicorn_server = f"gunicorn --workers 3 --bind 0.0.0.0:{port} 'spartaqube_app'.wsgi:application &"
        waitress_server = f"waitress-serve --host=0.0.0.0 --port={port} spartaqube_app.wsgi:application &"
        platform = get_platform()
        server_req = gunicorn_server
        if platform == 'windows':
            server_req = waitress_server

        # server_req = dev_server
        # server_req = f"/usr/local/bin/python3.11 --version"
        # print("server_req > "+str(server_req))
        with open(stderr_file_path, 'w') as stderr_file:
            process = subprocess.Popen(
                server_req, 
                stdout=subprocess.PIPE, 
                stderr=stderr_file,
                # stderr=subprocess.PIPE, 
                shell=True,
                cwd=base_path,
            )
            if is_blocking:
                process.communicate() # This line is important to block the terminal running spartaqube

    # Create a temporary file to hold the stderr output
    stderr_file = tempfile.NamedTemporaryFile(delete=False)
    stderr_file_path = stderr_file.name
    stderr_file.close()

    t_wsgi = threading.Thread(target=thread_job_wsgi, args=(stderr_file_path, ))
    t_wsgi.start()
    # thread_job()
    
    i = 0
    while True:
        if not silent:
            # animation
            if i > 3:
                i = 0
            erase_line()
            sys.stdout.write(f'\rStarting SpartaQube server{i*"."}')
            sys.stdout.flush()
            i += 1

        # Check if the stderr file has any content
        with open(stderr_file_path, 'r') as f:
            stderr_output = f.read()
            if stderr_output is not None:
                if len(stderr_output) > 0:
                    global thread_failed, thread_error_msg
                    thread_failed = True
                    thread_error_msg = stderr_output

        if is_server_live(f"http://127.0.0.1:{port}"):
            break
        
        if thread_failed:  # Check if thread is alive or if it failed
            print("\nThread crashed or command failed. Exiting loop.")
            raise Exception(thread_error_msg)
            # break

        time.sleep(1)  # Wait for a second before pinging again

    # Clean up the temporary file
    try:
        os.unlink(stderr_file_path)
    except:
        pass
    
    if not silent:
        erase_line()
    
    app_data_dict = {'default_port': port}
    current_path = os.path.dirname(__file__)
    with open(os.path.join(current_path, "app_data.json"), "w") as json_file:
        json.dump(app_data_dict, json_file)

def stop_server(port=None):
    if port is None:
        port = get_last_or_default_wsgi_port()

    if port is not None:
        process = find_process_by_port(port)
        if process:
            print(f"Found process running on port {port}: {process.pid}")
            process.terminate()
            print(f"SpartaQube server stopped")
        else:
            print(f"No process found running on port {port}.")
    else:
        raise Exception("Port not specify")

def stop_server_asgi(port=None):
    if port is None:
        port = get_last_or_default_asgi_port()

    if port is not None:
        process = find_process_by_port(port)
        if process:
            # print(f"Found process running on port {port}: {process.pid}")
            process.terminate()
            # print(f"SpartaQube server stopped")
        else:
            print(f"No process found running on port {port}.")
    else:
        raise Exception("Port not specify")

def django_setup():
    '''
    Set up Django environment
    '''
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spartaqube_app.settings')
    django.setup()

def entrypoint(port, asgi_port, force_startup=False, silent=False):
    '''
    port and asgi_port must be free.
    This is for the local server only. If we want to connect to another instance, just use the api token
    '''
    if not silent:
        sys.stdout.write("Preparing SpartaQube, please wait...")

    # print("port >>>>>>>>>>> "+str(port))
    # print("asgi_port >>>>>>>>>>> "+str(asgi_port))

    # if is_port_busy(port) and not force_startup:
    #     # We do nothing as we should already be connected to the required port
    #     # Application is supposed to be running already on this port. If an error, it will be found in the get_status called after
    #     print("Api port is busy")
    #     start_asgi_server(asgi_port=asgi_port, silent=silent) # Case for multiple spartaqube app launched (all running on the API token)
    # else:
    # set_spartaqube_shortcut()
    django_setup()
    # has_changes = db_make_migrations()
    # print("--- %s seconds db_make_migrations ---" % (time.time() - start_time))
    # if has_changes:
    #     db_migrate()
    db_make_migrations_migrate()
    create_public_user()
    create_admin_user()

    # if not is_port_busy(asgi_port):
    # print("Start ASGI server here")
    # print("asgi_port")
    # print(asgi_port)
    start_asgi_server(asgi_port=asgi_port, silent=silent)
    start_server(port=port, silent=silent)

if __name__ == '__main__':
    entrypoint()
