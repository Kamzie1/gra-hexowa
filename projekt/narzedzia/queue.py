class Queue:
    def __init__(self) -> None:
        self.queue = []

    def append(self, value):
        self.queue.append(value)

    def pop(self):
        element = self.queue[0]
        self.queue.remove(element)
        return element

    def empty(self) -> bool:
        return len(self.queue) == 0

    def __str__(self):
        r = ""
        for element in self.queue:
            r += str(element) + ", "
        return r
