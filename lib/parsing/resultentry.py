# -*- coding: utf-8 -*-
from __future__ import absolute_import


class InvalidEntryError(Exception):
    """
    This is an exception for denoting that an entry is invalid.
    """


class CCResultEntry(object):
    """
    This class wraps the contents of a single entry found within a lavalamp Common Crawl analysis file.
    """

    # Class Members

    RECORD_ENTRY = "00"
    SERVER_NAME_ENTRY = "01"
    SERVER_PATH_ENTRY = "02"
    RECORD_SEPARATOR = "_';)_"

    # Instantiation

    def __init__(self, entry_contents):
        self._entry_contents = entry_contents
        self._entry_type = None
        self._server_type = None
        self._url_path = None
        self._count = None
        self.__validate_entry_contents()
        self.__parse_entry_contents()

    # Static Methods

    # Class Methods

    # Public Methods

    # Protected Methods

    # Private Methods

    def __parse_entry_contents(self):
        """
        Parse the contents of self.entry_contents to populate fields within this object.
        :return: None
        """
        contents_split = self.entry_contents.split("\t")
        record_content = contents_split[0]
        count = contents_split[-1]
        self._count = int(count)
        record_content = record_content[2:]
        self._entry_type = record_content[:2]
        record_content = record_content[2 + len(self.RECORD_SEPARATOR):]
        if self.is_server_name:
            self._server_type = record_content[:-2]
        elif self.is_server_path:
            self._server_type = record_content[:record_content.find(self.RECORD_SEPARATOR)]
            record_content = record_content[record_content.find(self.RECORD_SEPARATOR) + len(self.RECORD_SEPARATOR): -2]
            self._url_path = record_content

    def __validate_entry_contents(self):
        """
        Validate that the contents of self.entry_contents represent a valid entry.
        :return: None
        """
        if not self.entry_contents.startswith("< "):
            raise InvalidEntryError("Entry did not start with '< ': %s" % self.entry_contents)

    # Properties

    @property
    def count(self):
        """
        Get the number associated with this entry.
        :return: the number associated with this entry.
        """
        return self._count

    @property
    def entry_contents(self):
        """
        Get the contents of the entry that this instance wraps.
        :return: the contents of the entry that this instance wraps.
        """
        return self._entry_contents

    @property
    def entry_type(self):
        """
        Get the type of entry that self.entry_contents represents.
        :return: the type of entry that self.entry_contents represents.
        """
        return self._entry_type

    @property
    def is_record_processed_type(self):
        """
        Get whether or not this record is a records process count.
        :return: whether or not this record is a records process count.
        """
        return self.entry_type == self.RECORD_ENTRY

    @property
    def is_server_name(self):
        """
        Get whether or not this record is a server name record.
        :return: whether or not this record is a server name record.
        """
        return self.entry_type == self.SERVER_NAME_ENTRY

    @property
    def is_server_path(self):
        """
        Get whether or not this record is a server path record.
        :return: whether or not this record is a server path record.
        """
        return self.entry_type == self.SERVER_PATH_ENTRY

    @property
    def server_type(self):
        """
        Get the type of server that this record represents.
        :return: the type of server that this record represents.
        """
        return self._server_type

    @property
    def url_path(self):
        """
        Get the URL path segment that this entry contains.
        :return: the URL path segment that this entry contains.
        """
        return self._url_path

    # Representation and Comparison

    def __repr__(self):
        if self.is_server_name:
            return "<%s - %s (%s, %s)>" % (
                self.__class__.__name__,
                self.entry_type,
                self.server_type,
                self.count,
            )
        elif self.is_server_path:
            return "<%s - %s (%s, %s, %s)>" % (
                self.__class__.__name__,
                self.entry_type,
                self.server_type,
                self.url_path,
                self.count,
            )

