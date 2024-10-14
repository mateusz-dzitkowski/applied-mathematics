from functools import partial
from itertools import product
from multiprocessing import Pool
from typing import Any, Iterable

from pandas import DataFrame
from tqdm import tqdm

from .model import Model


def batch_run(
    cls: type[Model],
    params: dict[str, Any | Iterable[Any]],
    iterations: int = 1,
) -> DataFrame:
    runs_list = []
    run_id = 0
    for iteration in range(iterations):
        for kwargs in _make_model_kwargs(params):
            runs_list.append((run_id, iteration, kwargs))
            run_id += 1

    results: list[dict[str, Any]] = []

    with tqdm(total=len(runs_list)) as pbar, Pool() as p:
        for data in p.imap_unordered(partial(_process_func, cls), runs_list):
            results.extend(data)
            pbar.update()

    return DataFrame(data=results)


def _process_func(cls: type[Model], run: tuple[int, int, dict[str, Any]]) -> list[dict[str, Any]]:
    run_id, iteration, kwargs = run
    model = cls(**kwargs)
    return [
        {
            "run_id": run_id,
            "iteration": iteration,
            **kwargs,
            **model.run_and_collect(),
        }
    ]


def _make_model_kwargs(parameters: dict[str, Any | Iterable[Any]]) -> list[dict[str, Any]]:
    parameter_list = []
    for param, values in parameters.items():
        if isinstance(values, str):
            all_values = [(param, values)]
        else:
            try:
                all_values = [(param, value) for value in values]
            except TypeError:
                all_values = [(param, values)]
        parameter_list.append(all_values)
    all_kwargs = product(*parameter_list)
    kwargs_list = [dict(kwargs) for kwargs in all_kwargs]
    return kwargs_list
