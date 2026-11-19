#!/usr/bin/env python3
"""Synthetic outbound-network canary for an owned Linear Code sandbox.

The script sends only fixed, synthetic strings. It does not inspect the
environment, read files, or collect host/runtime metadata.
"""

from __future__ import annotations

import argparse
import sys
import urllib.parse
import urllib.request


CANARY_RECEIVER = "https://webhook.site/df2bab8d-ac3a-4ac1-97a2-59bb66db9e11"
TEST_ID = "linear-synthetic-network-20261119-153943"
SYNTHETIC_VALUE = "synthetic-canary-not-a-secret-20261119-153943"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        print("verification: FAIL (missing --check)")
        return 2

    query = urllib.parse.urlencode(
        {
            "test_id": TEST_ID,
            "event": "verify",
            "synthetic_value": SYNTHETIC_VALUE,
        }
    )
    req = urllib.request.Request(
        CANARY_RECEIVER + "?" + query,
        headers={"User-Agent": "linear-synthetic-network-canary/1.0"},
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            response.read(1024)
            status = response.status
    except Exception as exc:
        print(f"verification: FAIL ({exc.__class__.__name__})")
        return 2

    if 200 <= status < 300:
        print(f"verification: PASS (receiver_http={status})")
        return 0

    print(f"verification: FAIL (receiver_http={status})")
    return 2


if __name__ == "__main__":
    sys.exit(main())
