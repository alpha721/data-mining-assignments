README FILE: Data Mining Assignment 1

Name: Neetu
ID no: 2015A7PS0079H

Assignment 1: The  goal  of  this  assignment  is  to generate  frequent item  sets and  interesting  association  rules  using Apriori  algorithm 

Dataset used : groceries.csv

To run the code:

- python apriori.py

It asks for a minimum support value and minimum confidence value:

For a sample run: 
try - minsup = 30
      minconf = 0.01
      
The frequent itemsets generated are stored in: frequent_itemsets.txt
The association rules generated are stored in: rules.txt

Format followed by the output files:

frequent_itemset.txt : [Freq Itemset] (count)
rules.txt : LHS (item set (count))--->RHS (item set (count)) -confidence value
