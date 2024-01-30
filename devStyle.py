

from sys import platform
import subprocess
from sys import argv
import numpy as np
import osmnx as ox
from os import path
import functions as fun
import matplotlib.pyplot as plt
ox.config(log_console=False, use_cache=True)

(lat, lon, label, fName, distance, TYPE, PATH) = (
    "19.5968444", "-99.227526", "Piso 9 CEDETEC\nTEC/CEM",
    "Piso9", "7500",
    "Art", "/Users/sanchez.hmsc/Pictures/Maps"
)
(lat, lon, label, fName, distance, TYPE, PATH) = (
    "18.922782", "-98.925879", "Volcanes\nLomas de Cocoyoc",
    "Volcanes", "7500", 
    "Art", "/Users/sanchez.hmsc/Pictures/Maps"
)
PATH = path.join(PATH, TYPE)
DST = int(distance)
point = (float(lat), float(lon))
INKSCAPE = False
###############################################################################
# Constants
###############################################################################
(MARKER, COORDS) = (True, True)
BLDG = False
if platform == "linux" or platform == "linux2":
    (FONT_FACE, FONT_SIZE, DPI) = ('Gotham Light', 325, 350)
elif platform == "darwin":
    (FONT_FACE, FONT_SIZE, DPI) = ('Savoye LET', 325, 350)
# label = bytes(label, "utf-8").decode("unicode_escape")'latin-1'
label = bytes(label, 'latin-1').decode("unicode_escape")
###############################################################################
# Label
###############################################################################
degs = [fun.decdeg2dms(i) for i in point]
degs = [[i for i in j] for j in degs]
(latStr, lonStr) = ["{:.0f}° {:.0f}' {:.2f}".format(*i) for i in degs]
###############################################################################
# Colors
###############################################################################
if TYPE=='Modern':
    (bgColor, bdColor) = ('#100F0F22', '#ffffff11')
    (rdColor, rdAlpha, rdScale, txtColor) = ('#ffffff', .400, 4.75, '#ffffff')
elif TYPE=='Art':
    (bgColor, bdColor) = ('#DCD4C6', '#75393E')
    (rdColor, rdAlpha, rdScale, txtColor) = ('#58586B', .350, 4.75, '#474139')
else:
    (bgColor, bdColor) = ('#100F0F22', '#ffffff11')
    (rdColor, rdAlpha, rdScale, txtColor) = ('#000000', .500, 5, '#100F0FDD')
###############################################################################
# Get Network
###############################################################################
print("* Processing {}".format(fName), end='\r')
G = ox.graph_from_point(
    point, dist=DST, network_type='all',
    retain_all=True, simplify=True, truncate_by_edge=True
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
        rdLen = item['length']
        if rdLen <= 100:
            linewidth = 0.15*rdScale
            color = fun.lighten('#8C3987', .65)
        elif rdLen > 100 and rdLen <= 200:
            linewidth = 0.25*rdScale
            color = fun.lighten('#E16C5B', .9)
        elif rdLen > 200 and rdLen <= 400:
            linewidth = 0.25*rdScale
            color = fun.lighten('#2F5079', .9)
        elif rdLen > 400 and rdLen <= 800:
            linewidth = 1.0*rdScale
            color = fun.lighten('#434869', 0.9)
        else:
            linewidth = 1.0*rdScale
            color = fun.lighten(rdColor, 1.0) 
        linewidth = np.interp(rdLen, [0, 1000, 10000], [1.25, 4, 5])
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
    0.5, 0.9, '{}'.format(label), family=FONT_FACE,
    horizontalalignment='center', verticalalignment='top', 
    transform=ax.transAxes, color=txtColor, fontsize=FONT_SIZE
)
if COORDS:
    ax.text(
        0.5, 0.1, 'N: {}\nW: {}'.format(latStr, lonStr), family=FONT_FACE,
        horizontalalignment='center', verticalalignment='bottom', 
        transform=ax.transAxes, color=txtColor, fontsize=FONT_SIZE*0.8
    )
###############################################################################
# Export
###############################################################################
fig.tight_layout(pad=0)
fig.savefig(
    path.join(PATH, fName+'.png'), 
    dpi=DPI, bbox_inches='tight', format="png", 
    facecolor=fig.get_facecolor(), transparent=False
)
plt.clf();plt.cla();plt.close(fig);plt.gcf();
###############################################################################
# Inkscape
###############################################################################
if INKSCAPE:
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