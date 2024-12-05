class GameVar:
    def __init__(self, offense, defense):
        self._homeScore = 0
        self._awayScore = 0
        self._homeTeam = None
        self._awayTeam = None
        self._down = 1
        self._quarter = 1
        self._clock = 0
        self._position = 0
        self._firstDown = 10 
        self._endZone = 100
        self._offense = offense
        self._defense = defense
        self._switchSides = False
        self._touchDown = False
        self._fieldGoal = False
        self._kickOff = True
    
    # Getter and Setter for Teams
    def get_homeTeam(self):
        return self._homeTeam

    def set_homeTeam(self, value):
        self._homeTeam = value
    
    def get_awayTeam(self):
        return self._awayScore
    
    def set_awayTeam(self, value):
        self._awayTeam = value

    # Getter and Setter for scores
    def get_homeScore(self):
        return self._homeScore
    
    def get_awayScore(self):
        return self._awayScore
    
    def add_Score(self, value):
        if self.get_offense == self.get_homeTeam():
            self._homeScore =+ value
        elif self.get_offense == self.get_awayTeam():
            self._awayScore =+ value
        else: 
            print("You have made a mistake")

    # Getter and Setter for down
    def get_down(self):
        return self._down
    
    def add_down(self):
        self._down += 1

    def set_down(self, value):
        self._down = value

    # Getter and Setter for quarter
    def get_quarter(self):
        return self._quarter

    def set_quarter(self, value):
        self._quarter = value

    # Getter and Setter for clock
    def get_clock(self):
        return self._clock

    def add_clock(self, value):
        self._clock =+ value

    def set_clock(self, value):
        self._clock = value

    # Getter and Setter for position
    def get_position(self):
        return self._position
    
    def add_position(self, value):
        self._position =+ value

    def set_position(self, value):
        self._position = value

    # Getter and Setter for firstDown
    def get_first_down(self):
        return self._firstDown

    def set_first_down(self, value):
        self._firstDown = value

    # Getter and Setter for endZone
    def get_end_zone(self):
        return self._endZone

    def set_end_zone(self, value):
        self._endZone = value

    # Getter and Setter for offense
    def get_offense(self):
        return self._offense

    def set_offense(self, value):
        self._offense = value

    # Getter and Setter for defense
    def get_defense(self):
        return self._defense

    def set_defense(self, value):
        self._defense = value

    # Getter and Setter for switchSides
    def get_switch_sides(self):
        return self._switchSides

    def set_switch_sides(self, value):
        self._switchSides = value

    # Getter and Setter for touchDown
    def get_touch_down(self):
        return self._touchDown

    def set_touch_down(self, value):
        self._touchDown = value

    # Getter and Setter for fieldGoal
    def get_field_goal(self):
        return self._fieldGoal

    def set_field_goal(self, value):
        self._fieldGoal = value

    # Getter and Setter for kickOff
    def get_kick_off(self):
        return self._kickOff

    def set_kick_off(self, value):
        self._kickOff = value