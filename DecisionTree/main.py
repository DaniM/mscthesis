import DecisionTree
from Data import createDatabase
import DecisionNode

### NOTE: training examples are taken from Ian Millington's and John Funge's book "Artificial Intelligence for Games"

def main():
    #Insert input file
    file = open('example_training.csv')
    target = "action"
    data = [[]]
    for line in file:
        line = line.strip("\r\n")
        data.append(line.split(','))
    data.remove([])
    attributes = data[0]
    data.remove(attributes)
    db = createDatabase(attributes,data)
    #Run ID3
    # Note: we can remove the target attribute from the attributes list
    tree = DecisionTree.makeTree(db, attributes, target, 0)
    print "generated tree"
    tree.accept(DecisionNode.PrintTreeVisitor())
    print 'adding new examples'
    example1 = ['hurt','exposed','with_ammo','defend']
    print example1
    tree = DecisionTree.updateTree(tree, db, example1, attributes, target)
    tree.accept(DecisionNode.PrintTreeVisitor())
    example2 = ['healthy','exposed','with_ammo','run']
    print example2
    tree = DecisionTree.updateTree(tree, db, example2, attributes, target)
    tree.accept(DecisionNode.PrintTreeVisitor())
    
if __name__ == '__main__':
    main()