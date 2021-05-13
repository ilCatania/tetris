import os
import subprocess
import tempfile


def run_cmd(*args):
    """Run the tetris command with the input arguments"""
    p = subprocess.run(["python", "src/tetris/cmd.py"] + list(args), capture_output=True, text=True)
    assert p.returncode == 0
    return p.stdout


def test_single_piece_input():
    assert run_cmd("I0") == "1\n"
    assert run_cmd("Q0") == "2\n"


def test_input_multiple_pieces():
    assert run_cmd("I0 I1 I2") == "3\n"
    assert run_cmd("Q0 S0 T2") == "4\n"


def test_input_multiple_sets():
    assert run_cmd("I0 I1 I2", "S0 Z2 I0") == "3\n4\n"
    assert run_cmd("Q0 Q2 Q4 Q6 Q8", "Q0 S0 T2") == "0\n4\n"


def test_file_input():
    f = tempfile.NamedTemporaryFile("w", delete=False)
    try:
        f.writelines(["I0 I1 I2\n", "S0 Z2 I0"])
        f.close()
        assert run_cmd(f.name) == "3\n4\n"
    finally:
        os.remove(f.name)
