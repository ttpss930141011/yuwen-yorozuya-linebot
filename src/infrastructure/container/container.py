class Container:
    def __init__(self):
        self._dependencies = {}

    def register(self, key, dependency):
        self._dependencies[key] = dependency

    def resolve(self, key):
        return self._dependencies[key]

    def __getitem__(self, key):
        return self.resolve(key)

    def __setitem__(self, key, dependency):
        self.register(key, dependency)
