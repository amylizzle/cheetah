import math

import matplotlib.pyplot as plt
import numpy as np
import torch

from cheetah import ParticleBeam, Segment

# from scalene import scalene_profiler

DEVICE = "cpu"

incoming_beam = ParticleBeam.from_astra("FEBE.astra")
beam_energy = incoming_beam.energy
# attempt to downsample the beam
raw_beam = incoming_beam.to_xyz_pxpypz()
indeces = np.random.choice(
    np.arange(raw_beam.shape[0]), size=int(raw_beam.shape[0] / 10), replace=False
)
downsampled_beam = raw_beam[indeces]
incoming_beam = ParticleBeam.from_xyz_pxpypz(downsampled_beam, energy=beam_energy)

# incoming_beam = ParticleBeam.from_twiss(num_particles=1000000,
#                                             beta_x=1.0, beta_y=1.0,
#                                             alpha_x=0.0, alpha_y=0.0,
#                                             emittance_x=1e-6, emittance_y=1e-6,
#                                             energy=1e9)

# incoming_beam.plot_2d_distribution("x", "y")
# plt.show()
lattice = Segment.from_elegant("FEBE.lte", name="febe")
lattice.to_lattice_json("FEBE.json")
#
# screens = []
# i = 0
# for ele in lattice.elements:
#     if isinstance(ele, Screen):
#         if i % 4 == 0:
#             screens.append(ele)
#         i += 1

# print(f"Found {len(screens)} screens in the lattice.")
# Turn profiling on
# scalene_profiler.start()
lattice.track(incoming_beam)
lattice.plot_overview(incoming_beam)
plt.show()

TESLA_PER_METER = 20
MAX_CURRENT = 94.5

normalised_power = torch.tensor(
    np.arange(-1, 1, 0.1, dtype=np.float32)
)  # np.arange(-1, 1, 0.1)
lattice.cla_s07_mag_quad_07.k1 = (
    300 * (normalised_power * TESLA_PER_METER) / 250
)  # 17 is T/m
lattice.track(incoming_beam)
print("done! plotting...")
# plot all screens

screens = lattice.cla_s07_dia_scr_03.reading
fig, ax = plt.subplots(
    math.floor(screens.shape[0] / 5) + 1,
    math.floor(screens.shape[0] / 5),
    figsize=(20, 20),
)
ax = ax.flatten()
# ax = [ax]

for i, screen in enumerate(screens):
    ax[i].imshow(screen)
    ax[i].set_title(f"{normalised_power[i] * MAX_CURRENT:.2f} A")
    ax[i].set_aspect("equal")
# fig.tight_layout()
# scalene_profiler.stop()
plt.show()
