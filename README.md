# nfl-simulator
<h1>Installations</h1>
pip install dash dash_bootstrap_components<br>
pip install scipy<br>
pip install pandas<br>
pip install nfl-data-py<br>
<h1>To run:</h1>
python app.py<br>
open http://localhost:8050/ in browser<br>
input teams and number of games<br>
click 'Compare'<br>
Simulation can take up to 1 minute per game, <br>
The results page is blank until all games are done. <br>
recommend testing with two games for that reason. <br>
when all games are finished the results will appear on your screen<br>
navigate between games by clicking on their card on the left<br>
scroll to the bottom of the page to download a csv file!<br>
<h1>Issues Installing nfl-data-py</h1>
nfl-data-py may throw an error on windows machines <br>
when building wheel dependencies for fastparquet<br>
In this case, fastparquet can be manually installed first<br>
Once Git is installed on the machine:<br>
pip install cython<br>
pip install git+https://github.com/dask/fastparquet<br>
then retry nfl-py-data<br>