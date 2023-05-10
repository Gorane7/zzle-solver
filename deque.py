


class Deque:
    def __init__(self):
        self.s_in = []
        self.s_out = []
    
    def add(self, val):
        self.s_in.append(val)
    
    def get(self):
        if not self.s_out:
            while self.s_in:
                self.s_out.append(self.s_in.pop())
        return self.s_out.pop()

    def size(self):
        return len(self.s_in) + len(self.s_out)