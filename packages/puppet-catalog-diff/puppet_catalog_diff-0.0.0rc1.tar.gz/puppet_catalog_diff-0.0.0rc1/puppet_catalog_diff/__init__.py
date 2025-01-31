#!/usr/bin/env python3


import argparse
import difflib
import io
import json
import sys

import ruamel.yaml


yaml = ruamel.yaml.YAML()


def main():
    parser = argparse.ArgumentParser(description="Puppet Catalog Diff")

    parser.add_argument(
        "--old",
        dest="old",
        required=True,
    )

    parser.add_argument(
        "--new",
        dest="new",
        required=True,
    )

    args = parser.parse_args()

    try:
        old = _load_file(args.old)
        new = _load_file(args.new)
        _diff = diff(old, new)
        yaml.dump(_diff, sys.stdout)
        sys.exit(0)
    except PuppetCatalogDiffError as err:
        print(err)
        sys.exit(1)


class PuppetCatalogDiffError(Exception):
    pass


def _extract_resources(data) -> dict:
    resources = {}
    for item in data.get("resources", []):
        resource_type = item.get("type")
        resource_title = item.get("title")
        if resource_type and resource_title:
            resources[f"[{resource_type}]{resource_title}"] = item.get("parameters", {})
    return resources


def _load_file(_file: str) -> dict:
    try:
        with open(_file) as f:
            if _file.endswith(".json"):
                try:
                    return json.load(f)
                except json.decoder.JSONDecodeError:
                    raise PuppetCatalogDiffError(f"{_file} Invalid JSON")
            elif _file.endswith(".yaml"):
                try:
                    return yaml.load(f)
                except ruamel.yaml.YAMLError:
                    raise PuppetCatalogDiffError(f"{_file} Invalid YAML")
            else:
                raise PuppetCatalogDiffError(
                    f"{_file} Invalid file type, can only be JSON or YAML"
                )
    except OSError as err:
        raise PuppetCatalogDiffError(f"{_file} {err}")


def _generate_diff(old, new):
    buff_old = io.BytesIO()
    yaml.dump(old, buff_old)
    buff_old.seek(0)
    buff_new = io.BytesIO()
    yaml.dump(new, buff_new)
    buff_new.seek(0)
    return list(
        difflib.unified_diff(
            buff_old.read().decode("utf-8").splitlines(),
            buff_new.read().decode("utf-8").splitlines(),
            lineterm="",
        )
    )


def diff(old: dict, new: dict) -> dict:
    old = _extract_resources(old)
    new = _extract_resources(new)
    added = {k: new[k] for k in new if k not in old}
    removed = {k: old[k] for k in old if k not in new}
    changed = {
        k: _generate_diff(old[k], new[k]) for k in old if k in new and old[k] != new[k]
    }

    return {
        "added": added,
        "changed": changed,
        "removed": removed,
    }


if __name__ == "__main__":
    main()
