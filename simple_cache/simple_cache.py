# encoding=utf-8

from collections import OrderedDict


class SimpleCache(object):

    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key in self.cache:
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        else:
            return None

    def put(self, key, value):
        if len(self.cache) >= self.capacity:  # 移除最老的数据
            self.cache.popitem(last=False)

        if key in self.cache:
            self.cache.pop(key)
        self.cache[key] = value


lru_cache = SimpleCache(50)


if __name__ == '__main__':
    lru = SimpleCache(3)
    lru.put('a', 1)
    lru.put('b', 1)
    lru.put('c', 1)
    lru.put('d', 1)
    lru.put('e', 1)
    lru.put('f', 1)

    data = lru.cache
    for k, v in data.items():
        print k, v

    lru.get('d')
    for k, v in data.items():
        print k, v

