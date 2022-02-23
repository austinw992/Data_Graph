
###created during a Summer MURI Internship
#Authors: Austin Wang, Daniel E, Alex J



import glob
import os
import sys
import csv
import matplotlib.pyplot as plt

if len(sys.argv) != 2:
    print("Usage: python graph_maker.py relative_directory")
    sys.exit(1)


class Graph_Maker:
    # file_columns is a dictionary
    # containing the name of the file
    # and the names of the columns within
    # the file. This will be set to a 
    # member variable
    #
    # init will use os in order to get
    # the path for each of the .dat files in
    # the directory structure
    #
    # init sets a file pointer to the
    # first file in the list
    def __init__(self, file_columns):
        self.file_columns = file_columns

        root = sys.argv[1]

        # Get a list of all .dat files recursively
        self.file_list = [f for f in glob.iglob(root + '/**/*.dat', recursive=True)]
        
        # Set up the first file in list
        self.index = 0
        self.current_file = self.file_list[self.index]
        self.graphs = list()

    # For each file, set up the dictionary of
    # names and data points.
    #
    # Read through the file and add data points. 
    # After that, close file and move on to next
    # Return the set of graphs
    def Make_Graphs(self):
        # iterate through file lists
        for this_file in self.file_list:
        
            """ For some reason, pop_data.dat was getting repeated with the file names
                .eps and .png. In order to prevent the repeats, I have added this sanity
                check.
            """
            if this_file == "" or this_file is None:
                continue

            # get base file name for dictionary
            filename = os.path.basename(this_file)
            # make sure that filename is in dictionary
            if filename not in self.file_columns:
                print("The file " + filename + " is not in file_columns!")
                sys.exit(1)

            # Get the columns from the file name
            columns = self.file_columns[filename]

            # Create a dictionary that contains the
            # column name as a key and then a list
            # of data points as the value

            columns_datapoints = dict()

            # add each column to dictionary
            for column in columns:
                columns_datapoints[column] = list()

            with open(this_file, 'r') as obj_read:
                csv_reader = csv.reader(obj_read)

                for row in csv_reader:
                    # this makes indexing easier.
                    # otherwise, getting the column name would
                    # be a lot harder
                    for i in range(len(row)):
                        # Get column name
                        column = columns[i]
                        # Remove white space
                        row[i] = row[i].replace(' ', '')
                        # add the data point to that column
                        if row[i].isdigit():
                            columns_datapoints[column].append(int(row[i]))
                        else:
                            columns_datapoints[column].append(float(row[i]))
            # Create a new container for the datapoints and filename
            graph_obj = Graph(columns_datapoints, filename)
            # Add it to the list of graphs
            self.graphs.append(graph_obj)

        return self.graphs


class Graph:
    # columns_datapoints is a dictionary that contains
    # the name of the columns as a key and then the
    # values will be lists of data points for that columns
    # 
    # filename is the name of the file to which this
    # graph represents. This will allow us to associate
    # the graph with a given file
    #
    # The init will set up two member variables:
    # name and data. There will probably not
    # be any particular methods since this only
    # represents a container for the data within
    # a file
    def __init__(self, columns_datapoints, filename):
        self.data_dict = columns_datapoints
        self.filename = filename


file_columns = dict()
file_columns['med_diff_data.dat'] = ['MCS', 'Viral', 'Cytokine', 'Oxidator']
file_columns['pop_data.dat'] = ['MCS', 'uninfected', 'infected',
                                'virus releasing', 'dying', 'immune',
                                'immune activated']

file_columns['death_data.dat'] = ['MCS', 'viral', 'oxified', 'contact', 'bystander']

g_maker = Graph_Maker(file_columns)

graphs = g_maker.Make_Graphs()

for graph in graphs:
    plt.clf()
    # Split the file extension from name
    name = graph.filename.split('.', 1)[0]
    # Get the values for MCS. This will act as x-axis
    MCS = graph.data_dict['MCS']

    # Go through each column (except for MCS) and plot
    for column in (i for i in graph.data_dict if i != 'MCS'):

        # Get the data for the column
        y = graph.data_dict[column]
        # Plot it
        plt.plot(MCS, y, label=column)
        plt.yticks(fontsize="small")

    plt.yscale("log")
    plt.xlabel('MCS')
    plt.xticks(fontsize="small")
    # Set the title to the file name

    plt.legend(bbox_to_anchor=(1.04, 0.5), loc='lower left')
    plt.tight_layout()
    plt.savefig(name + ".eps", format='eps')
    plt.savefig(name + ".png", format='png')

    # Show the plot
    #plt.show()

sys.exit(0)