#!/usr/bin/env python3
""" utility for generating documentation of this repo """
import argparse
import sys
from typing import Any, Dict, Final, List, Union

from ruamel.yaml import YAML

CELL_SEP: Final = " | "
INPUTS_KEYPATH: Final = "on.workflow_call.inputs"
SECRETS_KEYPATH: Final = "on.workflow_call.secrets"


def get_keypath(obj: Dict, keypath_str: str, delimiter: str = ".") -> Any:
    """
    given a deeply nested object and a delimited keypath, retrieve the deep
    value at that keypath
    """
    keypath: List[str] = keypath_str.split(delimiter)
    sub_obj: Any = obj
    key: Union[str, int]
    for depth, key in enumerate(keypath):
        try:
            if isinstance(sub_obj, list):
                key = int(key)
            sub_obj = sub_obj[key]
        except KeyError:
            raise KeyError(
                f"unable to resolve keypath '{keypath_str}'; failed to "
                f"retrieve '{key}' component (depth: {depth})"
            ) from None
    return sub_obj


def read_yaml(path: str, encoding: str = "utf-8") -> Any:
    """
    load the yaml file at the given path and return its parsed contents
    """
    yaml = YAML()
    with open(path, "rt", encoding=encoding) as yml_in:
        return yaml.load(yml_in)


def print_heading(fields: List[str]):
    """
    directly prints a markdown table heading for the given list of fields
    """
    print(CELL_SEP.join(fields))
    print(CELL_SEP.join(["-" * len(f) for f in fields]))


def print_leaf(data: Any, fields: List[str]):
    """
    directly prints a markdown table of the given data structure with the given headings
    """
    print(f"\n### {fields[0].capitalize()}s\n")
    # print a markdown table to document the inputs of the given workflow
    print_heading(fields)
    for item_name, item in data.items():
        cells = [item_name] + [str(item.get(k, "-")) for k in fields[1:]]
        print(CELL_SEP.join(cells))


def main() -> int:
    """
    entrypoint for direct execution; returns an integer suitable for use with sys.exit
    """

    argp = argparse.ArgumentParser(
        description=("utility for generating documentation of this repo"),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    argp.add_argument(
        "--debug",
        action="store_true",
        help="enable debug output",
    )
    argp.add_argument(
        "workflows",
        help="path(s) to the workflow files to report on",
        nargs="+",
    )
    args = argp.parse_args()

    k_input: Final = "input"
    k_secret: Final = "secret"
    k_default: Final = "default"
    k_description: Final = "description"
    k_required: Final = "required"
    k_type: Final = "type"
    inputs_headings: Final = [k_input, k_required, k_type, k_default, k_description]
    secrets_headings: Final = [k_secret, k_required, k_description]

    for workflow_file in args.workflows:
        workflow_data = read_yaml(workflow_file)
        inputs_data = get_keypath(workflow_data, INPUTS_KEYPATH)
        secrets_data = get_keypath(workflow_data, SECRETS_KEYPATH)

        # print a markdown table to document the inputs of the given workflow
        print_leaf(inputs_data, inputs_headings)

        # print a markdown table to document the secrets of the given workflow
        print_leaf(secrets_data, secrets_headings)

        print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
