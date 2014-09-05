import os
import time
import shutil
import sublime
import sublime_plugin

"""
Sublime Text 3 plugin for file synchronization between workspaces.
https://github.com/weverss/FSync
"""


class FSync(sublime_plugin.EventListener):
    """
    Class extends Sublime event listener to start synchronization triggered

    by user save actions.
    """

    # Last synchronization time between locations. Used to determine
    # whether the files needs to be synchronized or not.
    last_sync_time = 0

    def on_post_save_async(self, view):
        """
        Method asynchronously called by Sublime Text on user save actions.
        """

        # Load settings
        self.settings = sublime.load_settings('FSync.sublime-settings')
        self.local_workspace = self.settings.get('local_workspace')
        self.remote_workspace = self.settings.get('remote_workspace')
        self.ignore_extensions = self.settings.get('ignore_extensions', [])

        if self.local_workspace is None or self.remote_workspace is None:
            print(
                'FSync WARNING: Please, fill \'local_workspace\' and'
                ' \'remote_workspace\' at user settings.'
            )
            return

        self.run_pre_sync()
        self.sync()

    def run_pre_sync(self):
        """
        Use file to determine tha last sync time.
        """

        if os.path.isfile(self.local_workspace + '/.FSync'):

            # Read file properties to get last sync time.
            self.last_sync_time = os.path.getmtime(
                self.local_workspace + '/.FSync'
            )

        # Touch file for the next operation reference.
        open(self.local_workspace + '/.FSync', 'w').close()

    def sync(self):
        """
        Perform synchronization between locations. The first operation will not
        check for modified files. Instead, it will copy all files and
        directories on the remote workspace.
        """

        # Get changed files.
        changed_files = self.get_changed_files()

        if not changed_files:
            return

        print('Synchronizing files:')
        for local_file in changed_files:

            remote_file_directory = local_file['directory_path'].replace(
                self.local_workspace,
                self.remote_workspace
            )

            # Create folders on the remote location, in case they don't
            # exist.
            if os.path.isdir(remote_file_directory) is False:
                os.makedirs(remote_file_directory)

            # Perform copy.
            shutil.copy(local_file['file_path'], remote_file_directory)
            print("+ " + local_file['file_path'])

        print('Files synchronized.')

    def get_changed_files(self):
        """
        Return modified files since last synchronization.
        """

        changed_files = []

        for top, directories, files in os.walk(self.local_workspace):
            for file in files:

                # Set file path and modification time.
                file_path = os.path.join(top, file)
                file_modification_time = os.path.getmtime(file_path)

                # Skip not modified files.
                if file_modification_time < self.last_sync_time:
                    continue

                # Ignore some files based on its extension.
                if self.ignore_file(file_path):
                    continue

                changed_files.append({
                    'directory_path': top,
                    'file_path': file_path
                })

        return changed_files

    def ignore_file(self, file_path):
        """
        Determine whether ignore a file or not based on its extension.
        """

        for ignored_file_extension in self.ignore_extensions:
            if file_path.endswith(ignored_file_extension):
                return True

        return False
