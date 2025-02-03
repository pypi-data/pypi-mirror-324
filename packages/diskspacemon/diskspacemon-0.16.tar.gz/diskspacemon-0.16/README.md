# DiskSpaceMon
Monitoring space of directory/path/drive then send notification to growl and syslog/remote syslog with multiple host and port

## Installing

Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/):

```bash
$ pip install diskspacemon
```

## Example

```python
>>> from diskspacemon import DiskSpaceMon
>>> m = DiskSpaceMon()
>>> m.GROWL_HOST = ['127.0.0.1', '192.168.100.2']
>>> m.SYSLOG_HOST = ['127.0.0.1', '192.168.100.2']
>>> m.monitor_directory("/", 60, 100, True) # parameter: path, interval time sleep, size threshold, verbose
```

run on terminal/cmd

```bash
$ usage: diskspacemon [-h] [-t SIZE_THRESHOLD] [-i INTERVAL] [--syslog-host SYSLOG_HOST] [--syslog-port SYSLOG_PORT] [--growl-host [GROWL_HOST ...]] [--growl-port [GROWL_PORT ...]] [-v]
                  PATHS

positional arguments:
  PATHS                 Directory to watching

options:
  -h, --help            show this help message and exit
  -t SIZE_THRESHOLD, --size-threshold SIZE_THRESHOLD
                        Size threshold default = 100 MB
  -i INTERVAL, --interval INTERVAL
                        Interval time
  --syslog-host SYSLOG_HOST
                        Syslog host name/ip, default: 127.0.0.1
  --syslog-port SYSLOG_PORT
                        Syslog port, default: 514
  --growl-host [GROWL_HOST ...]
                        Growl host name/ip, default: 127.0.0.1
  --growl-port [GROWL_PORT ...]
                        Growl port, default: 23053
  -v, --verbose         Show detail process
```

## Support

- Python 3.x

## Author
[Hadi Cahyadi](mailto:cumulus13@gmail.com)

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/cumulus13)

[![Donate via Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/cumulus13)

[Support me on Patreon](https://www.patreon.com/cumulus13)


