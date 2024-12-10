from GameVar import GameVar
from Plays import Play, KickOff, FieldGoal, RushPlay, PassPlay, Punt
from Game import Game
from Team import Team
import random
endZone = 100

def main(homeTeam, awayTeam):
    global endZone
    game = Game()
    #These will be input from the GUI Jayanth is making
    homeTeam = Team(homeTeam)
    awayTeam = Team(awayTeam)
    #Coin Toss
    if random.uniform(0.00, 1.00) >= 0.50:
        var = GameVar(homeTeam, awayTeam)
    else:
        var = GameVar(awayTeam, homeTeam)
    var.set_homeTeam(homeTeam)
    var.set_awayTeam(awayTeam)

    x=0
    while var.get_quarter() <= 4:
        while var.get_clock() <= float(15*60): #time in seconds
            #Check if sides need to be switched
            if var.get_switch_sides() == True:
                teamToSwitch = var.get_offense()
                var.set_offense(var.get_defense())
                var.set_defense(teamToSwitch)
                var.set_switch_sides(False)
            offense = var.get_offense()
            defense = var.get_defense()

            #Check what type of play needs to be made using
            if var.get_field_goal() == True:
                play = FieldGoal()
            elif var.get_kick_off() == True:
                play = KickOff()
            else:
                choice = var.get_offense().choosePlay(offense, defense) ########################Test
                if choice == ['rush_attempt']:
                  play = RushPlay()
                elif choice == ['pass_attempt']:
                  play = PassPlay()
                elif choice == ['kickoff_attempt']:
                    play = Punt()

            #Some way to calculate chances of each sides success for the play
            #Maybe it should instead calculate a chance of success for offense
            #Then determine a range of yards given success
            if isinstance(play, Punt) or  isinstance(play, FieldGoal):
                result = play.makePlay(offense, var.get_position()) #Might need puntorkickargument
            else:
                result=play.makePlay(offense, defense) ####################Test

            if play.get_name == 'interception':
              if var.get_position()+result['yards'] >+ endZone:
                var.add_Score(6)
                var.set_field_goal(True)
                var.set_position(65)
                var.add_clock(result['timeElapsed'])
                var.add_touchdown()
                var.set_switch_sides(True)
              else:
                var.set_position(20)
                var.add_clock(result['timeElapsed'])
                var.set_switch_sides(True)

            if var.get_position()+result['yards'] >+ endZone:
                var.add_Score(6)
                var.set_field_goal(True)
                var.set_position(65)
                var.add_clock(result['timeElapsed'])
                var.add_touchdown()


            elif var.get_kick_off() == True:
                var.add_position(result['yards'])
                var.add_clock(result['timeElapsed'])
                var.set_kick_off(False)

            elif var.get_field_goal() == True:
                #If it was a succesful fieldgoal, add 1 to the offense teams score
                if play.getSuccess() == True:
                    var.add_Score(1)
                #Reset fieldgoal flag, add time elapsed during play, and flip on switch sides flag
                var.set_field_goal(False)
                var.set_kick_off(True)
                var.add_clock(result['timeElapsed'])
                var.set_position(0)
                var.set_first_down(10)
                var.set_switch_sides(True)


            elif var.get_down() == 4:
                if var.get_position()+play.get_yards() >= var.get_first_down():
                    var.set_down(1)
                    var.set_first_down(var.get_position()+10)
                    var.add_touchdown()
                    var.set_field_goal(True)
                    var.set_position(65)
                    var.add_clock(result['timeElapsed'])
                else:
                    var.set_down(1)
                    var.set_position(65)
                    var.set_switch_sides(True)
                    var.add_clock(result['timeElapsed'])

            elif play.isPenalty():
                var.add_position(result['yards'])
                var.add_clock(result['timeElapsed'])
                if var.get_position()+play.get_yards() >= var.get_first_down():
                #This check needs to be improved to not count for certain situations
                    var.set_down(1)
                    var.set_first_down(var.get_position()+10)

            elif var.get_position()+play.get_yards() >= var.get_first_down():
                #This check needs to be improved to not count for certain situations
                    var.set_down(1)
                    var.set_first_down(var.get_position()+10)
                    var.add_position(result['yards'])
                    var.add_clock(result['timeElapsed'])
            else:
                var.add_down()
                var.add_position(result['yards'])
                var.add_clock(result['timeElapsed'])
            x +=1
            print(f'Play {x} {play.get_name()}: Home: {var.get_homeScore()}, Away: {var.get_awayScore()}, Clock: {var.get_clock()}, Down: {var.get_down()}, Position: {var.get_position()}, Offense: {var.get_offense().get_name()}, Defense: {var.get_defense().get_name()}')
            play.set_game_results(var.get_homeScore(), var.get_awayScore(),result['yards'],result['timeElapsed'], var.get_down(), var.get_quarter(), 0, play.isPenalty(), var.get_field_goal(), play.get_success(), var.get_switch_sides())
            game.updatePlayList(play.get_game_results())
        quarter = var.get_quarter()
        var.set_quarter(quarter+1)
    game.finishGame()
    return var.get_homeScore(), var.get_awayScore(), game.getGame() #Returns game Dataframe


def runSimulation(homeTeam = 'BUF', awayTeam = 'KC', numGames = 10):
    game_scores = [] #score from each game
    games = [] #Each games dataframe
    #homeTeam = Team('BUF')
    #awayTeam = Team('KC')
    for x in range(numGames):
        a, b, c = main(homeTeam, awayTeam)
        game_scores.append((a, b))
        games.append(c)
    return games, game_scores








