import cPickle as pickle

x = pickle.load(open( "matrixstring.p", "rb" ) )
print x.format("SUPERUSER")
