# Copyright (C) 2007-2009 Samuel Abels.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2, as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

class StreamAnalyzer(object):
    """
    A StreamAnalyzer monitors everything that happens on a Transport,
    and attempts to collect data out of the network activity.
    For example, a stream monitor may watch for specific patterns in the
    network traffic to decide what operating system a connected host is
    running.
    A StreamAnalyzer is completely passive, and attempts no changes on the
    protocol adapter.
    """

    def __init__(self, conn):
        self.conn = conn
        self.info = {}

    def set(self, key, value, confidence = 100):
        """
        Defines the given value with the given confidence, unless the same
        value is already defined with a higher confidence level.
        """
        if value is None:
            return
        if self.info.has_key(key):
            old_confidence, old_value = self.info.get(key)
            if old_confidence > confidence:
                return
        self.info[key] = (confidence, value)

    def set_from_match(self, key, regex_list, string):
        """
        Given a list of tuples (regex, value, confidence), this function
        walks through them and checks whether any of the matches the given
        string.
        If a match is found, and the confidence level is higher
        than the currently defined one, the given value is defined with
        the given confidence.
        """
        for regex, value, confidence in regex_list:
            if regex.search(string):
                self.set(key, value, confidence)

    def get(self, key, confidence = 0):
        """
        Returns the info with the given key, if it has at least the given
        confidence. Returns None otherwise.
        """
        if not self.info.has_key(key):
            return None
        conf, value = self.info.get(key)
        if conf >= confidence:
            return value
        return None

    def data_received(self, data):
        """
        Called by the transport whenever new data was received from the
        connected host.
        """
        pass

    def response_received(self):
        """
        Like data_received(), but is only called when a response is
        complete (in other words, once a prompt has matched).
        """
        pass

    def data_sent(self, data):
        """
        Called by the transport whenever anything was sent to the
        connected host.
        """
        pass