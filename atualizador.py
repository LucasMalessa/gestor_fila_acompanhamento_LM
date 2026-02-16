import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class Watcher:
    def __init__(self, csv_file, notebook_file):
        self.csv_file = csv_file
        self.notebook_file = notebook_file
        self.observer = Observer()

    def run(self):
        event_handler = Handler(self.notebook_file)
        self.observer.schedule(event_handler, os.path.dirname(self.csv_file), recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

class Handler(FileSystemEventHandler):
    def __init__(self, notebook_file):
        self.notebook_file = notebook_file

    def on_modified(self, event):
        if event.src_path.endswith('.csv'):
            print(f'{event.src_path} foi modificado. Executando o notebook...')
            subprocess.run(['jupyter', 'nbconvert', '--to', 'notebook', '--execute', self.notebook_file])

def buscar_relatorio_acompanhamento():
    """Busca relatorioAcompanhamento.csv em todas as subpastas do OneDrive."""
    user_profile = os.environ.get('USERPROFILE', os.path.expanduser('~'))
    onedrive_dir = os.path.join(user_profile, 'OneDrive - EDENRED')
    
    if not os.path.isdir(onedrive_dir):
        return None
    
    for pasta in os.listdir(onedrive_dir):
        caminho = os.path.join(onedrive_dir, pasta, 'relatorioAcompanhamento.csv')
        if os.path.isfile(caminho):
            return caminho
    return None

if __name__ == '__main__':
    user_profile = os.environ.get('USERPROFILE', os.path.expanduser('~'))
    
    csv_file = buscar_relatorio_acompanhamento()
    notebook_file = os.path.join(
        user_profile,
        'OneDrive - EDENRED',
        'Gestor de Filas Acompanhamento LM',
        'gestor_filas_acompanhamento_LM.ipynb'
    )
    
    if csv_file is None:
        print("ERRO: relatorioAcompanhamento.csv não encontrado em nenhuma subpasta do OneDrive - EDENRED.")
        print("Verifique se a pasta do SharePoint está sincronizada.")
    else:
        print(f"Monitorando: {csv_file}")
        watcher = Watcher(csv_file, notebook_file)
        watcher.run()