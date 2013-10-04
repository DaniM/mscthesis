#-------------------------------------------------------------------------------
# Name:        n-grams
# Purpose:     Just a demo of n-grams and hierarchy n-grams for an MSc thesis.
#              It's just a copy of Ian Millington's book (Artificial Intelligence for games) pseudocode
#
# Author:      Daniel Márquez Quintanilla
#
# Created:     23/09/2013
# Copyright:   (c) Daniel Márquez Quintanilla 2013
# Licence:     GPL v3
#-------------------------------------------------------------------------------

class KeyDataRecord:
    """Just a hash table to store frequencies of values"""
    def __init__(self):
        self.counts = dict()
        self.total = 0

    def prettyPrint(self):
        _elements = []
        for key in self.counts:
            _elements.append(str.format("{0} : {1}", key, self.counts[key]))
        _elements.append(str.format("Total Entries: {0}",self.total))
        print '\r\n'.join([e for e in _elements])

class NGram:
    def registerSequence(self, actionsSequence):
        pass
    def getMostLikely(self, previousActions, num_likely):
        pass

class NGramPredictor(NGram):
    """Basic N-gram created from a window size and a hash function"""

    def __init__(self, windowSize, hash_function):
        '''Note: hash_function must expect an array of actions and return somekind of code'''
        self._windowSize = windowSize
        self.data = dict()
        self._hash = hash_function

    @property
    def windowSize(self):
        return self._windowSize

    def registerSequence(self, actionsSequence):
        """Register a sequence of actions"""
        if self._windowSize == 0:
            value = actionsSequence[0]
        else:
            value = actionsSequence[self._windowSize]
        # use the hash function to generate the key
        key = self._hash(actionsSequence[0:self._windowSize])

        # if this sequence hasn't been registered already, do it
        if not key in self.data:
            self.data[key] = KeyDataRecord()

        keyData = self.data[key]

        # if this value hasn't been registered with this sequence yet
        # initialize with 0
        if not value in keyData.counts:
            keyData.counts[value] = 0

        keyData.counts[value] = keyData.counts[value] + 1
        keyData.total = keyData.total + 1

    def getMostLikely(self, previousActions, num_likely):
        """Get the most num_likey actions that happens more frequently after that sequence"""
        key = self._hash(previousActions)
        if not key in self.data:
            return None
        else:
            sorted_actions = sorted(self.data[key].counts.iterkeys(),key=lambda k : self.data[key].counts[k], reverse=True)
            return sorted_actions[0:num_likely]

    def prettyPrint(self):
        print str.format('{0}-Gram',self._windowSize+1)
        for key in self.data:
            print '-----------------------'
            print key
            self.data[key].prettyPrint()
            print ""

class HierarchicalNGramPredictor (NGram):
    def __init__(self, windowSize, hash_function, threshold):
        self._ngrams = [NGramPredictor(w, hash_function) for w in xrange(0,windowSize+1)]
        self._threshold = threshold
        self._hash = hash_function

    @property
    def windowSize(self):
        return len(self._ngrams) - 1

    def registerSequence(self, actionsSequence):
        #only update the n-grams with a valid window size for that sample
        for i in xrange(len(actionsSequence)):
            self._ngrams[i].registerSequence(actionsSequence[0:self._ngrams[i].windowSize+1])

    def getMostLikely(self, previousActions, num_likely):
        for i in xrange(len(self._ngrams)-1, -1, -1):
            #start from the biggest n-gram and slice the sequence from last to window size
            subsequence = previousActions[len(previousActions) -self._ngrams[i].windowSize : len(previousActions)]
            key = self._hash(subsequence)
            if self._ngrams[i].data[key] and self._ngrams[i].data[key].total >= self._threshold:
                return self._ngrams[i].getMostLikely(subsequence, num_likely)
        return None

    def prettyPrint(self):
        for ngram in self._ngrams:
            ngram.prettyPrint()


# test input for a 3-gram from 345 Ludic Computing, Lecture 12, Adaptative games
# Imperial College, London. Simon Colton & Alison Pease
_3gram_test = 'PKPSSKPPKSPKPKPSPPSSPKKPKPSPPK'
_3gram_hash = lambda actions : ''.join(actions)
def main():
    #3-gram test
    print '***********'
    print '3-gram test'
    print '***********'
    print 'Collecting data...'
    _3gram = NGramPredictor(2,_3gram_hash)
    for i in xrange(2,len(_3gram_test)):
        _3gram.registerSequence(_3gram_test[(i-2):(i+1)])
    print 'Results:'
    _3gram.prettyPrint()
    print _3gram.getMostLikely('PK',1)
    print _3gram.getMostLikely('KP',1)
    print _3gram.getMostLikely('PS',1)

    print '**********************************'
    print 'Hierchical 3-gram, threshold : 6'
    print '**********************************'
    print 'Collecting data...'
    _H3Gram = HierarchicalNGramPredictor(2,_3gram_hash,6)
    for i in xrange(2,len(_3gram_test)):
        _H3Gram.registerSequence(_3gram_test[(i-2):(i+1)])
    #add the last samples
    for i in xrange(_H3Gram.windowSize,0,-1):
        _H3Gram.registerSequence(_3gram_test[len(_3gram_test)-i:len(_3gram_test)])
    print "Results: "
    _H3Gram.prettyPrint()
    print _H3Gram.getMostLikely('PK',1)
    print _H3Gram.getMostLikely('KP',1)
    print _H3Gram.getMostLikely('PS',1)


if __name__ == '__main__':
    main()
