class Mark:
    pass

class Stack:
    def __init__(self):
        self._list = list()

    def push(self, val):
        self._list.append(val)
        
    def pop(self):
        return self._list.pop()

    def swap(self):
        one = self._list.pop()
        two = self._list.pop()
        self._list.append(one)
        self._list.append(two)

    def drop(self):
        self._list.pop()

    def dup(self):
        one = self._list.pop()
        self._list.append(one)
        self._list.append(one)

    def rot3(self):
        one = self._list.pop()
        two = self._list.pop()
        three = self._list.pop()
        self._list.append(one)
        self._list.append(three)
        self._list.append(two)

    def mark(self):
        self._list.append(Mark)

    def array(self):
        result = list()
        while True:
            item = self._list.pop()
            if item == Mark:
                break
            result.append(item)
        result.reverse()
        return result

    def print_last(self):
        value = self._list[-1]
        print(str(value))

    def print_all(self):
        for each in self._list:
            print(str(each))

    def dump(self):
        return self._list
