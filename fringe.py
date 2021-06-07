
import queue
import sys


class Fringe(object):
    """Wrapper for queue lib from python to keep track of some statistics. Written by Davide Grossi."""

    # DO NOT CHANGE MAXFRINGESIZE
    __MAX_FRINGE_SIZE = 500000
    __fringe = None
    __insertions = 0
    __deletions = 0
    __max_size = 0

    def __init__(self, q_type):
        self.__type = q_type
        super(Fringe, self).__init__()
        self.__fringe = self.create_fringe(self.__type)

    def create_fringe(self, q_type):
        if q_type == "STACK":
            return queue.LifoQueue(self.__MAX_FRINGE_SIZE)
        elif q_type == "FIFO":
            return queue.Queue(self.__MAX_FRINGE_SIZE)

    def push(self, item):
        """Push item in fringe."""
        # if fringe is full, print error and exit
        if self.__fringe.full():
            # item.getRoom().maze.printMazeWithPath(item)
            print(f"Error: trying to apply push on an fringe that already contains "
                  f"MAX(={str(self.__MAX_FRINGE_SIZE)}) elements")
            self.print_stats()
            sys.exit(1)
        self.__fringe.put(item, block=False)
        if self.__fringe.qsize() > self.__max_size:
            self.__max_size = self.__fringe.qsize()
        self.__insertions += 1

    def pop(self):
        """Return item from fringe. Return None object if fringe is empty"""
        if self.__fringe.empty():
            return None
        self.__deletions += 1
        return self.__fringe.get()

    def is_empty(self):
        """Return bool for fringe is empty"""
        return self.__fringe.empty()

    def get_insertions(self):
        """Return the number of insertions"""
        return self.__insertions

    def get_deletions(self):
        """Return the number of deletions"""
        return self.__deletions

    def print_stats(self):
        print("#### fringe statistics:")
        print("size: {0:>15d}".format(self.__fringe.qsize()))
        print("maximum size: {0:>7d}".format(self.__max_size))
        print("insertions: {0:>9d}".format(self.get_insertions()))
        print("deletions: {0:>10d}".format(self.get_deletions()))
