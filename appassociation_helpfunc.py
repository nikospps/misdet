# import numpy as np
# import matplotlib.pyplot as plt
import pandas as pd
from apyori import apriori
# import os
# os.getcwd()

def preprocess(data):
    store_data = pd.read_csv(data, encoding='unicode_escape', header=None)
    store_data = store_data.drop([2, 3, 4, 6], axis=1)
    store_data = store_data.drop(0)
    records = []
    for i in range(0, 4432):
        records.append([str(store_data.values[i, j]) for j in range(0, 3)])  # 3=number of columns
    association_rules = apriori(records, min_support=0.005, min_confidence=0.2, min_lift=3, min_length=2)
    association_results = list(association_rules)
    return association_results

def association_results(results):
    # results=preprocess(data)
    # global df
    rule1 = []
    rule2 = []
    support = []
    confidence = []
    lift = []
    for item in results:
        pair = item[0]
        items = [x for x in pair]
        # rule.append(items[0] + " -> " + items[1])
        rule1.append(items[0])
        rule2.append(items[1])
        support.append(str(item[1]))
        confidence.append(str(item[2][0][2]))
        lift.append(str(item[2][0][3]))
        df = pd.DataFrame({'Rule': rule1, 'Rule2': rule2, 'Support': support, 'Confidence': confidence, 'Lift': lift})
        df['Support'] = df['Support'].astype(float)
        df['Confidence'] = df['Confidence'].astype(float)
        df['Lift'] = df['Lift'].astype(float)
    return df

def association_results2(results):
    rule = []
    support = []
    confidence = []
    lift = []
    for item in results:
        pair = item[0]
        items = [x for x in pair]
        rule.append(items[0] + " -> " + items[1])
        # rule1.append(items[0])
        # rule2.append(items[1])
        support.append(str(item[1]))
        confidence.append(str(item[2][0][2]))
        lift.append(str(item[2][0][3]))
        df = pd.DataFrame({'Rule': rule, 'Support': support, 'Confidence': confidence, 'Lift': lift})
        df['Support'] = df['Support'].astype(float)
        df['Confidence'] = df['Confidence'].astype(float)
        df['Lift'] = df['Lift'].astype(float)
    return df
# a = preprocess('cep1.csv')
# b=association_results('cep1.csv')
# c = pd.read_csv('/home/nikospps/Downloads/processed_data.csv',index_col=0)
# aa=c['Rule2'].value_counts().reset_index().rename(columns={"index": "value", 0: "count"})
# plot=aa.plot.pie(y='count', figsize=(5, 5))
