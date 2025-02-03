#!/usr/bin/env python3
#author: Hadi Cahyadi
#email: cumulus13@gmail.com

import sys
from ctraceback import CTraceback
sys.excepthook = CTraceback()
from ctraceback.custom_traceback import console
import importlib
import os
import time
import subprocess
import logging
from configset import configset
from pathlib import Path
import argparse
from sendgrowl import Growl
import bitmath
from datetime import datetime


if sys.platform == 'win32':
    spec_syslog = importlib.util.spec_from_file_location("syslog", str(Path(__file__).parent / 'syslogx.py'))
    syslog = importlib.util.module_from_spec(spec_syslog)
    spec_syslog.loader.exec_module(syslog)
else:
    import syslog
    
if sys.platform == 'win32': import win32com.client as com

from pydebugger.debug import debug
    
class DiskSpaceMon:
    VERBOSE = False
    CONFIG = configset(str(Path(__file__).parent / Path(__file__).stem) + ".ini")
    WATCH_DIR = CONFIG.get_config_as_list('drive', 'names')  # Change to the directory you want to monitor
    THRESHOLD_MB = bitmath.MB(CONFIG.get_config('size', 'threshold') or 100).bytes  # Alert if space increases by more than 100MB
    CHECK_INTERVAL = CONFIG.get_config('check', 'interval') or 60  # Check every 60 seconds
    SYSLOG_SERVER = CONFIG.get_config('syslog', 'host') or "127.0.0.1"  # Change to your remote syslog server
    SYSLOG_PORT = CONFIG.get_config('syslog', 'port') or 514  # Change to your remote syslog port
    GROWL_HOST = CONFIG.get_config('growl', 'host') or "127.0.0.1"  # Change to your remote growl host server
    GROWL_PORT = CONFIG.get_config('growl', 'port') or 23053  # Change to your remote growl port server
    
    if os.getenv('VERBOSE') == '1': VERBOSE = True
    
    if VERBOSE in [2, '2']:
        debug(WATCH_DIR = WATCH_DIR, debug = 1)
        debug(THRESHOLD_MB = THRESHOLD_MB, debug = 1)
        debug(CHECK_INTERVAL = CHECK_INTERVAL, debug = 1)
        debug(SYSLOG_SERVER = SYSLOG_SERVER, debug = 1)
        debug(SYSLOG_PORT = SYSLOG_PORT, debug = 1)
        debug(GROWL_HOST = GROWL_HOST, debug = 1)
        debug(GROWL_PORT = GROWL_PORT, debug = 1)

    # Setup logging for remote syslog
    logger = logging.getLogger("DiskMonitor")
    logger.setLevel(logging.DEBUG)

    @classmethod
    def get_directory_size(cls, path, verbose = False):
        """Returns the directory size in MB"""
        def get_size(p):
            if os.path.isdir(p):
                if sys.platform == 'win32':
                    try:
                        fso = com.Dispatch("Scripting.FileSystemObject")
                        size = fso.GetFolder(p).Size
                        return size
                    except Exception as e:
                        console.print(f"[error]Error getting directory size: {e}[/], [bold #00FFFF]set VERBOSE env or verbose or use -v/-vv/-vvv for more details[/]")
                        if verbose == 3 or cls.VERBOSE in ['3', 3]: CTraceback(*sys.exc_info())
                        return -1
                else:
                    try:
                        size = subprocess.check_output(["du", "-smh", path]).split()[0]
                        size = bitmath.parse_string_unsafe(size).bytes
                        return int(size)
                    except Exception as e:
                        console.print(f"[error]Error getting directory size: {e}[/], [bold #00FFFF]set VERBOSE env or verbose or use -v/-vv/-vvv for more details[/]")
                        if verbose == 3 or cls.VERBOSE in ['3', 3]: CTraceback(*sys.exc_info())
                        return -1
            else:
                console.print(f"[error]directory '{p}' is not a directory !.")
            return -1
                    
        # if not isinstance(path, list or tuple): path = [path]
        if verbose  == 2 or cls.VERBOSE in [2, '2']: debug(path = path, debug = 1)
        
        if isinstance(path, list or tuple):
            for p in path:
                return get_size(p)
        else:
            return get_size(path)
                

    @classmethod
    def send_growl_notification(cls, message, host = None, port = None, verbose = False):
        """Sends notification using Growl (if available)"""
        host = host or cls.GROWL_SERVER or '127.0.0.1'
        port = port or cls.GROWL_PORT or 514
        
        if not isinstance(host, list or tuple): host = [host]
        if not isinstance(port, list or tuple): port = [port]
        
        if verbose  == 2 or cls.VERBOSE in [2, '2']:
            debug(host = host, debug = 1)
            debug(port = port, debug = 1)
        try:
            if verbose  == 2 or cls.VERBOSE in [2, '2']: console.print(f"[notice]send message to growl[/] [warning]{host}[/]:[critical]{port}[/]")
            Growl().send("DiskSpaceMon", 'monitor', 'DiskSpaceMon', message, host = host, port = port)
        except Exception as e:
            console.print(f"[error]Error send to growl: {e}[/], [bold #00FFFF]set VERBOSE env or verbose or use -v/-vv/-vvv for more details[/]")
            if verbose == 3 or cls.VERBOSE in ['3', 3]: CTraceback(*sys.exc_info())
            return -1
    
    @classmethod
    def send_syslog_notification(cls, message, host = None, port = None, verbose = False):
        """Sends notification to remote syslog"""
        host = host or cls.SYSLOG_SERVER or '127.0.0.1'
        port = port or cls.SYSLOG_PORT or 514
        
        if not isinstance(host, list or tuple): host = [host]
        if not isinstance(port, list or tuple): port = [port]
        
        if verbose  == 2 or cls.VERBOSE in [2, '2']:    
            debug(host = host, debug = 1)
            debug(port = port, debug = 1)
            
        for h in host:    
            try:
                if sys.platform == 'win32':
                    if verbose  == 2 or cls.VERBOSE in [2, '2']: console.print(f"[notice]send message to syslog[/] [warning]{host}[/]:[critical]{port}[/]")
                    # message = message.encode() if not isinstance(message, bytes) else message
                    syslog.send(message, host = h, port = port[host.index(h)] if len(host) == len(port) else port[0]) 
                else:
                    if verbose == 3 or cls.VERBOSE in ['3', 3]: console.print(f"[notice]send message to syslog[/] [warning]{host}[/]:[critical]{port}[/]")
                    syslog_handler = logging.handlers.SysLogHandler(address=(h, port[host.index(h)] if len(host) == len(port) else port[0]))
                    cls.logger.addHandler(syslog_handler)
                    syslog.syslog(syslog.LOG_INFO, message)
                    cls.logger.info(message)
            except Exception as e:  
                console.print(f"[error]Error send to syslog: {e}[/], [bold #00FFFF]set VERBOSE env or verbose or use -v/-vv/-vvv for more details[/]")
                if verbose == 3 or cls.VERBOSE in ['3', 3]: CTraceback(*sys.exc_info())
                return -1

    @classmethod
    def get_date(cls):
        return datetime.strftime(datetime.now(), '%Y/%m/%d %H:%M:%S.%f')
    
    @classmethod
    def monitor_directory(cls, paths = None, interval = None, threshold = None, verbose = False):
        """Monitors the directory and sends notifications if usage increases significantly"""
        
        console.print(f"[#00FFFF bold]{cls.get_date()} - [bold #FFFF00]Monitoring directory:[/] [notice]{paths}[/] in [critical]{interval or cls.CHECK_INTERVAL}[/] seconds, size threshold: [allert]{threshold or cls.THRESHOLD_MB} MB[/]")
        paths = paths or cls.WATCH_DIR
        previous_size = cls.get_directory_size(paths, verbose=verbose)
        if verbose == 2 or cls.VERBOSE in [2, '2']: debug(paths = paths, debug = 1)
        while True:
            time.sleep(interval or cls.CHECK_INTERVAL)
            if verbose > 1: console.print(f"[#00FFFF bold]{cls.get_date()} - [bold #FFFF00]Monitoring directory:[/] [notice]{paths}[/] in [critical]{interval or cls.CHECK_INTERVAL}[/] seconds, size threshold: [allert]{threshold or cls.THRESHOLD_MB} MB[/]")   
            current_size = cls.get_directory_size(paths)

            if current_size == -1:
                continue

            increase = current_size - previous_size
            if increase > bitmath.MB(threshold).bytes if threshold else cls.THRESHOLD_MB:
                message = f"{cls.get_date()} - Disk Usage Alert: {paths} increased by {str(bitmath.best_prefix(increase).MB)} !"
                message1 = f"[#FF5500 bold]{cls.get_date()}[/] - [warning]Disk Usage Alert:[/] [critical]{paths}[/] [notice]increased by[/] [error]{str(bitmath.best_prefix(increase).MB)} ![/]"
                message2 = f"[warning]Disk Usage Alert:[/] [critical]{paths}[/] [notice]increased by[/] [error]{str(bitmath.best_prefix(increase).MB)} ![/]"
                
                console.print(message1)  # Print for logging in the container

                cls.send_growl_notification(message, verbose=verbose)
                cls.send_syslog_notification(message2, verbose=verbose)

            previous_size = current_size
            
    @classmethod
    def usage(cls):
        parser = argparse.ArgumentParser()
        parser.add_argument('PATHS', help = 'Directory to watching')
        parser.add_argument('-t', '--size-threshold', action = 'store', help = 'Size threshold default = 100 MB', default = cls.THRESHOLD_MB, type = int)
        parser.add_argument('-i', '--interval', action = 'store', help = 'Interval time', default = cls.CHECK_INTERVAL, type = int)
        parser.add_argument('--syslog-host', action = 'store', help = f'Syslog host name/ip, default: {cls.SYSLOG_SERVER}', default = cls.SYSLOG_SERVER)
        parser.add_argument('--syslog-port', action = 'store', help = f'Syslog port, default: {cls.SYSLOG_PORT}', default = cls.SYSLOG_PORT, type = int)
        parser.add_argument('--growl-host', action = 'store', help = f'Growl host name/ip, default: {cls.GROWL_HOST}', default = cls.GROWL_HOST, nargs = '*')
        parser.add_argument('--growl-port', action = 'store', help = f'Growl port, default: {cls.GROWL_PORT}', default = cls.GROWL_PORT, nargs = '*', type = int)
        parser.add_argument('-v', '--verbose', help = "Show detail process", action='count')
        
        if len(sys.argv) == 1:
            parser.print_help()
        else:
            args = parser.parse_args()
            cls.VERBOSE = args.verbose or cls.VERBOSE
            cls.THRESHOLD_MB = bitmath.MB(args.size_threshold).bytes or cls.THRESHOLD_MB
            cls.SYSLOG_SERVER = args.syslog_host or cls.SYSLOG_SERVER
            cls.SYSLOG_PORT = args.syslog_port or cls.SYSLOG_PORT
            cls.GROWL_SERVER = args.growl_host or cls.GROWL_SERVER
            cls.GROWL_PORT = args.growl_port or cls.GROWL_PORT

            if args.PATHS: cls.monitor_directory(args.PATHS, args.interval, args.size_threshold, args.verbose)
                

if __name__ == "__main__":
    DiskSpaceMon.usage()
