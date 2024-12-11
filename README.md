# nfl-simulator
<h1>Installations</h1>
pip install dash dash_bootstrap_components
pip install scipy
pip install pandas
pip install nfl-data-py
<h1>To run:</h1>
python app.py
open http://localhost:8050/ in browser
input teams and number of games
click 'Compare'
Simulation can take up to 1 minute per game, 
when all games are finished the results will appear on your screen
navigate between games by clicking on their card on the left
scroll to the bottom of the page to download a csv file

<h1>Issues Installing nfl-data-py</h1>
nfl-data-py may throw an error on windows machines 
when building wheel dependencies for fastparquet
In this case, fastparquet can be manually installed first
Once Git is installed on the machine:
pip install cython
pip install git+https://github.com/dask/fastparquet
then retry nfl-py-data