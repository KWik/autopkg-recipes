#!/usr/local/autopkg/python

import sys

def main(args) -> int:
    with open('foo.txt', 'w') as f:
        f.write(' '.join(args) + '\n')
    
if __name__ == '__main__':
    exit(main(sys.argv))
    
