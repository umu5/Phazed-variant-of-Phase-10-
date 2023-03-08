from itertools import combinations

from phazed_group_type import (valid_run_of_cards, same_colour,
same_colour_for_accumulation, atleast_2_natural_cards, phazed_group_type)
from phazed_phase_type import (phazed_phase_type)
from phazed_is_valid_play import (building_accumulation, card_from_deck_or_discard, 
phazed_is_valid_play)

RED_COLOUR = 'HD'
BLACK_COLOUR = 'SC'
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, 
          '9': 9, '0': 10, 'J': 11, 'Q': 12, 'K': 13}
VALUE = 0
SUIT = COLOUR = 1
PHASE_TYPE = 0
PHASE_CONTENT = 1

# Constants related to `turn_history`.
LAST_TURN = -1
PLAYER_ID = 0
TURN_CONTENT = -1
PLAY_TYPE = 0
PLAY_CONTENT = 1


def ace_card(lst_group):
    """It takes the list of cards `lst_group` and returns the first ace card
    from the list. If ace card is not present it returns integer 0."""
    card = 0
    for i in lst_group:
        if i[VALUE] == 'A':
            card = i
            break
    return card
        
    
def max_value_card(list_group_card):
    """It  takes the list of cards `list_group_card` and returns the maximum
    value card. Values are taken from dictionary VALUES."""
    
    maximum_value = 0
    card = 0
    for i in list_group_card:
        if VALUES[i[VALUE]] >= maximum_value:
            maximum_value = VALUES[i[VALUE]]
            card = i
    return card
 
    
