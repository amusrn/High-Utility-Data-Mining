import timeit
from random import randrange

class Node():
    
    def __init__(self,itemsets):
        self.pattern = [0]*itemsets
        self.transaction = list()
        self.transaction_id = list()
        self.SDP = False
        self.left = None
        self.right = None
    
    def __str__(self):
        return "Pattern : {0} Transactions : {1} SDP : {2}".format(self.pattern,self.transaction,self.SDP)

class Graph(Node):
    
    def __init__(self,itemsets,s):
        self.root = Node(itemsets)
        self.total_contrib = s
        self.cntitem = 0
        self.high_utility = {}
    
    def subscription_set(self,node):
        """Subset of transactions in database which satisfy Pk"""
        
        count = -1
        
        for trans in database:
            count+=1
            flag = True
            for i in range(no_of_items):
                if node.pattern[i]==1 and trans[i]==0:
                    flag = False
                    break
                elif node.pattern[i]==-1 and trans[i]>0:
                    flag = False
                    break
            if flag:
                node.transaction.append(trans)
                node.transaction_id.append(count)
    
    def set_contrib(self,node):
        res = 0
        for trans in node.transaction:
            for i in range(no_of_items):
                if node.pattern[i] is not -1:
                    res+=trans[i]
        return res
    
    def one_contrib(self,node):
        res = 0
        for trans in node.transaction:
            for i in range(no_of_items):
                if node.pattern[i] is 1:
                    res+=trans[i]
        return res
    
    def cal_pattern_ratio(self,node):
        try:
            Cp= self.one_contrib(node)
            C = self.set_contrib(node)
            dk = Cp/C
            gamma = C/self.total_contrib
            
            if dk >= def_param and gamma >= sig_param:
                node.SDP = True
        
        except:
            dk = 0
            gamma = 0
        
        return gamma
    
    
    def YG(self,node):
        #splitting Criteria :- 'Yield Greedy'
        
        ans = 0
        idx = 0
        for i in range(no_of_items):
            if node.pattern[i] is not 0: continue
            curr = 0
            for trans in node.transaction:
                curr+=trans[i]
            
            if curr>ans:
                ans = curr
                idx = i
        return idx
    
    
    def dfs(self,node,pattern):
        node.pattern = pattern
        self.subscription_set(node)
        
        #if no transaction satisfy that pattern, return
        if len(node.transaction) == 0: return 0
        
        gamma = self.cal_pattern_ratio(node)
        
        #check recursion part for this
        if gamma<sig_param or node.SDP or len(node.transaction)==0: 
            return 0
        
        max_yield = self.YG(node)
        node.left = Node(no_of_items)
        node.right = Node(no_of_items)
        
        pattleft = [0]*no_of_items
        pattright = [0]*no_of_items
        
        for i in range(no_of_items):
            if i==max_yield: 
                pattleft[i]=1
                pattright[i]=-1
            else:
                pattleft[i]=pattern[i]
                pattright[i]=pattern[i]

        self.dfs(node.left,pattleft)
        self.dfs(node.right,pattright)
    
    def printSDPnodes(self,node):
        """to print all SDP NODES"""
        
        if node.SDP == True:
            for index in node.transaction_id:
                self.high_utility[index] = 1
            
            print("SDP node: ",end=" ")
            print(node.pattern,node.transaction,node.transaction_id)
            
            
            self.cntitem+=len(node.transaction)
        
        else:
            print("Non SDP node: ",end=" ")
            print(node.pattern,node.transaction,node.transaction_id)
            
        
        if node.left is not None:
            self.printSDPnodes(node.left)
        if node.right is not None:
            self.printSDPnodes(node.right)
    
    
def generate_database(support_list,utility_list,itemset_list):
    
    database = list() #a 2d matrix
    itemset_database = list()
    
    with open("HF.txt","r") as f:
        data = f.readlines()
        
        for line in data:
            itemset = list(map(str,line.split(" ")))
            support_list.append(int(itemset[1]))
            itemset = list(itemset[0])
            itemset_list = [item for item in itemset]
            
            
        
        for line in data:
           
            itemset = list(map(str,line.split(" ")))
            itemset_database.append(itemset[0])
            itemset = list(itemset[0])
            lis = [randrange(1,20) if item in itemset else 0 for item in itemset_list]
            
            utility_list.append(sum(lis))
            
            database.append(lis)
            
        
    
    return database,itemset_database
    
            
            
            
            
    
        

#CODE STARTS here

start_time = timeit.default_timer()

def_param = 0.8
sig_param = 0.05

itemset_list = set()
support_list = list()
utility_list = list()

database,itemset_database = generate_database(support_list,utility_list,itemset_list)

no_of_trans = len(database)
no_of_items = len(itemset_list)

#s = it is the total contribution of the database
s = 0
for line in database:
    s+=sum(line)
    
print(s)

tree = Graph(no_of_items,s)

#main function in Graph class
tree.dfs(tree.root,[0]*no_of_items)

#to print all SDP nodes
print("ALL SDP nodes are : " )
tree.printSDPnodes(tree.root)

print("MAIN TABLE")
print(tree.high_utility)

stop_time = timeit.default_timer()



#answer

HFHU = list()
HFLU = list()

count = -1

for trans in itemset_database:
    count+=1
    if count in tree.high_utility:
        lis = (trans,support_list[count],utility_list[count])
        
        HFHU.append(lis)
        
    else:
        lis = (trans,support_list[count],utility_list[count])
        
        HFLU.append(lis)
        

#creating a HFHU file 
f = open("HFHU.txt","w")
for item,supp,util in HFHU:
    f.write(str(item)+" "+str(supp)+" "+str(util)+"\n")
f.close()

#creating a HFLU File
f = open("HFLU.txt","w")
for item,supp,util in HFLU:
    f.write(str(item)+" "+str(supp)+" "+str(util)+"\n")
f.close()


