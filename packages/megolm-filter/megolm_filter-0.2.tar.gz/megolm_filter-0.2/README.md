### `megolm_filter.py` ###

Modify your offline megolm key backups from a shell.  

The main use of megolm_filter is to filter what keys you'd like to share with another user. Let's say you have a 1:1 chat, and the other user lost all their keys and
you need to give them access without giving access to all of your rooms.  

[There is currently no Element-based support for this](https://github.com/element-hq/element-meta/issues/1287), so this script can help in the meantime.  

Install
-------

```
pip install megolm-filter
```

Command Line Interface
----------------------

```
usage: megolm_filter [-h] [-o OUTPUT] [--plain] [file] [room_id]

Operate on megolm session backups.

positional arguments:
  file                 megolm session data
  room_id              Room id to filter (optional)

options:
  -h, --help           show this help message and exit
  -o, --output OUTPUT  Output to file
  -p, --plain          Returns the plain unencrypted content
```

You can filter your keys fairly easily running:

```bash
megolm_filter element-keys.txt '!room1:matrix.org' '!room2:matrix.org' ...
```

___
Copyright (C) 2019 Aleksa Sarai <cyphar@cyphar.com>  
Copyright (C) 2025 Lain Iwakura <lain@serialexperiments.club>  

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
