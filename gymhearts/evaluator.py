
from treys.card import Card


class Evaluator(object):

    SPADES_QUEEN = Card.new('Qs')   

    def __init__(self):
        pass
        
    def calculate_score(self, cards):
        suits = [Card.get_suit_int(c) for c in cards]
        score = suits.count(Card.CHAR_SUIT_TO_INT_SUIT['h'])
        if Evaluator.SPADES_QUEEN in cards:
            score += 13
        return score

    def identify_looser(self, cards, ids):
        suits = [Card.get_suit_int(c) for c in cards]
        if suits[1:].count(suits[0]) == 0:
            return ids[0]
        first_rank = Card.get_rank_int(cards[0])
        max_rank = first_rank
        max_index = 0
        number_of_cards = len(cards)
        for i in range(1, number_of_cards):
            if suits[i] == suits[0]:
                tmp_rank = Card.get_rank_int(cards[i])
                if tmp_rank > max_rank:
                    max_index = i
                    max_rank = tmp_rank
        return ids[max_index]
                
    def evaluate(self, cards, ids):
        return self.calculate_score(cards), self.identify_looser(cards, ids)

