from GameVar import GameVar, Team
from Play import Play, PassPlay, RushPlay, KickOff, FieldGoal
import random
endZone = 100

def main():
    global endZone
    playByplay = []
    #These will be input from the GUI Jayanth is making
    homeTeam = 'x'
    awayTeam = 'y'
    #Coin Toss
    if random.uniform(0.00, 1.00) >= 0.50:
        var = GameVar(homeTeam, awayTeam)
    else:
        var = GameVar(awayTeam, homeTeam)

    while var.get_quarter() <= 4:
        while var.get_clock <= float(15*60): #time in seconds
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
                var.get_offense().choosePlay(offense, defense) ########################Test
                play = RushPlay()
                play = PassPlay()

            #Some way to calculate chances of each sides success for the play
            #Maybe it should instead calculate a chance of success for offense
            #Then determine a range of yards given success
            result=play.makePlay(offense, defense) ####################Test
            

            if var.get_position()+result['yards'] >+ endZone:
                var.add_Score(6)
                var.set_field_goal(True)
                var.add_clock(result['timeElapsed'])

            if var.get_kick_off == True:
                var.add_position(result['yards'])
                var.add_clock(result['timeElapsed'])
                var.set_kick_off == False

            elif var.get_field_goal == True:
                #If it was a succesful fieldgoal, add 1 to the offense teams score
                if play.getSuccess() == True:
                    var.add_Score(1)
                #Reset fieldgoal flag, add time elapsed during play, and flip on switch sides flag
                var.set_field_goal(False)
                var.add_clock(result['timeElapsed'])
                var.set_switch_sides(True)
            
            elif var.get_position()+play.get_yards() >= var.get_first_down():
                var.set_down(1)
                var.set_first_down(var.get_position+10)
                var.add_position(result['yards'])
                var.add_clock(result['timeElapsed'])

            elif var.get_down() == 4:
                var.set_down(1)
                var.set_switch_sides(True)

            else:
                var.add_down()
                var.add_position(result['yards'])
                var.add_clock(result['timeElapsed'])
            playByplay.append(play)
        #Add code to add play results to playbyplay
    return var.get_homeScore, var.get_awayScore, playByplay
            
if __name__ == '__main__':

    
    main()
        






