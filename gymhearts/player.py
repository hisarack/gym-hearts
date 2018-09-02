
class Player(object):

    def __init__(self, player_id, strategy):
        self._player_id = player_id
        self._score = 0
        self._strategy = strategy
        self._hand_cards = []
        self._round_scores = []
    
    def reset(self, cards):
        self._score = 0
        self._hand_cards = cards
        self._round_scores = []

    def reset_hand_cards(self, cards):
        self._hand_cards = cards

    def remove_hand_card(self, action_card):
        if action_card in self._hand_cards:
            self._hand_cards.remove(action_card)
        else:
            raise Exception("Error! action card not in the hand cards")

    def _watch(self, observation, info):
        try:
            self._strategy.watch(observation, info)
        except NotImplementedError:
            pass

    def move(self, observation):
        action = self._strategy.move(observation)
        return action

    def add_score(self, score):
        self._score += score

    def get_hand_cards(self, is_sorted=False):
        if is_sorted is False:
            return self._hand_cards
        else:
            suitrank_ints = [c & 0xFF00 for c in self._hand_cards]
            sorted_indices = sorted(range(len(suitrank_ints)), key=lambda k: suitrank_ints[k])
            sorted_cards = [self._hand_cards[ind] for ind in sorted_indices]
            return sorted_cards

    def get_score(self):
        return self._score

    def commit_new_round_score(self):
        self._round_scores.append(self._score)

    def get_uncommited_score(self):
        if len(self._round_scores) == 0:
            return self._score
        else:
            return self._score - self._round_scores[-1]

    def rollback_to_last_commited_score(self):
        if len(self._round_scores) == 0:
            self._score = 0
        else:
            self._score = self._round_scores[-1]
