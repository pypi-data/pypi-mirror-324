# rconnet
The project is a module for python, and the task of the module is to create a connection to the RCON Battlefield 2142, Battlefield 2 server. Simply put, it is an RCON client.

Main idea of the project was to implement something similar to ORM, as for databases.

It was developed on version python 3.12, it was not tested on other versions.

You can learn more about the module and its API in [Wiki](https://github.com/VordyV/rconnet/wiki)

### Install
`pip install rconnet`

[pypi.org/project/rconnet/](https://pypi.org/project/rconnet/)

### Features
- Separate methods for server management
- Maplist manager
- Settings manager
- Ban manager
- Player manager
- Managers allow you to "objects" manage

### Specifications
- Adminscript - default support
- Modmanager - in the process of implementing the support
- Battlefield 2142 support (It has not been tested in Battlefield 2, but it can work)

You can do anything with this module, for example, a web banlist, a GUI program, a bot for Discord or telegram. That was the goal, to use a ready-made solution for different purposes.

## Examples
1. Simple output of the server name
```python
from rconnet.rconbf2142 import Default

with Default("127.0.0.1", "super123") as rcon:
    name = rcon.settings.server_name()
    print(name)
    # Battlefield 2142
```
2. View the maplist and install the next map
```python
from rconnet.rconbf2142 import Default

with Default("127.0.0.1", "super123") as rcon:
    maplist = rcon.maplist.list
    print(maplist)
    # {0: Map(name=minsk, gpm=gpm_cq, size=32), 1: Map(name=fall_of_berlin, gpm=gpm_cq, size=32), 2: Map(name=suez_canal, gpm=gpm_ti, size=48)}
    maplist.get(1).set_next()
    rcon.run_next_level()
```
3. Adding a ban to the list
```python
from rconnet.rconbf2142 import Default

with Default("127.0.0.1", "super123") as rcon:
    rcon.banmanager.add_ban("172.123.54.6")
    banlist = rcon.banmanager.list
    print(banlist)
    # [Ban(address=172.123.54.6, period=Perm)]
```
