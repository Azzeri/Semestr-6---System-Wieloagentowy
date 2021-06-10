import json
import math
import random
from datetime import datetime
from MusicAlbum import Album


class AgentSeller:
    def __init__(self, name):
        self.name = name
        self.busy = 0
        self.albums = []
        self.albums_to_return = []
        self.read_albums_from_magasine()
        # self.display_data()
        # self.init_albums()

    # TODO - PARAMETERS, ORDERING
    def return_albums(self, is_finished):
        if is_finished == 0:
            if not self.albums_to_return:
                self.finish()
            else:
                album_to_return = self.albums_to_return[0]
                self.albums_to_return.pop(0)
                return album_to_return
        else:
            self.finish()

    def finish(self):
        self.busy = 0
        self.albums_to_return = []
        return 0

    def init_return(self, parameters):
        self.busy = 1
        checksum = 0
        # print(parameters)
        # for album in self.albums:
        #     print(album.lengthmatch[1])
        #     self.albums_to_return.append(album)
        for album in self.albums:
            if parameters[0][0] == "Krótka" and album.lengthmatch[0] != 0:
                checksum += 1
            if parameters[0][0] == "Średnia" and album.lengthmatch[1] != 0:
                checksum += 1
            elif parameters[0][0] == "Długa" and album.lengthmatch[2] != 0:
                checksum += 1

            if parameters[1][0] == "Starsza" and album.yearsmatch[0] != 0:
                checksum += 1
            if parameters[1][0] == "Średnia" and album.yearsmatch[1] != 0:
                checksum += 1
            elif parameters[1][0] == "Nowoczesna" and album.yearsmatch[2] != 0:
                checksum += 1

            if parameters[2][0] == "Polska" and album.nationmatch[0] != 0:
                checksum += 1
            if parameters[2][0] == "Zagraniczna" and album.nationmatch[1] != 0:
                checksum += 1

            # if parameters[4][0] == "Kompakt" and album.albumformat == "Kompakt":
            #     checksum += 1
            # if parameters[4][0] == "Winyl" and album.albumformat == "Winyl":
            #     checksum += 1
            # elif parameters[4][0] == "MP3" and album.albumformat == "MP3":
            #     checksum += 1

            if parameters[6][0] == "polski" and album.languagesmatch[0] != 0:
                checksum += 1
            if parameters[6][0] == "angielski" and album.languagesmatch[1] != 0:
                checksum += 1
            elif parameters[6][0] == "inny" and album.languagesmatch[2] != 0:
                checksum += 1

            atm_checksum = 0
            if 'Smutna' in parameters[3] and album.atmospheresmatch[0] != 0:
                atm_checksum += 1
            if 'Wesoła' in parameters[3] and album.atmospheresmatch[1] != 0:
                atm_checksum += 1
            if 'Lekka' in parameters[3] and album.atmospheresmatch[2] != 0:
                atm_checksum += 1
            if 'Ciężka' in parameters[3] and album.atmospheresmatch[3] != 0:
                atm_checksum += 1
            if 'Relaksacyjna' in parameters[3] and album.atmospheresmatch[4] != 0:
                atm_checksum += 1
            if 'Szybka' in parameters[3] and album.atmospheresmatch[5] != 0:
                atm_checksum += 1
            if 'Podniosła' in parameters[3] and album.atmospheresmatch[6] != 0:
                atm_checksum += 1
            if atm_checksum >= 3:
                checksum += 1

            occ_checksum = 0
            if 'Impreza' in parameters[5] and album.occassionsmatch[0] != 0:
                occ_checksum += 1
            if 'Trening' in parameters[5] and album.occassionsmatch[1] != 0:
                occ_checksum += 1
            if 'Praca' in parameters[5] and album.occassionsmatch[2] != 0:
                occ_checksum += 1
            if 'Rozmowa' in parameters[5] and album.occassionsmatch[3] != 0:
                occ_checksum += 1
            if 'Relaks' in parameters[5] and album.occassionsmatch[4] != 0:
                occ_checksum += 1
            if occ_checksum >= 2:
                checksum += 1

            if checksum == 6:
                # print(album.name, sep=" : ")
                self.albums_to_return.append(album)
                return 1
            else:
                return None

    def read_albums_from_magasine(self):
        with open('Magasine' + self.name + '.json') as json_file:
            data = json.load(json_file)
            for album in data:
                date = datetime.strptime(album['date'], '%Y-%m-%d')
                new_album = Album(album['name'], album['artist'], date,
                                  album['length'], album['albumformat'], album['price'],
                                  album['atmospheresmatch'], album['languagesmatch'], album['nationmatch'],
                                  album['occassionsmatch'], album['quantity'])
                self.albums.append(new_album)

    def init_albums(self):
        with open('MagasineMain.json') as json_file:
            data = json.load(json_file)
            albums_to_return_number = math.floor(len(data) * 0.75)
            albums_quantity_to_return = random.randint(40, 75)
            albums_quantity_yet_returned = 0
            albums_indexes = []
            for _ in range(albums_to_return_number):
                index = random.randint(0, len(data) - 1)
                while index in albums_indexes:
                    index = random.randint(0, len(data) - 1)
                albums_indexes.append(index)

            for i in albums_indexes:
                album = data[i]
                price = round(album['price'] + album['price'] * (random.uniform(0.01, 0.2)), 2)
                quantity = random.randint(1, math.floor(albums_quantity_to_return / 1.5))
                new_album = Album(album['name'], album['artist'], album['date'],
                                  album['length'], album['albumformat'], price,
                                  album['atmospheresmatch'], album['languagesmatch'], album['nationmatch'],
                                  album['occassionsmatch'], quantity)
                self.albums.append(new_album)
                albums_quantity_yet_returned += quantity

            if albums_quantity_yet_returned < albums_quantity_to_return:
                self.albums[0].quantity += albums_quantity_to_return - albums_quantity_yet_returned

        with open('Magasine' + self.name + '.json', 'w') as json_file:
            json_file.write('[')
            i = 1
            for album in self.albums:
                json.dump(album.__dict__, json_file, indent=4)
                if i != len(self.albums):
                    json_file.write(',')
                    i = i + 1
            json_file.write(']')

    def display_data(self):
        for album in self.albums:
            print(album.name, album.albumformat, album.quantity, album.date, album.price, sep=" : ")
