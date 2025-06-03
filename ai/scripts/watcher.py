from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time, threading
from src.app import build_and_deploy_static_site 

class ChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_change = time.time()
        self.deploy_scheduled = False

    def on_any_event(self, event):
        self.last_change = time.time()
        if not self.deploy_scheduled:
            self.deploy_scheduled = True
            threading.Thread(target=self.wait_and_deploy).start()

    def wait_and_deploy(self):
        while time.time() - self.last_change < 10:  # 10s sakinleşme süresi
            time.sleep(1)
        print("Deploy başlatılıyor...")
        
        try:
            build_and_deploy_static_site()
        except Exception as e:
            print(f"[ERROR] Deploy failed: {e}")
        
        self.deploy_scheduled = False

observer = Observer()
handler = ChangeHandler()
observer.schedule(handler, "/app/frontend/out", recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
