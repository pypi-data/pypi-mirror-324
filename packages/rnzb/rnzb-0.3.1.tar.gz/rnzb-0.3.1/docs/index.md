# rnzb

[![Tests](https://img.shields.io/github/actions/workflow/status/Ravencentric/rnzb/tests.yml?label=tests)](https://github.com/Ravencentric/rnzb/actions/workflows/tests.yml)
[![Docs](https://img.shields.io/github/actions/workflow/status/Ravencentric/rnzb/docs.yml?label=docs)](https://github.com/Ravencentric/rnzb/actions/workflows/docs.yml)
[![Build](https://img.shields.io/github/actions/workflow/status/Ravencentric/rnzb/release.yml?label=build)](https://github.com/Ravencentric/rnzb/actions/workflows/release.yml)
![PyPI - Types](https://img.shields.io/pypi/types/rnzb)
![License](https://img.shields.io/pypi/l/rnzb?color=success)

[![PyPI - Latest Version](https://img.shields.io/pypi/v/rnzb?color=blue)](https://pypi.org/project/rnzb)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/rnzb)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/rnzb)

Python bindings to the [nzb-rs](https://crates.io/crates/nzb-rs) library - a [spec](https://sabnzbd.org/wiki/extra/nzb-spec) compliant parser for [NZB](https://en.wikipedia.org/wiki/NZB) files, written in Rust.

## Installation

`rnzb` is available on [PyPI](https://pypi.org/project/rnzb/), so you can simply use pip to install it.

```bash
pip install rnzb
```

## Usage

```py
from rnzb import Nzb

nzb = Nzb.from_file("big_buck_bunny.nzb")

print(f"{nzb.file.name} ({nzb.meta.category}) was posted on {nzb.file.posted_at} by {nzb.file.poster}.")
#> Big Buck Bunny - S01E01.mkv (TV) was posted on 2024-01-28 11:18:28+00:00 by John <nzb@nowhere.example>.

for file in nzb.files:
    print(file.name)
    #> Big Buck Bunny - S01E01.mkv
    #> Big Buck Bunny - S01E01.mkv.par2
    #> Big Buck Bunny - S01E01.mkv.vol00+01.par2
    #> Big Buck Bunny - S01E01.mkv.vol01+02.par2
    #> Big Buck Bunny - S01E01.mkv.vol03+04.par2
```

## Related projects

Considering this is the fourth library for parsing a file format that almost nobody cares about and lacks a formal specification, here's an overview to help you decide:

| Project                                                  | Description                 | Parser | Meta Editor |
| -------------------------------------------------------- | --------------------------- | ------ | ----------- |
| [`nzb`](https://pypi.org/project/nzb)                    | Original Python Library     | ✅     | ✅          |
| [`nzb-rs`](https://crates.io/crates/nzb-rs)              | Rust port of `nzb`          | ✅     | ❌          |
| [`rnzb`](https://pypi.org/project/nzb)                   | Python bindings to `nzb-rs` | ✅     | ❌          |
| [`nzb-parser`](https://www.npmjs.com/package/nzb-parser) | Javascript port of `nzb`    | ✅     | ❌          |

## Performance

Although [`nzb`](https://pypi.org/project/nzb) is already quite fast due to its use of the non-validating C-based [expat](https://docs.python.org/3/library/pyexpat.html) parser from Python's standard library, `rnzb` offers even better performance, being approximately 8 times faster than `nzb`.

```console
$ hyperfine --warmup 1 "python test_nzb.py" "python test_rnzb.py"
Benchmark 1: python test_nzb.py
  Time (mean ± σ):      6.306 s ±  0.075 s    [User: 5.992 s, System: 0.225 s]
  Range (min … max):    6.225 s …  6.478 s    10 runs

Benchmark 2: python test_rnzb.py
  Time (mean ± σ):     767.5 ms ±   3.4 ms    [User: 591.9 ms, System: 163.8 ms]
  Range (min … max):   762.2 ms … 772.7 ms    10 runs

Summary
  python test_rnzb.py ran
    8.22 ± 0.10 times faster than python test_nzb.py
```

The above benchmark was performed by looping over 10 random NZB files I had lying around. This benchmark isn't super scientific, but it gives a pretty good idea of the performance difference.

## Supported platforms

Refer to the following table for the platforms and Python versions for which `rnzb` publishes prebuilt wheels:

| Platform                            | CPython 3.9-3.13 | CPython 3.13 (t) | PyPy 3.9-3.10 |
| ----------------------------------- | ---------------- | ---------------- | ------------- |
| 🐧 Linux (`x86_64`, `glibc>=2.28`)  | ✅               | ✅               | ✅            |
| 🐧 Linux (`x86_64`, `musl>=1.2`)    | ✅               | ✅               | ✅            |
| 🐧 Linux (`aarch64`, `glibc>=2.28`) | ✅               | ✅               | ✅            |
| 🐧 Linux (`aarch64`, `musl>=1.2`)   | ✅               | ✅               | ✅            |
| 🪟 Windows (`x86`)                  | ✅               | ✅               | ❌            |
| 🪟 Windows (`x86_64`)               | ✅               | ✅               | ✅            |
| 🍏 macOS (`x86_64`)                 | ✅               | ✅               | ✅            |
| 🍏 macOS (`arm64`)                  | ✅               | ✅               | ✅            |

The library itself is not inherently tied to any specific platform or Python version. The available wheels are based on what can be (reasonably) built using GitHub Actions.

## Building from source

Building from source requires the [Rust toolchain](https://rustup.rs/) and [Python 3.9+](https://www.python.org/downloads/).

- With [`uv`](https://docs.astral.sh/uv/):

  ```bash
  git clone https://github.com/Ravencentric/rnzb
  cd rnzb
  uv build
  ```

- With [`pypa/build`](https://github.com/pypa/build):

  ```bash
  git clone https://github.com/Ravencentric/rnzb
  cd rnzb
  python -m build
  ```

## License

Licensed under either of:

- Apache License, Version 2.0 ([LICENSE-APACHE](https://github.com/Ravencentric/rnzb/blob/main/LICENSE-APACHE) or <https://www.apache.org/licenses/LICENSE-2.0>)
- MIT license ([LICENSE-MIT](https://github.com/Ravencentric/rnzb/blob/main/LICENSE-MIT) or <https://opensource.org/licenses/MIT>)

at your option.

## Contributing

Contributions are welcome! Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in the work by you, as defined in the Apache-2.0 license, shall be dual licensed as above, without any additional terms or conditions.
