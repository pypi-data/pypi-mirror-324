# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import os
import sys
import zipfile
from functools import lru_cache
from pathlib import Path
from typing import List

import blessed
import requests
from rich.progress import (BarColumn, DownloadColumn, Progress,
                           TaskProgressColumn, TextColumn, TimeRemainingColumn)

from trt_cloud.constants import (TRTC_PREBUILT_ENGINE_ORG,
                                 TRTC_PREBUILT_ENGINE_TEAM)


def download_file(
    url: str,
    output_filepath: str,
    headers: dict = None,
    quiet: bool = False
) -> str:
    response = requests.get(url, allow_redirects=True, stream=True, headers=headers)
    if not response.ok:
        raise RuntimeError(f"Failed to download {url}", response)

    total_length = int(response.headers["Content-Length"])
    chunk_size = 2 ** 20  # 1MB

    # Create a Progress bar
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        DownloadColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        disable=quiet,
    ) as progress:

        # Create a Task object to represent the progress of the download
        task = progress.add_task(f"Downloading to {os.path.basename(output_filepath)}", total=total_length)

        with open(output_filepath, "wb") as output:
            for content in response.iter_content(chunk_size):
                if content:
                    output.write(content)
                    progress.update(task, advance=len(content))

    return output_filepath


def check_and_display_eula(license_path: str, eula_name: str, license_preamble: str = "",
                           license_path_format_string="Please find a copy of the license here: {}.") -> bool:
    if os.path.exists(license_path):
        with open(license_path, "r", encoding="utf8") as f:
            license_text = f.read()
    else:
        raise ValueError(f"{eula_name} not found. Must agree to EULA to proceed.")
    print(f"\n{eula_name}\n{license_preamble}{license_text}"
          f"\n{license_path_format_string.format(license_path)}\n")
    user_input = input(
        f"Do you agree to the {eula_name}? (yes/no) "
    ).lower().strip()

    user_agreed = user_input in {"y", "yes"}
    if not user_agreed:
        raise ValueError(f"You must agree to the {eula_name} to proceed.")

    return user_agreed

def upload_file(
    url: str,
    filepath: str,
    headers: dict = None,
):
    total_length = os.stat(filepath).st_size
    chunk_size = 2 ** 20  # 1MB

    class ReadFileWithProgressBar(object):
        def __init__(self, filepath):
            self.file = open(filepath, "rb")
            self.total_length = os.stat(filepath).st_size
            self.progress = Progress(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                DownloadColumn(),
                TaskProgressColumn(),
                TimeRemainingColumn(),
            )
            self.progress.start()
            self.task = self.progress.add_task(f"Uploading {filepath}", total=self.total_length)

        def read(self, size=chunk_size):
            chunk = self.file.read(size)
            self.progress.update(self.task, advance=len(chunk))
            if len(chunk) == 0:
                self.progress.stop()
                self.file.close()
            return chunk

        def __len__(self):
            return total_length

    resp = requests.put(
        url,
        data=ReadFileWithProgressBar(filepath),
        headers=headers,
    )
    return resp

def extract_onnx_file(tmpdir, onnx_zip) -> str:
    with zipfile.ZipFile(onnx_zip, "r") as zip:
        zip.extractall(tmpdir)
    onnx_files_in_zip = list(Path(tmpdir).rglob('*.onnx'))
    if not onnx_files_in_zip:
        raise ValueError(f"No .onnx files found in {onnx_zip}.")
    if len(onnx_files_in_zip) > 1:
        raise ValueError(
            f"Multiple .onnx files found in archive: {onnx_files_in_zip}"
        )
    return str(onnx_files_in_zip[0])

def find_dir_with_file(root_dir, filename):
    dirs: List[str] = list()
    for root, _, files in os.walk(root_dir):
        if filename in files:
            dirs.append(root)
    if len(dirs) == 0:
        raise FileNotFoundError(f"Cannot find {filename} in input dir.")
    if len(dirs) > 1:
        raise FileNotFoundError(f"Found multiple files named {filename} in input dir.")
    return dirs[0]


def add_verbose_flag_to_parser(parser):
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase logging verbosity.")


@lru_cache()
def get_ngc_model_org():
    return os.environ.get("TRTC_ENGINE_ORG", "") or TRTC_PREBUILT_ENGINE_ORG


@lru_cache()
def get_ngc_model_team():
    return os.environ.get("TRTC_ENGINE_TEAM", None) or TRTC_PREBUILT_ENGINE_TEAM

class Display:
    class DummyTerminal:
        # Use when the terminal is not available
        width = 100
        def move_x(self, x): return ""
        def move_up(self, x): return ""
        def clear_eol(self): return ""
        def clear_eos(self): return ""
        def bold(self, x): return x

    def __init__(self):
        if sys.stdout.isatty():
            self.term = blessed.Terminal()
        else:
            # Terminal is not available.
            self.term = Display.DummyTerminal()

        self.num_lines = 1
        self.width = self.term.width - 4
        print()

    def print(self, text, heading=""):
        msg_len = len(text) + len(heading) + 2

        # Shorten long messages so they fit into one line.
        if msg_len > self.width:
            half = self.width // 2 - 5
            text = f"{text[:half]}...{text[-half:]}"

        # Pad messages so they are exactly 'width' long
        msg_len = len(text) + len(heading) + 2
        text += ' ' * max(0, self.width - msg_len)

        to_print = self.term.move_x(0) + self.term.clear_eol() + '│ '
        if heading:
            to_print += self.term.bold(heading)
        to_print += text
        to_print += ' │'
        print(to_print)
        self.num_lines += 1

    def _print_bar(self, start, middle, end):
        print(self.term.move_x(0) + self.term.clear_eol() + start + middle * self.width + end)
        self.num_lines += 1

    def print_top_bar(self): self._print_bar("┌", "─", "┐")
    def print_middle_bar(self): self._print_bar("├", "─", "┤")
    def print_bottom_bar(self): self._print_bar("└", "─", "┘")

    def reset(self):
        print(self.term.move_up(self.num_lines) + self.term.clear_eos())
        self.num_lines = 1
        self.width = self.term.width - 4
