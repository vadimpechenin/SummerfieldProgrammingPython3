"""
Многопоточная программа поиска слова в файлах
модуль multiprocessing
"""

import multiprocessing
import optparse
import os
import sys

# The maximum length of the word to be search for is BLOCK_SIZE
BLOCK_SIZE = 8000
#Костыль
sys.argv = ['grepword.py', 'DOM', 'data/forenames.txt', 'data/forenames2.txt', 'data/forenames3.txt', 'data/forenames4.txt']

class Worker(multiprocessing.Process):

    def __init__(self, work_queue, word, number):
        super().__init__()
        self.work_queue = work_queue
        self.word = word
        self.number = number

    def run(self):
        while True:
            try:
                filename = self.work_queue.get()
                self.process(filename)
            finally:
                self.work_queue.task_done()

    def process(self, filename):
        previous = ""
        try:
            with open(filename, "rb") as fh:
                while True:
                    current = fh.read(BLOCK_SIZE)
                    if not current:
                        break
                    current = current.decode("utf8", "ignore")
                    if (self.word in current or
                            self.word in previous[-len(self.word):] +
                            current[:len(self.word)]):
                        print("{0}{1}".format(self.number, filename))
                        break
                    if len(current) != BLOCK_SIZE:
                        break
                    previous = current
        except EnvironmentError as err:
            print("{0}{1}".format(self.number, err))


def parse_options():
    parser = optparse.OptionParser(
        usage=("usage: %prog [options] word name1 "
               "[name2 [... nameN]]\n\n"
               "names are filenames or paths; paths only "
               "make sense with the -r option set"))
    parser.add_option("-p", "--processes", dest="count", default=7,
                      type="int",
                      help=("the number of processes to use (1..20) "
                            "[default %default]"))
    parser.add_option("-r", "--recurse", dest="recurse",
                      default=False, action="store_true",
                      help="recurse into subdirectories")
    parser.add_option("-d", "--debug", dest="debug", default=False,
                      action="store_true")
    opts, args = parser.parse_args()
    if len(args) == 0:
        parser.error("a word and at least one path must be specified")
    elif len(args) == 1:
        parser.error("at least one path must be specified")
    if (not opts.recurse and
            not any([os.path.isfile(arg) for arg in args])):
        parser.error("at least one file must be specified; or use -r")
    if not (1 <= opts.count <= 20):
        parser.error("process count must be 1..20")
    return opts, args[0], args[1:]


def get_files(args, recurse):
    filelist = []
    for path in args:
        if os.path.isfile(path):
            filelist.append(path)
        elif recurse:
            for root, dirs, files in os.walk(path):
                for filename in files:
                    filelist.append(os.path.join(root, filename))
    return filelist


def main():
    opts, word, args = parse_options()
    filelist = get_files(args, opts.recurse)
    work_queue = multiprocessing.JoinableQueue()
    for i in range(opts.count):
        number = "{0}: ".format(i + 1) if opts.debug else ""
        worker = Worker(work_queue, word, number)
        worker.daemon = True
        worker.start()
    for filename in filelist:
        work_queue.put(filename)
    work_queue.join()


if __name__ == "__main__":  # This is *vital* on Windows!
    main()