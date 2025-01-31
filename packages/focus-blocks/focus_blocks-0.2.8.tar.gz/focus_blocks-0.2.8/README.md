# `fob`

[![Build & Test](https://github.com/tensorturtle/fob/actions/workflows/tests.yaml/badge.svg?branch=main)](https://github.com/tensorturtle/fob/actions/workflows/tests.yaml)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

**A CLI program for implementing Focus Blocks in your daily life.**

![](/assets/fob-v0.2.6-sup.png)

# Intro

**Focus Blocks** is my take on time management inspired by Flow State, Pomodoro Technique, Timeboxing, and Deep Work. Please read the [Introduction to Focus Blocks](/FOCUS_BLOCKS.md) first to understand the motivation for the creation of this program.

**`fob`** is a simple CLI program that lets you plan your month, and then visualize & update your progress within the Focus Blocks time management framework.

It is written in Python with minimal dependencies and can be installed on Mac, Linux, and Windows.

# Quick Start

First, install `uv` (directions [here](https://docs.astral.sh/uv/getting-started/installation/))

Download and install `fob` to your system:
```
uv tool install focus-blocks
```

Now, `fob` is available from anywhere on the system. Try:
```
fob help
```

# A Day in the Life

#### It's the beginning of a new month - let's set our goals.

![](/assets/fob-v0.2.6-new_month.png)

#### It's a new day! Say good morning!

![](/assets/fob-v0.2.6-gm.png)

#### Check off the first block of the day:

![](/assets/fob-v0.2.6-did-1.png)

#### Let's remind ourselves what the day ahead looks like:

![](/assets/fob-v0.2.6-sup.png)

#### Oops, we couldn't do block 3. Let's change that block to 'Buffer', which is exactly for unforeseen things like this.

![](/assets/fob-v0.2.6-didnt-3.png)

#### Checking off the final block for the day. Great job.

![](/assets/fob-v0.2.6-did-4.png)

#### Come back tomorrow and say good morning to repeat.

# Additional Features

## Cloud Sync

Bring your own cloud.

`fob` runs on a single database file. You can store this database on Dropbox or your own cloud. Just pass the path to the `--database` option when running `fob`. For example:

```
fob --database /home/tensorturtle/Dropbox/my-fob.db help
```

For more convenience, you can export a `FOB_DB_PATH` variable in your shell.
For example, add the following line to `~/.bashrc` (for bash shell):
```
export FOB_DB_PATH="/home/tensorturtle/Dropbox/my-fob.db"
source ~/.bashrc
```

# Development

Install uv.

Clone this repository:

```
git clone https://github.com/tensorturtle/fob.git
```

Run `fob` without installing it by using `uv run`:
```
uv run fob help
```

Run app in debug mode:
```
uv run fob --debug
```

Use database at custom path:
```
uv run fob --database ~/Downloads/testing_fob.db
```

The so-called database is actually just a human-readable JSON file. To see its location:
```
uv run fob info
```

## Testing

```
uvx pytest
```

This is an end-to-end test. It installs `fob` to a temporary directory using `install.sh` and runs commands against it. Github Actions is set up to run the same test upon pushing to main branch.


## Distribution 

Update version number in `pyproject.toml` and `utils/utils.py`

Build and publish package to PyPI:
```
rm -r dist/
uv build
uv publish --token $TOKEN
```

Wait a moment for PyPI database to be updated (maybe a minute) and run:
```
uvx --from focus-blocks@latest fob
```

## Database Versioning

This package uses [SemVer](https://semver.org/), with an additional convention:

Releases with the same major-minor (0.0.X) version share the same database schema.
If a new major-minor version is released, a new database is created and no migrations occur. The old database is not deleted.

