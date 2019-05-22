import random

def generate_database(trans,itemset,revenue):

    database = list()

    
    for i in range(trans):
        database.append([])
        value = random.randrange(1,itemset)
        for j in range(value):
            database[i].append(random.randrange(1,itemset))
        
    return database

transactions,itemsets,revenue = map(int,input().split())
database = generate_database(transactions,itemsets,revenue)


for i in range(len(database)):
    database[i] = list(set(database[i]))

f = open("temp_input.txt","w")
for i in range(len(database)):
    utility = list()
    sm = 0
    for j in range(len(database[i])):
        val = random.randrange(1,100)
        sm+=val
        utility.append(val)
        f.write(str(database[i][j]))
        if j != len(database[i])-1:
            f.write(" ")

    f.write(":"+str(sm)+":")
    for j in range(len(utility)):
        f.write(str(utility[j]))
        if j != len(utility)-1:
            f.write(" ")
    f.write("\n")
f.close()
