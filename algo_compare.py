###############################################################################
'''

         A program for testing the efficiency of various algorithms
                        and plotting the results


                               9/7/2018

                        Author: Cory Kennedy




Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the “Software”), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.


'''
###############################################################################


from timeit import timeit
from random import randint, random
from math import floor
import matplotlib.pyplot as plt
plt.style.use('ggplot')


# --- ALGORITHM 1 ---

# NOTE: be sure algorithms being tested are in the form of
## a user-defined function that takes a list of integers
### as a parameter

ALGO_1 = 'Fisher-Yates Shuffle'
def fisher_yates_shuffle(the_list):
    list_range = range(0, len(the_list))
    for i in list_range:
        j = randint(list_range[0], list_range[-1])
        the_list[i], the_list[j] = the_list[j], the_list[i]
    return 1


# --- ALGORITHM 2 ---

ALGO_2 = 'Insertion Sort'
def insertion_sort(the_list):
    for i in range(1, len(the_list)):
        tmp = the_list[i]
        k = i
        while k > 0 and tmp < the_list[k - 1]:
            the_list[k] = the_list[k - 1]
            k -= 1
            the_list[k] = tmp
    return 1


# --- ALGORITHM 3 ---

ALGO_3 = 'Binary Search'
def binary_search(the_list, item):
    first = 0
    last = len(the_list) - 1

    while first <= last:
        i = int((first + last) / 2)

        if the_list[i] == item:
            return 1
        elif the_list[i] > item:
            last = i - 1
        elif the_list[i] < item:
            first = i + 1
        else:
            return 1


# --- Helper Functions ---

# Wrapper for timing user-defined functions
def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped


# --- Generate Data ---

# Track number of iterations per run
## The length of x_all is independent variable (n)
x_all = []

# Track times taken by each algorithm
y_fisher = []
y_insert = []
y_binary = []

# List for algorithms to work on
rand_ints = []

ROUNDS = 100
INT_RANGE = 100
NUM_INTS = 100
SEARCHED_NUM = 10
TIME_TESTS = 10

# Test each algorithm for 100 rounds
for i in range(ROUNDS):

    # Append 100 random ints to rand_ints
    rand_ints += [int(NUM_INTS*random()) for i in range(INT_RANGE)]
    # Sort them incase an algo requires a sorted lust
    sorted_ints = sorted(rand_ints)

    # Wrap each algo function call for timing execution
    fisher_wrapped = wrapper(fisher_yates_shuffle, rand_ints)
    insert_wrapped = wrapper(insertion_sort, rand_ints)
    binary_wrapped = wrapper(binary_search, sorted_ints, SEARCHED_NUM)

    # Capture the data
    x_all += [len(rand_ints)]
    # Execution times
    y_fisher += [timeit(fisher_wrapped, number=TIME_TESTS)]
    y_insert += [timeit(insert_wrapped, number=TIME_TESTS)]
    y_binary += [timeit(binary_wrapped, number=TIME_TESTS)]


# --- Generate Plots ---

# NOTE: if additional plots are desired, the remaining code
## will need to be exteneded to accomodate
NUM_PLOTS = 3

# Initialize plot objects
f, axarr = plt.subplots(NUM_PLOTS, sharex=True)
f.suptitle('Algorithm Analysis')

# Create subplots
axarr[0].plot(x_all, y_fisher, color='blue', label=ALGO_1)
axarr[1].plot(x_all, y_insert, color='green', label=ALGO_2)
axarr[2].plot(x_all, y_binary, color='orange', label=ALGO_3)

# Bring subplots close to each other
f.subplots_adjust(hspace=0)
# Hide x labels and tick labels for all but bottom plot
for ax in axarr:
    ax.label_outer()

# Place a legend in the corner of each plot
axarr[0].legend(loc="upper right")
axarr[1].legend(loc="upper right")
axarr[2].legend(loc="upper right")

# Set axes labels
axarr[1].set_ylabel(ylabel='Execution time (in seconds)', labelpad=40)
axarr[2].set_xlabel(xlabel='Length of input array (n)', labelpad=30)

# Save it
plt.savefig('algo_compare.png', bbox_inches='tight')
