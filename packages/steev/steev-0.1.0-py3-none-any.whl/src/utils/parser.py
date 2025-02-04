import yaml


def parse_input(yaml_path: str) -> dict:
    """
    Parse the input arguments and return the additional arguments
    """

    if yaml_path:
        with open(yaml_path, "r") as f:
            additional_args = yaml.safe_load(f)
            if not isinstance(additional_args, dict):
                additional_args = dict(additional_args) if additional_args else {}
        return additional_args

    return {}
