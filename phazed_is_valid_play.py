from phazed_group_type import (valid_run_of_cards, same_colour,
same_colour_for_accumulation, atleast_2_natural_cards, phazed_group_type)
from phazed_phase_type import (phazed_phase_type)

VALUE = 0
SUIT = COLOUR = 1
RED_COLOUR = 'HD'
BLACK_COLOUR = 'SC'
VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, 
          '9': 9, '0': 10, 'J': 11, 'Q': 12, 'K': 13}
PLAY_TYPE = 0
PLAY_CONTENT = 1
PHASE_TYPE = 0
PHASE_CONTENT = 1
CARD_TYPE = 0
ACCUMULATION_BUILD_UP = [55, 68, 76, 81, 84, 86, 87, 88]

# Constants related to `turn_history`
LAST_TURN = -1
PLAYER_ID = 0
TURN_CONTENT = -1
PLAY_TYPE = 0
PLAY_CONTENT = 1

def building_accumulation(list_of_group, card, hand):
    """ Returns False if the card added to the `list_of_group` donot build up
    on the accumulation in a correct manner that is either if `hand` contains
    one card only so `card` played donot complete the accumulation or the
    the build up play is not in additive sequence, otherwise True."""
    
    # `prev_group_sum` is a sum of the values of cards in `list_of_group`. 
    # Values of cards are taken from dictionary `VALUES`.
    prev_group_sum = sum(([VALUES[i[VALUE]] for i in list_of_group]))                
    new_group = list_of_group.copy()
    new_group.append(card) 
    # `new_group_sum` is a sum of the values of cards in `list_of_group` plus 
    # the sum of the value of the card played.
    new_group_sum = sum([VALUES[i[VALUE]] for i in new_group])
                
    # Player attempting to play a card has only one card left in `hand`, so, 
    # returns False if accumulation not completes.
    if len(hand) == 1:
        if not (new_group_sum in ACCUMULATION_BUILD_UP):
            return False
    else:
        # Assigns the value to `accumulation_buildup` to which a player is 
        # attempting to build up the accumulation.
        accumulation_buildup = 0
        for i in ACCUMULATION_BUILD_UP:
            if prev_group_sum < i:
                accumulation_buildup = i
                break
        # Returns False if the card attempted to be added in a group donot 
        # build accumulation to the next value in the additive sequence.
        if VALUES[card[VALUE]] > accumulation_buildup - prev_group_sum:
            return False
    return True
    

def card_from_deck_or_discard(turn_history, player_id):
    """It takes the list `turn_history` as an argument and returns False if the 
    last element  donot contain a tuple indicating the play type 1 or 2 played 
    by a person who is attempting to play the play type other than 1 or 2."""
    
    # A base case when the turn history is empty and person attempting to play
    # a phase is the very first person and have not picked up a card from a 
    # deck or discard pile.
    if not turn_history:
        return False
    # Returns False if player has not completed any of the play in his turn.
    elif turn_history[LAST_TURN][PLAYER_ID] != player_id:
        return False
    
    # `play_type_in_turn` is id of the first play type made by a recent player
    # in `turn_history`.
    play_type_in_turn = turn_history[LAST_TURN][TURN_CONTENT][0][PLAY_TYPE]
    
    # Return False if a player attempting to play a play type other than 1 or 2
    # play type has not picked up a card from a discard pile or deck.
    if (play_type_in_turn != 1) and (play_type_in_turn != 2):
        return False
    else:
        return True
    

