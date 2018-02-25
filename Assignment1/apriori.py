from collections import defaultdict
import sys

dataset = ''
minsupp = 0.00 
minconf = 0.00

rules = dict() #association rules
transactions = [] #database of transactions
itemsets = [] #frequent itemsets generated
    
def preprocess(dataset):
    ''' preprocess the dataset and generate the initial itemset'''   
    initial_set = dict()
    for readline in open(dataset, 'r'):
        for line in readline.split('\r'):
            t = line.strip().split(',')
            transactions.append(set(t))
            for item in t:
                item_set = frozenset([item])
                if item_set not in initial_set:
                    initial_set[item_set]=1
                else:
                    initial_set[item_set]+=1
    itemsets.append(initial_set)
    return itemsets,transactions


def initial_itemset():
    ''' prune the initial itemset to generate itemsets with high support count'''
    initial_itemset = itemsets[0]
    for item in initial_itemset.copy().keys():
        sup = initial_itemset[item]#/
        if sup < minsupp:
            del initial_itemset[item]
        else:
            initial_itemset[item] = sup

def generate_frequent_itemsets():
    ''' generate frequnet itemsets based on support based pruning'''
    old_itemset = list(itemsets[0].keys())
    while len(old_itemset) is not 0:
        new_set_len = len(old_itemset[0])+1
        candidate_itemsets = dict()
        for i in range(0, len(old_itemset)):
            for j in range(i+1, len(old_itemset)):
                present_set = old_itemset[i] | old_itemset[j]
                if len(present_set) is new_set_len:
                    count = 0
                    for itemset in old_itemset:
                        if itemset <= present_set:
                            count += 1
                    if count == len(present_set):
                        candidate_itemsets[present_set] = 0
    
        ''' pruning of itemsets based on support value takes place in the next steps'''
        if len(candidate_itemsets) is not 0:
            for t in transactions:
                for itemset in candidate_itemsets:
                    if itemset <= t:
                        candidate_itemsets[itemset] += 1
            for itemset in list(candidate_itemsets.keys()):
                sup = candidate_itemsets[itemset]#/
                if sup < minsupp:
                    del candidate_itemsets[itemset] 
                else:
                    candidate_itemsets[itemset] = sup
        if len(candidate_itemsets) is not 0:
            itemsets.append(candidate_itemsets)
        old_itemset = list(candidate_itemsets.keys())

def generate_rules():
    ''' generate the association rules based on confidence based pruning'''
    for itemsetss in itemsets[1:]:
        for itemset in itemsetss.keys():
            for item in itemset:
                left_items = itemset - frozenset([item])
                freq_count = itemsets[len(itemset) - 1][itemset]
                total_count = itemsets[len(left_items) - 1][left_items]
                conf = float(freq_count) / total_count
                if conf >= minconf:
                    line = "[" + ", ".join(list(left_items)) + "] (" + str(total_count) + ") => [" + item + "] " +"("+ str(itemsets[len(frozenset([item]))-1][frozenset([item])])+ ")"+ " - conf ("+str(conf)  + ")"#+ ", Supp: " + str ((itemsetss[itemset])) + ")"
                    rules[line] = conf
    
def generate_output():
    ''' write the frequent itemsets generated into the candidate_itemsets.txt file '''
    f = open('frequent_itemsets.txt','w')
    for item in itemsets:
        for i in range(0,len(item)):
            f.write("%s ," % list(list(item.keys())[i]))
            f.write("(%s)\n" % list(item.values())[i])
    f.close()
    
    ''' write the rules generated into the rules.txt file'''
    g = open('rules.txt','w')
    for rule in rules:
        g.write("%s\n" % rule)
    g.close()
    
def main():
    global dataset
    global minsupp
    global minconf
    global itemsets
    global transactions
    
    dataset = 'groceries.csv'
    minsupp = int(input('enter minimum support value: '))
    minconf = float(input('enter minimum confidence value: '))

    
    itemsets, transactions = preprocess(dataset)
    initial_itemset()
    generate_frequent_itemsets()
    generate_rules()
    generate_output()
    
main()