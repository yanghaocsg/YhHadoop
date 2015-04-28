# -*- coding: UTF-8 -*-
import sys, re, operator, os, gc
import logging
from unipath import Path
from datrie import Trie
import YhLog
logger = logging.getLogger(__file__)
    
'''
# Chineese
  (unichr(0x4e00), unichr(0x9fa5)),
  # Number
  (chr(0x0030), chr(0x0039)),
  # Alphabet
  (chr(0x0041), chr(0x005a)),
  (chr(0x0061), chr(0x007a))
'''

class YhDatrie(Trie):
    def __init__(self, ranges=[(unichr(0x4e00), unichr(0x9fa5)), (chr(0x0030), chr(0x0039)), (chr(0x0041), chr(0x005a)),(chr(0x0061), chr(0x007a))]):
        super(YhDatrie, self).__init__(ranges=ranges)
  
def test():
    trie = YhDatrie()
    trie[u'foo'] = 5
    trie[u'123'] = 6
    #print trie.__setitem__(u'foo', 5)
    trie[u'中国测试'] = 7
    trie[u'中国1'] = 7
    trie[u'中国a'] = 7
    trie[u'中国'] = 7
    #print trie.__setitem__(u'中国', 5)
    #trie[u'foo']
    logger.error( trie[u'foo'])
    logger.error(trie[u'123'])
    logger.error(trie[u'中国'])
    logger.error('\t'.join([k[0] for k in trie.prefixes(u'中国baaaaaaa')]))
    logger.error('\t'.join([k[0] for k in trie.prefix_items(u'中国aaaaaaaa')]))
    logger.error('\t'.join([k[0] for k in trie.keys(u'中国')]))

def test_file(ifn='./txt/dict_keyword.txt'):
    logger.error('start test_file')
    trie = YhDatrie()
    len_line = 0
    for l in open(ifn):
        l = unicode(l.strip(), 'utf8', 'ignore')
        if not l: continue
        k, _ = re.split('\t', l, 1)
        trie[k] = 1
        len_line += 1
        logger.error('%s\t%s' % (len_line, len(trie)))
    logger.error(trie.len())
    logger.error(trie[u'中国'])
    logger.error('\t'.join([k[0] for k in trie.prefixes(u'中国baaaaaaa')]))
    logger.error('\t'.join([k[0] for k in trie.prefix_items(u'中国aaaaaaaa')]))    
    
if __name__=='__main__':
    #test()
    test_file()