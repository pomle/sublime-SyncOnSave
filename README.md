# sublime-SyncOnSave

Sublime plugin for syncing on save or full project to one or more remotes using rsync.

### Configuration

You have to be in a project to use. The config is connected to the project settings. 
If you haven't already, find the menu item Project > Save Project As...

The go to Project > Edit Project and add the settings clause.

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
