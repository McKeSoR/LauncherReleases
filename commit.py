import os
import shutil
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

source_dir = '/home/ubuntu/MTechLaunchServer/gameFiles/release'
destination_dir = '/home/ubuntu/git'
git_repo_dir = '/home/ubuntu/kesor-git'  # Путь к локальному git репозиторию
git_repo_url = 'https://McKeSoR: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a@github.com/McKeSoR/LauncherReleases.git'

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            self.sync_directories()

    def on_created(self, event):
        if not event.is_directory:
            self.sync_directories()

    def on_deleted(self, event):
        if not event.is_directory:
            self.sync_directories()

    def sync_directories(self):
        source_files = set(os.listdir(source_dir))
        dest_files = set(os.listdir(destination_dir))

        for filename in source_files:
            source_file = os.path.join(source_dir, filename)
            dest_file = os.path.join(destination_dir, filename)
            if os.path.isfile(source_file):
                shutil.copy2(source_file, dest_file)

        for filename in dest_files:
            if filename not in source_files:
                dest_file = os.path.join(destination_dir, filename)
                os.remove(dest_file)

        self.commit_to_git()

    def commit_to_git(self):
        os.chdir(git_repo_dir)
        subprocess.run(['git', 'add', '.'])
        subprocess.run(['git', 'commit', '-m', 'Автоматический коммит файлов'])
        subprocess.run(['git', 'push', git_repo_url])

        print("Все файлы успешно синхронизированы и закоммичены на GitHub.")

event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, source_dir, recursive=True)

observer.start()
try:
    while True:
        pass
except KeyboardInterrupt:
    observer.stop()
observer.join()
