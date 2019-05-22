import timeit

class node():
    
    def __init__(self):
        self.child = []
        self.value = ""
        self.support =0
        self.children = {}
        
    def __str__(self):
        return str(print("The value is : " + str(self.value) + "\nChild nodes are : " + str(self.child) + "\nSupport :" + str(self.support) + "\n\n"))

class FP_Tree():
    
    def __init__(self):
        self.root = node()
        self.new_patterns = {}
        self.pattern_support = {}
    
    def build(self,database):
        
        for index,trans in enumerate(database):
            print("trans is :"+str(trans))
            curr = self.root
            for item in trans:
                
                if item in curr.child:
                    curr = curr.children[item]
                    curr.support+=1
                else:
                    curr.child.append(item)
                    curr.children[item] = node()
                    curr = curr.children[item]
                    curr.value = item
                    curr.support+=1
                    
    
    def dfs(self,curr):
        print(curr)
        for child in curr.child:
            self.dfs(curr.children[child])
    
    def pattern_base(self,curr,pattern):
        
        curr_patterns = {}
        
        for item,supp in pattern:
            curr_patterns[(item,supp)]=1
        
        for item,supp in pattern:
            item = item + curr.value
            curr_patterns[(item,curr.support)]=1
        
        if len(curr.child)==0:
            for item,supp in curr_patterns:
                self.new_patterns[(item,supp)]=1
        
        for child in curr.child:
            self.pattern_base(curr.children[child],curr_patterns)
    
    
                    
            

# CODE STARTS HERE 

start_time = timeit.default_timer()

#Initialize matrix 
database = []

frequency_table = {}



#Read the input file

with open("FINAL PROJECT/new_input.txt","r") as f:
    data = f.readlines()
    
    for line in data:
        line=line[:-1]
        words = line.split(" ")
        
        for item in words:
            if item in frequency_table:
                frequency_table[item]+=1
            else:
                frequency_table[item]=1
        
        database.append(words)
        

#sorting items in decreasing order of frequency
itemset_sorted = sorted(frequency_table,key = frequency_table.get,reverse = True)

#sort database as per itemsets
database2 = []
for trans in database:
    transaction = sorted(trans,key=lambda x:itemset_sorted.index(x[0]))
    database2.append(transaction)
    
#Creating an object
tree = FP_Tree()
tree.build(database2)

tree.dfs(tree.root)

patterns = {("",0)}
tree.pattern_base(tree.root,patterns)

stop_time = timeit.default_timer()

total_time = stop_time - start_time

print(tree.new_patterns)

HF_itemsets = [(item,supp) for item,supp in tree.new_patterns if supp>=2]
LF_itemsets = [(item,supp) for item,supp in tree.new_patterns if supp<2 and item!=""]

#creating a HF File
f = open("HF.txt","w")
for item,supp in HF_itemsets:
    f.write(str(item)+" "+str(supp)+"\n")
f.close()

#creating a LF File
f = open("LF.txt","w")
for item,supp in LF_itemsets:
    f.write(str(item)+" "+str(supp)+"\n")
f.close()
