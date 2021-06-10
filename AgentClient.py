import random


def check_album(album, minprice, maxprice, priorities):
    checksum = 0
    if float(maxprice) >= float(album.price) >= float(minprice):
        checksum += 1

    # if priorities[0] == 'Niski':
    #     checksum += 1
    # elif priorities[0] == 'Średni' and (album.lengthmatch[1] == 3 or album.lengthmatch[1] == 2):
    #     checksum += 1
    # elif priorities[0] == 'Wysoki' and album.lengthmatch[2] == 3:
    #     checksum += 1

    if checksum == 1:
        return 1
    else:
        return 0


class AgentClient:
    def __init__(self, name):
        self.name = name
        self.albums_to_return = []

    def return_album(self, data_sets, minprice, maxprice, agents_seller, out_queue):
        accepted = 0
        album = 0
        i = 0

        parameters = []
        for par in data_sets:
            parameters.append(par.array)

        priorities = []
        for prio in data_sets:
            priorities.append(prio.priority)

        while accepted == 0 and i <= len(agents_seller):
            random_index = random.randint(0, len(agents_seller) - 1)
            if agents_seller[random_index].busy == 0:
                any_found = agents_seller[random_index].init_return(parameters)
                print(any_found)
                if any_found is None:
                    out_queue.put(None)
                    break
                while accepted == 0:
                    album = agents_seller[random_index].return_albums(0)
                    if album == 0 or album is None:
                        album = agents_seller[random_index].return_albums(1)
                        # print("Nie zwrocono albumu")
                        break
                    if album != 0 and album is not None:
                        accepted = check_album(album, minprice, maxprice, priorities)
                if accepted == 1 and album != 0:
                    self.albums_to_return.append(album)
                    # print(agents_seller[random_index].name, album.name, sep=" : ")
                i += 1
        if not self.albums_to_return:
            return None
        else:
            self.choose_album(out_queue)

    def choose_album(self, out_queue):
        out_queue.put(self.albums_to_return[0])
        return self.albums_to_return[0]
