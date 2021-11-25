# StylishMaps

Really simple repo to generate stylish street maps using [OSMnx](https://github.com/gboeing/osmnx), matplotlib and [inkscape](https://inkscape.org/).

Maps can be parsed from bash with the following command:

`python main.py FILE_NAME LATITUDE LONGITUDE TITLE ZOOM STYLE OUT_PATH`

For example:

`python main.py "Belvedere" "48.192824269178004" "16.38504366701092" "Schloss Belvedere\nWien, AT" "15000" "Modern" "~/"`

exports:

![](https://chipdelmal.github.io/media/map/MAP_Belvedere.png)


Please note that it'll export the street traces with a transparent background for further use with software like [inkscape](https://inkscape.org/). Code to automate the process is provided but needs some panel setup (see my [blogpost](https://chipdelmal.github.io/artsci/2021-11-15-ArtsyMaps.html) for more information). 

Requirements: [OSMnx](https://github.com/gboeing/osmnx), [matplotlib](https://matplotlib.org/) 

<img src="https://raw.githubusercontent.com/Chipdelmal/pyMSync/master/media/pusheen.jpg" height="130px" align="middle"><br>


Author: Héctor M. Sánchez C. ([chipdelmal](chipdelmal.github.io))