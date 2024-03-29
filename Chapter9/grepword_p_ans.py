"""
Многопроцессная программа поиска слова в файлах
данные вводятся из командной строки
"""

import optparse
import os
import subprocess
import sys

#Костыль
sys.argv = ['grepword.py', 'DOM', 'data/forenames.txt', 'data/forenames2.txt', 'data/forenames3.txt', 'data/forenames4.txt']


def main():
    child = os.path.join(os.path.dirname(__file__),
                         "grepword_p_child.py")
    opts, word, args = parse_options()
    filelist = get_files(args, opts.recurse)
    files_per_process = len(filelist) // opts.count
    start, end = 0, files_per_process + (len(filelist) % opts.count)
    number = 1

    pipes = []
    while start < len(filelist):
        command = [sys.executable, child]
        if opts.debug:
            command.append(str(number))
        pipe = subprocess.Popen(command, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE)
        pipes.append((pipe, pipe.stdout))
        pipe.stdin.write(word.encode("utf8") + b"\n")
        for filename in filelist[start:end]:
            pipe.stdin.write(filename.encode("utf8") + b"\n")
        pipe.stdin.close()
        number += 1
        start, end = end, end + files_per_process

    results = []
    while pipes:
        pipe, stdout = pipes.pop()
        results.extend(stdout.readlines())
        pipe.wait()
    for line in sorted(results):
        print(line.decode("utf8").rstrip())


def parse_options():
    parser = optparse.OptionParser(
        usage=("usage: %prog [options] word name1 "
               "[name2 [... nameN]]\n\n"
               "names are filenames or paths; paths only "
               "make sense with the -r option set"))
    parser.add_option("-p", "--processes", dest="count", default=7,
                      type="int",
                      help=("the number of child processes to use (1..20) "
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


main()