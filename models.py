import json


class Plytoteka:
    def __init__(self):
        try:
            with open("plytoteka.json", "r") as f:
                self.plytoteka = json.load(f)
        except FileNotFoundError:
            self.plytoteka = []

    def all(self):
        return self.plytoteka
    
    def create_id(self):
        id = self.all()[-1]['id'] + 1
        return id

    def get(self, id):
        plyty = [plyty for plyty in self.all() if plyty['id'] == id]
        if plyty:
            return plyty[0]
        return []

    def create(self, data):
        self.plytoteka.append(data)
        self.save_all()

    def save_all(self):
        with open("plytoteka.json", "w") as f:
            json.dump(self.plytoteka, f)

    def update(self, id, data):
        plyty = self.get(id)
        if plyty:
            index = self.plytoteka.index(plyty)
            self.plytoteka[index] = data
            self.save_all()
            return True
        return False

    def delete(self, id):
        plyty = self.get(id)
        if plyty:
            self.plytoteka.remove(plyty)
            self.save_all()
            return True
        return False

plytoteka = Plytoteka()