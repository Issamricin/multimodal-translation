import subprocess
import time

class Libretranslate_Server():
    def __init__(self):
        pass
    def start_libretranslate_server(self, libport):
        self.process = subprocess.Popen(
            [ "libretranslate", "--port", f"{libport}"],  
            stdout=subprocess.PIPE,   
            stderr=subprocess.PIPE,
        )
        try:
            outs, errs = self.process.communicate(timeout=3)
        except subprocess.TimeoutExpired:
            pass
        else:
            raise Exception

        time.sleep(2)

    def stop_libretranslate_server(self):
        self.process.kill()
        self.process.wait()