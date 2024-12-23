import pytest
from Play import Play
from Plays import FieldGoal
from Team import Team

@pytest.mark.parametrize("time, output", [("15:00", 900), ("13:56", 836), ("8:32", 512), ("00:41", 41)])
def test_convert_time_to_seconds(time, output):
  play = Play("Sample Play")
  result = play.convert_time_to_seconds(time)
  assert result == output

@pytest.mark.parametrize("flag_type, play_type, output", [("Roughing the Passer", "pass_attempt", -15), ("Offensive Holding", "pass_attempt", -10), ("Intentional Grounding", "pass_attempt", -15)])
def test_flag_yards(flag_type, play_type, output):
    play = Play("Sample Play")
    result = play.flag_yards(flag_type, play_type)
    assert result == output

@pytest.mark.parametrize("currentPosition, offense, output", [(10, "BUF", 0), (45, "KC", 0)]) #No team has attempted a 100 yard field goal, no team has made a 70+ yard field goal
def test_field_goal_percentage(currentPosition, offense, output):
    play = FieldGoal(1)
    team = Team(offense)
    result = play.field_goal_percentage(currentPosition, team)
    assert result == output

def test_average_yards():
    team = Team('KC')
    result, a, b = team.average_yards(play_type="incomplete_pass", offdef='posteam') # incomplete passes are 0 yards
    assert result == 0

def test_average_time():
    team = Team('KC')
    complete, a, b = team.average_time(play_type = "complete_pass") #incomplete passes should take less time than complete
    assert 0 <= complete
