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
    [tmp,mleft,sleft,mtop,stop,msize,ssize] = sys.argv    
    print(tmp)
    mleft=int(mleft)
    sleft=int(sleft)
    mtop =int(mtop)
    stop =int(stop)
    msize=int(msize)
    ssize=int(ssize)
    
    config='config.txt'
    config_file = Path(config)

    if config_file.is_file():
        f = open('config.txt','r')
        for line in f:
            if line[0:2] in conf:
                conf[line[0:2]]=int(line[line.index('=')+1:])

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
        value=k+'='+str(v)
        print(value)
        f.write(value+'\n')
    
    f.close()

if __name__ == "__main__":
   main()
