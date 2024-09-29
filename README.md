# Flexible data copy
Most of the time data is copied from A to B in the same format.
There are plenty of tools for this, to name a few: totalcommander, robocopy and freefilesync.
However, occasionally the order of folders/naming must also be changed.
For example from xx/yy/zz to zz/yy/xx, this requires a more flexible copy operation.
This script is intended as universal basis for these usecases, giving the user complete freedom to change the format.

See main.py for more information and the parameters.

Why  this script?
- Lambda's for fast checksum computation
- Multiprocessed filemoves with checksum
- Status csv's to double check/debug operations