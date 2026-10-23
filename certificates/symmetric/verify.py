"""Replay the compact symmetric witness exactly. Python 3.10+, stdlib only."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parent.parent


def local_module(name):
    key = "_symmetric_public_" + name
    spec = importlib.util.spec_from_file_location(key, HERE / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    sys.modules[key] = module
    spec.loader.exec_module(module)
    return module


construction = local_module("construction")
independent = local_module("independent")
runtime = local_module("runtime")
BOUND = Fraction(471404576987, 500000000000)


def load(path):
    return json.loads(
        Path(path).read_text(encoding="utf-8"),
        object_pairs_hook=independent.object_pairs,
        parse_float=independent.forbidden,
        parse_constant=independent.forbidden,
    )


def inventory():
    manifest = load(HERE / "MANIFEST.json")
    seen = set()
    for member in manifest["files"]:
        name = member["path"]
        relative = Path(name)
        if (
            not isinstance(name, str)
            or relative.is_absolute()
            or ".." in relative.parts
            or relative.as_posix() != name
            or name in seen
        ):
            raise ValueError("unsafe or duplicate package manifest path")
        seen.add(name)
        path = (HERE / relative).resolve()
        if not path.is_relative_to(HERE.resolve()):
            raise ValueError("package manifest path escapes its directory")
        if (
            path.stat().st_size != member["bytes"]
            or runtime.digest(path) != member["sha256"]
        ):
            raise ValueError("package manifest identity mismatch: " + name)
    required = {
        "WITNESS.json",
        "construction.py",
        "independent.py",
        "runtime.py",
        "verify.py",
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
            for name in ("construction", "independent", "runtime", "verify")
        },
        "witness_sha256": runtime.digest(witness_path),
        "array_sha256": runtime.digest(array_path) if array_path else None,
        "export_path": str(Path(export_path).resolve()) if export_path else None,
    }


def canonical_row(values, denominator):
    return json.dumps(
        [str(Fraction(value, denominator)) for value in values], separators=(",", ":")
    ).encode()


def export_chunks(replay, k, values, denominator):
    directory = replay.directory / "chunks"
    directory.mkdir(exist_ok=True)
    path = directory / f"{k:04d}.json"
    content = canonical_row(values, denominator)
    if path.exists() and path.read_bytes() == content:
        return
    runtime.atomic(path, content)


def assemble_export(data, replay, path):
    n, length, _, _ = construction.parse(data)
    metadata = {
        "format_version": independent.SCHEMA,
        "block_size": 2 * n,
        "window_length": length,
        "declared_bound": str(BOUND),
        "mixing": [str(independent.weight(n, k)) for k in range(1, n + 1)],
        "kernels": [
            [
                str(Fraction(1, 2 * k)) if n - k <= j < n + k else "0"
                for j in range(2 * n)
            ]
            for k in range(1, n + 1)
        ],
    }
    path = Path(path)
    expected = data["provenance"]["declared_dense_sha256"]
    if path.exists():
        if runtime.digest(path) != expected:
            raise ValueError("export destination already contains different bytes")
        return expected
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".partial")
    with temporary.open("wb") as stream:
        stream.write(
            json.dumps(metadata, separators=(",", ":")).encode()[:-1] + b',"boundary":['
        )
        for k in range(1, n + 1):
            replay.heartbeat("export_assembly", k)
            chunk = replay.directory / "chunks" / f"{k:04d}.json"
            if k > 1:
                stream.write(b",")
            with chunk.open("rb") as row:
                for block in iter(lambda: row.read(1 << 20), b""):
                    stream.write(block)
        stream.write(b"]}\n")
        stream.flush()
        os.fsync(stream.fileno())
    actual = runtime.digest(temporary)
    if actual != expected:
        raise ValueError(
            "export bytes differ from the independently archived stronger copy"
        )
    os.replace(temporary, path)
    return actual


def replay_witness(witness_path, state_dir=None, export_path=None):
    data = load(witness_path)
    construction.parse(data)
    if export_path is not None and state_dir is None:
        raise ValueError(
            "--export needs a repository-local --state-dir for resumable chunks"
        )
    session = runtime.Replay(state_dir, identity(witness_path, export_path=export_path))
    try:
        parameters = construction.repair(data, session)
        n, length = parameters[:2]
        saved = session.stage("verification")
        start = saved["next_k"] if saved else 1
        callback = None
        if export_path is not None:

            def callback(k, values, denominator):
                export_chunks(session, k, values, denominator)

        result = independent.check_rows(
            n,
            length,
            BOUND,
            construction.rows(*parameters, start=start),
            session,
            callback,
        )
        if result["accepted"] and export_path is not None:
            result["export_sha256"] = assemble_export(data, session, export_path)
        if result["accepted"]:
            if runtime.digest(witness_path) != session.identity["witness_sha256"]:
                raise ValueError("compact witness changed during exact verification")
            session.finish()
        return result
    finally:
        session.close()


def check_array(path, witness_path, state_dir=None):
    session = runtime.Replay(state_dir, identity(witness_path, array_path=path))
    try:
        n, length = independent.metadata(
            path, BOUND, lambda: session.heartbeat("array_metadata")
        )
        saved = session.stage("verification")
        start = saved["next_k"] if saved else 1
        result = independent.check_rows(
            n, length, BOUND, independent.boundary_rows(path, n, length, start), session
        )
        actual_sha = runtime.digest(path)
        if actual_sha != session.identity["array_sha256"]:
            raise ValueError("actual certificate changed during exact verification")
        if result["accepted"]:
            session.finish()
        result["array_sha256"] = actual_sha
        return result
    finally:
        session.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("witness", nargs="?", type=Path, default=HERE / "WITNESS.json")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--export", type=Path)
    mode.add_argument("--check-array", type=Path)
    checkpoint = parser.add_mutually_exclusive_group()
    checkpoint.add_argument(
        "--state-dir", type=Path, default=REPOSITORY / "tmp" / "symmetric_replay"
    )
    checkpoint.add_argument("--no-checkpoint", action="store_true")
    args = parser.parse_args()
    try:
        inventory()
        state = None if args.no_checkpoint else args.state_dir
        if state is not None:
            resolved = state.resolve()
            # An explicitly provided repository-local state directory may be in
            # another local checkout. System temporary storage is never chosen.
            if resolved == REPOSITORY:
                raise ValueError(
                    "state directory must be a dedicated repository-local folder"
                )
        if args.check_array:
            result = check_array(args.check_array, args.witness, state)
        else:
            result = replay_witness(args.witness, state, args.export)
        if (
            args.witness.resolve() == (HERE / "WITNESS.json").resolve()
            and not args.check_array
        ):
            expected = load(HERE / "EXPECTED_RESULTS.json")
            compared = {
                key: value for key, value in result.items() if key != "export_sha256"
            }
            if compared != expected:
                raise ValueError(
                    "fresh exact result differs from the frozen public reference"
                )
    except (
        OSError,
        ValueError,
        TypeError,
        KeyError,
        IndexError,
        OverflowError,
    ) as error:
        print(
            json.dumps({"accepted": False, "input_error": str(error)}, sort_keys=True)
        )
        return 2
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0 if result["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
