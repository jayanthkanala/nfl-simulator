from GameVar import GameVar
from Play import Play, KickOff, FieldGoal, RushPlay, PassPlay, Penalty
from Game import Game
from Team import Team
import random
endZone = 100

def main():
    global endZone
    game = Game()
    #These will be input from the GUI Jayanth is making
    homeTeam = Team('BUF')
    awayTeam = Team('KC')
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
                elif choice == ['penalty']:
                  play = Penalty()

            #Some way to calculate chances of each sides success for the play
            #Maybe it should instead calculate a chance of success for offense
            #Then determine a range of yards given success
            result=play.makePlay(offense, defense) ####################Test

            if var.get_position()+result['yards'] >+ endZone:
                var.add_Score(6)
                var.set_field_goal(True)
                var.add_clock(result['timeElapsed'])
                var.add_touchdown()
                var.set_position(0)
                var.set_first_down(var.get_position()+10)

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
                var.add_clock(result['timeElapsed'])
                var.set_switch_sides(True)

            elif var.get_position()+play.get_yards() >= var.get_first_down():
                var.set_down(1)
                var.set_first_down(var.get_position()+10)
                var.add_position(result['yards'])
                var.add_clock(result['timeElapsed'])

            elif var.get_down() == 4:
                var.set_down(1)
                var.set_switch_sides(True)
                var.add_clock(result['timeElapsed'])

            elif isinstance(play, Penalty):
                var.set_first_down(var.get_position()-result['yards'])
                var.add_position(result['yards'])
                var.add_clock(result['timeElapsed'])
            else:
                var.add_down()
                var.add_position(result['yards'])
                var.add_clock(result['timeElapsed'])
            x +=1
            print(f'Play {x} {play.get_name()}: Home: {var.get_homeScore()}, Away: {var.get_awayScore()}, Clock: {var.get_clock()}, Down: {var.get_down()}, Position: {var.get_position()}, Offense: {var.get_offense().get_name()}, Defense: {var.get_defense().get_name()}')
            play.set_game_results(var.get_homeScore(), var.get_awayScore(),result['yards'],result['timeElapsed'], var.get_down(), var.get_quarter(), 0, isinstance(play, Penalty), var.get_field_goal(), play.get_success(), var.get_switch_sides())
            game.updatePlayList(play.get_game_results())
        quarter = var.get_quarter()
        var.set_quarter(quarter+1)
    game.finishGame()
    return var.get_homeScore(), var.get_awayScore(), game

game_results = []
games = []
for x in range(20):
  a, b, c = main()
  game_results.append((a, b))
  games.append(c)

print(game_results)
print(games)






