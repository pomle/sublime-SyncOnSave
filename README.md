# sublime-SyncOnSave

Sublime plugin for syncing a file on save or syncing a full project on demand to one or more remotes using rsync.

### Installation

```
git clone https://github.com/pomle/sublime-SyncOnSave.git '~/Library/Application Support/Sublime Text 2/Packages/' SyncOnSave
```

### Configuration

You have to be in a project to use. The config is connected to the project settings.
If you haven't already, find the menu item Project > Save Project As...

Then go to Project > Edit Project and add the settings clause. You have to specify exact folder as source and saved files must reside inside that folders. This is a safety precaution and to prevent syncing files that are open but not part of project.

```
{
    "folders":
    [
        {
            "path": "/Users/pom/dev/some_project_to_reflect_remotely"
        }
    ],
    "settings":
    {
        "sync_on_save":
        [
            {
                "source": "/Users/pom/dev/some_project_to_reflect_remotely",
                "remotes": [
                    "remote_server.cloud.company.nett:dev/remote_project",
                    "optional_secondary_remore_server.mirror.com:remote"
                ]
            }
        ]
    }
}
```
