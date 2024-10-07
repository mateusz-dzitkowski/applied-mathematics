from mesa.visualization import (
    CanvasGrid,
    ChartModule,
    ModularServer,
    PieChartModule,
    Slider,
)

from projects.agent_based_modelling.assignment_1.forest_fire import (
    ForestFire,
    Tree,
    TreeState,
)


def forest_fire_portrayal(tree: Tree):
    if tree is None:
        return
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
    (x, y) = tree.pos
    portrayal["x"] = x
    portrayal["y"] = y
    portrayal["Color"] = tree.state.color()
    return portrayal


canvas_element = CanvasGrid(forest_fire_portrayal, 100, 100, 500, 500)
tree_chart = ChartModule([{"Label": state, "Color": state.color()} for state in [TreeState.FINE, TreeState.BURNING, TreeState.BURNED_DOWN]])
pie_chart = PieChartModule([{"Label": state, "Color": state.color()} for state in [TreeState.FINE, TreeState.BURNING, TreeState.BURNED_DOWN]])

model_params = {
    "height": 100,
    "width": 100,
    "p": Slider("Tree density", 0.65, 0.01, 1.0, 0.01),
    "wind_x": Slider("Wind X", 0, 0, 2, 1),
    "wind_y": Slider("Wind Y", 0, -2, 2, 1),
}

server = ModularServer(ForestFire, [canvas_element, tree_chart, pie_chart], "Forest Fire", model_params)

server.launch(open_browser=True)
