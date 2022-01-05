class Player():

    def is_valid(self):
        return self.username != "" and self.housenumber != ""

    def separate_args_with_commas(self, player):
        args = map(lambda x: str(x), player)
        return ",".join(args)

    def to_csv_row(self, player_data):
        player = self.generate_row(player_data)
        return self.separate_args_with_commas(player)

    def generate_row(self, player_data):
        player = ()
        for item in player_data:
            attribute_name = list(item.keys())[0].replace("_", "")
            player = player + (self.__dict__[attribute_name],)

        return player

    def __setattr__(self, name, value):
        raise Exception("It is read only!")

    def __init__(self, player_data):
        for entry in player_data:
            key = list(entry.keys())[0]
            value = list(entry.values())[0]
            self.__dict__[key.replace("_", "")] = value

    def __repr__(self):
        return str(self.telegramusername)
