#!/usr/bin/env python

"""
This script pulls the font awesome spec from a downloaded copy of their repo on github,
then generates a python mapping of the icons names to their unicode value.

"""

import yaml
import sys

INDENT = ' ' * 2
IDICT = {}

def main(yfile):
    out = sys.stdout
    global IDICT

    with open(yfile,'r') as f:
      try:
        icons_list = yaml.load(f)['icons']
        #out.write('faicons = {\n')
        curwide = 0
        styles = ''
        count = 0
        ztotal = 0
        zmaxlen = 0
        unused = 0
        overwrites = 0
        for icon in icons_list:
            # dict entry with character code
            id = icon['id']
            code = icon['unicode']
            name = icon['name']
            
            try:
              prev = IDICT[code]
              overwrites += 1
            except:
              IDICT[code] = id #simple code to id mapping for later interspersed output
            
            nlen = len(name)
            if nlen > zmaxlen:
              zmaxlen = nlen
            
            entry = '.fa-%s:before {content: "\\%s";}' % (id, code)
            if curwide:
              curwide = 0
              entry += '\n'
            else:
              curwide = 1
              entry += '\t' #or a space if you prefer
              
            styles += entry
            ztotal += 1
        out.write(styles)
        out.write('\n<!-- %d icons found. Max FA name length was %d. Body follows -->\n' % (ztotal, zmaxlen))
        
        unused = 0
        
        for x in range(0xf000, 0xf300): #get min/max in loop above, TBD
          code = '%04x' % x
          try:
            id = IDICT[code]
          except:
            id = 'unused'
            unused += 1
          #hentry = '<ruby><i class="fa fa-fw fa-%s"></i> <rt>%s</rt></ruby>\n' % (id, code)
          hentry = '<ruby><a title="%s" href="#"><i class="fa fa-fw fa-%s"></i> </a><rt>%s</rt></ruby>\n' % (id, id, code)
          count += 1
          if count >= 32:
            count = 0
            hentry += '<br>'
          out.write(hentry)
          
        out.write('\n<!-- %d unused icons found, %d overwrites -->\n' % (unused, overwrites))
       
         

   #     out.write('}\n')
      except yaml.YAMLError as exc:
        print(exc)
      


if __name__ == '__main__':
    main('icons.yml')
