#!/usr/bin/env python
import logging

from errno import ENOENT
from stat import S_IFDIR, S_IFLNK, S_IFREG
from time import time

from fuse import FUSE, FuseOSError, Operations, LoggingMixIn

file_count = 0


class Node(object):
    def __init__(self, mode, nlink=1):
        global file_count

        now = time()
        file_count += 1
        self.file_handle = file_count
        self.attributes = dict(
            st_mode=mode,
            st_nlink=nlink,
            st_size=0,
            st_ctime=now,
            st_mtime=now,
            st_atime=now,
        )

    def __setitem__(self, key, value):
        self.attributes[key] = value

    def __getitem__(self, key):
        return self.attributes[key]


class NullFS(LoggingMixIn, Operations):
    'Null filesystem.'

    def __init__(self):
        self.files = {}
        self.files['/'] = Node(S_IFDIR | 0o755, 2)

    def chmod(self, path, mode):
        self.files[path]['st_mode'] &= 0o770000
        self.files[path]['st_mode'] |= mode
        return 0

    def chown(self, path, uid, gid):
        self.files[path]['st_uid'] = uid
        self.files[path]['st_gid'] = gid

    def create(self, path, mode):
        self.files[path] = Node(S_IFREG | mode)
        return self.files[path].file_handle

    def getattr(self, path, fh=None):
        if path not in self.files:
            raise FuseOSError(ENOENT)

        return self.files[path].attributes

    def mkdir(self, path, mode):
        self.files[path] = Node(S_IFDIR | mode, 2)
        self.files['/']['st_nlink'] += 1  # TODO use parent path

    def open(self, path, flags):
        return self.files[path].file_handle

    def read(self, path, size, offset, fh):
        return []

    def readdir(self, path, fh):
        return ['.', '..'] + [x[1:] for x in self.files if x != '/']

    def readlink(self, path):
        return []

    def rename(self, old, new):
        self.files[new] = self.files.pop(old)

    def rmdir(self, path):
        self.files.pop(path)
        self.files['/']['st_nlink'] -= 1  # TODO use parent path

    def statfs(self, path):
        return dict(f_bsize=512, f_blocks=4096, f_bavail=2048)

    def symlink(self, target, source):
        self.files[target] = Node(S_IFLNK | 0o777)

    def truncate(self, path, length, fh=None):
        pass

    def unlink(self, path):
        self.files.pop(path)

    def utimens(self, path, times=None):
        now = time()
        atime, mtime = times if times else (now, now)
        self.files[path]['st_atime'] = atime
        self.files[path]['st_mtime'] = mtime

    def write(self, path, data, offset, fh):
        return len(data)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('mount')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)
    fuse = FUSE(NullFS(), args.mount, foreground=True, allow_other=True)
