"""Replay the exact finite-grid certificate. Python 3.10+, stdlib only."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parent.parent
BOUND = Fraction(11785113371, 12500000000)


def local_module(name):
    key = "_finite_grid_public_" + name
    spec = importlib.util.spec_from_file_location(key, HERE / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    sys.modules[key] = module
    spec.loader.exec_module(module)
    return module


reconstruction = local_module("reconstruction")
runtime = local_module("runtime")


def load(path):
    data, _ = reconstruction._read(Path(path))
    return data


def inventory():
    manifest = load(HERE / "MANIFEST.json")
    if not isinstance(manifest.get("files"), list):
        raise ValueError("package manifest must contain a file inventory")
    seen = set()
    for member in manifest["files"]:
        if not isinstance(member, dict) or set(member) != {"path", "bytes", "sha256"}:
            raise ValueError("invalid package manifest record")
        name = member["path"]
        if not isinstance(name, str):
            raise ValueError("package manifest path must be a string")
        relative = Path(name)
        if (
            relative.is_absolute()
            or ".." in relative.parts
            or relative.as_posix() != name
            or name in seen
        ):
            raise ValueError("unsafe or duplicate package manifest path")
        seen.add(name)
        path = (HERE / relative).resolve()
        if not path.is_relative_to(HERE):
            raise ValueError("package manifest path escapes its directory")
        if (
            type(member["bytes"]) is not int
            or member["bytes"] < 0
            or path.stat().st_size != member["bytes"]
            or runtime.digest(path) != member["sha256"]
        ):
            raise ValueError("package manifest identity mismatch: " + name)
    required = {
        "WITNESS.json",
        "reconstruction.py",
        "runtime.py",
        "verify.py",
        "arraycheck.py",
        "exporter.py",
        "EXPECTED_RESULTS.json",
        "README.md",
        "PROOF.md",
        "PROVENANCE.md",
    }
    if not required <= seen:
        raise ValueError("package manifest omits a required public input")


def identity(witness_path, array_path=None, export_path=None):
    return {
        "code": {
            name: runtime.digest(HERE / (name + ".py"))
            for name in (
                "reconstruction",
                "runtime",
                "verify",
                "arraycheck",
                "exporter",
            )
        },
        "witness_sha256": runtime.digest(witness_path),
        "array_sha256": runtime.digest(array_path) if array_path is not None else None,
        "export_path": str(Path(export_path).resolve()) if export_path is not None else None,
    }


def _unchanged(path, expected):
    if runtime.digest(path) != expected:
        raise ValueError("verification input changed during exact replay")


def replay_witness(witness_path, state_dir=None, export_path=None):
    witness_path = Path(witness_path)
    if export_path is not None and state_dir is None:
        raise ValueError("--export-gzip needs a dedicated repository-local --state-dir")
    session = runtime.Replay(state_dir, identity(witness_path, export_path=export_path))
    try:
        report = reconstruction.verify(
            witness_path,
            state=session.stage("compact"),
            progress=lambda state: session.save("compact", state),
            guard=lambda: session.heartbeat("compact"),
        )
        _unchanged(witness_path, session.identity["witness_sha256"])
        if report["accepted"] and export_path is not None:
            exporter = local_module("exporter")
            report["export"] = exporter.export(
                load(witness_path),
                export_path,
                session.directory / "export_work",
                state=session.stage("export"),
                progress=lambda state: session.save("export", state),
                guard=lambda: session.heartbeat("export"),
            )
            _unchanged(witness_path, session.identity["witness_sha256"])
        if report["accepted"]:
            session.finish()
        return report
    finally:
        session.close()


def check_array(path, witness_path, state_dir=None):
    witness_path, path = Path(witness_path), Path(path)
    data = load(witness_path)
    target = Fraction(data["target"])
    expected = None
    if witness_path.resolve() == (HERE / "WITNESS.json").resolve():
        if target != BOUND:
            raise ValueError("bundled witness has the wrong stronger declaration")
        expected_path = HERE / "EXPECTED_RESULTS.json"
        expected = load(expected_path) if expected_path.is_file() else None
    session = runtime.Replay(state_dir, identity(witness_path, path))
    try:
        arraycheck = local_module("arraycheck")
        arguments = {}
        if expected is not None:
            if "array_sha256" in expected:
                arguments["expected_sha"] = expected["array_sha256"]
            if "array_raw_sha256" in expected:
                arguments["expected_raw_sha"] = expected["array_raw_sha256"]
        report = arraycheck.verify(
            path,
            expected_bound=target,
            state=session.stage("arrays"),
            progress=lambda state: session.save("arrays", state),
            guard=lambda: session.heartbeat("arrays"),
            **arguments,
        )
        for key in ("V", "a", "b", "ab"):
            if Fraction(report[key]) != Fraction(data[key]):
                raise ValueError("actual array and compact witness disagree on " + key)
        _unchanged(witness_path, session.identity["witness_sha256"])
        _unchanged(path, session.identity["array_sha256"])
        if report["accepted"]:
            session.finish()
        return report
    finally:
        session.close()


def compare_reference(report, expected):
    """Compare explicit scalar reference fields after fresh exact arithmetic."""
    fields = ("accepted", "V", "a", "b", "ab", "cover_count", "all_covers_exactly_one")
    for key in fields:
        if key not in expected or report[key] != expected[key]:
            raise ValueError("fresh exact result differs from expected " + key)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("witness", nargs="?", type=Path, default=HERE / "WITNESS.json")
    operation = parser.add_mutually_exclusive_group()
    operation.add_argument("--check-array", type=Path, metavar="PATH")
    operation.add_argument("--export-gzip", type=Path, metavar="PATH")
    checkpoints = parser.add_mutually_exclusive_group()
    checkpoints.add_argument(
        "--state-dir", type=Path, default=REPOSITORY / "tmp" / "finite_grid_replay"
    )
    checkpoints.add_argument("--no-checkpoint", action="store_true")
    args = parser.parse_args(argv)
    try:
        inventory()
        bundled = args.witness.resolve() == (HERE / "WITNESS.json").resolve()
        if bundled and load(args.witness)["target"] != str(BOUND):
            raise ValueError("bundled witness has the wrong stronger declaration")
        state = None if args.no_checkpoint else args.state_dir
        if state is not None and state.resolve() in (REPOSITORY, HERE):
            raise ValueError("state directory must be a dedicated repository-local folder")
        if args.check_array:
            report = check_array(args.check_array, args.witness, state)
        else:
            report = replay_witness(args.witness, state, args.export_gzip)
        if bundled:
            compare_reference(report, load(HERE / "EXPECTED_RESULTS.json"))
    except (
        OSError,
        ValueError,
        TypeError,
        KeyError,
        IndexError,
        OverflowError,
        ArithmeticError,
    ) as error:
        print(json.dumps({"accepted": False, "input_error": str(error)}, sort_keys=True))
        return 2
    print(json.dumps(report, sort_keys=True, indent=2))
    return 0 if report["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
