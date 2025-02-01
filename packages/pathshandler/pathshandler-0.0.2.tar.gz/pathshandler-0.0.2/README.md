# pathshandler

The people you works with use a different operating system than you ? Or they store the project you are working on together in a different location on their computer ?

This package attributes a given name to a desired path, so each member of a team can refer to a similar name while directing to different paths specific to each computer.


Main features
-------------

- **Paths naming**.

- **Queries on files and folders**.



Installation or upgrade
-----------------------

To install `pathshandler`, use::

     pip install pathshandler

To upgrade from an older version, use::

     pip install --upgrade pathshandler



Quick usage example
-----------------------

```python
import pathshandler as ph

# store a path inside the config file
ph.register_path('notebooks', '/home/john/Documents/projects/notebooks')

# retrieve the path
path_notebooks = ph.get_path('notebooks')

# search for all files containing the expression 'experimentB' in the folder attributed to the name 'notebooks'
wanted_files = ph.search(name='notebooks', pattern='experimentB', category='files') 
```


API Reference
-----------------------
 
| Function | Description
| :---------| :----------
| `get_path()` | Return the path corresponding to the given name
| `load_config()` | Return the content of paths_config.json which contains the names and the corresponding paths
| `register_path()` | Add a path and its corresponding name inside the paths_config.json file
| `remove_path()` | Remove a path and its corresponding name from the paths_config.json file
| `search()` | Select files in a given folder
| `save_config()` | Save the paths_config.json file


Further details are in the online documentation
<https://g-patin.github.io/pathshandler/>.
