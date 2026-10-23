"""Portable exact replay checkpoints; Python 3.10+ standard library only."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
import time
from pathlib import Path


def digest(path):
    result = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            result.update(chunk)
    return result.hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def object_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate replay checkpoint field")
        result[key] = value
    return result


def atomic(path, content):
    temporary = path.with_name(path.name + ".partial")
    with temporary.open("wb") as stream:
        stream.write(content)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


class Replay:
    """Persist only completed component units and emit ten-second heartbeats.

    Completed prior runs start fresh. An incomplete run resumes authenticated
    accumulators, not a saved success flag. Operators and exact array arithmetic
    still determine acceptance. Only unfinished export assembly restarts.
    """

    def __init__(self, directory, identity):
        self.directory = Path(directory) if directory is not None else None
        self.identity = identity
        self.state = {"identity": identity, "stages": {}, "complete": False}
        self.started = self.last_heartbeat = time.monotonic()
        self.lock = None
        if self.directory is None:
            return
        self.directory.mkdir(parents=True, exist_ok=True)
        self.lock = (self.directory / "replay.lock").open("a+b")
        try:
            if os.name == "nt":
                import msvcrt

                if self.lock.seek(0, 2) == 0:
                    self.lock.write(b"0")
                    self.lock.flush()
                self.lock.seek(0)
                msvcrt.locking(self.lock.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(self.lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as error:
            self.lock.close()
            self.lock = None
            raise ValueError("another process owns this replay directory") from error
        try:
            latest = self.directory / "latest.json"
            if latest.exists():
                saved = json.loads(
                    latest.read_text(encoding="utf-8"), object_pairs_hook=object_pairs
                )
                if not isinstance(saved, dict):
                    raise ValueError("replay checkpoint must be an object")
                checksum = saved.pop("checksum", None)
                if checksum != hashlib.sha256(canonical(saved)).hexdigest():
                    raise ValueError("replay checkpoint checksum mismatch")
                if (
                    set(saved) != {"identity", "stages", "complete"}
                    or not isinstance(saved["stages"], dict)
                    or type(saved["complete"]) is not bool
                ):
                    raise ValueError("invalid replay checkpoint envelope")
                if not saved["complete"] and saved["identity"] != identity:
                    raise ValueError("replay checkpoint code/input identity mismatch")
                if not saved["complete"]:
                    self.state = copy.deepcopy(saved)
        except Exception:
            self.close()
            raise

    def stage(self, name):
        return copy.deepcopy(self.state["stages"].get(name))

    def save(self, name, value):
        self.state["stages"][name] = copy.deepcopy(value)
        self.persist()
        self.heartbeat(name, value.get("next_k"))

    def persist(self):
        if self.directory is None:
            return
        latest = self.directory / "latest.json"
        if latest.exists():
            atomic(self.directory / "previous.json", latest.read_bytes())
        payload = copy.deepcopy(self.state)
        payload["checksum"] = hashlib.sha256(canonical(payload)).hexdigest()
        atomic(latest, canonical(payload) + b"\n")

    def heartbeat(self, stage, next_k=None, force=False):
        now = time.monotonic()
        if force or now - self.last_heartbeat >= 10:
            print(
                json.dumps(
                    {
                        "heartbeat": True,
                        "stage": stage,
                        "next_k": next_k,
                        "elapsed_seconds": round(now - self.started, 3),
                    },
                    sort_keys=True,
                ),
                file=sys.stderr,
                flush=True,
            )
            self.last_heartbeat = now

    def finish(self):
        self.state["complete"] = True
        self.persist()

    def close(self):
        if self.lock is not None:
            self.lock.close()
            self.lock = None
