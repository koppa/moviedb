# -*- coding: utf-8 -*-

import fuse
import errno
import stat
import os

from time import time

import logging

LOG_FILENAME = '/tmp/fuse.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)


def zstat(mode, size):
    """

    :param mode: S_IFDIR
    :return:
    """
    now = time()
    return dict(st_mode=(mode | 0o755), st_ctime=now,
                st_mtime=now, st_atime=now, st_nlink=2, st_size=size)

    # stat.st_mode = 0
    # stat.st_ino = 0
    # stat.st_dev = 0
    # stat.st_nlink = 1
    # stat.st_uid = os.getuid()
    # stat.st_gid = os.getgid()
    # stat.st_size = 0
    # stat.st_atime = time.time()
    # stat.st_mtime = time.time()
    # stat.st_ctime = time.time()
    # return stat


# class Filesystem(fuse.LoggingMixIn, fuse.Operations):
#     def __init__(self, db):
#         self.data = movies.flatten()
#
#     def getattr(self, path, fh=None):
#         logging.warning("getattr %s" % path)
#
#         splitted = path.split('/')
#
#         st = zstat(fuse.Stat())
#
#         # / Root Directory
#         if path == "/":
#             st.st_mode = 0o555 | stat.S_IFDIR
#             st.st_size = len(self.data)
#             return st
#
#         if len(splitted) == 2:
#             if splitted[1] in self.data:
#                 st.st_mode = 0o555 | stat.S_IFDIR
#                 st.st_size = len(self.data[splitted[1]])
#                 return st
#
#         if len(splitted) == 3:
#             st.st_mode = 0o555 | stat.S_IFDIR
#             st.st_size = 0
#             return st
#
#         if len(splitted) == 4:
#             st.st_mode = 0o644 | stat.S_IFLNK
#             st.st_size = 0
#             return st
#
#         logging.error("getattr entry not found: %s" % path)
#         return fuse.FuseOSError(errno.ENOENT)
#
#     def readdir(self, path, offset):
#         logging.warning("readdir %s" % path)
#         if path == '/':
#             for c in list(self.data.keys()):
#                 yield fuse.Direntry(c)
#         else:
#             splitted = path.split('/')
#             if len(splitted) == 2:
#                 logging.warning('reading %s' % splitted[1])
#                 logging.warning('content %s' % self.data[splitted[1]])
#                 for i in ['.', '..'] + list(self.data[splitted[1]].keys()):
#                     logging.warning('yield %s' % i)
#                     yield fuse.Direntry(i)
#
#             if len(splitted) == 3:
#                 logging.warning('reading %s' % splitted[2])
#                 for i in ['.', '..'] + \
#                         list(self.data[splitted[1]][splitted[2]].keys()):
#                     yield fuse.Direntry(i)
#
#     def readlink(self, path):
#         logging.warning("readlink path %s", path)
#         splitted = path.split('/')
#         return self.data[splitted[1]][splitted[2]][splitted[3]]


def parsepath(path):
    return [e for e in path.split('/') if len(e) > 0]


class Filesystem(fuse.LoggingMixIn, fuse.Operations):
    'Example memory filesystem. Supports only one level of files.'
    fd = 0

    def __init__(self, structure):
        self.structure = structure

    def getattr(self, path, fh=None):
        curr = self.structure
        try:
            for el in parsepath(path):
                curr = curr[el]
        except KeyError:
            # not found
            raise fuse.FuseOSError(errno.ENOENT)

        return zstat(fuse.S_IFDIR, len(curr))

    def open(self, path, flags):
        self.fd += 1
        return self.fd

    def read(self, path, size, offset, fh):
        raise NotImplementedError()
        # return self.data[path][offset:offset + size]

    def readdir(self, path, fh):
        curr = self.structure
        for el in parsepath(path):
            curr = curr[el]
        subdirs = list(curr.keys())
        return ['.', '..'] + subdirs

    def readlink(self, path):
        raise NotImplementedError()
        # return self.data[path]

    def statfs(self, path):
        return dict(f_bsize=512, f_blocks=4096, f_bavail=2048)
