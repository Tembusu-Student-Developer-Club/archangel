class Player():

    def is_valid(self):
        return self.username != "" and self.housenumber != ""

    def separate_args_with_commas(self, *args):
        args = map(lambda x: str(x), args)
        return ",".join(args)

    def to_csv_row(self):
        return self.separate_args_with_commas(self.username, self.playername, self.roomnumber, self.housenumber,
                                              self.faculty, self.genderplayer, self.genderpref, self.yearofstudy,
                                              self.likes, self.dislikes, self.comments)

    def __init__(self, player_data=[], **kwargs):
        self.username = kwargs.get('username')
        self.playername = kwargs.get('playername')
        self.roomnumber = kwargs.get('roomnumber')
        self.housenumber = kwargs.get('housenumber')
        self.faculty = kwargs.get('faculty')
        self.genderplayer = kwargs.get('genderplayer')
        self.genderpref = kwargs.get('genderpref')
        self.yearofstudy = kwargs.get('yearofstudy')
        self.likes = kwargs.get('likes')
        self.dislikes = kwargs.get('dislikes')
        self.comments = kwargs.get('comments')



    def __repr__(self):
        return str(self.username)
