import cPickle as pickle
import sys
x = pickle.load(open("matrixstring.p","rb"))
for i in xrange(len(sys.argv)-1):
    print x.format(sys.argv[i+1])
