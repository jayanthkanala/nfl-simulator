class GameVar:
    '''
    Initializes a new instance of the game state with relevant football game settings.

    This constructor sets up the initial state for the football game simulation,
    including scores, possession, down information, and special game events.

    Args:
        offense (Any): Team that starts with possession of ball after initial cointoss
        defense (Any): Team that starts on defense after initial coin toss

    Attributes:
        _homeScore (int): The score for the home team, initialized to 0.
        _awayScore (int): The score for the away team, initialized to 0.
        _homeTeam (Any): Represents the home team, initialized to None.
        _awayTeam (Any): Represents the away team, initialized to None.
        _down (int): The current down in the game, starting at 1.
        _quarter (int): The current quarter, starting at 1.
        _clock (float): The clock for a given quarter
        _position (float): The position of the team with possession
        _firstDown (int): The first down distance, intialized to 10 yards
        _offense (Team Object): team with possession of ball
        _defense (Team Object): team defending 
        _switchSides (bool): Indicates whether teams change possession
        _touchDown (bool): Tracks whether a touchdown has occurred, default is False.
        _fieldGoal (bool): Tracks whether a field goal condition is triggered
        _kickOff (bool): Tracks whether a kickoff  condition is triggered
        _touchdowns (int): Tracks the number of touchdowns scored, initialized to 0.
    """
    '''
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
        self._offense = offense
        self._defense = defense
        self._switchSides = False
        self._touchDown = False
        self._fieldGoal = False
        self._kickOff = True
        self._touchdowns = 0

    # Getter and Setter for variables
    def get_touchdowns(self):
        return self._touchdowns

    def add_touchdown(self):
        self._touchdowns =+ 1

    def get_homeTeam(self):
        return self._homeTeam

    def set_homeTeam(self, value):
        self._homeTeam = value

    def get_awayTeam(self):
        return self._awayTeam

    def set_awayTeam(self, value):
        self._awayTeam = value

    def get_homeScore(self):
        return self._homeScore

    def get_awayScore(self):
        return self._awayScore

    def add_Score(self, value, interception = False):
        if interception: #If there was an interception and a touchdown was scored, the first if else statement checks for this and changes teams
          defense = self.get_offense().get_name()
          offense  = self.get_offense().get_name()
        else:
          offense = self.get_offense().get_name()
          defense  = self.get_offense().get_name()
        if offense == self.get_homeTeam().get_name(): #If the home team is on offense, give them the points
            self._homeScore += value
        elif offense == self.get_awayTeam().get_name(): #If the away team is on offense, give them the points
            self._awayScore += value
        else:
            print("You have made a mistake")


    # Getter and Setter and Adder for down
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
        newClock = float(self._clock) + round(float(value), 2)
        self._clock = round(newClock, 2)

    def set_clock(self, value):
        self._clock = value

    # Getter and Setter for position
    def get_position(self):
        return self._position

    def add_position(self, value):
        newPos = float(self._position) + round(float(value), 2)
        if newPos < 0: #If position is negative, make it 0
          newPos = 0
        self._position = round(newPos, 2)

    def set_position(self, value):
        self._position = value

    # Getter and Setter for firstDown
    def get_first_down(self):
        return self._firstDown

    def set_first_down(self, value):
        self._firstDown = value if value > 10 else 10 #first down line cannot be below 10 yards 

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