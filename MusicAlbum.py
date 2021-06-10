import datetime


class Album:
    def __init__(self, name, artist, date, length, albumformat, price, atmospheresmatch, languagesmatch, nationmatch,
                 occassionsmatch, quantity):
        self.name = name
        self.artist = artist
        self.date = date
        self.length = length
        self.albumformat = albumformat
        self.price = price

        self.atmospheresmatch = atmospheresmatch
        self.languagesmatch = languagesmatch
        self.nationmatch = nationmatch
        self.occassionsmatch = occassionsmatch

        self.quantity = quantity

        if length <= 15:
            self.lengthmatch = [3, 0, 0]
        elif 15 < length <= 30:
            self.lengthmatch = [2, 1, 0]
        elif 30 < length <= 45:
            self.lengthmatch = [1, 2, 1]
        elif 45 < length <= 60:
            self.lengthmatch = [0, 3, 2]
        elif 60 < length <= 75:
            self.lengthmatch = [0, 2, 3]
        elif length > 75:
            self.lengthmatch = [0, 1, 3]

        nodays = ((datetime.datetime.now() - self.date).days / 365)
        if nodays >= 51:
            self.yearsmatch = [3, 0, 0]
        elif 51 > nodays >= 31:
            self.yearsmatch = [2, 1, 0]
        elif 31 > nodays >= 21:
            self.yearsmatch = [1, 2, 1]
        elif 21 > nodays >= 11:
            self.yearsmatch = [0, 3, 2]
        elif 11 > nodays >= 1:
            self.yearsmatch = [0, 2, 3]
        elif nodays < 1:
            self.yearsmatch = [0, 1, 3]
