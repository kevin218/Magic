
import numpy as np
import matplotlib.pyplot as plt
import ObsTable as mast

plt.rcParams['figure.constrained_layout.use'] = True

# constants
c = 2.99792458e8        # m/s, speed of light
# Wavelengths/frequencies of interest
wave = np.array([7.7, 18, 21])*1e-6
freq = c/wave

# Look at only planet flux (in MJy/sr)
temp = np.linspace(100, 1000, 50)
# flux_pl = mast.planck(wave[:,np.newaxis], temp[np.newaxis,:])
flux_pl = mast.planck_freq(freq[:,np.newaxis], temp[np.newaxis,:])*1e20

# c1 = np.log10((flux[0] - flux[1]) / flux[1] + 1)
c1 = (flux_pl[0] - flux_pl[1]) / flux_pl[1]
c2 = (flux_pl[2] - flux_pl[1]) / flux_pl[1]

plt.figure(1, figsize=(6,4))
plt.clf()
plt.title("Planet")
plt.scatter(c1, c2, s=12, c=temp, cmap='plasma', marker='o')
cbar = plt.colorbar()
cbar.set_label('Temperature (K)', rotation=90)
plt.xlabel("(7.7-18)/18")
plt.ylabel("(21-18)/18")

plt.savefig("ColorColor-Planet.png", dpi=150)


# Look at only WD flux
temp_wd = np.linspace(5000, 10000, 50)
# flux_wd = mast.planck(wave[:,np.newaxis], temp_wd[np.newaxis,:])
flux_wd = mast.planck_freq(freq[:,np.newaxis], temp_wd[np.newaxis,:])*1e20

# Colors
c1 = (flux_wd[0] - flux_wd[1]) / flux_wd[1]
c2 = (flux_wd[2] - flux_wd[1]) / flux_wd[1]

plt.figure(2, figsize=(6,4))
plt.clf()
plt.title("White Dwarf")
plt.scatter(c1, c2, s=12, c=temp_wd, cmap='plasma', marker='o')
cbar = plt.colorbar()
cbar.set_label('WD Temperature (K)', rotation=90)
plt.xlabel("(7.7-18)/18")
plt.ylabel("(21-18)/18")
plt.savefig("ColorColor-WD.png", dpi=150)


# Assume Jupiter-size planet and Earth-size WD
area_ratio = 1/11.2**2
# Combine planet and WD flux
plt.figure(3, figsize=(6,4))
plt.clf()
plt.title("White Dwarf + Jupiter-Size Planet")
for i in range(50):
    flux_tot = flux_pl + flux_wd[:,i,np.newaxis]*area_ratio
    c1 = (flux_tot[0] - flux_tot[1]) / flux_tot[1]
    c2 = (flux_tot[2] - flux_tot[1]) / flux_tot[1]
    plt.scatter(c1, c2, s=12, c=temp, cmap='plasma', marker='o')

cbar = plt.colorbar()
cbar.set_label('Temperature (K)', rotation=90)
plt.xlim(0.5, 4.25)
plt.ylim(-0.265, -0.115)
plt.xlabel("(7.7-18)/18")
plt.ylabel("(21-18)/18")
plt.savefig("ColorColor-WD+Jupiter.png", dpi=150)



# Assume Neptune-size planet and Earth-size WD
area_ratio = 1/3.88**2
# Combine planet and WD flux
plt.figure(4, figsize=(6,4))
plt.clf()
plt.title("White Dwarf + Neptune-Size Planet")
for i in range(50):
    flux_tot = flux_pl + flux_wd[:,i,np.newaxis]*area_ratio
    c1 = (flux_tot[0] - flux_tot[1]) / flux_tot[1]
    c2 = (flux_tot[2] - flux_tot[1]) / flux_tot[1]
    plt.scatter(c1, c2, s=12, c=temp, cmap='plasma', marker='o')

cbar = plt.colorbar()
cbar.set_label('Temperature (K)', rotation=90)
plt.xlim(0.5, 4.25)
plt.ylim(-0.265, -0.115)
plt.xlabel("(7.7-18)/18")
plt.ylabel("(21-18)/18")
plt.savefig("ColorColor-WD+Neptune.png", dpi=150)


#############################
model_file = '/Users/stevekb1/Documents/data/JWST/WD/Magic-2024-07/CPD-69-177/0310-688.txt'
model_wave, model_flux = np.genfromtxt(model_file, unpack=True)

# bb = mast.planck(model_wave*1e-6, 7500)

plt.figure(10)
plt.clf()
plt.loglog(model_wave, model_flux*model_wave, '-', label='Model')
# plt.loglog(model_wave, bb, '-', label='BB')
plt.xlim(5,25)
plt.ylim(2, 20)

#############################

c1 = (flux_pl[0] + flux_pl[2] - 2*flux_pl[1]) / flux_pl[1]
c2 = (flux_pl[2] - flux_pl[1]) / flux_pl[1]

plt.figure(11, figsize=(6,4))
plt.clf()
plt.title("Planet")
plt.scatter(c1, c2, s=12, c=temp, cmap='plasma', marker='o')
cbar = plt.colorbar()
cbar.set_label('Temperature (K)', rotation=90)
plt.xlabel("(7.7+21-2*18)/18")
plt.ylabel("(21-18)/18")
plt.savefig("Fig11-ColorColor-Planet.png", dpi=150)

# Look at only WD flux
# Colors
c1 = (flux_wd[0] + flux_wd[2] - 2*flux_wd[1]) / flux_wd[1]
c2 = (flux_wd[2] - flux_wd[1]) / flux_wd[1]

