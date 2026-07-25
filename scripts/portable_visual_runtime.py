#!/usr/bin/env python3
"""Portable image conversion, browser capture, and dependency bootstrap adapter.

Only the Python standard library is required to start this adapter. When a
browser or image converter is absent, the adapter can use a known operating
system package manager, re-discover the executable, and retry the requested
operation. It never downloads or executes an arbitrary binary URL.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Callable

BROWSER_CANDIDATES = (
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
    "chrome",
    "msedge",
    "microsoft-edge",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "chrome.exe",
    "msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
)
BROWSER_EXECUTION_PROFILES = (
    {
        "id": "headless_new",
        "arguments": ("--headless=new",),
        "purpose": "Chromium's current headless implementation.",
    },
    {
        "id": "headless_compatibility",
        "arguments": ("--headless",),
        "purpose": "A compatibility retry for Chromium-family builds that do not accept --headless=new.",
    },
)
CONVERTER_CANDIDATES = ("magick", "convert", "rsvg-convert", "inkscape")

DEPENDENCY_LABELS = {
    "browser": "Chromium-compatible browser",
    "image_converter": "image converter",
}

RunCommand = Callable[[list[str]], tuple[int, str, str]]
DiscoverExecutable = Callable[[tuple[str, ...], str | None], str | None]


def converter_candidates() -> tuple[str, ...]:
    # Windows convert.exe is a disk utility, not ImageMagick. Require
    # ImageMagick's explicit magick command there unless a caller overrides.
    return ("magick", "rsvg-convert", "inkscape") if os.name == "nt" else CONVERTER_CANDIDATES


def emit(payload: dict, exit_code: int = 0) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    raise SystemExit(exit_code)


def discover_all(candidates: tuple[str, ...], override: str | None = None) -> tuple[str, ...]:
    """Return distinct executable paths in deterministic priority order.

    An explicit override is an exact caller choice. It deliberately disables
    automatic fallback so a requested browser can be diagnosed without silently
    substituting another executable.
    """
    paths: list[str] = []
    candidates_to_check = (override,) if override else candidates
    for candidate in candidates_to_check:
        candidate_path = Path(candidate)
        if candidate_path.is_file() and os.access(candidate_path, os.X_OK):
            found = str(candidate_path)
        else:
            found = shutil.which(candidate)
        if not found:
            continue
        identity = os.path.normcase(os.path.realpath(found))
        if identity not in {os.path.normcase(os.path.realpath(path)) for path in paths}:
            paths.append(found)
    return tuple(paths)


def discover(candidates: tuple[str, ...], override: str | None = None) -> str | None:
    paths = discover_all(candidates, override)
    return paths[0] if paths else None


def run(command: list[str]) -> tuple[int, str, str]:
    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    return completed.returncode, completed.stdout, completed.stderr


def clip(value: str, limit: int = 2000) -> str:
    """Keep structured installation evidence useful without emitting huge logs."""
    return value if len(value) <= limit else f"{value[:limit]}\n... [truncated]"


def platform_name() -> str:
    if os.name == "nt":
        return "Windows"
    if sys.platform == "darwin":
        return "Darwin"
    return "Linux" if sys.platform.startswith("linux") else sys.platform


def command_exists(command: str) -> str | None:
    return shutil.which(command)


def is_privileged() -> bool:
    geteuid = getattr(os, "geteuid", None)
    return bool(geteuid and geteuid() == 0)


def package_manager_for(
    system_name: str,
    exists: Callable[[str], str | None] = command_exists,
) -> str | None:
    if system_name == "Darwin":
        return "brew" if exists("brew") else None
    if system_name == "Windows":
        return "winget" if exists("winget") else None
    if system_name == "Linux":
        for manager in ("apt-get", "dnf", "yum", "pacman", "apk"):
            if exists(manager):
                return manager
    return None


def package_commands(dependency: str, manager: str) -> list[list[str]]:
    """Return package-manager commands as argv lists, never shell strings."""
    if dependency not in DEPENDENCY_LABELS:
        raise ValueError(f"Unsupported dependency: {dependency}")
    packages = {
        "brew": {
            "browser": ["brew", "install", "--cask", "google-chrome"],
            "image_converter": ["brew", "install", "imagemagick"],
        },
        "apt-get": {
            "browser": ["apt-get", "install", "-y", "chromium"],
            "image_converter": ["apt-get", "install", "-y", "imagemagick"],
        },
        "dnf": {
            "browser": ["dnf", "install", "-y", "chromium"],
            "image_converter": ["dnf", "install", "-y", "ImageMagick"],
        },
        "yum": {
            "browser": ["yum", "install", "-y", "chromium"],
            "image_converter": ["yum", "install", "-y", "ImageMagick"],
        },
        "pacman": {
            "browser": ["pacman", "-Sy", "--noconfirm", "chromium"],
            "image_converter": ["pacman", "-Sy", "--noconfirm", "imagemagick"],
        },
        "apk": {
            "browser": ["apk", "add", "--no-cache", "chromium"],
            "image_converter": ["apk", "add", "--no-cache", "imagemagick"],
        },
        "winget": {
            "browser": [
                "winget",
                "install",
                "--exact",
                "--id",
                "Google.Chrome",
                "--accept-package-agreements",
                "--accept-source-agreements",
                "--disable-interactivity",
            ],
            "image_converter": [
                "winget",
                "install",
                "--exact",
                "--id",
                "ImageMagick.ImageMagick",
                "--accept-package-agreements",
                "--accept-source-agreements",
                "--disable-interactivity",
            ],
        },
    }
    return [packages[manager][dependency]]


def installation_plan(
    dependency: str,
    *,
    system_name: str | None = None,
    exists: Callable[[str], str | None] = command_exists,
    privileged: bool | None = None,
) -> dict:
    """Build a safe, inspectable package-manager plan for one dependency."""
    system_name = system_name or platform_name()
    privileged = is_privileged() if privileged is None else privileged
    manager = package_manager_for(system_name, exists)
    base = package_commands(dependency, manager) if manager else []
    manual_commands = list(base)
    automatic_commands = list(base)
    needs_privilege = system_name == "Linux" and manager in {"apt-get", "dnf", "yum", "pacman", "apk"}
    can_attempt = bool(manager)
    reason = None
    manual_execution_context = "Run these commands in a normal terminal."

    if needs_privilege and not privileged:
        if exists("sudo"):
            manual_commands = [["sudo", *command] for command in base]
            manual_execution_context = "Run these commands in an interactive terminal that can request administrator permission."
            # -n makes a missing sudo grant fail immediately instead of hanging
            # an agent in an invisible password prompt. The manual plan remains
            # available for an interactive terminal.
            automatic_commands = [["sudo", "-n", *command] for command in base]
        else:
            automatic_commands = []
            can_attempt = False
            manual_execution_context = "Open an administrator/root shell, then run these commands."
            reason = "Administrator permission is required, but sudo is unavailable."

    if not manager:
        reason = f"No supported package manager was found for {system_name}."

    return {
        "dependency": dependency,
        "dependency_label": DEPENDENCY_LABELS[dependency],
        "system": system_name,
        "package_manager": manager,
        "automatic_commands": automatic_commands,
        "manual_install_commands": manual_commands,
        "manual_execution_context": manual_execution_context,
        "can_attempt": can_attempt,
        "reason": reason,
    }


def installation_guidance(plan: dict) -> dict:
    """Expose exactly what a user needs to inspect, approve, or run manually."""
    return {
        "dependency": plan["dependency"],
        "dependency_label": plan["dependency_label"],
        "system": plan["system"],
        "package_manager": plan["package_manager"],
        "manual_install_commands": plan["manual_install_commands"],
        "manual_execution_context": plan["manual_execution_context"],
        "after_install": "Run the same visual-authoring-runtime command again. The adapter also retries automatically after a successful install.",
        "safety_boundary": "Only a known OS package manager is used. No arbitrary binary URL is downloaded or executed.",
    }


def ensure_dependency(
    dependency: str,
    candidates: tuple[str, ...],
    override: str | None,
    *,
    auto_install: bool,
    dry_run: bool = False,
    system_name: str | None = None,
    exists: Callable[[str], str | None] = command_exists,
    privileged: bool | None = None,
    runner: RunCommand = run,
    discoverer: DiscoverExecutable = discover,
) -> tuple[str | None, dict]:
    """Discover, install if permitted, re-discover, then return structured state."""
    found = discoverer(candidates, override)
    if found:
        return found, {
            "state": "already_available",
            "dependency": dependency,
            "path": found,
            "auto_install_attempted": False,
        }

    plan = installation_plan(
        dependency,
        system_name=system_name,
        exists=exists,
        privileged=privileged,
    )
    guidance = installation_guidance(plan)
    if not auto_install:
        return None, {
            "status": "dependency_installation_required",
            "auto_install_attempted": False,
            "reason": "Automatic tool installation is disabled.",
            "guidance": guidance,
        }
    if not plan["can_attempt"]:
        return None, {
            "status": "dependency_installation_unavailable",
            "auto_install_attempted": False,
            "reason": plan["reason"],
            "guidance": guidance,
        }
    if dry_run:
        return None, {
            "status": "dependency_installation_planned",
            "auto_install_attempted": False,
            "reason": "Dry run only; no package-manager command was executed.",
            "guidance": guidance,
        }

    attempts = []
    for command in plan["automatic_commands"]:
        code, stdout, stderr = runner(command)
        attempts.append(
            {
                "command": command,
                "exit_code": code,
                "stdout": clip(stdout),
                "stderr": clip(stderr),
            }
        )
        if code != 0:
            found = discoverer(candidates, override)
            if found:
                return found, {
                    "state": "installed_and_verified",
                    "dependency": dependency,
                    "path": found,
                    "auto_install_attempted": True,
                    "attempts": attempts,
                    "guidance": guidance,
                }
            return None, {
                "status": "dependency_installation_failed",
                "auto_install_attempted": True,
                "reason": "The package-manager command did not complete successfully.",
                "attempts": attempts,
                "guidance": guidance,
            }

    found = discoverer(candidates, override)
    if found:
        return found, {
            "state": "installed_and_verified",
            "dependency": dependency,
            "path": found,
            "auto_install_attempted": True,
            "attempts": attempts,
            "guidance": guidance,
        }
    return None, {
        "status": "dependency_installation_failed",
        "auto_install_attempted": True,
        "reason": "Package installation completed, but the required executable was not discoverable.",
        "attempts": attempts,
        "guidance": guidance,
    }


def auto_install_enabled(args: argparse.Namespace) -> bool:
    return not getattr(args, "no_auto_install", False) and os.environ.get(
        "VISUAL_AUTHORING_AUTO_INSTALL_TOOLS",
        "1",
    ) != "0"


def probe() -> dict:
    browser = discover(BROWSER_CANDIDATES, os.environ.get("VISUAL_AUTHORING_BROWSER"))
    converter = discover(converter_candidates(), os.environ.get("VISUAL_AUTHORING_IMAGE_CONVERTER"))
    return {
        "status": "dependencies_ready" if browser and converter else "partial",
        "python": sys.version.split()[0],
        "browser": browser,
        "image_converter": converter,
        "capabilities": {
            "image_conversion": bool(converter),
            "web_capture": bool(browser),
            "dom_text_assertion": bool(browser),
            "image_generation": False,
        },
        "execution_readiness": {
            "image_conversion": "not_verified",
            "web_capture": "not_verified",
            "dom_text_assertion": "not_verified",
        },
        "capability_interpretation": "capabilities reports executable discovery only. Run convert-image or capture-web to verify the requested operation.",
        "remediation": {
            "command": "visual-authoring-runtime bootstrap",
            "environment_opt_out": "VISUAL_AUTHORING_AUTO_INSTALL_TOOLS=0",
            "claim": "bootstrap uses only known OS package managers and re-discovers the executable after installation.",
        },
        "claim_boundary": "This probe observes local executables only. It does not prove a successful capture or conversion, accessibility, usability, comprehension, behavior change, or release approval.",
    }


def terminate_process(process: subprocess.Popen) -> None:
    """Stop a headless browser once its requested artifact has been observed."""
    if process.poll() is not None:
        return
    try:
        if os.name == "posix":
            os.killpg(process.pid, signal.SIGTERM)
        else:
            process.terminate()
        process.wait(timeout=2)
    except (OSError, subprocess.TimeoutExpired):
        try:
            if os.name == "posix":
                os.killpg(process.pid, signal.SIGKILL)
            else:
                process.kill()
        except OSError:
            pass


def run_until_file(command: list[str], output: Path, timeout_seconds: float = 20) -> tuple[int, str, str]:
    """Run a browser only until it writes the requested screenshot."""
    process = subprocess.Popen(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=(os.name == "posix"),
    )
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if output.is_file() and output.stat().st_size > 0:
            terminate_process(process)
            stdout, stderr = process.communicate()
            return 0, stdout, stderr
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            return process.returncode, stdout, stderr
        time.sleep(0.1)
    terminate_process(process)
    stdout, stderr = process.communicate()
    return 124, stdout, stderr


def dump_dom(command: list[str], timeout_seconds: float = 20) -> tuple[int, str, str]:
    """Collect a complete DOM dump without relying on browser process exit."""
    with tempfile.NamedTemporaryFile(prefix="visual-authoring-dom-", delete=False) as stream:
        dom_path = Path(stream.name)
    try:
        with dom_path.open("w", encoding="utf-8") as stdout:
            process = subprocess.Popen(
                command,
                text=True,
                stdout=stdout,
                stderr=subprocess.PIPE,
                start_new_session=(os.name == "posix"),
            )
        deadline = time.monotonic() + timeout_seconds
        while time.monotonic() < deadline:
            dom = dom_path.read_text(encoding="utf-8", errors="replace")
            if "</html>" in dom.lower():
                terminate_process(process)
                _, stderr = process.communicate()
                return 0, dom, stderr
            if process.poll() is not None:
                _, stderr = process.communicate()
                return process.returncode, dom, stderr
            time.sleep(0.1)
        terminate_process(process)
        _, stderr = process.communicate()
        return 124, dom_path.read_text(encoding="utf-8", errors="replace"), stderr
    finally:
        dom_path.unlink(missing_ok=True)


def process_evidence(returncode: int) -> dict:
    """Normalize Popen return codes so a signal is not mistaken for an exit code."""
    payload = {
        "returncode": returncode,
        "exit_code": returncode if returncode >= 0 else None,
        "signal": None,
    }
    if returncode < 0:
        signal_number = -returncode
        try:
            signal_name = signal.Signals(signal_number).name
        except ValueError:
            signal_name = f"SIGNAL_{signal_number}"
        payload["signal"] = {"number": signal_number, "name": signal_name}
    return payload


def browser_command_evidence(command: list[str]) -> list[str]:
    """Keep diagnostics reproducible without retaining deleted temporary paths."""
    redacted = []
    for argument in command:
        if argument.startswith("--user-data-dir="):
            redacted.append("--user-data-dir=<temporary-profile>")
        elif argument.startswith("--screenshot="):
            redacted.append("--screenshot=<temporary-output>")
        else:
            redacted.append(argument)
    return redacted


def browser_runtime_guidance() -> dict:
    return {
        "reason": "A Chromium-compatible executable was discovered, but it did not complete both local screenshot and DOM capture.",
        "next_actions": [
            "Review attempts, then resolve the recorded browser runtime error and rerun the same capture command.",
            "Pass --browser <known-good-executable> when a specific compatible browser should be tested without automatic substitution.",
            "Use a host-provided browser adapter only when that host permits the target URL, and record its screenshot plus DOM/state evidence separately.",
        ],
        "installation_boundary": "A discovered but non-executing browser is a runtime failure, not a missing dependency. Package-manager installation is not repeated solely for this condition.",
        "host_policy_boundary": "Do not bypass a host browser's URL policy or substitute an unrelated browser-control mechanism after that policy blocks the target.",
    }


def execute_browser_capture(
    browser_paths: tuple[str, ...],
    url: str,
    output: Path,
    width: str,
    height: str,
    contains: list[str],
    *,
    run_until_file_fn: Callable[[list[str], Path], tuple[int, str, str]] = run_until_file,
    dump_dom_fn: Callable[[list[str]], tuple[int, str, str]] = dump_dom,
) -> dict:
    """Attempt deterministic browser/profile combinations and retain bounded evidence.

    A screenshot is copied to the requested output only after its matching DOM
    assertion also succeeds. This avoids leaving a partial image that could be
    mistaken for verified target-surface evidence.
    """
    attempts = []
    output.parent.mkdir(parents=True, exist_ok=True)
    for browser in browser_paths:
        for profile in BROWSER_EXECUTION_PROFILES:
            with tempfile.TemporaryDirectory(prefix="visual-authoring-browser-") as profile_dir:
                screenshot_path = Path(profile_dir) / "capture.png"
                base = [
                    browser,
                    *profile["arguments"],
                    "--disable-gpu",
                    "--hide-scrollbars",
                    "--no-first-run",
                    "--no-default-browser-check",
                    "--disable-background-networking",
                    "--disable-component-update",
                    "--disable-extensions",
                    "--disable-sync",
                    "--noerrdialogs",
                    f"--user-data-dir={profile_dir}",
                    f"--window-size={width},{height}",
                ]
                screenshot_command = base + [f"--screenshot={screenshot_path}", url]
                attempt = {
                    "browser": browser,
                    "profile": profile["id"],
                    "profile_purpose": profile["purpose"],
                    "screenshot": {"command": browser_command_evidence(screenshot_command)},
                }
                try:
                    screenshot_code, stdout, stderr = run_until_file_fn(screenshot_command, screenshot_path)
                except OSError as error:
                    attempt["status"] = "browser_invocation_error"
                    attempt["screenshot"].update(
                        {
                            "runtime_error": f"{type(error).__name__}: {error}",
                            "artifact_written": False,
                        }
                    )
                    attempts.append(attempt)
                    continue

                screenshot_written = screenshot_path.is_file() and screenshot_path.stat().st_size > 0
                attempt["screenshot"].update(
                    {
                        "process": process_evidence(screenshot_code),
                        "stdout": clip(stdout),
                        "stderr": clip(stderr),
                        "artifact_written": screenshot_written,
                    }
                )
                if screenshot_code != 0 or not screenshot_written:
                    attempt["status"] = "screenshot_failed"
                    attempts.append(attempt)
                    continue

                dom_command = base + ["--dump-dom", url]
                attempt["dom"] = {"command": browser_command_evidence(dom_command)}
                try:
                    dom_code, dom, dom_stderr = dump_dom_fn(dom_command)
                except OSError as error:
                    attempt["status"] = "dom_invocation_error"
                    attempt["dom"].update({"runtime_error": f"{type(error).__name__}: {error}"})
                    attempts.append(attempt)
                    continue

                missing = [value for value in contains if value not in dom]
                attempt["dom"].update(
                    {
                        "process": process_evidence(dom_code),
                        "stderr": clip(dom_stderr),
                        "missing_assertions": missing,
                    }
                )
                if dom_code != 0 or missing:
                    attempt["status"] = "dom_assertion_failed"
                    attempts.append(attempt)
                    continue

                try:
                    shutil.copy2(screenshot_path, output)
                except OSError as error:
                    attempt["status"] = "output_write_failed"
                    attempt["output_write_error"] = f"{type(error).__name__}: {error}"
                    attempts.append(attempt)
                    return {
                        "status": "capture_output_write_failed",
                        "adapter": "portable_visual_runtime",
                        "operation": "capture_web",
                        "url": url,
                        "viewport": f"{width}x{height}",
                        "browser_candidates": list(browser_paths),
                        "attempts": attempts,
                        "claim_boundary": "The browser produced a temporary screenshot, but the requested output path could not be written. No target-surface evidence was retained at that output path.",
                    }

                attempt["status"] = "pass_local"
                attempts.append(attempt)
                return {
                    "status": "pass_local",
                    "adapter": "portable_visual_runtime",
                    "operation": "capture_web",
                    "browser": browser,
                    "browser_execution_profile": profile["id"],
                    "url": url,
                    "viewport": f"{width}x{height}",
                    "screenshot": str(output),
                    "contains_assertions": contains,
                    "missing_assertions": [],
                    "attempts": attempts,
                    "claim_boundary": "A screenshot and DOM text assertion prove a local render observation only; they do not prove accessibility, usability, preference, comprehension, behavior change, or release approval.",
                }

    return {
        "status": "browser_runtime_failed",
        "adapter": "portable_visual_runtime",
        "operation": "capture_web",
        "url": url,
        "viewport": f"{width}x{height}",
        "contains_assertions": contains,
        "browser_candidates": list(browser_paths),
        "attempts": attempts,
        "manual_runtime_guidance": browser_runtime_guidance(),
        "claim_boundary": "No screenshot plus DOM assertion completed. Browser executable discovery and failed process attempts do not prove target-surface rendering, accessibility, usability, preference, comprehension, behavior change, or release approval.",
    }


def convert_image(args: argparse.Namespace) -> None:
    source = Path(args.source).resolve()
    output = Path(args.output).resolve()
    if not source.is_file():
        emit({"status": "blocked_missing_input", "source": str(source)}, 2)
    output.parent.mkdir(parents=True, exist_ok=True)
    if source.suffix.lower() == output.suffix.lower():
        shutil.copy2(source, output)
        emit(
            {
                "status": "pass_local",
                "adapter": "portable_visual_runtime",
                "operation": "copy_same_format",
                "output": str(output),
            }
        )

    converter, installation = ensure_dependency(
        "image_converter",
        converter_candidates(),
        args.converter,
        auto_install=auto_install_enabled(args),
    )
    if not converter:
        emit(installation, 1)
    name = Path(converter).name
    if name == "rsvg-convert":
        command = [converter, str(source), "-o", str(output)]
    elif name == "inkscape":
        command = [converter, str(source), "--export-filename", str(output)]
    else:
        command = [converter, str(source), str(output)]
    code, stdout, stderr = run(command)
    if code != 0 or not output.is_file():
        emit(
            {
                "status": "fail_local",
                "adapter": "portable_visual_runtime",
                "command": command,
                "exit_code": code,
                "stdout": stdout,
                "stderr": stderr,
                "dependency_installation": installation,
            },
            1,
        )
    emit(
        {
            "status": "pass_local",
            "adapter": "portable_visual_runtime",
            "operation": "convert_image",
            "command": command,
            "output": str(output),
            "dependency_installation": installation,
            "claim_boundary": "A local conversion proves only that the resulting file was written by this adapter. It does not prove visual quality, accessibility, comprehension, behavior change, or release approval.",
        }
    )


def capture_web(args: argparse.Namespace) -> None:
    browser_override = args.browser or os.environ.get("VISUAL_AUTHORING_BROWSER")
    browser, installation = ensure_dependency(
        "browser",
        BROWSER_CANDIDATES,
        browser_override,
        auto_install=auto_install_enabled(args),
    )
    output = Path(args.output).resolve()
    if not browser:
        emit(installation, 1)
    try:
        width, height = args.viewport.lower().split("x", 1)
    except ValueError:
        emit({"status": "invalid_viewport", "value": args.viewport}, 2)
    if not width.isdigit() or not height.isdigit():
        emit({"status": "invalid_viewport", "value": args.viewport}, 2)
    # An explicit CLI or environment override is an exact diagnostic target.
    # With normal discovery, attempt all compatible local browsers in priority
    # order before reporting a runtime failure.
    browser_paths = (browser,) if browser_override else discover_all(BROWSER_CANDIDATES)
    if browser not in browser_paths:
        browser_paths = (browser, *browser_paths)
    payload = execute_browser_capture(
        browser_paths,
        args.url,
        output,
        width,
        height,
        args.contains,
    )
    payload["dependency_installation"] = installation
    emit(payload, 0 if payload["status"] == "pass_local" else 1)


def bootstrap(args: argparse.Namespace) -> None:
    selected = args.dependency or ["browser", "image_converter"]
    reports = {}
    available = {}
    for dependency in selected:
        candidates = BROWSER_CANDIDATES if dependency == "browser" else converter_candidates()
        override_name = "VISUAL_AUTHORING_BROWSER" if dependency == "browser" else "VISUAL_AUTHORING_IMAGE_CONVERTER"
        found, report = ensure_dependency(
            dependency,
            candidates,
            os.environ.get(override_name),
            auto_install=auto_install_enabled(args),
            dry_run=args.dry_run,
        )
        reports[dependency] = report
        if found:
            available[dependency] = found
    status = "ready" if len(available) == len(selected) else "dependency_installation_incomplete"
    emit(
        {
            "status": status,
            "adapter": "portable_visual_runtime",
            "operation": "bootstrap",
            "available": available,
            "dependencies": reports,
            "claim_boundary": "Bootstrap proves only executable discovery after a local installation attempt. It does not prove the requested operation, accessibility, usability, comprehension, behavior change, or release approval.",
        },
        0 if status == "ready" else 1,
    )


def self_test() -> None:
    """Exercise installation plans and retry logic without network or installs."""
    plan_checks = []
    for system, manager in (("Darwin", "brew"), ("Linux", "apt-get"), ("Windows", "winget")):
        exists = lambda name, expected=manager: f"/mock/{name}" if name == expected else None
        plan = installation_plan(
            "browser",
            system_name=system,
            exists=exists,
            privileged=True,
        )
        assert plan["package_manager"] == manager
        assert plan["automatic_commands"]
        plan_checks.append({"system": system, "package_manager": manager})

    installed = {"value": False}

    def fake_discover(_candidates: tuple[str, ...], _override: str | None) -> str | None:
        return "/mock/google-chrome" if installed["value"] else None

    def fake_run(_command: list[str]) -> tuple[int, str, str]:
        installed["value"] = True
        return 0, "installed", ""

    fake_exists = lambda name: "/mock/brew" if name == "brew" else None
    found, installed_report = ensure_dependency(
        "browser",
        BROWSER_CANDIDATES,
        None,
        auto_install=True,
        system_name="Darwin",
        exists=fake_exists,
        privileged=True,
        runner=fake_run,
        discoverer=fake_discover,
    )
    assert found == "/mock/google-chrome"
    assert installed_report["state"] == "installed_and_verified"

    _, disabled_report = ensure_dependency(
        "image_converter",
        converter_candidates(),
        None,
        auto_install=False,
        system_name="Darwin",
        exists=fake_exists,
        privileged=True,
        discoverer=lambda _candidates, _override: None,
    )
    assert disabled_report["status"] == "dependency_installation_required"
    assert "blocked_missing_" not in json.dumps(disabled_report)

    _, unavailable_report = ensure_dependency(
        "image_converter",
        converter_candidates(),
        None,
        auto_install=True,
        system_name="Unknown",
        exists=lambda _name: None,
        privileged=True,
        discoverer=lambda _candidates, _override: None,
    )
    assert unavailable_report["status"] == "dependency_installation_unavailable"
    assert "blocked_missing_" not in json.dumps(unavailable_report)

    def fake_dom(_command: list[str]) -> tuple[int, str, str]:
        return 0, "<html><body>Capture ready</body></html>", ""

    with tempfile.TemporaryDirectory(prefix="visual-authoring-runtime-self-test-") as test_dir:
        test_root = Path(test_dir)

        def profile_retry_run(command: list[str], output: Path) -> tuple[int, str, str]:
            if "--headless=new" in command:
                return -int(signal.SIGABRT), "", "mock first-profile abort"
            output.write_bytes(b"mock-png")
            return 0, "mock screenshot", ""

        profile_retry = execute_browser_capture(
            ("/mock/google-chrome",),
            "https://example.test/profile-retry",
            test_root / "profile-retry.png",
            "1440",
            "1000",
            ["Capture ready"],
            run_until_file_fn=profile_retry_run,
            dump_dom_fn=fake_dom,
        )
        assert profile_retry["status"] == "pass_local"
        assert profile_retry["browser_execution_profile"] == "headless_compatibility"
        assert len(profile_retry["attempts"]) == 2
        assert profile_retry["attempts"][0]["screenshot"]["process"]["signal"]["name"] == "SIGABRT"

        def candidate_retry_run(command: list[str], output: Path) -> tuple[int, str, str]:
            if command[0] == "/mock/browser-a":
                return -int(signal.SIGABRT), "", "mock candidate-a abort"
            output.write_bytes(b"mock-png")
            return 0, "mock screenshot", ""

        candidate_retry = execute_browser_capture(
            ("/mock/browser-a", "/mock/browser-b"),
            "https://example.test/candidate-retry",
            test_root / "candidate-retry.png",
            "1440",
            "1000",
            ["Capture ready"],
            run_until_file_fn=candidate_retry_run,
            dump_dom_fn=fake_dom,
        )
        assert candidate_retry["status"] == "pass_local"
        assert candidate_retry["browser"] == "/mock/browser-b"
        assert len(candidate_retry["attempts"]) == 3

        def always_fail_run(_command: list[str], _output: Path) -> tuple[int, str, str]:
            return -int(signal.SIGABRT), "", "mock browser abort"

        browser_failure = execute_browser_capture(
            ("/mock/google-chrome",),
            "https://example.test/all-fail",
            test_root / "all-fail.png",
            "1440",
            "1000",
            ["Capture ready"],
            run_until_file_fn=always_fail_run,
            dump_dom_fn=fake_dom,
        )
        assert browser_failure["status"] == "browser_runtime_failed"
        assert len(browser_failure["attempts"]) == len(BROWSER_EXECUTION_PROFILES)
        assert browser_failure["attempts"][0]["screenshot"]["process"]["signal"]["name"] == "SIGABRT"

    emit(
        {
            "status": "pass_local",
            "adapter": "portable_visual_runtime",
            "operation": "self_test",
            "plan_checks": plan_checks,
            "retry_check": installed_report["state"],
            "disabled_check": disabled_report["status"],
            "unavailable_check": unavailable_report["status"],
            "browser_profile_retry_check": profile_retry["status"],
            "browser_candidate_retry_check": candidate_retry["status"],
            "browser_runtime_failure_check": browser_failure["status"],
            "claim_boundary": "This is a deterministic adapter self-test with mocked package-manager calls. It does not install software or prove a browser, converter, or user outcome on this host.",
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    probe_parser = subparsers.add_parser("probe", help="discover local browser and image converter")
    probe_parser.add_argument(
        "--install-missing",
        action="store_true",
        help="attempt package-manager installation for missing browser/converter",
    )
    bootstrap_parser = subparsers.add_parser(
        "bootstrap",
        help="install missing supported browser/converter through a known package manager",
    )
    bootstrap_parser.add_argument(
        "--dependency",
        choices=("browser", "image_converter"),
        action="append",
        help="limit bootstrap to one dependency; repeatable",
    )
    bootstrap_parser.add_argument("--dry-run", action="store_true", help="show the installation plan without running it")
    bootstrap_parser.add_argument(
        "--no-auto-install",
        action="store_true",
        help="return installation guidance without running package-manager commands",
    )
    convert = subparsers.add_parser("convert-image", help="convert a local image; installs a missing supported converter by default")
    convert.add_argument("source")
    convert.add_argument("output")
    convert.add_argument("--converter")
    convert.add_argument(
        "--no-auto-install",
        action="store_true",
        help="return installation guidance instead of attempting installation",
    )
    capture = subparsers.add_parser("capture-web", help="capture a URL; installs a missing supported browser by default")
    capture.add_argument("url")
    capture.add_argument("output")
    capture.add_argument("--viewport", default="1440x1000")
    capture.add_argument("--contains", action="append", default=[], help="required text in dumped DOM; repeatable")
    capture.add_argument("--browser")
    capture.add_argument(
        "--no-auto-install",
        action="store_true",
        help="return installation guidance instead of attempting installation",
    )
    subparsers.add_parser("self-test", help="run deterministic dependency-bootstrap tests without network or installation")
    args = parser.parse_args()
    if args.command == "probe":
        if args.install_missing:
            bootstrap(
                argparse.Namespace(
                    dependency=None,
                    dry_run=False,
                    no_auto_install=False,
                )
            )
        emit(probe())
    if args.command == "bootstrap":
        bootstrap(args)
    if args.command == "self-test":
        self_test()
    if args.command == "convert-image":
        convert_image(args)
    capture_web(args)


if __name__ == "__main__":
    main()
