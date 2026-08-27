# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 5.x     | yes       |
| < 5.0   | no        |

## Reporting a vulnerability

Please report security issues privately through
[GitHub security advisories](https://github.com/shpaker/makeqr/security/advisories/new)
rather than opening a public issue.

Include what you did, what happened, and the version you were running. You can
expect an initial response within a week.

## Note on passwords

`makeqr` takes WiFi passwords on the command line, so they land in your shell
history and in the process list. The QR code itself always encodes the password
in clear text — that is how the format works, and anyone who can scan the code
can read it.
