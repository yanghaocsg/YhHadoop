# -*- coding: UTF-8 -*-

import darts
import time

class Singleton(object):
     def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

class PyDarts(object):
    def __init__(self, dict_path):
        list_data = open(dict_path).readlines()
        if not list_data:
            print >>sys.stderr, 'PyDarts %s is null' % dict_path
            raise
        list_data.sort()
        ofh = open('%s.tmp' % dict_path, 'w+').write('\n'.join(list_data))
        self.build_time = darts.build_trie('%s.tmp' % dict_path)

    def get_dict_length(self):
        return darts.get_dict_length()

    def get_build_time(self):
        return darts.get_build_time()

    def get_last_error(self):
        return darts.get_last_error()

    def trans_code(self, query):
        if isinstance(query, unicode):
            query = query.encode("utf-8", 'utf8')
        return query
        
    def common_prefix_search(self, query, num = 10000):
        query = self.trans_code(query)
        res = darts.common_prefix_search(query, num)
        return res

    def exact_match_search(self, query):
        query = self.trans_code(query)
        res = darts.exact_match_search(query)
        return res

if __name__ == "__main__":
    worker = PyDarts("/data/YhHadoop/txt/dict_keyword.txt")
    print "build time: ", worker.get_build_time()
    print "dict length: ", worker.get_dict_length()
    print "last error: ", worker.get_last_error()
    print worker.exact_match_search("中南林科大涉外学院")
    print "\t".join(worker.common_prefix_search("中南林科大涉外学院"))
