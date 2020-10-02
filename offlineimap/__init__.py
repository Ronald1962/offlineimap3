__all__ = ['OfflineImap']

__productname__ = 'OfflineIMAP'
# Expecting trailing "-rcN" or "" for stable releases.
__version__ = "7.3.0"
__copyright__ = "Copyright 2002-2019 John Goerzen & contributors"
__author__ = "John Goerzen"
__author_email__ = "offlineimap-project@lists.alioth.debian.org"
__description__ = "Disconnected Universal IMAP Mail Synchronization/Reader Support"
__license__ = "Licensed under the GNU GPL v2 or any later version (with an OpenSSL exception)"
__bigcopyright__ = """%(__productname__)s %(__version__)s
  %(__license__)s""" % locals()
__homepage__ = "http://www.offlineimap.org"

banner = __bigcopyright__

from offlineimap.init import OfflineImap
