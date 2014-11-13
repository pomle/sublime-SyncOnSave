import sublime, sublime_plugin, os

class SyncOnSave(sublime_plugin.EventListener):

  def on_post_save(self, view):
    def shellquote(s):
      return "'" + s.replace("'", "'\\''") + "'"

    remote_dirs = view.settings().get('sync_on_save')
    if not remote_dirs:
      print 'SyncOnSave: Project not configured for sync_on_save. Try setting sync_on_save in project settings.'
      return

    if isinstance(remote_dirs, basestring):
      remote_dirs = [remote_dirs]

    commands = []
    for remote_dir in remote_dirs:
      remote_dir = remote_dir.strip('/') + '/'

      folder = view.window().folders()[0]
      file_name = view.window().active_view().file_name()

      if folder not in file_name:
        print 'File %s not child of %s' % (file_name, folder)
        return

      relative_file_name = file_name.replace(folder, '').strip('/')
      command = 'rsync --relative %s %s' % (shellquote(relative_file_name), shellquote(remote_dir))

      commands.append(command)

    view.window().run_command('exec', {'cmd':[" && ".join(commands)], 'working_dir':folder, 'shell': True})