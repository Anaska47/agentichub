from __future__ import annotations

import json
import os
import shutil
import subprocess
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ToolStatus:
    name: str
    ok: bool
    detail: str


def collect_environment_status() -> list[ToolStatus]:
    return [
        command_status("python", ["python", "--version"]),
        command_status("node", ["node", "--version"]),
        command_status("npm", ["npm", "--version"]),
        command_status("git", ["git", "--version"]),
        java_status(),
        android_sdk_status(),
        adb_status(),
    ]


def command_status(name: str, command: list[str]) -> ToolStatus:
    resolved = resolve_command(command[0])
    if not resolved:
        return ToolStatus(name=name, ok=False, detail="missing or not runnable")
    command = [resolved, *command[1:]]
    try:
        completed = subprocess.run(command, capture_output=True, text=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        return ToolStatus(name=name, ok=False, detail="missing or not runnable")
    detail = (completed.stdout or completed.stderr).strip() or "available"
    return ToolStatus(name=name, ok=True, detail=detail)


def java_status() -> ToolStatus:
    java_home = os.environ.get("JAVA_HOME")
    java_cmd = shutil.which("java")
    if not java_home and not java_cmd:
        return ToolStatus(name="java", ok=False, detail="JAVA_HOME missing and java not in PATH")

    status = command_status("java", ["java", "-version"])
    detail = status.detail
    if java_home:
        detail = f"{detail} | JAVA_HOME={java_home}"
    return ToolStatus(name="java", ok=status.ok, detail=detail)


def android_sdk_status() -> ToolStatus:
    sdk_root = os.environ.get("ANDROID_SDK_ROOT") or os.environ.get("ANDROID_HOME")
    if not sdk_root:
        return ToolStatus(name="android-sdk", ok=False, detail="ANDROID_SDK_ROOT or ANDROID_HOME missing")
    return ToolStatus(name="android-sdk", ok=True, detail=sdk_root)


def adb_status() -> ToolStatus:
    adb = shutil.which("adb")
    if not adb:
        return ToolStatus(name="adb", ok=False, detail="adb not found in PATH")
    return command_status("adb", ["adb", "version"])


def resolve_command(command: str) -> str | None:
    direct = shutil.which(command)
    if direct:
        return direct
    if os.name != "nt":
        return None
    for suffix in (".cmd", ".exe", ".bat"):
        candidate = shutil.which(command + suffix)
        if candidate:
            return candidate
    return None


def render_doctor_report() -> str:
    statuses = collect_environment_status()
    lines = []
    for status in statuses:
        icon = "OK" if status.ok else "MISSING"
        lines.append(f"[{icon}] {status.name}: {status.detail}")
    return "\n".join(lines)


def render_doctor_json() -> str:
    return json.dumps([asdict(item) for item in collect_environment_status()], indent=2)