def phazed_is_valid_play(play, player_id, table, turn_history, phase_status, 
                         hand, discard):
    """It takes a 2-tuple for `play` which itself indicates the play type and 
    the content of the play respectively. For `player_id` it takes integer 
    number indicating the id of the player attempting to play. For `table` it 
    takes a 4-element list in which each element represents a phase played by
    each player in the current hand. For `turn_history` it takes a list of all 
    turns in the hand to date that is based on the sequence of the play. For 
    `phase_status` it takes the 4-element list in which each element repesents 
    the phases each players 0-3 have achieved respectively in game. For `hand` 
    it take a list of cards that a current player holds i.e. player with id 
    number `player_id`. For discard it takes the 2-element string which 
    represents the card at the top of discard pile. Function returns `True`if 
    `play` is valid according to the current hand state, otherwise, `False`."""

    if not play:
        return False
    
    else:
        # Pick up play from discard pile (a type 1 play).
        if play[PLAY_TYPE] == 1:
            # Returns False if the `turn_history` is not empty and the player
            # attempting to pick up a a card from discard pile was not actually
            # the first play of his turn.
            if turn_history:
                if turn_history[LAST_TURN][PLAYER_ID] == player_id:
                    return False
            # Return False if player attempting to pick up a card from discard 
            # pile donot matches to the actual card on the discard pile.
            elif play[PLAY_CONTENT] != discard:
                return False
        
        # Pick up play from the deck (a type 2 play).
        elif play[PLAY_TYPE] == 2:
            # Returns False if the `turn-history` is not empty and player 
            # attempting to pick up a card from a deck was not actually the
            # first play of his turn.
            if turn_history:
                if turn_history[LAST_TURN][PLAYER_ID] == player_id:
                    return False
            
        # Placing a phase to the table from the players hand. (a type 3 play).
        elif play[PLAY_TYPE] == 3:
            
            # Return False if a player attempting to play a phase have already
            # played a phase in a ongoing hand.
            if table[player_id] != (None, []):
                return False
            
            content_play = play[PLAY_CONTENT]
            phase_id = content_play[PHASE_TYPE]  # based on IDs from Q2.
            phase_content = content_play[PHASE_CONTENT]
            phases_achieved = phase_status[player_id]
            
            # Returns False if the turn history was empty and so player cannot
            # initiate the play type 3 beacuse we are right at the beginning
            # of the game
            if not turn_history:
                return False
            
            # Returns False if player attempting to play a phase has not 
            # completed any of the individual play in the turn.
            elif turn_history[LAST_TURN][PLAYER_ID] != player_id:
                return False
            
            # `play_type_id` is id of the recent play type from `turn_history`.
            play_type_id = turn_history[LAST_TURN][TURN_CONTENT][-1][PLAY_TYPE]
            hand_copy = hand.copy()
            
            # Return False if a plyer attempting to play a phase have not
            # picked up a card from a discard pile or deck.
            if play_type_id != 1 and play_type_id != 2:
                return False
            
            # Return False if the phase play is not the phase type that the 
            # player is required to play for the current hand.
            elif phase_id != (phases_achieved + 1):
                return False
            
            # Return False if the phase play donot matches the declared phase
            # type.
            elif not (phase_id in phazed_phase_type(phase_content)):
                return False

            # Assuming phase contains only a single group. It returns False,
            # if any of the card in phase played was not present in `hand`.
            elif len(phase_content) == 1:
                for i in phase_content[0]:
                    if i in hand_copy:
                        hand_copy.remove(i)
                    else:
                        return False
                    
            # Assuming phase contains two groups. It returns False, if any of 
            # the card attempted to play in a phase was not present in `hand`.
            elif len(phase_content) == 2:
                total_cards_in_phase = phase_content[0] + phase_content[1]
                for i in total_cards_in_phase:
                    if i in hand_copy:
                        hand_copy.remove(i)
                    else:
                        False
                        
        # Attempting to place a single card from the player's hand to a phase 
        # on the table. (a play type 4).              
        elif play[PLAY_TYPE] == 4:
           
            content_play = play[PLAY_CONTENT]
            card = content_play[0]
            position_tuple = content_play[1]
            group_of_player_id = position_tuple[0]
            
            # Player attemptimg to play a card on the table to particular
            # player who have not completed a phase yet.
            if table[group_of_player_id] == (None, []):
                return False
            
            group_index = position_tuple[1]
            # Index at which card is to be inserted in a group.
            inside_group_index = position_tuple[-1]
            # `phase_played` is a phase on which `card` is to be played.
            phase_played = table[group_of_player_id]
            phase_type = phase_played[PHASE_TYPE]
            phase_content = phase_played[PHASE_CONTENT]
            
            # Return False as player attemptimg to play a card on the group 
            # that donot exist.
            if group_index >= len(phase_content):
                return False
            
            phase_content_copy = phase_content.copy()
            # It is the group list on which `card` has to be played.
            group_on_card_played = phase_content_copy[group_index]
            
            if not (card in hand):
                return False
            
            # Return False as player attempting to play a card on a group has 
            # not completed a phase yet.
            elif table[player_id] == (None, []):
                return False
            
            # Return False as player attempting to play a card on a group has 
            # not picked up a card from a deck or discard pile.
            elif not(card_from_deck_or_discard(turn_history, player_id)):
                return False
            
            # Index at which `card` is to be played on a group is not 
            # appropriate.
            elif inside_group_index > len(group_on_card_played):
                return False
            
            # Assigns the value and suit of the first natural card in a 
            # `group_on_card_played` to the `group_value` and `group_suit`
            # respectively.
            group_value = 0
            group_suit = 0
            for i in group_on_card_played:
                if i[VALUE] != 'A':
                    group_value = i[VALUE]
                    group_suit = i[SUIT]
                    break
            group_colour = group_suit
                    
            # Returns False if player attempts to play a `card` on a selected 
            # group on the table donot have the same value as a value of group.
            if phase_type == 1 or phase_type == 4: 
                if group_value != card[VALUE] and ('A' != card[VALUE]):
                    return False
            
            # Returns False if player attempts to play a `card` on a selected 
            # group on the table that donot have the same suit.
            elif phase_type == 2:
                if group_suit != card[SUIT] and ('A' != card[VALUE]):
                    return False
                
            # Return False if the index at which card to be inserted in 
            # group is not the 0 or ending index i.e. breaks the run.   
            elif phase_type == 5:
                if not ((inside_group_index == 0 
                         or inside_group_index == len(group_on_card_played))):
                    return False
                
                # Group is already made up of 12 cards so no further card can 
                # be added to build up a run.
                elif len(group_on_card_played) >= 12:
                    return False
                
                # Return False if playing a card at index 0 breaks the run.
                if inside_group_index == 0:
                    group_copy = group_on_card_played.copy()
                    group_copy.insert(0, card)
                    if not (4 in phazed_group_type(group_copy[:9])):
                        return False
                
                # Return False if playing a card at the end of the group breaks
                # the run.
                if inside_group_index == len(group_on_card_played):
                    group_copy = group_on_card_played.copy()
                    group_copy.insert(len(group_on_card_played), card)
                    starting_index = len(group_copy) - 8
                    ending_index = len(group_copy) 
                    new_group1 = group_copy[starting_index:ending_index]
                    if not (4 in phazed_group_type(new_group1)):
                        return False
                
            elif phase_type == 7:
                # Return False if the card donot matches with group colour on
                # which it has to be played and is not consistent with the run.
                if group_index == 0:
                    # Return False if `card` colour donot matches with group
                    # colour.
                    if group_colour in RED_COLOUR:
                        if not ((card[COLOUR] in RED_COLOUR) 
                                or card[VALUE] == 'A'):
                            return False
                    if group_colour in BLACK_COLOUR:
                        if not ((card[COLOUR] in BLACK_COLOUR) 
                                or card[VALUE] == 'A'):
                            return False
                    # Return False if the index at which card to be inserted in 
                    # group is not the 0 or ending index i.e. breaks the run.    
                    elif not ((inside_group_index == 0 
                               or (inside_group_index 
                                   == len(group_on_card_played)))):
                        return False
                    # Return False if run in a group already have 12 cards.
                    elif len(group_on_card_played) >= 12:
                        return False
                    
                    # Return False if playing a card at index 0 breaks the run.
                    if inside_group_index == 0:
                        group_copy = group_on_card_played.copy()
                        group_copy.insert(0, card)
                        if not (5 in phazed_group_type(group_copy[:5])):
                            return False
                        
                    # Return False if playing a card at the end of the group
                    # breaks the run.
                    if inside_group_index == len(group_on_card_played):
                        group_copy = group_on_card_played.copy()
                        group_copy.insert(len(group_on_card_played), card)
                        starting_index = len(group_copy) - 4
                        ending_index = len(group_copy) 
                        new_group1 = group_copy[starting_index:ending_index]
                        if not (5 in phazed_group_type(new_group1)):
                            return False
                    
                # Return False if the card to be played donot matches the 
                # 'group_value`
                elif group_index == 1:
                        if group_value != card[VALUE] and ('A' != card[VALUE]):
                            return False
                    
            elif phase_type == 3:
                # Return False if `card` is not consistent with accumulation.
                if not (building_accumulation(group_on_card_played, card, 
                                              hand)):
                    return False
                                    
            elif phase_type == 6:
                # Return False if `card` colour donot matches with accumulation
                # colour.
                if card[COLOUR] != group_on_card_played[0][COLOUR]:
                    return False
                # Return False if `card` is not consistent with accumulation.
                elif not (building_accumulation(group_on_card_played, 
                                                card, hand)):
                    return False
                
        # Attempting to discard a single card from a player's hand 
        # (play type 5).
        elif play[PLAY_TYPE] == 5:
            card = play[PLAY_CONTENT]
            if not(card in hand):
                return False
            
            # Return False if the turn_history is empty means that person 
            # cannot play the play type 5 because we are at the very beginning
            # of the game.
            if not turn_history:
                return False
            
            # Returns False if a person have not yet picked up a card from a 
            # deck or discard.
            if turn_history[LAST_TURN][PLAYER_ID] != player_id:
                return False
                                    
            all_recent_plays_in_turn = turn_history[LAST_TURN][TURN_CONTENT]
            recent_play = all_recent_plays_in_turn[-1]
            recent_play_type = recent_play[PLAY_TYPE]
            recent_play_content = recent_play[PLAY_CONTENT]
            
            # Returns False if person have already discarded a card.
            if recent_play_type == 5:
                return False
            
            if recent_play_type == 4:
                # `tuple_position` is a tuple from a most recent play in the 
                # in the turn in which player was building on accumulation.
                tuple_position = recent_play_content[-1]
                # id of the `table` on which player was recently building on 
                # accumulation.
                id_table = tuple_position[0]
                table_content = table[id_table]
                phase_type = table_content[PHASE_TYPE]
                
                if phase_type == 3 or phase_type == 6:
                    
                    # Index of group on which accumulation have been build up.
                    group_index_on_table = tuple_position[1]
                    phase_content = table_content[PHASE_CONTENT]
                    # Group on which recent accumulations has been played.
                    group_on_table = phase_content[group_index_on_table]
                
                    group_on_table_sum = sum(([VALUES[i[VALUE]] 
                                               for i in group_on_table]))
                
                    if not(group_on_table_sum in ACCUMULATION_BUILD_UP):
                        return False
                
    return True
        
             
