# encoding=utf-8
"""
a thread-safe file queue
"""

import os
import fcntl


class FileQueue:
    def __init__(self, filename):
        self.filename = filename
        self.lockfile = filename + ".lock"
        self._create_files()

    def _create_files(self):
        # 创建文件和锁文件
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                pass
        if not os.path.exists(self.lockfile):
            with open(self.lockfile, "w") as f:
                pass

    def enqueue(self, item):
        # 获取锁并写入数据
        # 文件的顺序写应该是线程安全的，这里没有锁应该也可以
        with FileLock(self.lockfile):
            with open(self.filename, "a") as f:
                f.write(item + "\n")

    def dequeue(self):
        # 获取锁并读取数据
        with FileLock(self.lockfile):
            with open(self.filename, "r+") as f:
                line = f.readline()
                if line:
                    # 删除该行数据
                    data = line.strip()
                    rest = f.read()
                    f.seek(0)
                    f.write(rest)
                    f.truncate()
                    return data

        return None


class FileLock:

    def __init__(self, filename):
        self.filename = filename
        self.handle = None

    def acquire(self):
        # 打开文件并获取锁
        self.handle = open(self.filename, "w")
        fcntl.flock(self.handle, fcntl.LOCK_EX)
        return self

    def release(self):
        # 释放锁并关闭文件
        if self.handle:
            fcntl.flock(self.handle, fcntl.LOCK_UN)
            self.handle.close()
            self.handle = None

    def __enter__(self):
        return self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
