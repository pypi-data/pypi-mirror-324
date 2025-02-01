import os

from blue_objects import file, README
from blue_options.help.functions import get_help

from blue_sandbox import NAME, VERSION, ICON, REPO_NAME
from blue_sandbox.microsoft_building_damage_assessment import (
    README as microsoft_building_damage_assessment_README,
)
from blue_sandbox.list import list_of_experiments

items = [
    "{}[`{}`]({}) {} [![image]({})]({}) {}".format(
        experiment["ICON"],
        experiment_name,
        experiment["url"],
        experiment["status"],
        experiment["marquee"],
        experiment["url"],
        experiment["title"],
    )
    for experiment_name, experiment in list_of_experiments.items()
    if experiment_name != "template"
]


def build():
    return all(
        README.build(
            items=thing.get("items", []),
            cols=thing.get("cols", 2),
            path=os.path.join(file.path(__file__), thing["path"]),
            help_function=thing.get("help_function", None),
            ICON=ICON,
            NAME=NAME,
            VERSION=VERSION,
            REPO_NAME=REPO_NAME,
        )
        for thing in (
            [
                {
                    "items": items,
                    "path": "..",
                },
                {
                    "items": microsoft_building_damage_assessment_README.items,
                    "cols": len(
                        microsoft_building_damage_assessment_README.list_of_steps
                    ),
                    "path": "microsoft_building_damage_assessment",
                },
                {
                    "path": "cemetery",
                },
                {
                    "path": "sagesemseg",
                },
            ]
        )
    )
