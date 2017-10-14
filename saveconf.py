# save to config file
# save the settings to the config file

import sys, getopt
import optparse
from   pathlib import Path

conf={
    'src':2190,
    'out':1024,
    'fov':200,
    'vnh':1,
    'del':30,
    'mlf':155,
    'slf':250,
    'amt':100,
    'ast':105,
    'msz':2190,
    'ssz':2190
}

def main():
    mleft,sleft,mtop,stop,msize,ssize = parse_arguments()
    
    config='config.txt'
    config_file = Path(config)

    if config_file.is_file():
        f = open('config.txt','wb')
        for line in f:
            if line[0:2]=='src':
                conf['src']=int(line[line.index('=')+1:])
            if line[0:2]=='out':
                conf['out']=int(line[line.index('=')+1:])
            if line[0:2]=='fov':
                conf['fov']=int(line[line.index('=')+1:])
            if line[0:2]=='v/h':
                vnh=line[line.index('=')+1:]
                conf['vnh']=int(vnh=='v')
            if line[0:2]=='del':
                conf['del']=int(line[line.index('=')+1:])
            if line[0:2]=='mlf':
                conf['mlf']=int(line[line.index('=')+1:])
            if line[0:2]=='slf':
                conf['slf']=int(line[line.index('=')+1:])
            if line[0:2]=='amt':
                conf['amt']=int(line[line.index('=')+1:])
            if line[0:2]=='ast':
                conf['ast']=int(line[line.index('=')+1:])
            if line[0:2]=='msz':
                conf['msz']=int(line[line.index('=')+1:])
            if line[0:2]=='ssz':
                conf['ssz']=int(line[line.index('=')+1:])

        f.close()
    
    f= open(config,"w+")

    conf['mlf']=mleft
    conf['slf']=sleft
    conf['amt']=mtop
    conf['ast']=stop
    conf['msz']=msize
    conf['ssz']=ssize
    conf['src']=msize
    conf['out']=1024

    for k, v in conf.items():
        f.write('{0}={1}',k,v)
    
    f.close()

if __name__ == "__main__":
   main()
