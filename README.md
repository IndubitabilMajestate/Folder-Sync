# Folder-Sync
It's a simple folder synchronization script between the original and a target replica.

`-s/--src` pass the absolute path of an existing source folder or it will create an empty folder at the passed path 

`-d/--dest` pass the absolute path of an existing destination folder or it will create an empty folder at the passed path

`-t/--time` delay in seconds between synchronizations

`-l/--log` absolute path to the log file or creates an empty log file

Each argument is passed followed by its value and is parsed by the `argsParser`

Run as(example, synch is defaul: 60s):
```
py main_script.py -s "path\\to\\source" -d "path\\to\\destination" -l "path\\to\\log"
```
