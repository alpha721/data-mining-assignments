from collections import defaultdict
#import pdb as pd

#pd.set_trace()

dataset_file = '/home/neetu/pn/groceries.csv'


#item_list, basket = create_candidate_item_set(dataset_file)
transactions = []
itemsets = []
def load_transactions(dataset_file):
        first_itemsets = dict()
        for readline in open(dataset_file, 'r'):
            for line in readline.split('\r'):
                t = line.strip().split(',')
                transactions.append(set(t))
                for item in t:
                    #item_set = frozenset([item])
                    item_set = frozenset([item])
                    #print(item_set)
                    #print("\n")
                    if item_set not in first_itemsets:
                        first_itemsets[item_set]=1
                    else:
                        first_itemsets[item_set]+=1
        itemsets.append(first_itemsets)
        return itemsets,transactions
#        correct_first_itemset()
itemsets, transactions = load_transactions(dataset_file)

minsupp = 0.01
#def correct_first_itemset():
num_of_transactions  = len(transactions)
first_itemset = itemsets[0]
for item in first_itemset.copy().keys():
    support_value = float(first_itemset[item])/num_of_transactions
    if support_value < minsupp:
        del first_itemset[item]
    else:
        first_itemset[item] = support_value


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
            support_value = float(candidate_itemsets[itemset])/num_of_transactions
            if support_value < minsupp:
                del candidate_itemsets[itemset]
            else:
                candidate_itemsets[itemset] = support_value
    if len(candidate_itemsets) is not 0:
        itemsets.append(candidate_itemsets)
    prev_itemset = list(candidate_itemsets.keys())

minconf = 0.01

rules = dict()
for itemsetss in itemsets[1:]:
    for itemset in itemsetss.keys():
        for item in itemset:
            left_items = itemset - frozenset([item])
            num = itemsets[len(itemset) - 1][itemset]
            num_total = itemsets[len(left_items) - 1][left_items]
            conf = float(num) / num_total
            if conf >= minconf:
                line = "[" + ", ".join(list(left_items)) + "] => [" + item + "] (Conf: "+str(conf * 100) + "%, Supp: " + str ((itemsetss[itemset] * 100)) + "%)"
                rules[line] = conf

