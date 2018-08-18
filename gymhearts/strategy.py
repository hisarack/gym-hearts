
class IStrategy(object):

    def move(self, observation):
        raise NotImplementedError()

    def watch(self, observation, info):
        raise NotImplementedError()
