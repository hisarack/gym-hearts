from gymhearts import strategy

from treys import Card


class LowPlayStrategy(strategy.IStrategy):

    def move(self, observation):
        valid_hand_cards = observation['valid_hand_cards']
        valid_hand_ranks = [Card.get_rank_int(c) for c in valid_hand_cards]
        min_card_id = valid_hand_ranks.index(min(valid_hand_ranks))
        return valid_hand_cards[min_card_id]


