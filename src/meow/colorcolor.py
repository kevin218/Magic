
import numpy as np
import matplotlib.pyplot as plt
import sys
import ObsTable as mast

plt.rcParams['figure.constrained_layout.use'] = True

wave = np.array([7.7, 18, 21])*1e-6
temp = np.linspace(100, 1000, 50)
flux = mast.planck(wave[:,np.newaxis], temp[np.newaxis,:])

# c1 = np.log10((flux[0] - flux[1]) / flux[1] + 1)
c1 = (flux[0] - flux[1]) / flux[1]
c2 = (flux[2] - flux[1]) / flux[1]

plt.figure(1, figsize=(6,4))
plt.clf()
plt.scatter(c1, c2, s=12, c=temp, cmap='plasma', marker='o')
cbar = plt.colorbar()
cbar.set_label('Temperature (K)', rotation=90)
plt.xlabel("(7.7-18)/18")
plt.ylabel("(21-18)/18")

plt.savefig("ColorColor-Example.png", dpi=150)