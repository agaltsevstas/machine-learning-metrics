import matplotlib.pyplot as plt
import random
from pylab import *
import numpy as np
prefix = 6.18

rx = [prefix+(0.001*random.random()) for i in arange(100)]
ry = [prefix+(0.001*random.random()) for i in arange(100)]
plt.plot(rx,ry,'ko')

frame1 = plt.gca()
for xlabel_i in frame1.axes.get_xticklabels():
    xlabel_i.set_visible(False)
    xlabel_i.set_fontsize(0.0)
for xlabel_i in frame1.axes.get_yticklabels():
    xlabel_i.set_fontsize(0.0)
    xlabel_i.set_visible(False)
for tick in frame1.axes.get_xticklines():
    tick.set_visible(False)
for tick in frame1.axes.get_yticklines():
    tick.set_visible(False)

plt.show()