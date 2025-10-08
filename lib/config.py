import json


# simple config class. basically just boilerplate in case i change my mind about something in the future
class Config:
    def __init__(self, path):
        self.path = path

        with open(self.path, "r") as file:
            self.data = json.loads(file.read())

    def get(self, key):
        if "." in key:
            arr = key.split(".")
            last_element = self.data
            element = self.data[arr[0]]
            for idk, k in enumerate(arr):
                if idk == 0:
                    continue
                last_element = element
                element = last_element[k]
            return element
        else:
            return self.data[key]

    def set(self, key, value):
        self.data[key] = value

    def save(self):
        with open(self.path, "w") as file:
            file.write(json.dumps(self.data))
