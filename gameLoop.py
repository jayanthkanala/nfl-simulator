from GameVar import GameVar
from Plays import KickOff, FieldGoal, RushPlay, PassPlay, Punt
from Game import Game
from Team import Team
import random

def playGame(homeTeam, awayTeam):
    '''
    Simulates game between two teams
    :param homeTeam: user input home team
    :param awayTeam: user input away team
    :homeTeam type: str
    :awayTeam type: str
    :return var.get_homeScore(): Home team points, retrieved by GameVar method.
    :return var.get_awayScore(): Away team points,, retrieved by GameVar method.
    :return game.getGame(): Game results, retrieved by Game method.
    :var.get_homeScore() type: int
    :var.get_awayScore() type: int
    :game.getGame() type: DataFrame

    '''
    endZone = 100
    game = Game() #Instantiate instance of game to store results of each play in

    homeTeam = Team(homeTeam) #Create team objects for home and away
    awayTeam = Team(awayTeam)
    
    if random.uniform(0.00, 1.00) >= 0.50:  #Coin Toss
        var = GameVar(homeTeam, awayTeam) #Instianties GameVar object with home team on offense and away team on defense
    else:
        var = GameVar(awayTeam, homeTeam) #Instianties GameVar object with home team on defence and away team on offense
    #Updates game variables with home and away team
    var.set_homeTeam(homeTeam)
    var.set_awayTeam(awayTeam)

    x=0
    while var.get_quarter() <= 4: #A game lasts four quarters
        var.set_clock(0)  #If its quarter 2, this will restart the clock.

        if var.get_quarter() == 3: #Half Time Kick Off!
            var.set_kick_off(True)

        while var.get_clock() <= float(15*60): #Checks clock of a quarter using time in seconds
            #Check if sides need to be switched
            if var.get_switch_sides() == True: #Checks if results of last play indicate sides should change
                teamToSwitch = var.get_offense()
                var.set_offense(var.get_defense())
                var.set_defense(teamToSwitch)
                var.set_switch_sides(False)
            #Check GameVar object to see who is in possession of the ball
            offense = var.get_offense()
            defense = var.get_defense()

            #Checks what type of play needs to be made
            if var.get_field_goal() == True: #After a touch down, the field goal flag in GameVar is triggered, which will cause the next play to be a field goal
                play = FieldGoal(1) #Instantiate a field goal play with score set to 1
            elif var.get_kick_off() == True: #After a field goal, the kick off flag in GameVar is triggered, which will cause the next play to be a kick off
                play = KickOff() #Instantiate kick off play
            else:
                if (var.get_position() >= 60 and var.get_down() == 4): # if its 4th down and the endzone is within 40 yards
                    play = FieldGoal(3) if var.get_position() < 90 else RushPlay() #If the endzone is within 10 yards, go for it (rush), otherwise go for a fieldgoal
                elif var.get_position() < 60 and var.get_down() == 4: #If its 4th down and the endzone is more than 40 yards away
                    play = Punt() #initiate a punt play
                else:
                    choice = var.get_offense().choosePlay(offense, defense) 
                    #Checks var for offense team, then calls their choose play function, it can only output rush or pass.
                    if choice == ['rush_attempt']:
                        play = RushPlay() 
                    elif choice == ['pass_attempt']:
                        play = PassPlay()

            #Depending on the type of play, we need to hand its makePlay function the proper parameters
            if isinstance(play, Punt):
              result = play.makePlay(offense, var.get_position(), 'punt_attempt') #Simulates the results of a punt
            elif isinstance(play, FieldGoal):
                result = play.makePlay(offense, var.get_position()) #Simulates the results of a fieldgoal
            else:
                result=play.makePlay(offense, defense) #simulates results of a rush or pass play. 


            if play.get_name() == 'interception': #Did the defensive team intercept the ball?
              if var.get_position()+result['yards'] >= endZone: #Did they make it to the end zone?
                var.add_Score(6, True) #Adds score to the defensive team's total
                var.set_field_goal(True) #next play should be a field goal
                var.set_position(84) #Field goal position
                var.add_clock(result['timeElapsed'])
                var.add_touchdown()
                
              else: #If they didnt make it to the endzone, just give em the ball where they got it
                var.add_position(result['yards'])
                var.add_clock(result['timeElapsed'])
                var.set_switch_sides(True)
            elif play.isPenalty(): #did a penalty occur?
                var.add_position(result['yards'])
                var.add_clock(result['timeElapsed'])
                if var.get_position()+play.get_yards() >= var.get_first_down(): #Did the position get moved past first down line?
                    var.set_down(1)
                    var.set_first_down(var.get_position()+10)
            elif var.get_kick_off() == True: #Was this a kick off play?
                var.add_position(result['yards'])
                var.add_clock(result['timeElapsed'])
                var.set_down(1)
                var.set_kick_off(False) #Next play should not be a kickoff

            elif var.get_position()+result['yards'] >= endZone: #Did a touchdown occur?
                var.set_field_goal(True) #next play should be a field goal
                var.set_position(84)
                var.add_Score(6)
                var.add_clock(result['timeElapsed'])
                var.add_touchdown()
                play.set_name('touchdown')
            elif isinstance(play, Punt): #Did a punt occur?
                var.set_down(1)
                var.set_switch_sides(True)
                var.add_clock(result['timeElapsed'])
                var.set_position(20) #sets flat position after a punt for now, need to add return yards

            elif isinstance(play, FieldGoal): #Did a field goal happen?
                #If it was a succesful fieldgoal, add 1 to the offense teams score
                if play.getSuccess() == True: #Did they make it?
                    var.add_Score(play.getScore()) #Add appropriate score
                #Reset fieldgoal flag, add time elapsed during play, and flip on switch sides flag
                var.set_field_goal(False)
                var.set_kick_off(True)
                var.add_clock(result['timeElapsed'])
                var.set_position(0)
                var.set_first_down(1)
                var.set_switch_sides(True)


            elif var.get_position()+play.get_yards() >= var.get_first_down(): #Did the team pass the first down line?
                var.set_down(1) #Reset down to 1
                var.add_position(result['yards'])
                var.set_first_down(var.get_position()+10) #Sets new first down line
                var.add_clock(result['timeElapsed'])
            else: #Otherwise!
                var.set_down(var.get_down()+1) #Increment down 
                var.add_position(result['yards']) #Update positon
                var.add_clock(result['timeElapsed']) #Update clock
            x +=1
            print(f'Play {x} {play.get_name():>21}:: Home: {var.get_homeScore()}, Away: {var.get_awayScore()}, Clock: {var.get_clock()}, Down: {var.get_down()}, Position: {var.get_position()}, Offense: {var.get_offense().get_name()}, Defense: {var.get_defense().get_name()}')
            #Set the game results from that play after its results have been applied to the current game variables
            play.set_game_results(x, play.get_name(), var.get_homeScore(), var.get_awayScore(),offense.get_name(), defense.get_name(),var.get_position(),result['yards'],result['timeElapsed'], var.get_down(), var.get_quarter())
            #game has a parameters playList that has a list of the game result dictionary of each play, this appends the game result dictionary to that list
            game.updatePlayList(play.get_game_results())
        #Increment quarter
        quarter = var.get_quarter()
        var.set_quarter(quarter+1)
    #Finish game takes the playlist and turns it into an appropriate dataframe
    game.finishGame()
    return var.get_homeScore(), var.get_awayScore(), game.getGame() #Returns scores and game Dataframe


def runSimulation(homeTeam = 'BUF', awayTeam = 'KC', numGames = 10): #This will call the playGame function the number of times the user asks. 
    game_scores = [] #score from each game
    games = [] #Each games dataframe
    #homeTeam = Team('BUF')
    #awayTeam = Team('KC')
    for x in range(numGames):
        a, b, c = playGame(homeTeam, awayTeam)
        game_scores.append((a, b))
        games.append(c)
    return games, game_scores #Returns a list of game dataframes, and a list of tuples containing game scores

runSimulation()