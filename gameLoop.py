from classes import GameVar, Team
from plays import Play, PassPlay, RushPlay, KickOff, FieldGoal
endZone = 100

def main():
    global endZone
    offenseTeam, defenseTeam = coinToss(homeTeam, awayTeam)
    var = GameVar(offenseTeam, defenseTeam)

    while var.get_quarter() <= 4:
        while var.get_clock <= float(15*60) #time in seconds:
            if var.get_switch_sides() == True:
                teamToSwitch = var.get_offense()
                var.set_offense(var.get_defense())
                var.set_defense(teamToSwitch)
                var.set_switch_sides(False)

            if var.get_position() == 'FieldGoal':
                play = FieldGoal()
            elif var.get_position() == 'KickOff':
                play = KickOff()
            else:
                play = RushPlay()
                play = PassPlay()

            offenseChance = playCompletion(gameVar['offense'], play) #Maybe these should be team class members?
            defenseChance = defendChance(gameVar['defense'], play) #Maybe these should be team class members?

            result = play.makePlay(offenseChance, defenseChance)

            if var.get_position()+play.get_yards()>+ endZone:
                var.add_Score(play.get__score)
                var.set_field_goal(True)
                var.set_position = 'FieldGoal'
                var.add_clock(play.get_time_elapsed())
            
            elif result['fieldGoal'] == True:
                var.add_Score(play.get__score)
                var.set_field_goal(False)
                var.set_position = 'KickOff'
                var.add_clock(play.get_time_elapsed())
                var.set_switch_sides(True)
            
            elif var.get_position()+play.get_yards() >= var.get_first_down():
                var.set_down(1)
                var.add_position(play.get_yards())
                var.set_first_down(var.get_position+10)
                var.add_clock(play.get_time_elapsed())

            elif var.get_down() == 4:
                var.set_down(1)
                var.set_switch_sides(True)

            else:
                var.add_down()
                var.add_position(play.get_yards())
                var.add_clock(play.get_time_elapsed())
            
if __name__ == '__main__':
    main()
        






