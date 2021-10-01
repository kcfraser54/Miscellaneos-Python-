""" Homework 2 for CPSC 3400, Spring 2021
Solution by Kyle Fraser 
"""


import sys
import os

class ImproperTimeError(Exception): pass
class EmptyFileError(Exception): pass 


def create_time_list(filename):
    """ Reads and parses the input file. 



    Creates and returns a list of time tuples in the order of 
    (hours-integer, minutes-integer,AM/PM-string. Also throws exceptions
    if the input file does not exist, the input file is empty, or the 
    input file contains an improper time. 

    
    
    Assumptions: 
    None.


    Param: filename: Name of the input file (string)
    Return: A list of time tuples. Each tuple has three elements 
    corresponding to hour, minute, and AM/PM. 
    """
    if os.stat(filename).st_size == 0:
        raise EmptyFileError
    else:
        time_list = []
        with open(filename, 'r') as f:
            for line in f:

                currentTuple = ()
                time_elements = line.split()

                if len(time_elements)!= 3:
                    raise ImproperTimeError
                
                for place, item in enumerate(time_elements):
                    if len(item) != 2 and (place == 1 or place == 2):
                        raise ImproperTimeError
                    
                    if place == 0:

                        if len(item) != 2 and len(item) != 1:
                            raise ImproperTimeError
                        hours = int(item)
                        if (hours <= 0 or hours > 12 or
                            type(hours) != int):
                            raise ImproperTimeError
                                                 
                    if place == 1:
                        minutes = int(item)
                        
                        if (minutes < 0 or minutes > 59 or
                            type(minutes) != int):
                            raise ImproperTimeError

                    if place == 2:    
                        am_or_pm = item
                        if am_or_pm != 'PM' and am_or_pm != 'AM':
                            raise ImproperTimeError
                

                currentTuple = (hours, minutes, am_or_pm)
                time_list.append(currentTuple)

    
        return time_list


def build_time_list(time):
    """ Creates and returns a string corresponding to the 
        correct time tuple. 



        This function builds and returns a string from the 
        elements of a single time tuple. The element corresponding to 
        minutes will be padded with a zero if needed.



        Assumptions: The parameter time is a tuple consisting 
        of three elements corresponding to hours(int), minutes(int), 
        and AM/PM(string). The tuple is a proper representation 
        of time. 



        Param: time: A tuple representing a time (tuple).
        Returns: A string which corresponds to the time tuple 
                 being processed. 
        """  
    time_str = ''
    str_hours = str(time[0])
    str_min = str(time[1]).zfill(2)
    ampm = time[2]
    time_str = '%s:%s %s'%(str_hours, str_min, ampm)
    return time_str


def helper(time):
    """ This is a helper function for the sort and max functions. 
        


        Updates the hours element of a tuple based on the AM/PM 
        element so that times may be correctly sorted and the correct 
        maximum time may be found. 



        Assumptions: The parameter time is a tuple consisting of three 
        elements corresponding to hours(int), minutes(int), 
        and AM/PM(string). The tuple is a proper representation 
        of time. 


        
        param: time: A tuple representing a time (tuple).
        returns: A time tuple with a potentially updated hours 
        element. 
    """ 
    time = list(time)
    if time[2] == 'PM' and time[0] != 12:
        time[0] += 12
    if time[2] == 'AM' and time[0] == 12:
        time[0] = 0
    time = tuple(time)
    return time


def get_military_time(time):
    """ This function take in a single time tuple and converts the time 
        to military time. 




        A tuple of just two elements is created and returned. To 
        represent military time, the returned tuple only contains 
        hours and minutes. 



        
        Assumptions: The parameter time is a tuple consisting of three
        elements corresponding to hours(int), minutes(int),
        and AM/PM(string). The tuple is a proper representation
        of time.




        param: time: A tuple representing a time (tuple).
        returns: A time tuple of two elements, representing military
        time.
     """ 
    if time[2] == 'PM':

        if time[0] == 12:

            hours = 12
            minutes = time[1]

        else:
            hours = 12 + time[0]
            minutes = time[1]

    else:

        if time[0] == 12:
            hours = 0
            minutes = time[1]
        else:
            hours = time[0]
            minutes = time[1]

    return (hours, minutes)


def time_compare_gen(time_list, target):
    """ A generator function that will yield, for each 
        time tuple in time_list, a tuple that indicates how 
        far in the future it is from target. 



        The yielded tuples will contain two integer in the 
        order (hours, minutes). 



        Assumptions: Each tuple in the time list is 
        a proper representation of time consisting of 
        three elements (hours, minutes, AM/PM). The 
        target is a correct representation of time 
        consisting of three elements (hours, minutes, 
        AM/PM).



        param: time_list: A list of time tuples (list). 
        param: target: A time tuple (tuple). 
        returns: A tuple that indicates how far in the 
        future a particular time is from target. 
        """
    target = get_military_time(target)

    for times in time_list:

        comparison_time = get_military_time(times)
    
        if target > comparison_time:
            
            hours_until_midnight = 24 - target[0] - 1
            minutes = 60 - target[1]
            hours = hours_until_midnight + comparison_time[0]
            minutes = minutes + comparison_time[1]
            if minutes >= 60:
                hours += 1
                minutes -= 60
            yield (hours, minutes)
            
        elif target < comparison_time:
            if target[1] < comparison_time[1]:
                hours = comparison_time[0] - target[0]
                minutes = comparison_time[1] - target[1]
            elif target[1] > comparison_time[1]:
                hours = (comparison_time[0] - target[0]) - 1
                minutes = comparison_time[1] + (60 - target[1])

            else:
                hours = comparison_time[0] - target[0]
                minutes = 0
            yield (hours, minutes) 
        else:

            hours = 0
            minutes = 0
            yield (hours, minutes)
        

if __name__ == '__main__':         

    if len(sys.argv) != 2:
        print('Usage: python3 hw2.py TIME_FILE')
        sys.exit()
    input_file_cmd = 1
    filename = sys.argv[input_file_cmd]
    
    try:
        time_list = create_time_list(filename)
    except FileNotFoundError:
        print('Error: File not found')
        sys.exit()
    except EmptyFileError:
        print('Error: File is empty')
        sys.exit()
    except ImproperTimeError:
        print('Error: Improper time found')
        sys.exit()


    updated_time_list = []
    updated_time_list = [build_time_list(time) for time in time_list]
    print(updated_time_list)
    max_time = max(time_list, key=helper)
    print(max_time)
    sorted_time_list = sorted(time_list, key=helper)
    print(sorted_time_list)
    target = time_list[0]
    comparisons = time_compare_gen(time_list, target)
    comparison_list = []
    comparison_list = [times for times in comparisons]
    print(comparison_list)




    
    

