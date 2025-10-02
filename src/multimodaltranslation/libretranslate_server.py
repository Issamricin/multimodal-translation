import subprocess
import time


class Libretranslate_Server:
    """
    Handles the translation library server. Starts and stops the server through this object.
    """
    def start_libretranslate_server(self, libport:int) -> None:
        """
        Starts the library server. 

        Args:
            libport (int): The port for the translating library to start on.

        Returns:
            None
        """
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
            raise OSError

        time.sleep(2)

    def stop_libretranslate_server(self) -> None:
        """
        Stops the translator library server.

        Args:
            None

        Returns:
            None
        """
        self.process.kill()
        self.process.wait()
