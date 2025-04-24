import matplotlib.pyplot as plt

from cheetah import ParticleBeam, Screen, Segment

# from scalene import scalene_profiler

DEVICE = "cuda"

incoming_beam = ParticleBeam.from_astra("FEBE.astra").linspaced(10000)
lattice = Segment.from_elegant("FEBE.lte", name="febe")

screens = []
for ele in lattice.elements:
    if isinstance(ele, Screen):
        screens.append(ele)

print(f"Found {len(screens)} screens in the lattice.")
# Turn profiling on
# scalene_profiler.start()
lattice.plot_overview(incoming_beam)
lattice.track(incoming_beam)
# plot all screens
fig, ax = plt.subplots(
    int(len(screens) ** 0.5) + 1, int(len(screens) ** 0.5) + 1, figsize=(200, 200)
)
ax = ax.flatten()
for i, screen in enumerate(screens):
    ax[i].imshow(screen.reading)
    ax[i].set_title(screen.name)
    ax[i].set_aspect("equal")
fig.tight_layout()
# scalene_profiler.stop()
plt.show()
