import os

from blue_objects import file, README

from blue_cemetery import NAME, VERSION, ICON, REPO_NAME
from blue_cemetery.list import list_of_experiments


items = [
    "[`{}`](#) [![image]({})]({}) {}".format(
        experiment_name,
        experiment.get(
            "marquee",
            "https://github.com/kamangir/assets/raw/main/blue-plugin/marquee.png?raw=true",
        ),
        experiment["url"],
        experiment.get("title", ""),
    )
    for experiment_name, experiment in list_of_experiments.items()
]


def build():
    return README.build(
        items=items,
        path=os.path.join(file.path(__file__), ".."),
        ICON=ICON,
        NAME=NAME,
        VERSION=VERSION,
        REPO_NAME=REPO_NAME,
    )
