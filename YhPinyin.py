# -*- coding: UTF-8 -*-
import sys, random,pprint, re, operator
import httplib, urllib, urllib2, subprocess, urlparse
import logging.config, logging, logging.handlers

from unipath import Path

#self module
import YhLog, YhTool, YhChineseNorm
logger = logging.getLogger(__file__)


class YhPinyin:
    def __init__(self):
        self.cwd = Path(__file__).absolute().ancestor(1)
        self.dict_pinyin = {}
        self.load_pingyin()
        
        
    def load_pingyin(self, ifn='./txt/chinese2Pingyin.txt'):
        self.dict_pinyin.clear()
        for line in open(Path(self.cwd, ifn)):
            line = unicode(line.strip(), 'utf-8', 'ignore')
            pars = line.split('\t')
            if(len(pars) < 2):
                continue
            self.dict_pinyin[pars[0]] = pars[1:]
        logger.error('dict_pinyin len [%s]' % len(self.dict_pinyin))
    
    def line2py_list(self, line=u'一石二鸟'):
        list_py = []
        for k in line:
            if k in self.dict_pinyin:
                list_py.append(self.dict_pinyin[k][0])
            else:
                list_py.append(k)
        #logger.error('%s\t%s' % (line, ','.join(list_py)))
        return list_py
            
    def line2py(self, line=u'一石二鸟'):
        set_py = set()
        #more than 10, not translate
        if len(line)>10:
            return set_py
        for  w  in line:
            set_tmp = set()
            if w in self.dict_pinyin:
                for wpinyin in self.dict_pinyin[w]:
                    #logger.error('w wpinyin %s\t%s' % (w, wpinyin))
                    if not set_py:
                        set_tmp.add(wpinyin)
                    else:
                        for p in set_py:
                            set_tmp.add(p+wpinyin)
            else :
                if not set_py:
                    set_tmp.add(w)
                else:
                    for p in set_py:
                        set_tmp.add(p+w)
            set_py = set(set_tmp)
            #logger.error('%s\t%s' % (w, '|'.join(set_py)))
        if line in set_py:
            set_py.remove(line)
        if line in ['abc']:
            logger.error('%s\t%s' % (line, '|'.join(set_py)))
        logger.error('line2py_list %s\t%s' % (line, '|'.join(set_py)))
        return set_py
    
    def line2py_fuzzy(self, line=u'胃痛'):
        set_py = set()
        #more than 10, not translate
        if len(line)>10:
            return set_py
        for  w  in line:
            set_tmp = set()
            if w in self.dict_pinyin:
                for wpinyin in self.dict_pinyin[w]:
                    set_wpinyin = set([wpinyin])
                    if wpinyin[0] in ['l', 'n']:
                        set_wpinyin.add('l'+wpinyin[1:])
                        set_wpinyin.add('n'+wpinyin[1:])
                    if wpinyin[-2:] in ['an', 'on', 'in']:
                        set_wpinyin.add(wpinyin+'g')
                    if wpinyin[-3:] in ['ang', 'ing', 'ong']:
                        set_wpinyin.add(wpinyin[:-1])
                        #logger.error('|'.join(set_wpinyin))
                    #logger.error('w wpinyin %s\t%s\t%s' % (w, wpinyin, '|'.join(set_wpinyin)))
                    for sub_wpinyin in set_wpinyin:
                        if not set_py:
                            set_tmp.add(sub_wpinyin)
                        else:
                            for p in set_py:
                                set_tmp.add(p+sub_wpinyin)
                        
                    
            else :
                if not set_py:
                    set_tmp.add(w)
                else:
                    for p in set_py:
                        set_tmp.add(p+w)
            set_py = set(set_tmp)
            #logger.error('%s\t%s' % (w, '|'.join(set_py)))
        if line in set_py:
            set_py.remove(line)
        if line in ['abc']:
            logger.error('%s\t%s' % (line, '|'.join(set_py)))
        #logger.error('line2py_fuzzy %s\t%s' % (line, '|'.join(set_py)))
        return set_py
    
    
    def file2py(self, ifn='./txt/dict_white_singer.txt', ofn='./txt/dict_white_singer_py.txt'):
        ofh = open(ofn, 'w+')
        for line in open(ifn):
            line = unicode(line.strip(), 'utf-8', 'ignore')
            pair = line.split('\t')
            singer_name = pair[0].strip()
            set_py = self.line2py(singer_name)
            if set_py:
                ofh.write(('%s\t%s\n' % (singer_name, '|'.join(set_py))).encode('utf-8','ignore'))
        ofh.close()
        
yhpinyin = YhPinyin()
        
def test_Chinese2Pingying():
    logger.error(yhpinyin.line2py(u'心藏病'))
    logger.error(yhpinyin.line2py_list(u'心藏病'))
    logger.error(yhpinyin.line2py_fuzzy(u'胃痛'))
    logger.error(yhpinyin.line2py_fuzzy(u'味疼'))
    #yhpinyin.file2py('./txt/dict_keyword.txt', './txt/dict_keyword_py.txt')
    logger.error(yhpinyin.line2py_list())
    
if __name__=='__main__':
    test_Chinese2Pingying()
