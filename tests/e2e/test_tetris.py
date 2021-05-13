import os
import subprocess
import tempfile


def test_integration():
    _, tf = tempfile.mkstemp(suffix=".txt", text=True)
    try:
        p = subprocess.run(["tests/__data/run_e2e.sh", tf])
        assert p.returncode == 0
        with open(tf, "r") as actual, open("tests/__data/expected.txt", "r") as expected:
            assert actual.readlines() == expected.readlines()
    finally:
        os.remove(tf)
