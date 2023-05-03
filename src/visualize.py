#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
args = parser.parse_args()

# imports
import os
import json
from collections import Counter,defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
#import seaborn as sns

# make things pretty with seaborn
"""
sns.set(font=’Franklin Gothic Book’,
        rc={
 ‘axes.axisbelow’: False,
 ‘axes.edgecolor’: ‘lightgrey’,
 ‘axes.facecolor’: ‘None’,
 ‘axes.grid’: False,
 ‘axes.labelcolor’: ‘dimgrey’,
 ‘axes.spines.right’: False,
 ‘axes.spines.top’: False,
 ‘figure.facecolor’: ‘white’,
 ‘lines.solid_capstyle’: ‘round’,
 ‘patch.edgecolor’: ‘w’,
 ‘patch.force_edgecolor’: True,
 ‘text.color’: ‘dimgrey’,
 ‘xtick.bottom’: False,
 ‘xtick.color’: ‘dimgrey’,
 ‘xtick.direction’: ‘out’,
 ‘xtick.top’: False,
 ‘ytick.color’: ‘dimgrey’,
 ‘ytick.direction’: ‘out’,
 ‘ytick.left’: False,
 ‘ytick.right’: False})
sns.set_context("notebook", rc={"font.size":16,
                                "axes.titlesize":20,
                                "axes.labelsize":18})
"""
plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

# print the count values
items = sorted(counts[args.key].items(), key=lambda item: (item[1],item[0]), reverse=True)
for k,v in items:
    print(k,':',v)

# create lists of keys and values for the bar graph
top_items = items[:10] 
keys = [item[0] for item in top_items]
values = [item[1] for item in top_items]
keys = keys[::-1]
values = values[::-1]

# plot the bar graph
plt.bar(range(len(keys)), values, color = "seagreen")
plt.xticks(range(len(keys)), keys)

# set the title and axis labels
if args.input_path[-1] == 'g':
    plt.xlabel('Language')
else:
    plt.xlabel('Country')
if args.percent:
    plt.ylabel('% of Tweets')
else:
    plt.ylabel('# of Tweets')
plt.title('Coronavirus Twitter Analysis')

# save the bar graph as a PNG file
if args.input_path[-1] == 'g':
    plt.savefig(args.key[1:] + '_lang.png')
else:
    plt.savefig(args.key[1:] + '_country.png')
