import matplotlib.pyplot as plt

from cheetah import ParticleBeam, Screen, Segment

# from scalene import scalene_profiler

DEVICE = "cpu"

incoming_beam = ParticleBeam.from_astra("FEBE.astra")
# incoming_beam.plot_2d_distribution("x", "y")
# plt.show()
lattice = Segment.from_elegant("FEBE.lte", name="febe")
lattice.to_lattice_json("FEBE.json")
screens = []
i = 0
for ele in lattice.elements:
    if isinstance(ele, Screen):
        if i % 4 == 0:
            screens.append(ele)
        i += 1

print(f"Found {len(screens)} screens in the lattice.")
# Turn profiling on
# scalene_profiler.start()
lattice.plot_overview(incoming_beam)
lattice.track(incoming_beam)
print("done! plotting...")
# plot all screens
fig, ax = plt.subplots(5, 5, figsize=(20, 20))
ax = ax.flatten()
# ax = [ax]
for i, screen in enumerate(screens):
    ax[i].imshow(screen.reading)
    ax[i].set_title(screen.name)
    ax[i].set_aspect("equal")
fig.tight_layout()
# scalene_profiler.stop()
plt.show()
