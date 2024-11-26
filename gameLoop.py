



def possession(gameVar, result):

def fieldGoalChance():

def kickOff():

def pickPlay():

def playCompletion(play,):

def defendChance(play,):

def makePlay(play, ):

def main():
    quarter = 1
    down = 1
    time = 0
    currentPosition = 0
    firstDownLine = 10
    endZone = 100

    homeTeam = 'x'
    homeScore = 0
    awayTeam = 'y'
    awayScore = 0

    score = (homeScore, awayScore)

    gameVar = {
        'quarter' : 1,
        'down' : 1,
        'time' : 0,
        'currentPosition' : 0,
        'firstDownLine' : 10,
        'offense': homeTeam,
        'defense': awayTeam,
        'switchSides': False
    }

    result = { 
            'score': 0,
            'yards': 0,
            'timeElapsed':0,
            'fieldGoal': False,
            'touchDown': False}
    
    while quarter <= 4:
        while time <= 15*60:
            if gameVar['switchSides'] == True:
                teamToSwitch = gameVar['offense']
                gameVar['offense'] = gameVar['defense']
                gameVar['defense'] = teamToSwitch

            if currentPosition == 'FieldGoal':
                play = fieldGoalChance(gameVar['offense'])
            elif currentPosition == 'KickOff':
                play = kickOff(gameVar['defense'])
            else:
                play = pickPlay(gameVar['offense'], quarter, down, time, offenseScore, 
                            gameVar['offense'], currentPosition, firstDownLine, result)
            
            offenseChance = playCompletion(gameVar['offense'], play)
            defenseChance = defendChance(gameVar['defense'], play)

            result = makePlay(play, offenseChance, defenseChance)

            if currentPosition+result['yards']>+ endZone:
                offenseScore =+ result['score']
                fieldGoal = True
                currentPosition = 'FieldGoal'
                time =+ result['timeElapsed']
                gameVar['switchSides'] = True
            
            elif result['fieldGoal'] == True:
                offenseScore =+ result['score']
                currentPosition = 'KickOff'
                time =+ result['timeElapsed']
            
            elif currentPosition+result['yards'] >= firstDownLine:
                down = 1
                currentPosition += result['yards']
                firstDownLine += currentPosition +10
                time =+ result['timeElapsed']
            elif down == 4 and currentPosition+result < endZone:
                gameVar['switchSides'] = True

            else:
                down =+ 1
                time =+ result['timeElapsed']
                currentPosition =+ result['yards']
            
elif __name__ == '__main__':
    main()
        






