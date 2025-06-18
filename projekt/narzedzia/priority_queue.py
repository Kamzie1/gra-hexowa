class priority_queue:
    def __init__(self) -> None:
        self.queue = []

    def append(self, value):
        self.queue.append(value)

    def pop(self):
        maks = (-2, -2, -2)
        for element in self.queue:
            if element[2] > maks[2]:
                maks = element
        self.queue.remove(maks)
        return maks

    def empty(self) -> bool:
        return len(self.queue) == 0

    def __str__(self):
        r = ""
        for element in self.queue:
            r += str(element) + ", "
        return r
