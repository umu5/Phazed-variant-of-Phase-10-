from phazed_group_type import (valid_run_of_cards, same_colour,
same_colour_for_accumulation, atleast_2_natural_cards, phazed_group_type)

def phazed_phase_type(phase):
    """It takes the combinations of cards group in the form of a list `phase`.
    Each group itself is a list containing cards. It returns the sorted list of 
    of non-negative integers representing the phase type that combination
    of card group(s) belongs to. If `phase` is empty it returns None and if 
    combination of groups in `phase` donot belongs to any phase type it returns
    an empty list."""
    
    if not phase:
        return None
    
    phase_list = []
    
    # Checking the validity of phase type 2 and 5 as both phases are composed
    # of single group of cards.
    if len(phase) == 1:
        list_group_type = phazed_group_type(phase[0])
        
        # One set of 7 cards of the same suit (phase type 2).
        if 2 in list_group_type:
            phase_list.append(2)
        
        # Run of eight cards (phase type 5).
        elif 4 in list_group_type:
            phase_list.append(5)
    
    # Checking the validity of other phase types that are composed of 2 groups.
    if len(phase) == 2:
        list_group_type_sublist0 = phazed_group_type(phase[0])
        list_group_type_sublist1 = phazed_group_type(phase[1])
        
        # Two sets of three cards of the same value (phase type 1).
        if 1 in list_group_type_sublist0 and 1 in list_group_type_sublist1:
            phase_list.append(1)
               
        # Two sets of four cards of the same value (phase type 4).
        elif 3 in list_group_type_sublist0 and 3 in list_group_type_sublist1:
            phase_list.append(4)
        
        # Two 34-accumulations (phase type 3).
        if 6 in list_group_type_sublist0 and 6 in list_group_type_sublist1:
            phase_list.append(3)
        
        # Two 34-accumulations of the same colour (phase type 6).
        if 7 in list_group_type_sublist0 and 7 in list_group_type_sublist1:
            phase_list.append(6)
        
        # A run of four cards of the same colour and a set of four cards of the 
        # same value (phase type 7).
        if 5 in list_group_type_sublist0 and 3 in list_group_type_sublist1:
            phase_list.append(7)
         
    return sorted(phase_list)
 

if __name__ == '__main__':
    # Example calls to the function.
    print(phazed_phase_type([['2C', '2S', '2H'], ['7H', '7C', 'AH']]))
    print(phazed_phase_type([['2C', '2C', '4C', 'KC', '9C', 'AH', 'JC']]))
    print(phazed_phase_type([['2C', 'KH', 'QS', '7H'],
                             ['3H', '7S', '0D', 'KD', 'AD']]))
    print(phazed_phase_type([['4H', '4S', 'AC', '4C'],
                             ['7H', '7C', 'AH', 'AC']]))
    print(phazed_phase_type([['4H', '5S', 'AC', '7C',
                              '8H', 'AH', '0S', 'JC']]))
    print(phazed_phase_type([['2C', 'KC', 'QS', '7C'],
                             ['3H', '7H', '0D', 'KD', 'AD']]))
    print(phazed_phase_type([['4H', '5D', 'AC', '7H'],
                             ['7H', '7C', 'AH', 'AS']]))
    print(phazed_phase_type([['4H', '5D', '7C', 'AC'], ['AC', 'AS', 'AS']]))