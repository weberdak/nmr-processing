import matplotlib.pyplot as plt
import numpy as np
import nmrglue as ng
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

# Specify results files
spectrum = 'darr.ft.ft2'

# Initalize plot
fig, ax = plt.subplots(figsize=(3.5,3.5))

# Set contour levels
contour_start = 21538*5 # Baseline (noise level * X)
contour_num = 30 # number of contour levels
contour_factor = 1.15 # scaling factor between contour levels
levels = contour_start*contour_factor**np.arange(contour_num)

# Load spectrum
dic,data = ng.pipe.read(spectrum)

# Set ppm scales
uc_t1 = ng.pipe.make_uc(dic,data,dim=0)
ppm_t1 = uc_t1.ppm_scale()
ppm_t1_0, ppm_t1_1 = uc_t1.ppm_limits()
uc_t2 = ng.pipe.make_uc(dic,data,dim=1)
ppm_t2 = uc_t2.ppm_scale()
ppm_t2_0, ppm_t2_1 = uc_t2.ppm_limits()

# Plot contour
ax.contour(data,levels=levels,linewidths=0.25,colors='red',
        extent=(ppm_t2_0, ppm_t2_1, ppm_t1_0, ppm_t1_1))

# Set axis titles
ax.set_xlabel('$^{13}$C (ppm)',size=10)
ax.set_ylabel('$^{13}$C (ppm)',size=10)

# Set limits and tick labels
x_hi = 75
x_lo = 5
y_hi = 75
y_lo = 5
ax.set_xlim(x_hi,x_lo)
ax.set_ylim(y_hi,y_lo)
ax.xaxis.set_major_locator(MultipleLocator(10))
ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
ax.xaxis.set_minor_locator(MultipleLocator(2.5))
ax.yaxis.set_major_locator(MultipleLocator(10))
ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))
ax.yaxis.set_minor_locator(MultipleLocator(2.5))
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

# Draw slices
# Vertical
x = 38.2
yslice = data[:, uc_t2('{} ppm'.format(x))]
ax.plot(15*yslice/max(yslice)+x, ppm_t1, c='black', linewidth=0.5)
ax.axvline(x,color='black',linewidth=0.5)

# Horizontal
y = 38.2
#xslice = data[uc_t1('{} ppm'.format(y)),:]
#ax.plot(ppm_t2,15*xslice/max(xslice)+y, c='black', linewidth=0.5)
#ax.axhline(y,color='black',linewidth=0.5)


# Output
plt.tight_layout()
plt.savefig('plot_darr_ft.ps',dpi=300)
plt.savefig('plot_darr_ft.jpg',dpi=300)
plt.show()
