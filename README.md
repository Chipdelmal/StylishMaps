# StylishMaps

Really simple repo to generate stylish street maps using [OSMnx](https://github.com/gboeing/osmnx), matplotlib and [inkscape](https://inkscape.org/).

Maps can be parsed from bash with the following command:

`python main.py FILE_NAME LATITUDE LONGITUDE TITLE ZOOM STYLE OUT_PATH`

For example:

`python main.py "Belvedere" "48.192824269178004" "16.38504366701092" "Schloss Belvedere\nWien, AT" "15000" "~/"`

exports:

![](https://chipdelmal.github.io/media/map/MAP_Belvedere.png)

Requirements: [OSMnx](https://github.com/gboeing/osmnx), [matplotlib](https://matplotlib.org/) 

<img src="https://raw.githubusercontent.com/Chipdelmal/pyMSync/master/media/pusheen.jpg" height="130px" align="middle"><br>


Author: Héctor M. Sánchez C. ([chipdelmal](chipdelmal.github.io))