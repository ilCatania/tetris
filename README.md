[![Build](https://github.com/ilCatania/tetris/actions/workflows/tetris.yml/badge.svg)](https://github.com/ilCatania/tetris/actions/workflows/tetris.yml)
[![codecov](https://codecov.io/gh/ilCatania/tetris/branch/master/graph/badge.svg?token=KA6FZ4GHTO)](https://codecov.io/gh/ilCatania/tetris)

Basic Tetris project
===================

A basic Tetris game simulator where pieces never rotate and are just dropped onto a grid. The grid provides methods to
add pieces and exposes its current height expressed as number of non-empty rows.

The game accepts sequences of Tetris pieces, one sequence per line, and will return the grid height once all the pieces
have been added to the grid. Pieces and positions can be specified in the following format:

```
Q2 T3 S6
```

where each letter identifies a Tetris piece with a specific shape:

* `Q` is the square
* `I` is the straight piece, laid out horizontally
* `T`, `Z`, `S`, `J`, `L` have the same shape as their letter

and the number represents the leftmost column occupied by this piece.

For example, the sequence above will result in a grid of height 3 and the following layout:

```
|          |
|   TTT    |
|  QQT  SS |
|  QQ  SS  |
------------
```

while the following sequence:

```
I0 I0 Q4 I6 I6
```

will result in an empty grid as two full lines will be eliminated.

# Running

The program requires python 3 (it was tested with version `3.8.5`) by checking out the project, then running:

```shell
$ python src/tetris/cmd.py
```

and it accepts alternatively:

* a single file name argument:

```shell
$ echo "Q1 Q3" > in.txt
$ python src/tetris/cmd.py in.txt
2
```

* sequences of pieces as arguments:

```shell
$ python src/tetris/cmd.py "Q0 Q2 Z0 I2 I6" "I3 Z2 S5"
4
3
```

* piped input

```shell
$ echo "Q1 Q3 Z0 Z2 T1" | python src/tetris/cmd.py
6
```

# Running tests

In order to run tests you will need `poetry` - it's also a good idea to make sure your `pip` is up to date:

```shell
python -m pip install --upgrade pip
pip install poetry
```

with `poetry` installed you can then run the tests locally:

```shell
poetry run pytest
```