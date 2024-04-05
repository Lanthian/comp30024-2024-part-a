# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part A: Single Player Tetress

from queue import LifoQueue

class PriorityDict:
    items: dict[int, LifoQueue]={}
    size: int=0

    def put(self, priority, item):
        if priority not in self.items.keys():
            # No items of priority yet, create listing
            self.items[priority] = LifoQueue()
        self.items[priority].put(item)
        self.size += 1
        # PriorityQueue.put(self.items[priority], item)

    def get(self):
        k = list(self.items.keys())
        if len(k) == 0:
            # No items as of current
            return None
        smallest = min(k)
        
        t = self.items[smallest].get()
        if self.items[smallest].empty():
            del self.items[smallest]
        
        self.size -= 1
        return t
    
    def empty(self) -> bool:
        return len(list(self.items.keys())) == 0
    