if __name__ == '__main__':
    # Example calls to the function.
    print(phazed_is_valid_play((3, (1, [['2S', '2S', '2C'],
        ['AS', '5S', '5S']])), 0, [(None, []), (None, []),
        (None, []), (None, [])], [(0, [(2, 'JS')])],
        [0, 0, 0, 0], ['AS', '2S', '2S', '2C', '5S', '5S',
                       '7S', '8S', '9S', '0S', 'JS'], None))
    print(phazed_is_valid_play((4, ('KC', (1, 0, 0))),
        1, [(None, []), (2, [['2S', '2S', 'AS', '5S',
        '5S', '7S', 'JS']]), (None, []), (None, [])],
        [(0, [(2, 'JS'), (5, 'JS')]), (1, [(1, 'XX'),
        (3, [['2S', '2S', 'AS', '5S', '5S', '7S', 'JS']])])],
        [0, 2, 0, 0], ['5D', '0S', 'JS', 'KC'], '0H'))
    print(phazed_is_valid_play((5, 'JS'), 1, [(None, []),
        (1, [['2S', '2S', '2C'], ['AS', '5S', '5S']]),
        (None, []), (None, [])], [(0, [(2, 'JS'),
        (5, 'JS')]), (1, [(1, 'XX'), (3, [['2S', '2S',
        '2C'], ['AS', '5S', '5S']])])], [0, 1, 0, 0],
        ['AD', '8S', '9S', '0S', 'JS'], '3C'))
