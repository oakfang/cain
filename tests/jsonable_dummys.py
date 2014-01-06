__author__ = 'oakfang'


from cain.jsonable import Jsonable


class User(Jsonable):
    __jattrs__ = ["id", "score", "url", "broperties"]

    def __init__(self, uid, score, url, broperties=None):
        self.id = uid
        self.score = score
        self.url = url
        self.broperties = broperties if broperties is not None else []


class Broperty(Jsonable):
    __jattrs__ = ["title", "code"]

    def __init__(self, title, code):
        self.title = title
        self.code = code


class Pack(Jsonable):
    __jattrs__ = ["id", "name", "members"]

    def __init__(self, pid, name, members=None):
        self.id = pid
        self.name = name
        self.members = members if members is not None else []


class Brofeat(Jsonable):
    __jattrs__ = ["id", "title", "description", "worth"]

    def __init__(self, fid, title, description, worth):
        self.id = fid
        self.title = title
        self.description = description
        self.worth = worth


class Category(Jsonable):
    __jattrs__ = ["id", "name", "broperty", "feats"]

    def __init__(self, cid, name, broperty, feats):
        self.id = cid
        self.name = name
        self.broperty = broperty
        self.feats = feats


PACKS = [Pack(1,
              "Black",
              [User(5,
                    43,
                    'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-prn1/c43.42.525.525/s160x160/59918_10201661866087235_2088536012_n.jpg'),
               User(4,
                    20,
                    'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-frc3/c127.37.466.466/s160x160/291948_10150287259827843_1311495235_n.jpg'),
               User(3,
                    70,
                    'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-prn2/c0.3.180.180/s160x160/1452460_233920073451567_1113876057_a.jpg'),
               User(2,
                    0,
                    'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-prn1/c49.49.618.618/s160x160/523389_435749629853047_305678701_n.jpg'),
               User(1,
                    100,
                    'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-frc1/c4.0.172.172/s160x160/1380205_519319994826427_1502866643_a.jpg')]),
         Pack(2,
              "Room406",
              [User(5,
                    64,
                    'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-prn1/c43.42.525.525/s160x160/59918_10201661866087235_2088536012_n.jpg'),
               User(6,
                    15,
                    'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-prn1/c50.50.621.621/s160x160/149792_4097320921156_1087738215_n.jpg'),
               User(7,
                    100,
                    'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-prn1/c2.0.177.177/s160x160/945981_10200659602646499_842230034_a.jpg'),
               User(8,
                    0,
                    'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-prn1/c120.99.621.621/s160x160/65815_10151361379309413_932983550_n.jpg',
                    [])])]

FEATS = [Category(0, "Alcohol", Broperty("Alcoholic", "alcoholic"),
                  [Brofeat(9,
                           "Steal A Drink", "Steal a someone's drink without him/her noticing (1 shot or 2 gulps)",
                           3)]),
         Category(1, "Wingman", Broperty("Top Wingman", "wingman"),
                  []),
         Category(2, "Valor", Broperty("Knight", "knight"),
                  []),
         Category(3, "Bro In Need", Broperty("Bro Indeed", "bro-indeed"),
                  []),
         Category(4, "Game", Broperty("Player", "player"),
                  []),
         Category(5, "Style", Broperty("Peacock", "peacock"),
                  []),
         Category(6, "Food", Broperty("Epicure", "epicure"),
                  []),
         Category(7, "Health", Broperty("Immortal", "immortal"),
                  []),
         Category(8, "Carpe Diem", Broperty("Been There, Done That", "been-there"),
                  []),
         Category(9, "Misc.", Broperty("Jack of All Trades", "jack"),
                  [])]