#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Assignment 3: The Ship Rendezvous Problem

Your code should:

1. Read a problem instance (data) from a CSV file;
2. Run the greedy heuristic against the problem instance to obtain a solution.
3. Output the resulting path to a CSV file.
4. Output key performance indicators of the solution to a second CSV file.

See the assignment specification for details of the greedy heuristic,
calculation of key performance indicators and file formats for the CSVs.

Advice for completing the assignment:

1. Create and test alternative problem instances of the SRP.
2. Design your solution code carefully and write efficient, readable code.
3. Check that your code outputs files in the correct format.
4. Make regular backups of your code.
5. Before you submit your code - do one final test that it runs without error.

"""

import numpy as np

def main(csv_file):
    '''
    Main function for running and solving an instance of the SRP.

    Keyword arguments:
    csv_file -- the csv file name and path to a data for an instance of
                ship rendezvous problem.
    '''
    #read in the csv file to a numpy array
    problem_data = read_srp_input_data(csv_file)

    #These print statements can be deleted
    #They are just here to check what data has been loaded
    print(problem_data)
    print(problem_data.shape)

    # =========================================================================
    # To do:
    # 1. pre-process input_data into variables usable by your algorithm.
    # 2. Run the greedy algorithm provided in the assignment document.
    # 3. Write the solution to a CSV file "solution.csv".
    # 4. Write the KPIs to a CSV file "kpi.csv".
    # =========================================================================


def read_srp_input_data(csv_file):
    '''
    Problem instances for the SRP are stored within a .csv file
    This function reads the problem instance into Python.
    Returns a 2D np.ndarray (4 columns).
    Skips the headers and the first column.
    Columns are:
    x-coordinate, y-coordinate, x-speed and y-speed

    Keyword arguments:
    csv_file -- the file path and name to the problem instance file
    '''

    input_data = np.genfromtxt(csv_file, delimiter=',',
                               dtype=np.float64,
                               skip_header=1,
                               usecols=tuple(range(1, 5)))

    return input_data



def print_kpis(n_ships, total_time, max_wait, max_y, furthest_distance,
               avg_time):
    '''
    An OPTIONAL utility function to print the key performance measures
    of the SRP optimisation to the Python console.

    This function is designed to help with debugging the algorithm.
    It is NOT mandatory to use it. It can be removed from your code
    if it is not required.

    Keyword arguments:
    n_ships -- the number of ships
    total_time -- total time for the support ship to complete its tour
    max_wait -- the max time a ship waited for the support ship to rendezvous
    max_y -- the maximum y coordinate to which the support ship travelled
    furthest_distance -- the max distance travelled to rendezvous
    avg_time -- The average time to visit each ship

    '''
    #pylint: disable-msg=too-many-arguments
    print('\n === Key Performance Indicators ===')
    print('Ships visited    :\t{0}'.format(n_ships))
    print('Total time       :\t{0}'.format(total_time))
    print('Max. waiting time:\t{0}'.format(max_wait))
    print('Furthest Y coord.:\t{0}'.format(max_y))
    print('Furthest distance:\t{0}'.format(furthest_distance))
    print('Avg. waiting time:\t{0}'.format(avg_time))
    print('\n')


if __name__ == '__main__':
    # =========================================================================
    # you can change the name of the input file
    # to test different problem instances.
    # Please DOT NOT delete the 'if __name__ == '__main__':
    # =========================================================================
    PROBLEM_FILE = 'sample_srp_data.csv'
    main(PROBLEM_FILE)
