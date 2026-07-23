import math

from typing import Any


def discrete_compact_rank(data: list[Any]) -> list[int]:
    unique_data = sorted(set(data))
    data_map = {value: index for index, value in enumerate(unique_data, 1)}
    return [data_map[value] for value in data]


def discrete_average_rank(data: list[Any]) -> list[float]:
    unique_data = sorted(set(data))

    occurrence_count = {value: 0 for value in unique_data}
    for value in data:
        occurrence_count[value] += 1

    data_map = {}
    cumulative_rank = 0
    for value in unique_data:
        count = occurrence_count[value]
        average_rank = (cumulative_rank + 1 + cumulative_rank + count) / 2
        data_map[value] = average_rank
        cumulative_rank += count

    return [data_map[value] for value in data]


def calc_pearson(x: list[float], y: list[float]) -> float:
    ax = sum(x) / len(x)
    ay = sum(y) / len(y)
    xx = [xi - ax for xi in x]
    yy = [yi - ay for yi in y]
    sx = math.sqrt(sum(xi * xi for xi in xx))
    sy = math.sqrt(sum(yi * yi for yi in yy))
    return sum(xx[i] * yy[i] for i in range(len(x))) / (sx * sy)


def calc_spearman(x: list[float], y: list[float]) -> float:
    rx = discrete_average_rank(x)
    ry = discrete_average_rank(y)
    return calc_pearson(rx, ry)
