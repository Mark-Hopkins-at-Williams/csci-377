VERBOSE = False

if VERBOSE:
    def log(s):
        print(s)
else:
    def log(s):
        pass

def irange(i, j):
    return range(i, j+1)

    
def all_pairs(i, j):
    for a in irange(i, j):
        for b in irange(a+1, j):
            yield (a, b)

def all_pairs_from_seq(seq):
    for a in range(len(seq)):
        for b in range(a+1, len(seq)):
            yield seq[a], seq[b]