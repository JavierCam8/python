import sys
import subprocess
import time
import os

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class RestartHandler(FileSystemEventHandler):
    def __init__(self, script_path):
        self.script_path = script_path
        self.start_process()

    def start_process(self):
        print(f"Iniciando {self.script_path}...")
        self.process = subprocess.Popen([sys.executable, self.script_path])

    def on_modified(self, event):
        if event.is_directory:
            return
            
        # Comparamos si el archivo modificado coincide con nuestro script objetivo
        if os.path.abspath(event.src_path) == os.path.abspath(self.script_path):
            print(f"\nDetectado cambio en: {event.src_path}")
            print("Reiniciando aplicación...")

            self.process.terminate()
            self.process.wait()

            self.start_process()


if __name__ == "__main__":
    # Obtener la ruta absoluta de hotel2.py en la misma carpeta
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_a_vigilar = os.path.join(current_dir, "inicio.py")
    
    handler = RestartHandler(app_a_vigilar)

    observer = Observer()
    # Vigilar la carpeta actual de forma recursiva por si acaso
    observer.schedule(handler, path=current_dir, recursive=False)
    observer.start()

    print(f"Vigilando cambios en: {app_a_vigilar}")
    print("Presiona Ctrl+C para salir.")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nDeteniendo supervisor...")
        if handler.process:
            handler.process.terminate()
            handler.process.wait()
        observer.stop()

    observer.join()