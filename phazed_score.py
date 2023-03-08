SCORES = {'A': 25, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, 
          '9': 9, '0': 10, 'J': 11, 'Q': 12, 'K': 13, 'Z': 15}
VALUE = 0

def phazed_score(hand):
    """It takes the `hand` as list of cards in which each card is represented 
    by 2-element string. It returns the total score of the `hand` as a
    non-negative integer on the basis of dictionary `SCORES` (in the global 
    name space)."""
    
    # Hand is an empty list i.e. player donot have any card left at the end.
    if not hand:
        return 0
    
    # It creates a list `player_score` which contain the score of each card
    # in hand as an element using the dictionary `SCORES`.
    else:
        player_score = [SCORES[card[VALUE]] for card in hand]
        return sum(player_score)

  
if __name__ == '__main__':
    # Example calls to the function.
    print(phazed_score(['9D', '9S', '9D', '0D', '0S', '0D']))
    print(phazed_score(['2D', '9S', 'AD', '0D']))
    print(phazed_score([]))