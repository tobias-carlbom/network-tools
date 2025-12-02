import anvil.server
import time

@anvil.server.background_task
def keep_server_running():
    while True:
        time.sleep(5)