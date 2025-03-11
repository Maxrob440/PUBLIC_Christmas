class mode:
    def __init__(self):
        self.mode = ['photos','minutes_until_train',None]
    def enqueue(self, mode):
        self.mode.append(mode)
    def dequeue(self):
        return self.mode.pop(0)
    def change_mode(self):
        self.enqueue('photos')
        self.dequeue()
    def set_mode(self,mode):
        while self.mode[0] != mode:
            self.enqueue(mode)
            self.dequeue()
    def get_mode(self):
        return self.mode[0]