plt.figure(12, figsize=(6,4))
plt.clf()
plt.title("White Dwarf")
plt.scatter(c1, c2, s=12, c=temp_wd, cmap='plasma', marker='o')
cbar = plt.colorbar()
cbar.set_label('WD Temperature (K)', rotation=90)
plt.xlabel("(7.7+21-2*18)/18")
plt.ylabel("(21-18)/18")
plt.savefig("Fig12-ColorColor-WD.png", dpi=150)

# Assume Jupiter-size planet and Earth-size WD
area_ratio = 1/11.2**2
# Combine planet and WD flux
plt.figure(13, figsize=(6,4))
plt.clf()
plt.title("White Dwarf + Jupiter-Size Planet")
for i in range(50):
    flux_tot = flux_pl + flux_wd[:,i,np.newaxis]*area_ratio
    c1 = (flux_tot[0] + flux_tot[2] - 2*flux_tot[1]) / flux_tot[1]
    c2 = (flux_tot[2] - flux_tot[1]) / flux_tot[1]
    plt.scatter(c1, c2, s=12, c=temp, cmap='plasma', marker='o')

cbar = plt.colorbar()
cbar.set_label('Temperature (K)', rotation=90)
# plt.xlim(0.5, 4.25)
# plt.ylim(-0.265, -0.115)
plt.xlabel("(7.7+21-2*18)/18")
plt.ylabel("(21-18)/18")
plt.savefig("Fig13-ColorColor-WD+Jupiter.png", dpi=150)


#################################

log_fp = np.log(flux_pl)
log_wave = np.log10(wave)
slope1 = (log_fp[0]-log_fp[1])/(log_wave[0]-log_wave[1])
slope2 = (log_fp[2]-log_fp[1])/(log_wave[2]-log_wave[1])

c1 = slope2 - slope1
c2 = (flux_pl[2] - flux_pl[1]) / flux_pl[1]

plt.figure(21, figsize=(6,4))
plt.clf()
plt.title("Planet")
plt.scatter(c1, c2, s=12, c=temp, cmap='plasma', marker='o')
cbar = plt.colorbar()
cbar.set_label('Temperature (K)', rotation=90)
plt.xlabel("Slope2-Slope1")
plt.ylabel("(21-18)/18")
plt.savefig("Fig21-ColorColor-Planet.png", dpi=150)

# Look at only WD flux
log_wd = np.log(flux_wd)
slope1 = (log_wd[0]-log_wd[1])/(log_wave[0]-log_wave[1])
slope2 = (log_wd[2]-log_wd[1])/(log_wave[2]-log_wave[1])

c1 = slope2 - slope1
c2 = (flux_wd[2] - flux_wd[1]) / flux_wd[1]

plt.figure(22, figsize=(6,4))
plt.clf()
plt.title("White Dwarf")
plt.scatter(c1, c2, s=12, c=temp_wd, cmap='plasma', marker='o')
cbar = plt.colorbar()
cbar.set_label('WD Temperature (K)', rotation=90)
plt.xlabel("Slope2-Slope1")
plt.ylabel("(21-18)/18")
plt.savefig("Fig22-ColorColor-WD.png", dpi=150)



# Assume Jupiter-size planet and Earth-size WD
area_ratio = 1/11.2**2
# Combine planet and WD flux
plt.figure(23, figsize=(6,4))
plt.clf()
plt.title("White Dwarf + Jupiter-Size Planet")
for i in range(50):
    flux_tot = flux_pl + flux_wd[:,i,np.newaxis]*area_ratio
    log_tot = np.log(flux_tot)
    slope1 = (log_tot[0]-log_tot[1])/(log_wave[0]-log_wave[1])
    slope2 = (log_tot[2]-log_tot[1])/(log_wave[2]-log_wave[1])
    c1 = slope2 - slope1
    c2 = (flux_tot[2] - flux_tot[0]) / flux_tot[0]
    plt.scatter(c1, c2, s=5+i*0.3, c=temp, cmap='plasma', marker='o')

cbar = plt.colorbar()
cbar.set_label('Temperature (K)', rotation=90)
plt.xlim(-1.25, 1.25)
# plt.ylim(-0.265, -0.115)
plt.xlabel("Slope2 - Slope1")
plt.ylabel("(21-7.7)/7.7")
plt.savefig("Fig23-ColorColor-WD+Jupiter.png", dpi=150)



# Assume Jupiter-size planet and Earth-size WD
area_ratio = 1/3.88**2
# Combine planet and WD flux
plt.figure(24, figsize=(6,4))
plt.clf()
plt.title("White Dwarf + Neptune-Size Planet")
for i in range(50):
    flux_tot = flux_pl + flux_wd[:,i,np.newaxis]*area_ratio
    log_tot = np.log(flux_tot)
    slope1 = (log_tot[0]-log_tot[1])/(log_wave[0]-log_wave[1])
    slope2 = (log_tot[2]-log_tot[1])/(log_wave[2]-log_wave[1])
    c1 = slope2 - slope1
    c2 = (flux_tot[2] - flux_tot[0]) / flux_tot[0]
    plt.scatter(c1, c2, s=5+i*0.3, c=temp, cmap='plasma', marker='o')

cbar = plt.colorbar()
cbar.set_label('Temperature (K)', rotation=90)
plt.xlim(-1.25, 1.25)
plt.ylim(-0.265, -0.115)
plt.xlabel("Slope2-Slope1")
plt.ylabel("(21-7.7)/7.7")
plt.savefig("Fig24-ColorColor-WD+Neptune.png", dpi=150)