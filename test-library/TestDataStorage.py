#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------
# Copyright (c) 2010-2018 Denis Machard
# This file is part of the extensive testing project
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA
# -------------------------------------------------------------------

import pickle
import sys
import os

STORAGE_MODE_FILE = "FILE"
STORAGE_MODE_MEM = "MEM"

class TestDataStorage:
    """
    Test data storage
    """
    def __init__ (self, path, storageMode=STORAGE_MODE_MEM):
        """
        Constructor for the test data storage

        @param path:
        @type path:
        """
        self.__filename = 'storage.dat'
        self.__path = path
        self.__storageMode = storageMode
        self.__storageData = {}

    def save_data(self, data):
        """
        Save data on the storage

        @param data:
        @type data:
        """
        validData = False
        if isinstance(data, str):
            validData = True
        if isinstance(data, list):
            validData = True
        if isinstance(data, dict):
            validData = True
        if isinstance(data, tuple):
            validData = True

        if self.__storageMode == STORAGE_MODE_MEM:
            if validData:
                self.__storageData = data

        storagePath = '%s/%s' % (self.__path, self.__filename)
        try:
            if validData:
                fd = open(storagePath, 'wb')
                fd.write( pickle.dumps(data) )
                fd.close()
        except Exception as e:
            self.error( "[save_data] %s" % str(e) )

    def load_data(self):
        """
        Load data from the storage

        @param data:
        @type data:
        """
        if self.__storageMode == STORAGE_MODE_MEM:
            return self.__storageData

        storagePath = '%s/%s' % (self.__path, self.__filename)
        # check if the storage.dat file exists ?
        if not os.path.exists(storagePath):
            return {}
            
        # read the file and unpickle the content
        try:
            fd = open( storagePath, "r")
            data = fd.read()
            fd.close()
            return pickle.loads( data )
        except Exception as e:
            self.error( "[load_data] %s" % str(e) )
            return None
            
    def reset_data(self):
        """
        Reset data from the storage
        """
        if self.__storageMode == STORAGE_MODE_MEM:
            del self.__storageData
            self.__storageData = {}
            return True


        storagePath = '%s/%s' % (self.__path, self.__filename)
        # check if the file exists?
        if not os.path.exists(storagePath):
            return {}
            
        # Empty the file storage.dat
        try:
            fd = open(storagePath , "wb")
            fd.write( "" )
            fd.close()
            return True
        except Exception as e:
            self.error( "[reset_data] %s" % str(e) )
            return False
            
    def error (self, err):
        """
        Log error

        @param err:
        @type err:
        """
        sys.stderr.write( "[%s] %s\n" % ( self.__class__.__name__,err) )


TDS = None

def instance():
    """
    @return:
    @rtype:
    """
    if TDS:
        return TDS

def initialize( path):
    """
    @param path:
    @type path:

    """
    global TDS
    TDS = TestDataStorage(path = path)

def finalize():
    """
    """
    global TDS
    if TDS:
        TDS = None
