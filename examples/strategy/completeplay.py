from gymhearts import strategy
from gymhearts.evaluator import Evaluator

from treys import Card

# Focus on do not loose current trick when we are last player
# and play smallest card if we are not last player.
# optimize the rule if we can not win current trick or do not get punish score, drop the worst card
class CompletePlayStrategy(strategy.IStrategy):

    def __init__(self, first_action_card=None):
        self._evaluator = Evaluator()
        self._first_action_card = first_action_card

    def move(self, observation):

        # for Lookaheadplaystrategy
        if self._first_action_card is not None:
            first_action_card = self._first_action_card
            self._first_action_card = None
            return first_action_card

        number_of_playing_ids = len(observation['playing_ids'])
        valid_hand_cards = observation['valid_hand_cards']
        playing_cards = observation['playing_cards']
        valid_hand_ranks = [Card.get_rank_int(c) for c in valid_hand_cards]
        min_card_id = valid_hand_ranks.index(min(valid_hand_ranks))
        max_card_id = valid_hand_ranks.index(max(valid_hand_ranks))

        # if i am last player in this trick
        if number_of_playing_ids == observation['number_of_players']-1:
            first_suit = Card.get_suit_int(playing_cards[0])
            competitor_ranks = [Card.get_rank_int(c) for c in playing_cards if Card.get_suit_int(c) == first_suit]
            max_suit = Card.get_suit_int(valid_hand_cards[max_card_id])
            punish_score = self._evaluator.calculate_score(playing_cards)
            # we do not have same suit card, so just drop max card. it does not get punish score
            if (max_suit != first_suit) or (punish_score == 0):
                return valid_hand_cards[max_card_id]
            # we will be the looser in this round, so just drop max card.
            elif valid_hand_ranks[min_card_id] > max(competitor_ranks):
                return valid_hand_cards[max_card_id]
            # drop the card which is not larger then biggest playing card.
            else:
                max_safe_card_id = min_card_id
                max_safe_rank = valid_hand_ranks[min_card_id]
                max_competitor_ranks = max(competitor_ranks)
                for tmp_card_id, r in enumerate(valid_hand_ranks):
                    if (r < max_competitor_ranks) and (r > max_safe_rank):
                        max_safe_rank = r
                        max_safe_card_id = tmp_card_id
                return valid_hand_cards[max_safe_card_id]
        # otherwise
        else:
            return valid_hand_cards[min_card_id]



