from abc import ABC


class IStrategy(ABC):
    name = "strategy"

    def main(self):
        self.on_init()
        while True:
            self.on_tick()
            self.on_time()

    def on_init(self):
        raise NotImplementedError()

    def on_tick(self):
        raise NotImplementedError()

    def on_time(self):
        pass

    def __on_time_trigger__(self):
        pass
