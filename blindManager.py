baseAnteScoreReq = {-1 : 100, 0:100, 1:300, 2:800, 3:2000, 4:5000, 5:11000, 6:20000, 7:35000, 8:50000}
#baseAnteScoreReqGreenStake
#baseAnteScoreReqPlasmaDeck
currentAnte = 1
class Blind:
    def __init__(self, name = "Blind", scale = 1.0, description = "", modifiers = {}):
        self.name = name
        self.scale = scale
        self.description = description
        self.modifiers = modifiers
