# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [5.0.0]

### Fixed

- **WiFi codes with special characters were wrong.** `qr_data` escaped the SSID
  and password in place, so every call escaped them again. The command line
  reads the property twice, which meant the code written to disk carried a
  doubly-escaped payload and would not connect. `qr_data` is now pure.
- **Writing to an existing file could destroy it.** `--output notes.txt`
  truncated the file before Pillow rejected the extension, leaving it empty and
  still exiting 0. The image is now rendered in memory and moved into place
  atomically; an existing file is untouched unless the write succeeds.
- **`--cc` and `--bcc` shared a `-None` short flag.** Fields without an alias
  produced the literal option `-None`, and the second registration won, so
  `-None` silently set `bcc`. Short flags are only generated when a field
  defines an alias.
- **Links without a scheme were rejected.** The URL validator was never
  registered, because `@classmethod` wrapped `@field_validator` instead of the
  other way around. `makeqr link example.com` works again.
- **A WiFi password without `--security` was silently dropped**, producing a
  code for an open network.
- `MakeQR.save()` no longer leaves a zero-byte file behind when the format
  cannot be resolved.
- `MakeQR` accepts an error-correction level given as a string.

### Added

- Open WiFi networks are marked `T:nopass`, as the MECARD format expects.
- `py.typed`, so type hints reach downstream users.
- `CHANGELOG.md`, `LICENSE` and `SECURITY.md`.
- Help text for every option, a description for every command, and a README
  that documents all seven commands and the global options.

### Changed

- **Requires Python 3.11 or newer** (was 3.9). This unblocks Pillow 12.3, which
  carries a security fix that could not be applied under the old floor.
- WiFi passwords are `SecretStr` and are masked in verbose output.
- `--quiet` is the primary spelling; `--quite` still works.
- Errors are raised as click exceptions instead of calling `sys.exit`.
- Commands are discovered from `QRDataModel` subclasses, and click option types
  are inferred from field annotations, so the models no longer import click.
- Packaging moved to uv and PEP 621; the version is read from package metadata.
- The Docker image is built on Python 3.13, runs as a non-root user and is
  published for arm64 as well.

### Removed

- The `--print` / `-p` flag, which never did anything.
- `makeqr.typing`. The base model is now the public `makeqr.QRDataModel`;
  `QRDataModelType` remains as an alias.
- `makeqr.version`. Use `makeqr.__version__`.

### Breaking

- Python 3.11 is the minimum supported version.
- Boolean options are flags: use `--hidden`, not `--hidden true`.
- `--security` without a password is now a validation error.
- A password without `--security` now defaults to WPA rather than being ignored.
- `--print` / `-p` and `makeqr.typing` are gone.

## [4.4.1] and earlier

See the [releases page](https://github.com/shpaker/makeqr/releases).

[5.0.0]: https://github.com/shpaker/makeqr/releases/tag/5.0.0
[4.4.1]: https://github.com/shpaker/makeqr/releases/tag/4.4.1
