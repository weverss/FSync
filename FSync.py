import os
import time
import shutil
import sublime
import sublime_plugin

"""
Sync plugin for Sublime Text 3. Provides one-way synchronization between local
and remote workspaces.

https://github.com/weverss/FSync
"""


class FSync(sublime_plugin.EventListener):
    """
    Class extends Sublime event listener to start synchronization triggered
    by user save actions.
    """

    # User local and remote workspaces definition. The files and
    # directories are copied only from local to remote location.
    local_workspace = '/home/wevers/workspace'
    remote_workspace = '/mnt/dev_desenvolvedores/51'

    # Last synchronization time between locations. Used to determine
    # whether the files needs to be synchronized or not.
    last_sync_time = 0

    # File extensions ignored during sync.
    ignored_file_extensions = ['.FSync', '.svn-base', 'wc.db']

    def on_post_save_async(self, view):
        """
        Method asynchronously called by Sublime Text on user save actions.
        """

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

        for ignored_file_extension in self.ignored_file_extensions:
            if file_path.endswith(ignored_file_extension):
                return True

        return False
