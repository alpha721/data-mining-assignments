from collections import defaultdict
import sys

dataset_file = ''
minsupp = 0.00
minconf = 0.00

rules = dict()
transactions = []
itemsets = []
num_of_transactions  = 0
    
def load_transactions(dataset_file):
        first_itemsets = dict()
        for readline in open(dataset_file, 'r'):
            for line in readline.split('\r'):
                t = line.strip().split(',')
                transactions.append(set(t))
                for item in t:
                    item_set = frozenset([item])
                    if item_set not in first_itemsets:
                        first_itemsets[item_set]=1
                    else:
                        first_itemsets[item_set]+=1
        itemsets.append(first_itemsets)
        return itemsets,transactions
#itemsets, transactions = load_transactions(dataset_file)


def initial_itemset():
    global num_of_transactions
    num_of_transactions  = len(transactions)
    first_itemset = itemsets[0]
    for item in first_itemset.copy().keys():
        support_value = first_itemset[item]#/num_of_transactions
        if support_value < minsupp:
            del first_itemset[item]
        else:
            first_itemset[item] = support_value

def generate_frequent_itemsets():
    global num_of_transactions
    prev_itemset = list(itemsets[0].keys())
    while len(prev_itemset) is not 0:
        new_set_len = len(prev_itemset[0])+1
        candidate_itemsets = dict()
        for i in range(0, len(prev_itemset)):
            for j in range(i+1, len(prev_itemset)):
                present_set = prev_itemset[i] | prev_itemset[j]
                if len(present_set) is new_set_len:
                    count = 0
                    for itemset in prev_itemset:
                        if itemset <= present_set:
                            count += 1
                    if count == len(present_set):
                        candidate_itemsets[present_set] = 0
    
    #after the combinations of next possible itemsets have been generated we find each of there's support values.
        if len(candidate_itemsets) is not 0:
            for t in transactions:
                for itemset in candidate_itemsets:
                    if itemset <= t:
                        candidate_itemsets[itemset] += 1
            for itemset in list(candidate_itemsets.keys()):
                support_value = candidate_itemsets[itemset]#/num_of_transactions
                if support_value < minsupp:
                    del candidate_itemsets[itemset]
                else:
                    candidate_itemsets[itemset] = support_value
        if len(candidate_itemsets) is not 0:
            itemsets.append(candidate_itemsets)
        prev_itemset = list(candidate_itemsets.keys())

def generate_rules():
    for itemsetss in itemsets[1:]:
        for itemset in itemsetss.keys():
            for item in itemset:
                left_items = itemset - frozenset([item])
                num = itemsets[len(itemset) - 1][itemset]
                num_total = itemsets[len(left_items) - 1][left_items]
                conf = float(num) / num_total
                if conf >= minconf:
                    line = "[" + ", ".join(list(left_items)) + "] (" + str(num_total) + " => [" + item + "] " +"("+ str(itemsets[len(frozenset([item]))-1][frozenset([item])])+ ")"+ " - conf ("+str(conf)  + ")"#+ ", Supp: " + str ((itemsetss[itemset])) + ")"
                    rules[line] = conf
    
def print_result():
    f = open('candidate_itemsets.txt','w')
    #f.write(itemsets)
    for item in itemsets:
        for i in range(0,len(item)):
            f.write("%s ," % list(list(item.keys())[i]))
            f.write("(%s)\n" % list(item.values())[i])
    
    f.close()
    
    g = open('rules.txt','w')
   # g.write(rules)
    for rule in rules:
        g.write("%s\n" % rule)
    g.close()
    
def main():
#if __name__ == '__main__':
#    if len(sys.argv) != 4:
#        print("usage: [data.csv] [min_sup] [min_conf]")
#        sys.exit(2)
    global dataset_file
    global minsupp
    global minconf
    global itemsets
    global transactions
    
#    dataset_file = sys.argv[1]
#    minsupp = sys.argv[2]
#    minconf = sys.argv[3]
    dataset_file = '/home/neetu/pn/groceries.csv'
    minsupp = 30
    minconf = 0.01
 
    itemsets, transactions = load_transactions(dataset_file)
    initial_itemset()
    generate_frequent_itemsets()
    generate_rules()
    print_result()
    
main()