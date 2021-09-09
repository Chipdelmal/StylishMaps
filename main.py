
import subprocess
from sys import argv
import osmnx as ox
from os import path
import functions as fun
import matplotlib.pyplot as plt
ox.config(log_console=False, use_cache=True)

# (lat, lon, label, fName, distance) = (
#     "48.86228846291053", "2.2941683745020414", "Tour Eiffel\nParis, FR", "Paris", "15000"
# )
(lat, lon, label, fName, distance, TYPE, PATH) = (
    argv[2], argv[3], argv[4], argv[1], argv[5], argv[6], argv[7]
)
PATH = path.join(PATH, TYPE)
DST = int(distance)
point = (float(lat), float(lon))
###############################################################################
# Constants
###############################################################################
(MARKER, COORDS) = (True, True)
(FONT_FACE, FONT_SIZE, DPI) = ('Savoye LET', 250, 300)
BLDG = False
# label = bytes(label, "utf-8").decode("unicode_escape")'latin-1'
label = bytes(label, 'latin-1').decode("unicode_escape")
###############################################################################
# Colors
###############################################################################
degs = [fun.decdeg2dms(i) for i in point]
degs = [[i for i in j] for j in degs]
(latStr, lonStr) = ["{:.0f}° {:.0f}' {:.2f}".format(*i) for i in degs]
###############################################################################
# Colors
###############################################################################
(bgColor, bdColor) = ('#100F0F22', '#ffffff11')
if TYPE=='Modern':
    (rdColor, rdAlpha, rdScale, txtColor) = ('#ffffff', .400, 4.75, '#ffffff')
else:
    (rdColor, rdAlpha, rdScale, txtColor) = ('#000000', .5, 5, '#100F0FDD')
###############################################################################
# Get Network
###############################################################################
print("* Processing {}".format(fName), end='\r')
G = ox.graph_from_point(
    point, dist=DST, network_type='all',
    retain_all=True, simplify=True, truncate_by_edge=False
)
if BLDG:
    gdf = ox.geometries.geometries_from_point(
        point, tags={'building':True} , dist=DST
    )
###############################################################################
# Process Roads
###############################################################################
data = [i[-1] for i in G.edges(keys=True, data=True)]
(roadColors, roadWidths) = ([], [])
for item in data:
    if "length" in item.keys():
        if item["length"] <= 100:
            linewidth = 0.15*rdScale
            color = fun.lighten(rdColor, .7)
        elif item["length"] > 100 and item["length"] <= 200:
            linewidth = 0.25*rdScale
            color = fun.lighten(rdColor, .775)
        elif item["length"] > 200 and item["length"] <= 400:
            linewidth = 0.3*rdScale
            color = fun.lighten(rdColor, .85)
        elif item["length"] > 400 and item["length"] <= 800:
            linewidth = 0.5*rdScale
            color = fun.lighten(rdColor, 0.9)
        else:
            linewidth = 0.6*rdScale
            color = fun.lighten(rdColor, 1.0)
    else:
        color = rdColor
        linewidth = 0.10
    roadColors.append(color)
    roadWidths.append(linewidth)
###############################################################################
# Plot
###############################################################################
(fig, ax) = ox.plot_graph(
    G, node_size=0,figsize=(40, 40), 
    dpi=DPI, bgcolor=bgColor,
    save=False, edge_color=roadColors, edge_alpha=rdAlpha,
    edge_linewidth=roadWidths, show=False
)
if BLDG:
    (fig, ax) = ox.plot_footprints(
        gdf, ax=ax,
        color=bdColor, dpi=DPI, save=False, show=False, close=False
    )
if MARKER:
    ax.scatter(
        point[1], point[0], marker="x",
        zorder=10, color=txtColor,
        s=7500, linewidth=5
    )
ax.text(
    0.5, 0.825, '{}'.format(label), family=FONT_FACE,
    horizontalalignment='center', verticalalignment='center', 
    transform=ax.transAxes, color=txtColor, fontsize=FONT_SIZE
)
if COORDS:
    ax.text(
        0.5, 0.2, 'N: {}\nW: {}'.format(latStr, lonStr), family=FONT_FACE,
        horizontalalignment='center', verticalalignment='center', 
        transform=ax.transAxes, color=txtColor, fontsize=FONT_SIZE*0.8
    )
###############################################################################
# Export
###############################################################################
fig.tight_layout(pad=0)
fig.savefig(
    path.join(PATH, fName+'.png'), 
    dpi=DPI, bbox_inches='tight', format="png", 
    facecolor=fig.get_facecolor(), transparent=True
)
plt.clf();plt.cla();plt.close(fig);plt.gcf();
###############################################################################
# Inkscape
###############################################################################
fin = open(path.join(PATH, 'PANEL.svg'), "rt")
data = fin.read()
data = data.replace('MAP_IMG', fName)
fin.close()
fin = open(path.join(PATH, 'PANEL.svg'), "wt")
fin.write(data)
fin.close()
# Export composite image ------------------------------------------------------
cmd = [
    'inkscape', 
    '--export-type=png', 
    '--export-dpi='+str(DPI), 
    '--export-area-page',
    path.join(PATH, 'PANEL.svg'), 
    '--export-filename='+path.join(PATH, 'MAP_'+fName+'.png')
]
subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
# Return svg to original state ------------------------------------------------
fin = open(path.join(PATH, 'PANEL.svg'), "rt")
data = fin.read()
data = data.replace(fName,'MAP_IMG')
fin.close()
fin = open(path.join(PATH, 'PANEL.svg'), "wt")
fin.write(data)
fin.close()
print(" "*80, end='\r')