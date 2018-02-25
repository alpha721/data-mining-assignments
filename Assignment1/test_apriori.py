from collections import defaultdict
import itertools as it

dataset_file = '/home/neetu/pn/groceries.csv'

def create_candidate_item_set(dataset_file):
  ''' Create a dictionary of all candidate item sets from the data set with their corresponding count '''
  
  candidate_item_list = defaultdict(int)
  baskets = []

  with open(dataset_file) as file:
    for line in file:
      num_list = line.strip().split(',')
      baskets.append(num_list)

      for item in num_list:
        if item not in candidate_item_list:  
            candidate_item_list[item] = 1
        else: candidate_item_list[item] += 1

  return candidate_item_list, baskets


def create_frequent_item_set(item_list, min_threshold):
  ''' Return the frequent items from the candidate_item_list that meet the min_support '''

  # delete items that dont meet min threshold
  for key, value in list(item_list.items()):
    if value < min_threshold:
      del item_list[key]

  return item_list.keys(), item_list.values()
'''

def count(item_list, baskets):
   Count the number of frequent item sets in the baskets 
  count = dict(zip(item_list, [1]*len(item_list)))

  for basket in baskets:
    for key in count:
      if set(list(key)) < set(basket):
        count[key] += 1 

  return count
'''

def join(freq_item_sets, k):
  ''' Generate the joint transactions from candidate sets of size k '''
  
  # k is the size of each item set
  if k <= 2: 
    return list(it.combinations(freq_item_sets, k))
  else:
    return list(it.combinations(set(a for b in freq_item_sets[0] for a in b),k))


def apriori(dataset_file, threshold):  
  
  C1, baskets = create_candidate_item_set(dataset_file)
  F1_items, F1_values = create_frequent_item_set(C1, threshold)
  
  if not F1_values:
    return None
  else:
    # Remember the item sets
    L = [[F1_items, F1_values]]
    k = 2
    while(True):
      new_list = join(L[k-2][0], k)
      items = count(new_list, baskets)

      Fk_items, Fk_values = create_frequent_item_set(items, threshold)
      if len(Fk_items) > 0:
        L.append([[Fk_items, Fk_values]])
        k += 1
      else:
        break

    return L[k-2][0][0]
