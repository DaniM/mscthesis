class ExamplesDatabase:

    def __init__(self, attributes, examples):
        self.attributes = attributes
        self._id = 0
        self.examples = dict([(self._id,e) for e,self._id in zip(examples, xrange(len(examples)))])
        
    def addExample(self, example):
        self._id += 1
        exampleTuple = (self._id, example)
        self.examples[exampleTuple[0]] = exampleTuple[1]
        return exampleTuple
            
    def removeExample(self, exampleTuple):
        del self.examples[exampleTuple[0]]
            
def createDatabase(attributes, examples):
    db = ExamplesDatabase(attributes,examples)
    return db

def split(db, attribute,val):
    index = db.attributes.index(attribute)
    newDB = ExamplesDatabase(db.attributes,[])
    newDB.examples = dict(filter(lambda x : x[1][index] == val, db.examples.items()))
    newDB._id = db._id
    return newDB