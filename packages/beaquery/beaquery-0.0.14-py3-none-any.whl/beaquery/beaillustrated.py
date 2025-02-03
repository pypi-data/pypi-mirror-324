#! env python
#

import argparse
import os
import sys
import webbrowser

try:
    from beaquery import beaqueryq
except Exception as e:
    import beaqueryq

def main():
    argp = argparse.ArgumentParser(description='get BEA NIPA data')

    argp.add_argument('--format', default='json',
        help='requested BEA result format')

    argp.add_argument('--directory', default='/tmp',
        help='where to store the generated html')

    args=argp.parse_args()

    BN = beaqueryq.BEAQueryQ()

    hd = BN.hierarchy(args.format)
    htm = BN.hierarchyhtml(hd)
    BN.showhtml('%s/hierarchy.html' % args.directory, htm)

if __name__ == '__main__':
    main()
