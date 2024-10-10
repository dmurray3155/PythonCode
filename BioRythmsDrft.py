from datetime import date


bDay = date(1967, 1, 25)
today = date(2023, 9, 8)
delta = today - bDay
daysAlive = delta.days
print("Days Alive as of today: " + str(format(daysAlive, ',d')))

LDR = daysAlive - 15
RDR = daysAlive + 15

import numpy as np
import matplotlib
matplotlib.use('SVG')
import matplotlib.pyplot as plt

xp = np.arange(LDR, RDR, 0.1)
ypp = np.sin(2 * np.pi * xp / 23)		#	physical
ype = np.sin(2 * np.pi * xp / 28)		#	emotional
ypi = np.sin(2 * np.pi * xp / 33)		#	intellectual

fix, bio = plt.subplots()
bio.plot(xp, ypp, 'b-', label='physical')
bio.plot(xp, ype, 'r-', label='emotional')
bio.plot(xp, ypi, 'g-', label='intellectual')
bio.axvline(x=daysAlive, color='k', linestyle='-')

plt.xlabel('Days Alive')
plt.title('Biorythms: Birthdate: Jan. 25, 1967')

legend = bio.legend(loc='lower right', shadow=True, fontsize='small')
legend.get_frame().set_facecolor('#EFEFEF')
plt.grid(True)

plt.savefig('DonBio20230908.svg')
#	plt.show()