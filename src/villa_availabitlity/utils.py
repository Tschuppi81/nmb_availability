import json
import os


def load_villa_data(path: str) -> list[dict]:
    """
    Load the villa data from the file and store it in the global variable.
    """
    if not os.path.exists(path):
        return []

    with open(path, 'r') as f:
        villas = json.load(f)

    return villas


def store_villa_data(path: str, data: list[dict]) -> None:
    """
    Store the villa data to the file.
    """
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)


def merge_villas(villas: list[dict], more_villas: list[dict]) -> list[dict]:
    """
    Merge the two lists of villas. If a villa from `more_villas` is already
    in `villas`, update the existing villa with the new data. If it's not,
    add it to `villas`.

    Parameters:
    villas (list[dict]): The original list of villas.
    more_villas (list[dict]): Additional villas to be merged.

    Returns:
    list[dict]: The merged list of villas.
    """

    for more_villa in more_villas:
        for villa in villas:
            if villa['name'] == more_villa['name']:
                villa.update(more_villa)
                break
    else:
        villas.append(more_villa)

    return villas
