
class Player(object):

    def __init__(self, player_id, cards):
        self.player_id = player_id
        self.score = 0
        self.hand_cards = cards
    
    def reset(self, cards):
        self.score = 0
        self.hand_cards = cards

    def remove_hand_card(self, action_card):
        if action_card in self.hand_cards:
            self.hand_cards.remove(action_card)
        else:
            print("Error! action card not in the hand cards")

    def add_score(self, score):
        self.score += score

    def get_hand_cards(self):
        return self.hand_cards

    def get_score(self):
        return self.score
