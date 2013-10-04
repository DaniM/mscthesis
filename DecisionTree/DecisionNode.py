class DecisionNode:
    def __init__(self, val, children):
        self.setValue(val)
        self.children = children
        # lookup table, maintain the order
        self._children_index_lookup = dict([(child.value, i) for child,i in zip(children, xrange(len(children)))])
    
    def __str__(self):
        return str(self.value)
    
    def setValue(self, val):
        self.value = val
        
    def addChild(self,value,child):
        if self._children_index_lookup.has_key(value):
            self.children[self._children_index_lookup[value]] = child
        else:
            self._children_index_lookup[value] = len(self.children)
            self.children.append(child)
        return self
    
    def getChildByValue(self,value):
        return self.children[self._children_index_lookup[value]]
    
    def getChildByIndex(self,index):
        return self.children[index]
    
    def getChildrenValues(self):
        return sorted(self._children_index_lookup.keys(),key=lambda k:self._children_index_lookup[k])
    
    def numChildren(self):
        return len(self.children)
    
    def accept(self,visitor):
        visitor.visit(self)
        visitor.endVisit(self)
        

class Visitor:
    def visit(self,node):
        pass
    
    def endVisit(self,node):
        pass

class PrintTreeVisitor(Visitor):
    
    def __init__(self):
        self._indentation = []
        self._values_queues = []
    
    def visit(self,node):
        # if it's a composite node
        value=''
        if(len(self._values_queues) > 0):
            value = self._values_queues.pop()
        #print the decision node value
        print ''.join(self._indentation),value,' ',node
        if node.numChildren() > 0:
            # add indentation
            self._indentation.append('\t')
            
            #append all the children values
            children_names = node.getChildrenValues()
            for i in range(node.numChildren()):
                self._values_queues.append(children_names[i])
                node.getChildByIndex(i).accept(self)  
            
    def endVisit(self,node):
        # if it's a composite node
        if node.numChildren() > 0:
            # remove the indentation
            self._indentation.pop()
    