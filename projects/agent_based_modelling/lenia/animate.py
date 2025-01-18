from projects.agent_based_modelling.lenia.lenia import Lenia
from matplotlib import pyplot as plt
from matplotlib import animation
from tqdm import tqdm


def animate_lenia(lenia: Lenia, steps: int, filename: str):
    fig, ax = plt.subplots(figsize=(8, 8), constrained_layout=True)
    ax.set_aspect("equal")

    img = ax.imshow(lenia.arr, cmap=plt.cm.gray_r)  # type: ignore

    def update(_: int):
        lenia.step()
        img.set_data(lenia.arr)

    def init():
        img.set_data(lenia.arr)

    animation.FuncAnimation(
        fig=fig,
        func=update,  # type: ignore
        init_func=init,  # type: ignore
        frames=tqdm(range(steps)),
        cache_frame_data=False,
    ).save(
        filename=filename,
        writer=animation.PillowWriter(fps=30),
    )
    plt.close()


if __name__ == "__main__":
    import numpy as np

    size = 100
    initial = np.zeros((size, size))
    initial[size // 2, size // 2] = 1
    initial[size // 2 + 1, size // 2] = 1
    initial[size // 2 - 1, size // 2] = 1
    initial[size // 2, size // 2 - 1] = 1
    initial[size // 2 + 1, size // 2 + 1] = 1

    gol = Lenia.game_of_life(initial=initial)
    animate_lenia(gol, 300, "gol.gif")
