VALUE = 0
SUIT = COLOUR = 1
RED_COLOUR = 'HD'
BLACK_COLOUR = 'SC'
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, 
          '9': 9, '0': 10, 'J': 11, 'Q': 12, 'K': 13}


def valid_run_of_cards(arg1):
    """ It takes the list of cards `arg1` and returns True if the the list 
    contains a valid run of cards, otherwise False."""
    
    index = 0
    # Assigns the value to index at which first non wild card occccurs.
    for card in arg1:
        if card[VALUE] != 'A':
            break
        index += 1
               
    # `group_list` is a list containing all cards of `arg1` except starting 
    # wild cards in a list.
    group_list = arg1[index:]
    value_in_str = '234567890JQK234567890JQK'
    # Starting index refers to the index in `value_in_str` that corresponds to 
    # first value of a card in `group_list`.
    starting_index = value_in_str.index(group_list[0][VALUE])
    # `edited_value_str` corresponds to the sequence of values sliced from
    # `value_in_str` on the basis of which the cards in `group_list` should
    # have value to define a valid run.
    edited_value_str = value_in_str[starting_index:starting_index
                                    + len(group_list)]
    
    group_value_str = ''
    i = 0
    for card in group_list:
        # If card from `group_list` has a value `A` then the value is 
        # taken from  `edited_value_str` at same index  and is added to 
        # `group_value_str` instead of taking value from card itself.
        if card[VALUE] == 'A':
            group_value_str += edited_value_str[i]
        else:
            group_value_str += card[VALUE]
        i += 1
        
    return group_value_str in value_in_str
               
                      
def same_colour(arg):
    """ It returns True if the list `arg` contains all of the cards of the same
    colour, otherwise False. Also, it takes in account the behaviour of wild 
    cards"""
    
    all_same_colour_cards = True
    colour_first_natural_card = 0
    # Determines the colour/suit of the first natural card in`arg`.
    for i in arg:
        if i[VALUE] != 'A':
            colour_first_natural_card = i[COLOUR]
            break 

    # `all_same_colour_cards` is set to False if the cards (except wild cards)
    # in `arg`  donot have the same colour as `colour_first_natural_card`.
    if colour_first_natural_card in RED_COLOUR:
        for i in arg[1:]:
            if not ((i[COLOUR] in RED_COLOUR) or i[VALUE] == 'A'):
                all_same_colour_cards = False
                break
    else:
        for i in arg[1:]:
            if not ((i[COLOUR] in BLACK_COLOUR) or i[VALUE] == 'A'):
                all_same_colour_cards = False
                break          
    return all_same_colour_cards


def same_colour_for_accumulation(arg2):
    """ It returns True if the list `arg2` contains all of the cards of the 
    same colour, otherwise False. It donot takes into account the behaviour 
    of a wild card."""
    
    all_same_colour_cards = True
    colour_first_card = arg2[0][COLOUR]
    
    # `all_same_colour_cards` is set to False if all of the cards in `arg2` 
    # donot have the same colour as the first card in the list.
    if colour_first_card in RED_COLOUR:
        for i in arg2[1:]:
            if not (i[COLOUR] in RED_COLOUR):
                all_same_colour_cards = False
                break
    else:
        for i in arg2[1:]:
            if not (i[COLOUR] in BLACK_COLOUR):
                all_same_colour_cards = False
                break
                
    return all_same_colour_cards

               
def atleast_2_natural_cards(lst):
    """ Takes the list of cards `lst` as an argument. Returns 'True' if list 
    contains atleast 2 natural cards, otherwise, 'False'."""
    
    natural_cards = 0
    i = 0
    while natural_cards < 2:
        if lst[i][VALUE] != 'A':
            natural_cards += 1
        i += 1
        if i == len(lst):
            break
    return natural_cards == 2
        

def phazed_group_type(group):
    """It takes the list of cards `group` and return a sorted list
    `combination_types` which contains the integer number corresponding to the
    group types that `group` belongs to. A particular `group` may belong to one
    or more than one group type. It returns empty list if `group` belongs to 
    neither of the group type or returns None if a group is an empty list."""
    
    combination_types = []
    # Returns `None` if group is an empty list.
    if not group:
        return None
    
    # If `group` contains less than 2 natural cards it returns 
    # `combination_types` as an empty list
    elif not atleast_2_natural_cards(group):
        return combination_types
    
    else:
        # checks the validity of `group` with group type 1 or 3.
        if len(group) == 3 or len(group) == 4:
            first_natural_value_card = 0
            # Assigns the value of the first natural card from `group` to
            # `first_natural_value_card`
            for i in group:
                if i[VALUE] != 'A':
                    first_natural_value_card = i[VALUE]
                    break   
                    
            # Creates a list containing boolean values of each card from a
            # `group` as compared to value of each card with respect to the 
            # value of the `first_natural_value_card` from a list.
            lst = [(card[VALUE] == first_natural_value_card
                    or card[VALUE] == 'A') for card in group]

            # If statement is `True` if group corresponds to group type 1.
            if sum(lst) == 3 and len(group) == 3:
                combination_types.append(1)
            # If statement is `True` if group correspends to group type 3.  
            elif sum(lst) == 4 and len(group) == 4:
                combination_types.append(3)
                
        # Check the validity of `group` with group type 2.
        elif len(group) == 7:
            first_natural_suit_card = 0
            # Assigns the suit of the first natural card from `group` to
            # `first_natural_suit_card
            for i in group:
                if i[VALUE] != 'A':
                    first_natural_suit_card = i[SUIT]
                    break
                    
            # Creates a list containing boolean values of each card from a
            # `group` as compared to suit of each card with respect to the 
            # suit of the `first_natural_value_card` from a list.
            lst = [(card[SUIT] == first_natural_suit_card 
                    or card[VALUE] == 'A') for card in group]
            if sum(lst) == 7:
                combination_types.append(2)
                
        # Check the validity of `group` with group type 4.       
        elif len(group) == 8:
            if valid_run_of_cards(group):
                combination_types.append(4)
                        
        # Check the validity of `group` with group type 5.        
        if len(group) == 4:
            if same_colour(group):
                if valid_run_of_cards(group):
                    combination_types.append(5)
                    
        # Creates a list in which elements refers to the value taken from 
        # dictionary `VALUES`of each card in a `group`.
        list_of_original_values = []
        for i in group:
            list_of_original_values.append(VALUES[i[VALUE]])
        
        # Checks the validity of `group` with group type 6.
        if sum(list_of_original_values) == 34:
            combination_types.append(6)
            
        # Checks the validity of `group` with group type 7.
        if sum(list_of_original_values) == 34:
            if same_colour_for_accumulation(group):
                combination_types.append(7)
            
    return sorted(combination_types)
  
    
if __name__ == '__main__':
    # Example calls to the function.
    print(phazed_group_type(['2C', '2S', '2H']))
    print(phazed_group_type(['2C', '2C', '4C', 'KC', '9C', 'AH', 'JC']))
    print(phazed_group_type(['4H', '4S', 'AC', '4C']))
    print(phazed_group_type(['4H', '5S', 'AC', '7C', '8H', 'AH', '0S', 'JC']))
    print(phazed_group_type(['4H', '5D', 'AC', '7H']))
    print(phazed_group_type(['KS', '0C', '8C', '3S']))
    print(phazed_group_type(['2C', '2C', '4C', 'KC', '9C', 'AS', '3C']))
    print(phazed_group_type(['4H', '5D', '7C', 'AC']))