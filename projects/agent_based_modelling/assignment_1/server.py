from mesa.visualization import (
    CanvasGrid,
    ModularServer,
    Slider,
)

from projects.agent_based_modelling.assignment_1.forest_fire import (
    ForestFire,
    Tree,
)


def forest_fire_portrayal(tree: Tree | None) -> dict | None:
    if tree is None:
        return None

    x, y = tree.pos
    return dict(
        Shape="rect",
        x=x,
        y=y,
        w=1,
        h=1,
        Color=tree.state.color(),
        Filled=True,
        Layer=0,
    )


canvas_element = CanvasGrid(forest_fire_portrayal, 100, 100, 700, 700)

model_params = {
    "height": 100,
    "width": 100,
    "p": Slider("Tree density", 0.65, 0.01, 1.0, 0.01),
    "wind_x": Slider("Wind X", 0, 0, 2, 1),
    "wind_y": Slider("Wind Y", 0, -2, 2, 1),
}

server = ModularServer(ForestFire, [canvas_element], "Forest Fire", model_params)

server.launch(open_browser=True)
