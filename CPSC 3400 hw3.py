""" Homework 3 for CPSC 3400, Spring 2021
Solution by Kyle Fraser
"""


import sys


def mark_sweep(f):
    """ Performs the mark-sweep garbage collection algorithm after 
        processing a file which contains mappings of variables which 
        reference heap block fron 0 to n-1 and mappings of heap blocks 
        to other heap blocks. The first line in the file gives the 
        number of heap blocks and the rest of the lines in the file 
        give a single ordered pair to represent a mapping.   


    
        Creates and returns a dictionary specifying marked heap blocks
        and swept heap blocks. 



        Assumptions:
        Named pointers are referred to using variable names such as p, 
        stackptr and temp3.

        Heap blocks are referred to using integers.
      
        Input is valid and properly formatted. There are not spaces
        in an input file line. 

        A variable name consists of letters, digits, and underscores but 
        cannot begin with a digit.

        Variable names are unique.

        There is at least 1 heap block.



        Param: filename: Name of the input file (string)
        Return: A dictionary in the form {'marked':[],'swept':[]}
        where all marked heap blocks will be added to values of 
        the 'marked' key and swept blocks will be added to values of 
        the 'swept' key. The values of each key will be an ordered 
        list of integers. 
    """  
    variables_list = {}
    hb_connect = {}
    ms_dict = {'marked': [], 'swept': []}
    empty = []

    with open(f, 'r') as fname:
        number_of_heap_blocks = int(fname.readline())
      
        for line in fname:
            ref = line.split(',') 
            if ref[0][0].isalpha() == False and  ref[0][0] != '_':
          
                for variables in variables_list:
                    if int(ref[0]) in variables_list[variables]:
                        variables_list[variables].append(int(ref[1]))

                if int(ref[0]) in hb_connect:
                    hb_connect[int(ref[0])].append(int(ref[1]))
                else:
                    hb_connect[int(ref[0])] = empty[:]
                    hb_connect[int(ref[0])].append(int(ref[1]))
          
            else: 

                if ref[0] in variables_list:
                    variables_list[ref[0]].append(int(ref[1]))
                else:
                    variables_list[ref[0]] = empty[:]
                    variables_list[ref[0]].append(int(ref[1]))
                  
        marked = []
        search_count = 0
        for check in variables_list:
            for element in variables_list[check]:
                marked.append(element)
          
        while(search_count < number_of_heap_blocks): 
            for connection in hb_connect:
                if connection in marked:
                    for element in hb_connect[connection]:
                        marked.append(element)
            search_count += 1

        swept = []
        for check in hb_connect:
            if check not in marked:
                swept.append(check)
            for element in hb_connect[check]:
                if element not in marked:
                    swept.append(element)
            
        for element in range(number_of_heap_blocks):
            if element not in marked and element not in swept:
                swept.append(element)

        marked2 = []
        swept2 = []
        [marked2.append(m) for m in marked if m not in marked2]
        [swept2.append(s) for s in swept if s not in swept2]
      
        final_marked = sorted(marked2)
        final_swept = sorted(swept2)

        ms_dict['marked'] = final_marked
        ms_dict['swept'] = final_swept

        return ms_dict


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Usage: python3 hw3.py HEAP_FILE')
        sys.exit()

    filename = sys.argv[1]
    results = mark_sweep(filename)

    print('Marked nodes', end=': ')
    for element in results['marked']:
        print(element, end=' ')
    print()

    print('Swept nodes', end=': ')
    for element in results['swept']:
        print(element, end=' ')
    print()
