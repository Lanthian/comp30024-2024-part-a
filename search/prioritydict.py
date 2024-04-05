from queue import PriorityQueue, LifoQueue

class PriorityDict():
    items: dict[int, LifoQueue]

    def put(self, priority, item):
        if priority not in self.items.keys():
            # No items of priority yet, create listing
            self.items[priority] = PriorityQueue
        PriorityQueue.put(self.items[priority], item)

    def get(self):
        k = list(self.items.keys())
        if len(k) == 0:
            # No items as of current
            return None
        smallest = min(k)
        
        t = self.items[smallest].get()
        if self.items[smallest].empty():
            self.items[smallest].pop()
        return t

x = PriorityDict()
x.items = {}
x.put(2,"first")
x.put(1,"second")
print(x.get())
