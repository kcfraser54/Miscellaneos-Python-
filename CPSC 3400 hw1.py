"""Kyle Fraser 
   4/11/2021
   CPSC 3400-02
   hw1.py

   This program tabulates the results of a survey where 
   people are asked to vote for their top three favorite 
   colors (in order). The results of the survey are stored 
   in an input file that has one or more lines in the
   following format.

   blue green red
 """

import sys


def print_dictionary(color_dictionary):
    """ This function takes in a dictionary as a parameter
        and prints the dictionary in sorted order.
    """
    
    for items in sorted(color_dictionary):
        print(items + ':', color_dictionary[items])

        
def process_file(user_file):
    """ This function reads and parses the input file.


        Process_file will create 
        and return a dictionary consisting of key-value pairs.

 
        The key is a color and the value is a tuple 
        consisting of three integers which correspond to first,
        second, and third place votes.
    """
    
    process_dict = {}
    with open(user_file, 'r') as input_file:
        
        # Loop through the file.
        for line in input_file: 
            colors = line.split(' ')
            place = 0

            # For every color, either increment the relevant place
            # or add the color to the dictionary. 
            for i in colors:

                if '\n' in i:
                    i = i[:-1]
                    
                if i in process_dict.keys():
                    process_dict[i][place] += 1
                    
                else:
                    process_dict.update({i: [0, 0, 0]})
                    process_dict[i][place] += 1

                place += 1
                    
        # Convert the list within the dictionary to a tuple. 
        for item in process_dict:
            process_dict[item] = tuple(process_dict[item])

    return process_dict


def get_first_place_votes(color_dictionary, color):
    """ This function takes in the dictionary returned from
        process_file and a specified color as parameters.


        The number of first place votes for the specific color 
        will be returned as an integer.


        If the color is not present in the list, the function 
        returns 0. 
    """
    
    if color in color_dictionary:
        return color_dictionary[color][0]
    else:
        return 0

    
def create_favorite_color_list(color_dictionary):
     """ This function takes in the dictionary returned from 
         process_file as a parameter. 


         Returns an ordered list of colors based on the number 
         of 1st place votes. 
         

         The list only contains colors that 
         received a first place vote.


         Ties are broken using the number of second place votes, if 
         still tied, winner is the color with the higher number of 
         third place votes, if still tied, winner is the color that 
         appears earlier in alphabetical order. 
      """
     # Sort the items in the dictionary first by key and then
     # by value. 
     color_list = color_dictionary.copy()
     color_list = sorted(color_list.items(), key=lambda x: x[0])
     color_list = sorted(color_list, key=lambda x: x[1], reverse=True)
     color_list = dict(color_list)

     # Add colors to the ordered list if they have at least one
     # first place vote. 
     ordered_list = []
     for items in color_list:
         if color_list[items][0] != 0:
             ordered_list.append(items)     
            
     return ordered_list

 
def create_color_score_dict(c_dict):
    """ Takes in the dictionary returned from process_file 
        as a parameter.


        Creates and returns a dictionary consisting of key-value 
        pairs where the key is a color and the value is an integer.


        The dictionary only contains colors that appeared in the file
        given by the user. 


        Values are computed using the following formula, 
        (number of first place votes * 3) + (number of second
        place votes * 2) + (number of third place votes).
     """
    
    score_dictionary = {}

    # Apply the color score to each color. 
    for items in c_dict:
        val = c_dict[items][0]*3 + c_dict[items][1]*2 + c_dict[items][2]                                             
        score_dictionary[items] = val

    return score_dictionary

# implementation of a simple test driver.
input_file_cmd = 1
user_file = sys.argv[input_file_cmd]

survey = process_file(user_file)
print_dictionary(survey)

first_place_count = get_first_place_votes(survey, 'blue')
print(first_place_count)

first_place_count = get_first_place_votes(survey, 'green')
print(first_place_count)

favorite_color_list = create_favorite_color_list(survey)
print(favorite_color_list)

color_scores = create_color_score_dict(survey)
print_dictionary(color_scores)

                                               

                                                       


    

    