def phazed_play(player_id, table, turn_history, phase_status, hand, discard):
    """ It takes `player_id` as an integer number indicating the id of the 
    player attempting to play. For `table` it takes a 4-element list in which 
    each element represents a phase played by each player in the current hand. 
    For `turn_history` it takes a list of all turns in the hand to date that is 
    based on the sequence of the play. For `phase_status` it takes the 
    4-element list in which each element repesents the phases each players 0-3 
    have achieved respectively in the game. For `hand` it take a list of cards 
    that a current player holds i.e. player with id number `player_id`. For 
    discard it takes the 2-element string which represents the card at the top 
    of discard pile. Function returns 2-tuple describing the single valid play 
    a player wishes to play. The 2-tuple is itself made up of play ID and 
    associated play content.""" 
    
    # If statement is True if the Turn history is not empty.
    if turn_history:   
        recent_play = turn_history[LAST_TURN]
        player_id_recent_play = recent_play[PLAYER_ID]
        
        # Player has to play for the very first time in his turn so he can play 
        # play type 1 or 2 only.
        if player_id_recent_play != player_id:
            # Check if discard pile have an ace card and player have not
            # performed a phase yet. So pick up the ace card from discard pile.
            # Otherwise, pick the card from deck.
            if discard[VALUE] == 'A':
                if table[player_id] == (None, []):
                    return (2, discard)
            return (1, None) 
        
        # Player have not performed a phase yet.
        elif table[player_id] == (None, []):
            required_phase = phase_status[player_id] + 1
            
            # Check if player can play phase type 1.
            if required_phase == 1:
                if len(hand) >= 6:
                    copy_hand = hand.copy()
                    hand_sorted = sorted(copy_hand)
                    group_1 = []  # Set of 3 cards of same value.
                    group_2 = []  # Set of 3 cards of same value.
                    
                    # Check if player able to get the cards from `hand_sorted` 
                    # to complete group_1 using `combinations`.
                    for combination in combinations(hand_sorted, 3):
                        if 1 in phazed_group_type(list(combination)):
                            # Player able to get cards for `group_1`. So,
                            # remove those cards from `hand_sorted`.
                            group_1 = list(combination)
                            for i in group_1:
                                hand_sorted.remove(i)
                            break
                     
                    # Check if player able to get the cards from `hand_sorted`
                    # to complete group_2 using `combinations`.
                    if group_1:
                        if len(hand_sorted) >= 3:
                            for combination in combinations(hand_sorted, 3):
                                if 1 in phazed_group_type(list(combination)):
                                    group_2 = list(combination)
                                    break
                
                    if group_1 and group_2:
                        # Check if player can play a phase type 1 according to 
                        # ongoing condition of hand.
                        play = (3, (1, [group_1, group_2]))
                        if phazed_is_valid_play(play, player_id, table, 
                                                turn_history, phase_status, 
                                                hand, discard):
                            return play
                        
            # Check if player can play phase type 2.    
            elif required_phase == 2:
                copy_hand = hand.copy()
                hand_sorted = sorted(copy_hand, key=lambda x: x[SUIT])
              
                if len(hand) >= 7:
                    group_1 = []  # One set of 7 cards of same suit.
                    
                    # Check if player can get 7 cards of same suit from 
                    # `hand_sorted` using `combinations`.
                    for combination in combinations(hand_sorted, 7):
                        if 2 in phazed_group_type(list(combination)):
                            group_1 = list(combination)
                            break
                            
                    if group_1:
                        # Check if player can play a phase type 2 according to
                        # the ongoing condition of hand.
                        play = (3, (2, [group_1]))
                        if phazed_is_valid_play(play, player_id, table, 
                                                turn_history, phase_status, 
                                                hand, discard):
                            return play
                        
            # Check if player can play phase type 3.           
            elif required_phase == 3:
                # `score_list` contains the value of each card in `hand` taken
                # from `VALUES`.
                score_list = [VALUES[card[VALUE]] for card in hand]
                
                if sum(score_list) >= 68:
                    copy_hand = hand.copy()
                    group_1 = []  # 34 - accumulation.
                    group_2 = []  # 34 - accumulation.
                    
                    # `range` function helps to check each of the combination 
                    # types starting from 1 to the length of the `hand`.
                    for i in range(len(hand)):
                        i += 1  # To avoid staring from 0.
                        for combination in combinations(copy_hand, i):
                            if 6 in phazed_group_type(list(combination)):
                                # Player able to make group_1. So, remove the  
                                # cards of group_1 from `copy_hand`
                                group_1 = list(combination)
                                for j in group_1:
                                    copy_hand.remove(j)
                                break
                        if group_1:
                            break
                                                        
                    if group_1:
                        # Check after removing cards of group_1 does still  
                        # player can get score of atleast 34.
                        score_list2 = ([VALUES[card[VALUE]] 
                                        for card in copy_hand])
                        
                        if sum(score_list2) >= 34:
                            for i in range(len(copy_hand)):
                                i += 1
                                for x in combinations(copy_hand, i):
                                    if 6 in phazed_group_type(list(x)):
                                        group_2 = list(x)
                                        break
                                if group_2:
                                    break
                                
                    if group_1 and group_2:
                        # Check if player can play phase type 3 according to 
                        # the ongoing situation of hand.
                        play = (3, (3, [group_1, group_2]))
                        if phazed_is_valid_play(play, player_id, table, 
                                                turn_history, phase_status, 
                                                hand, discard):
                            return play
            
            # Check if player can play phase type 4.
            elif required_phase == 4:
                if len(hand) >= 8: 
                    copy_hand = hand.copy()
                    hand_sorted = sorted(copy_hand)
                    group_1 = []  # 4 cards of the same value.
                    group_2 = []  # 4 cards of the same value.
                    
                    # Check if player can get 4 cards of the same value from
                    # `hand_sorted`.
                    for combination in combinations(hand_sorted, 4):
                        if 3 in phazed_group_type(list(combination)):
                            group_1 = list(combination)
                            # Player able to create `group_1`. So, remove cards
                            # of group_1 from `hand_sorted`.
                            for i in group_1:
                                hand_sorted.remove(i)
                            break
                            
                    if group_1:
                        if len(hand_sorted) >= 4:
                            # Check if player can get 4 cards of same value.
                            for combination in combinations(hand_sorted, 4):
                                if 3 in phazed_group_type(list(combination)):
                                    group_2 = list(combination)
                                    break
                
                    if group_1 and group_2:
                        # Check if player can play phase type 4 on the ongoing
                        # condition of the hand.
                        play = (3, (4, [group_1, group_2]))
                        if phazed_is_valid_play(play, player_id, table, 
                                                turn_history, phase_status, 
                                                hand, discard):
                            return play
            
            # Check if player can play phase type 5.
            elif required_phase == 5:
                if len(hand) >= 8:  
                    copy_hand = hand.copy()
                    hand_sorted = sorted(copy_hand)
                    group_1 = []  # One run of eight cards.
                    
                    # Check if player can get a run of 8 cards from 
                    # `hand_sorted`.
                    for combination in combinations(hand_sorted, 8):
                        if 4 in phazed_group_type(list(combination)):
                            group_1 = list(combination)
                            break
                        
                    if group_1:
                        # Check if player can play phase type 5 on the ongoing
                        # condition of the hand.
                        play = (3, (5, [group_1]))
                        if phazed_is_valid_play(play, player_id, table, 
                                                turn_history, phase_status, 
                                                hand, discard):
                            return play
                        
            # Check if a player can play phase type 6.           
            elif required_phase == 6:
                # `score_list` contains the value of each card in `hand` taken
                # from `VALUES`.
                score_list = [VALUES[card[VALUE]] for card in hand]
                if sum(score_list) >= 68:
                    copy_hand = hand.copy()
                    group_1 = []  # 34 - accumulation of the same colour.
                    group_2 = []  # 34 - accumulation of the same colour.
                    
                    # `range` function helps to check each of the combination 
                    # types starting from  1 to the length of the `hand`.
                    for i in range(len(hand)):
                        i += 1  # To avoid staring from 0.
                        for combination in combinations(copy_hand, i):
                            if 7 in phazed_group_type(list(combination)):
                                group_1 = list(combination)
                                # Player able to make group_1. So, remove the 
                                # cards of group_1 from copy_hand.
                                for j in group_1:
                                    copy_hand.remove(j)
                                break
                        if group_1:
                            break
                            
                    if group_1:
                        # Check after removing cards of group_1 does still  
                        # player can get score of atleast 34.
                        score_list2 = ([VALUES[card[VALUE]] 
                                        for card in copy_hand])
                        
                        if sum(score_list2) >= 34:
                            for i in range(len(copy_hand)):
                                i += 1
                                for x in combinations(copy_hand, i):
                                    if 7 in phazed_group_type(list(x)):
                                        group_2 = list(x)
                                        break
                                if group_2:
                                    break
                                
                    if group_1 and group_2:
                        # Check if a player can play phase type 6 on the 
                        # ongoing condition of the hand.
                        play = (3, (6, [group_1, group_2]))
                        if phazed_is_valid_play(play, player_id, table, 
                                                turn_history, phase_status, 
                                                hand, discard):
                            return play
                        
            # Check if a player can play phase type 7.
            elif required_phase == 7:
                if len(hand) >= 8:
                    copy_hand = hand.copy()
                    hand_sorted = sorted(copy_hand)
                    group_1 = []  # Run of 4 cards of the same colour.
                    group_2 = []  # Set of 4 cards of the same value.
                    
                    # First try to build up group_2 as it saves some of the 
                    # time.
                    for combination in combinations(hand_sorted, 4):
                        if 3 in phazed_group_type(list(combination)):
                            group_2 = list(combination)
                            # Player able to build up group_2. So, remove cards
                            # of group_2 from `hand_sorted`.
                            for i in group_2:
                                hand_sorted.remove(i)
                            break
                            
                    if group_2:
                        if len(hand_sorted) >= 4:
                            for combination in combinations(hand_sorted, 4):
                                if 5 in phazed_group_type(list(combination)):
                                    group_1 = list(combination)
                                    break
                
                    if group_1 and group_2:
                        # Check if a player can play a phase type 7 according
                        # to ongoing condition of the hand.
                        play = (3, (7, [group_1, group_2]))
                        if phazed_is_valid_play(play, player_id, table, 
                                                turn_history, phase_status, 
                                                hand, discard):
                            return play
                        
        # Check if player has completed its phase so he can play a play type 4.
        if table[player_id] != (None, []):
            players_id = [0, 1, 2, 3]
            
            for i in players_id:
                if table[i] != (None, []):
                    # Avoid playing on accumulation phases.
                    if not((table[i][PHASE_TYPE] == 3 
                            or table[i][PHASE_TYPE] == 6)):
                        
                        for card in hand:
                            # Using 0 index position within group because it 
                            # will also be suitable for runs.
                            play = (4, (card, (i, 0, 0)))
                            # Check if `play` is a valid play according to 
                            # ongoing situation of the hand.
                            if phazed_is_valid_play(play, player_id, table, 
                                                    turn_history, phase_status, 
                                                    hand, discard):
                                return play
                            
                            # If the phase includes a run so a player could 
                            # also play `card` at the end of the first group.
                            if (table[i][PHASE_TYPE] == 5 
                                or table[i][PHASE_TYPE] == 7):
                                
                                index = len(table[i][PHASE_CONTENT][0])
                                play2 = (4, (card, (i, 0, index)))
                                # Check if `play2` is a valid play according to 
                                # ongoing condition of the hand.
                                if phazed_is_valid_play(play2, player_id, 
                                                        table, turn_history, 
                                                        phase_status, 
                                                        hand, discard):
                                    return play2
                            
                            # If phase contains two groups and player unable to
                            # play on first group. So, check if he can play on
                            # second group.
                            if len(table[i][PHASE_CONTENT]) == 2:
                                play3 = (4, (card, (i, 1, 0)))
                                # Check if `play3` is a valid play according to 
                                # ongoing situation of the hand.
                                if phazed_is_valid_play(play3, player_id, 
                                                        table, turn_history, 
                                                        phase_status, 
                                                        hand, discard):
                                    return play3
                            
                        
        # Helps to decrease score at the end of the hand. If unable to 
        # to complete phases. So, upto certain extent avoids picking up aces
        # from discard.
        elif (table[player_id] != (None, []) or phase_status[player_id] != 1 
              or phase_status[player_id] != 3 or phase_status[player_id] != 0):
            
            card_ace_in_hand = ace_card(hand)
            if card_ace_in_hand:
                return (5, card_ace_in_hand)
            
        # Using `max_value_card`, player removes the card of larger value
        # except wild cards.
        if hand:
            discarded_card = max_value_card(hand)
            return (5, discarded_card)
            
    # Turn history is empty so player starts just by picking up the card from
    # the deck or discard pile.
    else:
        # To some extent picks up the ace card which might help completing 
        # some of the phases.
        if not((phase_status[player_id] != 0 or phase_status[player_id] != 1
                or phase_status[player_id]  != 3)):
            
            if discard[VALUE] == 'A':
                return (2, discard)
            
        return (1, None)

    
if __name__ == '__main__':
    # Example call to the function.
    print(phazed_play(1, [(None, []), (4, [['2C', '3H', '4D', 'AD', '6S', '7C',
      '8S', '9H', '0S', 'JS']]), (None, []), (None, [])], [(0, [(2, 'JS'),
      (5, 'JS')]), (1, [(2, 'JS'), (3, (4, [['2C', '3H', '4D', 'AD', '6S',
      '7C', '8S', '9H']])), (4, ('0S', (1, 0, 8))), (4, ('JS',
      (1, 0, 9)))])], [0, 4, 0, 0], ['5D'], '7H'))
