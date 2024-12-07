import pandas as pd

class Game:
  def __init__(self):
    self._playList = []

  def updatePlayList(self, results):
    self._playList.append(results)

  def finishGame(self):
    self._gameDF = pd.DataFrame(self._playList)


  def getGame(self):
    return self._gameDF
