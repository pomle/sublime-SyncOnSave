import sublime
import sublime_plugin
import subprocess
import threading


class SyncManager(object):

    def __init__(self, cwd, source='./'):
        self.cwd = cwd
        self.source = source
        self.processes = []

    def add_remote(self, remote):
        process = ThreadedSyncer(self.source, remote)
        self.processes.append(process)

    def sync(self, delete=False):
        remotes = []
        for process in self.processes:
            process.cwd = self.cwd
            process.delete = delete
            process.start()
            remotes.append(process.remote)
        sublime.status_message('Queued sync to %d host(s): %s' %
                               (len(remotes), " ,".join(remotes)))


class ThreadedSyncer(threading.Thread):

    def __init__(self, source, remote):
        self.cwd = None
        self.delete = False
        self.source = source
        self.remote = remote
        self.result = None
        threading.Thread.__init__(self)

    def run(self):
        commands = ['rsync',
                    '-ruv',
                    '--relative',
                    self.source,
                    self.remote.strip('/') + '/']

        if self.delete:
            commands.append('--delete')

        print ('Calling subprocess %s from working dir %s' %
               (" ".join(commands), self.cwd))

        def complete():
            sublime.status_message('Completed syncing %s to %s' %
                                   (self.source, self.remote))

        try:
            subprocess.check_call(commands, cwd=self.cwd)
            sublime.set_timeout(complete, 0)
        except subprocess.CalledProcessError as e:
            sublime.error_message('Error syncing to %s\n%s' %
                                  (self.remote, e))


def get_sync_config(view):
    config = view.settings().get('sync_on_save')
    project_folders = view.window().folders()

    parsed_config = []

    if not config:
        print 'Sync: Project not configured for sync.'
        return False

    # Intercept legacy config and update it
    if (isinstance(config, basestring) or
       (isinstance(config, list) and isinstance(config[0], basestring))):
        remotes = config
        if isinstance(remotes, basestring):
            remotes = [remotes]

        # Legacy always uses only first folder
        project_folders = [view.window().folders()[0]]
        config = [{
            "source": project_folders[0],
            "remotes": remotes
        }]

    for path in config:
        source = path.get('source')
        if source not in project_folders:
            print ("Skipping %s because not a project folder %s",
                   (source, project_folders))
            continue
        parsed_config.append({
            "source": source,
            "remotes": path.get('remotes'),
        })

    return parsed_config


class ResyncCommand(sublime_plugin.TextCommand):

    def run(self, edit, delete=False):
        sync_config = get_sync_config(self.view)
        if not sync_config:
            sublime.message_dialog("No sync configured")
            return

        if delete and not sublime.ok_cancel_dialog("Are you sure you want to sync all files to remotes and delete all unknown files from remotes?"):
            return

        for path in sync_config:
            syncer = SyncManager(path['source'])
            for remote in path['remotes']:
                syncer.add_remote(remote)
            syncer.sync(delete)


class SyncOnSave(sublime_plugin.EventListener):

    def on_post_save(self, view):
        sync_config = get_sync_config(view)
        if not sync_config:
            return

        file_name = view.window().active_view().file_name()

        for path in sync_config:
            folder = path['source']
            if folder not in file_name:
                print 'File %s not child of %s' % (file_name, folder)
                continue

            relative_file_name = file_name.replace(folder, '').strip('/')

            syncer = SyncManager(folder, relative_file_name)
            for remote in path['remotes']:
                syncer.add_remote(remote)

            syncer.sync()
