
class Player(object):

    def __init__(self, player_id, strategy):
        self._player_id = player_id
        self._score = 0
        self._strategy = strategy
        self._hand_cards = []
    
    def reset(self, cards):
        self._score = 0
        self._hand_cards = cards

    def reset_hand_cards(self, cards):
        self._hand_cards = cards

    def remove_hand_card(self, action_card):
        if action_card in self._hand_cards:
            self._hand_cards.remove(action_card)
        else:
            print("Error! action card not in the hand cards")

    def move(self, observation):
        action = self._strategy.move(observation)
        return action

    def add_score(self, score):
        self._score += score

    def get_hand_cards(self):
        return self._hand_cards

    def get_score(self):
        return self._score
