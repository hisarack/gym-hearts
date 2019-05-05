from gymhearts import strategy


class FirstPlayStrategy(strategy.IStrategy):

    def move(self, observation):
        action = observation['valid_hand_cards'][0]
        return action
