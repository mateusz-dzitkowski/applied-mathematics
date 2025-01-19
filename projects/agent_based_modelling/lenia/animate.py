from matplotlib import animation
from matplotlib import pyplot as plt
from tqdm import tqdm

from projects.agent_based_modelling.lenia.lenia import Lenia


def animate_lenia(lenia: Lenia, steps: int, filename: str, fps: int = 30):
    fig, ax = plt.subplots(figsize=(8, 8), constrained_layout=True)
    ax.set_aspect("equal")

    img = ax.imshow(lenia.world.arr)

    def update(_: int):
        lenia.step()
        img.set_data(lenia.world.arr)

    def init():
        img.set_data(lenia.world.arr)

    animation.FuncAnimation(
        fig=fig,
        func=update,  # type: ignore
        init_func=init,  # type: ignore
        frames=tqdm(range(steps)),
        cache_frame_data=False,
    ).save(
        filename=filename,
        writer=animation.PillowWriter(fps=fps),
    )
    plt.close()
