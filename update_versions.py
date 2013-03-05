import sys
import os
import commands
import fnmatch
import re
import subprocess, shlex
import argparse
import shutil
import changelog

def cmdsplit(args):
    if os.sep == '\\':
        args = args.replace('\\', '\\\\')
    return shlex.split(args)

def main(mcversion, modversion):
    name = 'eplus'
    filename = 'version'

    dropbox = 'C:\Users\Stengel\Dropbox\Public\eplus'
    
    lines = []

    try:
        file = open(filename, 'rb')
        for line in file:
            lines.append(line.strip())
        file.close()
    except IOError:
        print 'Skipping reading the file'

    versions = []
    for line in lines:
        versions.append(line.split(':'))
        
    found = False
    for row in versions:
        if row[0] == mcversion:
            if not row[2] == modversion:
                versions[versions.index(row)][2] = modversion
                found = True
            elif row[2] == modversion:
                found = True

    if not found:
        versions.append([mcversion, name, modversion])    

    versions.sort()

    file = open(filename, 'wb')
    for line in versions:
        file.write('%s:%s:%s\n' % (line[0], line[1], line[2]))
    file.close()

    shutil.copy2(filename, dropbox + "/" + filename)

    sys.argv = ['sys.argv[0]']
    changelog.main()

    if not os.path.isdir(dropbox + "/changelog"):
        os.mkdir(dropbox + "/changelog")
    shutil.copy2('./resources/changelog', dropbox + "/changelog/" + modversion)
    
if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])

