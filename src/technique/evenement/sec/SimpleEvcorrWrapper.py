# -*- coding: utf-8 -*-
__author__ = "Tirath Ramdas"

import os
import subprocess
import fcntlmodule, time

#===============================================================================
# from threading  import Thread
# import sys, 
# try:
#     from Queue import Queue, Empty
# except ImportError:
#     from queue import Queue, Empty  # python 3.x
#     
# 
# ON_POSIX = 'posix' in sys.builtin_module_names
#===============================================================================


class SimpleEvcorrWrapperException(Exception):
    pass


class SimpleEvcorrWrapper(object):
    """
    A wrapper around Simple Event Correlator (http://simple-evcorr.sourceforge.net/).
    """

    def __init__(self, conf_path, bin_path="/home/kengne/sec_assets/sec"):
        """
        Create a wrapper around the local sec binary.

        :type conf_path: str
        :param conf_path: path to desired sec conf file
        :type bin_path: str
        :param bin_path: path to the sec binary (defaults to the homebrew-provided path)
        """
        self._conf_path = None
        self._bin_path = None
        self._run_sec = None

        self.bin_path = bin_path
        self.conf_path = conf_path

    @property
    def conf_path(self):
        return self._conf_path

    @conf_path.setter
    def conf_path(self, conf_path):
        assert isinstance(conf_path, str)
        os.path.isfile(conf_path)
        self._conf_path = conf_path

    @property
    def bin_path(self):
        return self._bin_path

    @bin_path.setter
    def bin_path(self, bin_path):
        assert isinstance(bin_path, str)
        os.path.isfile(bin_path)
        try:
            check_sec_exists = subprocess.Popen([bin_path, "-version"],
                                                stdout=subprocess.PIPE,
                                                stderr=subprocess.STDOUT)
            output = check_sec_exists.communicate()
            if check_sec_exists.returncode != 0:
                error_msg = "sec bin check failed: {}".format(output)
                raise SimpleEvcorrWrapperException(error_msg)
        except OSError, oserror_exception:
            error_msg = "{} does not exist? ({})".format(bin_path, oserror_exception)
            raise SimpleEvcorrWrapperException(error_msg)

        self._bin_path = bin_path

    def start(self, event_source_path):
        """
        Start sec with the previously specified conf, on the specified event source file. Returns a generator that
        yields lines from sec.

        :type event_source_path: str
        :param event_source_path: path to input event source
        :return: an event source generator
        """
        assert isinstance(event_source_path, str)
        os.path.isfile(event_source_path)
        sec_cmd = [self.bin_path, "-conf", self.conf_path, "-input", event_source_path, "-fromstart"]

        self._run_sec = subprocess.Popen(sec_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        fl = fcntlmodule.fcntl(self._run_sec.stdout, fcntlmodule.F_GETFL)
        fcntlmodule.fcntl(self._run_sec.stdout, fcntlmodule.F_SETFL, fl | os.O_NONBLOCK)        
        try:
            time.sleep(3)
            with self._run_sec.stdout:
                for line in iter(self._run_sec.stdout.readline, b""):
                    yield line.rstrip()
        except IOError:
            print 'stop'
        finally:
            self.stop()
                

    def stop(self):
        """
        Stops sec process if running (causes generator provided by 'start' to return).

        :rtype: None
        """
        if self._run_sec:
            self._run_sec.terminate()
            self._run_sec.wait()
            self._run_sec = None
            
    

    def __del__(self):
        self.stop()
        

    #===========================================================================
    # def enqueue_output(self, out, queue): 
    #     with out:
    #         for line in iter(out.readline(), b""):
    #             print line
    #             queue.put(line)
    #===========================================================================
    
#===============================================================================
#     def start(self, event_source_path):
#         """
#         Start sec with the previously specified conf, on the specified event source file. Returns a generator that
#         yields lines from sec.
# 
#         :type event_source_path: str
#         :param event_source_path: path to input event source
#         :return: an event source generator
#         """
#         assert isinstance(event_source_path, str)
#         os.path.isfile(event_source_path)
#         sec_cmd = [self.bin_path, "-conf", self.conf_path, "-input", event_source_path, "-input-timeout", 1, "-fromstart"]
# 
#         self._run_sec = subprocess.Popen(sec_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#         
#         q = Queue()
#         t = Thread(target=self.enqueue_output, args=(self._run_sec.stdout, q))
#         t.daemon = True # thread dies with the program
#         t.start()
#         
#         
#         
#         try:  
#             line = q.get_nowait() # or q.get(timeout=.1)
#         except Empty:
#             print q.empty()
#         else: #
#             try:
#                 with self._run_sec.stdout:
#                     for line in iter(self._run_sec.stdout.readline, b""):
#                         yield line.rstrip()
#             finally:
#                 self.stop()
#===============================================================================
