'''
Based on this tutorial http://onlamp.com/pub/a/python/2006/02/09/ai_decision_trees.html?page=1
'''
import math
import DecisionNode
import Data
from Data import split
#find most common value for an attribute
def majority(attributes, data, target):
    #find target attribute
    valFreq = {}
    #find target in data
    index = data.attributes.index(target)
    #calculate frequency of values in target attr
    for tuple in data.examples.values():
        if (valFreq.has_key(tuple[index])):
            valFreq[tuple[index]] += 1
        else:
            valFreq[tuple[index]] = 1
    major = sorted(valFreq.iterkeys(), key=lambda x : valFreq[x], reverse=True)[0]
    return (major,valFreq[major])

#Calculates the entropy of the given data set for the target attr
def entropy(attributes, data, targetAttr):

    valFreq = {}
    dataEntropy = 0.0

    #find index of the target attribute
    i = data.attributes.index(targetAttr)

    # Calculate the frequency of each of the values in the target attr
    for entry in data.examples.values():
        if (valFreq.has_key(entry[i])):
            valFreq[entry[i]] += 1.0
        else:
            valFreq[entry[i]]  = 1.0

    # Calculate the entropy of the data for the target attr
    for freq in valFreq.values():
        dataEntropy += (-freq/len(data.examples)) * math.log(freq/len(data.examples), 2)

    return dataEntropy

def gain(attributes, data, attr, targetAttr):
    """
    Calculates the information gain (reduction in entropy) that would
    result by splitting the data on the chosen attribute (attr).
    """
    valFreq = {}
    subsetEntropy = 0.0

    #find index of the attribute
    i = data.attributes.index(attr)

    # Calculate the frequency of each of the values in the target attribute
    for entry in data.examples.values():
        if (valFreq.has_key(entry[i])):
            valFreq[entry[i]] += 1.0
        else:
            valFreq[entry[i]]  = 1.0
    # Calculate the sum of the entropy for each subset of records weighted
    # by their probability of occuring in the training set.
    total =  sum(valFreq.values())
    for val in valFreq.keys():
        valProb        = valFreq[val] / total
        dataSubset     = split(data,attr,val)
        subsetEntropy += valProb * entropy(attributes, dataSubset, targetAttr)

    # Subtract the entropy of the chosen attribute from the entropy of the
    # whole data set with respect to the target attribute (and return it)
    return (entropy(attributes, data, targetAttr) - subsetEntropy)

#choose best attibute
def chooseAttr(data, attributes, target):
    best = attributes[0]
    maxGain = -1;
    #target can't be chosen
    for attr in attributes:
        if attr != target:
            newGain = gain(attributes, data, attr, target)
            if newGain>maxGain:
                maxGain = newGain
                best = attr
    return best

#get values in the column of the given attribute
def getValues(data, attributes, attr):
    index = data.attributes.index(attr)
    values = set()
    for entry in data.examples.values():
        values.add(entry[index])
    return values

def getExamples(data, attributes, best, val):
    index = attributes.index(best)
    examples = filter(lambda x: x[index]==val,data)
    return examples

def makeTree(data, attributes, target, recursion):
    recursion += 1

    vals = [record[data.attributes.index(target)] for record in data.examples.values()]
    default = majority(attributes, data, target)

    # If the attributes list is empty, return the
    # default value. When checking the attributes list for emptiness, we
    # need to subtract 1 to account for the target attribute.
    if len(attributes)-1 == 0:
        return DecisionNode.DecisionNode(default[0],[])
    # If all the records in the dataset have the same classification,
    # return that classification.
    elif default[1] == len(vals):
        return DecisionNode.DecisionNode(default[0],[])
    else:
        # Choose the next best attribute to best classify our data
        best = chooseAttr(data, attributes, target)
        # Create a new decision tree/node with the best attribute and an empty
        # dictionary object--we'll fill that up next.
        tree = DecisionNode.DecisionNode(best,[])

        newAttrs = data.attributes[:]
        newAttrs.remove(best)

        # Create a new decision tree/sub-node for each of the values in the
        # best attribute field
        for val in getValues(data, attributes, best):
            # Create a subtree for the current value under the "best" field
            newData = split(data, best, val)
            
            # If the dataset is empty
            if len(newData.examples) == 0:
                 return DecisionNode.DecisionNode(default[0],[])
            
            subtree = makeTree(newData, newAttrs, target, recursion)

            # Add the new subtree to the empty dictionary object in our new
            # tree/node we just created.
            tree.addChild(val,subtree)

    return tree

def updateTree(tree, data, newExample, attributes, target):
    #add the new example, but keep the tuple
    example = data.addExample(newExample)
    indexAtt = data.attributes.index(target)
    # it is a leaf node?
    if tree.numChildren() == 0:
        if tree.value == newExample[indexAtt]:
            return tree
        else:
            tree = makeTree(data, attributes, target, 0)
            return tree
    else:
        # Choose the next best attribute to best classify our data
        best = chooseAttr(data, attributes, target)
        if best == tree.value:
            indexAtt = data.attributes.index(best)
            value = newExample[indexAtt]
            newData = split(data, best, value)
            #remove the example from the new data
            newData.removeExample(example)
            newAttrs = data.attributes[:]
            newAttrs.remove(best)
            # the root is still the same, update the corresponding child
            tree.addChild(value, updateTree(tree.getChildByValue(value), newData, newExample, newAttrs, target))
            return tree
        else:
            tree = makeTree(data, attributes, target, 0)
            return tree