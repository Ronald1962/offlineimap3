# OfflineIMAP initialization code
# Copyright (C) 2002-2017 John Goerzen & contributors
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

import os
import sys
import socket
import logging
import traceback
import collections
from optparse import OptionParser

import offlineimap
import imaplib

from offlineimap import globals as glob
from offlineimap.CustomConfig import CustomConfigParser

PYTHON_VERSION = sys.version.split(' ')[0]


class OfflineImap:
    """The main class that encapsulates the high level use of OfflineImap.

    To invoke OfflineImap you would call it with::

      oi = OfflineImap()
      oi.run()
    """

    def get_env_info(self):
        info = "imaplib v%s, Python v%s" % (imaplib.__version__, PYTHON_VERSION)
        try:
            import ssl
            info = "%s, %s" % (info, ssl.OPENSSL_VERSION)
        except:
            pass
        return info

    def run(self):
        """Parse the commandline and invoke everything"""
        # next line also sets self.config and self.ui
        options, args = self.__parse_cmd_options()

    def __parse_cmd_options(self):
        parser = OptionParser(
            version=offlineimap.__version__,
            description="%s.\n\n%s" % (offlineimap.__copyright__,
                                       offlineimap.__license__)
        )

        parser.add_option("-V",
                          action="store_true", dest="version",
                          default=False,
                          help="show full version infos")

        parser.add_option("--dry-run",
                          action="store_true", dest="dryrun",
                          default=False,
                          help="dry run mode")

        parser.add_option("--info",
                          action="store_true", dest="diagnostics",
                          default=False,
                          help="output information on the configured email repositories")

        parser.add_option("-1",
                          action="store_true", dest="singlethreading",
                          default=False,
                          help="(the number one) disable all multithreading operations")

        parser.add_option("-P", dest="profiledir", metavar="DIR",
                          help="sets OfflineIMAP into profile mode.")

        parser.add_option("-a", dest="accounts",
                          metavar="account1[,account2[,...]]",
                          help="list of accounts to sync")

        parser.add_option("-c", dest="configfile", metavar="FILE",
                          default=None,
                          help="specifies a configuration file to use")

        parser.add_option("-d", dest="debugtype",
                          metavar="type1[,type2[,...]]",
                          help="enables debugging for OfflineIMAP "
                               " (types: imap, maildir, thread)")

        parser.add_option("-l", dest="logfile", metavar="FILE",
                          help="log to FILE")

        parser.add_option("-s",
                          action="store_true", dest="syslog",
                          default=False,
                          help="log to syslog")

        parser.add_option("-f", dest="folders",
                          metavar="folder1[,folder2[,...]]",
                          help="only sync the specified folders")

        parser.add_option("-k", dest="configoverride",
                          action="append",
                          metavar="[section:]option=value",
                          help="override configuration file option")

        parser.add_option("-o",
                          action="store_true", dest="runonce",
                          default=False,
                          help="run only once (ignore autorefresh)")

        parser.add_option("-q",
                          action="store_true", dest="quick",
                          default=False,
                          help="run only quick synchronizations (don't update flags)")

        parser.add_option("--delete-folder", dest="deletefolder",
                          default=None,
                          metavar="FOLDERNAME",
                          help="Delete a folder (on the remote repository)")

        parser.add_option("--mbnames-prune",
                          action="store_true", dest="mbnames_prune", default=False,
                          help="remove mbnames entries for accounts not in accounts")

        (options, args) = parser.parse_args()
        glob.set_options(options)

        if options.version:
            print(("offlineimap v%s, %s" % (
                offlineimap.__version__, self.get_env_info())
                   ))
            sys.exit(0)

        # Read in configuration file.
        if not options.configfile:
            # Try XDG location, then fall back to ~/.offlineimaprc
            xdg_var = 'XDG_CONFIG_HOME'
            if xdg_var not in os.environ or not os.environ[xdg_var]:
                xdg_home = os.path.expanduser('~/.config')
            else:
                xdg_home = os.environ[xdg_var]
            options.configfile = os.path.join(xdg_home, "offlineimap", "config")
            if not os.path.exists(options.configfile):
                options.configfile = os.path.expanduser('~/.offlineimaprc')
            configfilename = options.configfile
        else:
            configfilename = os.path.expanduser(options.configfile)

        config = CustomConfigParser()
        if not os.path.exists(configfilename):
            # TODO, initialize and make use of chosen ui for logging
            logging.error(" *** Config file '%s' does not exist; aborting!" %
                          configfilename)
            sys.exit(1)
        config.read(configfilename)
        return options, args
