# smugcli
[![Github release](https://img.shields.io/github/v/release/graveljp/smugcli.svg)](https://github.com/graveljp/smugcli/releases)
[![Linting: pylint](https://github.com/graveljp/smugcli/actions/workflows/pylint.yml/badge.svg)](https://github.com/graveljp/smugcli/actions/workflows/pylint.yml)
[![Linting: flake8](https://github.com/graveljp/smugcli/actions/workflows/flake8.yml/badge.svg)](https://github.com/graveljp/smugcli/actions/workflows/flake8.yml)
[![Unit tests](https://github.com/graveljp/smugcli/actions/workflows/tests.yml/badge.svg)](https://github.com/graveljp/smugcli/actions/workflows/tests.yml)
[![Pypi version](https://img.shields.io/pypi/v/smugcli)](https://pypi.org/project/smugcli/)
[![Python versions](https://img.shields.io/pypi/pyversions/smugcli)](https://pypi.org/project/smugcli/)
[![Pipy Wheels](https://img.shields.io/pypi/wheel/smugcli)](https://pypi.org/project/smugcli/)
[![Downloads](https://pepy.tech/badge/smugcli)](https://pepy.tech/project/smugcli)

Command line tool for SmugMug, useful for automatically synchronizing a local
folder hierarchy with a SmugMug account.

Implemented using the Smugmug V2 API.

Tested with Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13.

# Installation

Smugcli is written in [Python](https://www.python.org/) and is distributed via the [Pip](https://pypi.org/project/pip/) package manager. To install smugcli, first [install a Python 3](https://www.python.org/downloads/) distribution on your system (Python 2 is not supported). Pip is usually installed automatically, [install it manually](https://pip.pypa.io/en/stable/installation/) if it isn't. Then, install smugcli by running:
```
pip install smugcli
```
or, if `pip` can't be found, try:
```
python -m pip install smugcli
```

# Sample usage

To use this command line tool, you will need to request your own API key by
visiting https://api.smugmug.com/api/developer/apply. Using your key and secret,
log into smugcli using the following command:
```
$ ./smugcli.py login --key=<key> --secret=<secret>
```

This is a one time operation. From this point on, smugcli will be able to access
your SmugMug account. To logout, run the command: `$ ./smugcli.py logout`

You can list the content of your SmugMug account by doing:
```
$ ./smugcli.py ls
 Photography
 Portfolio
 Other

$ ./smugcli.py ls Photography
 2014
 2015
 2016

$ ./smugcli.py ls Photography/2015
 Photoshoot with Dave
```

Note that smugcli can also be used to access other public SmugMug account by
using the `--user` argument:
```
$ ./smugcli.py ls -u <username>
```

Folders can be created by using the `mkdir` command:
```
$ ./smugcli.py mkdir Photography/2017
```

Similarly, albums can be created by doing:
```
$ ./smugcli.py mkalbum 'Photography/2017/My new album'
```

To upload photos to an album, run:
```
$ ./smugcli.py upload local/folder/*.jpg 'Photography/2017/My new album'
```

Finally, the nicest feature of all, you can synchronize a whole local folder
hierarchy to your SmugMug account using the `sync` command:
```
$ ./smugcli.py sync local/folder remote/folder
Creating Folder "remote/folder/2015".
Creating Album "remote/folder/2015/2015-08-03, Mary's Wedding".
Uploading "local/folder/2015/2015-08-03, Mary's Wedding/DSC_0001.JPG"
Uploading "local/folder/2015/2015-08-03, Mary's Wedding/DSC_0002.JPG"
Uploading "local/folder/2015/2015-08-03, Mary's Wedding/DSC_0003.JPG"
...
Creating Album "remote/folder/2015/2015-09-10, Andy's Photoshoot"
Uploading "local/folder/2015/2015-09-10, Andy's Photoshoot/DSC_0043.JPG"
Uploading "local/folder/2015/2015-09-10, Andy's Photoshoot/DSC_0052.JPG"
...
```

The sync command can be re-executed to update the remote Albums in the event
that the local files might have been updated. Only the files that changed will
be re-uploaded.

Multiple sources can be synced in the same operation, the last argument being
the destination folder and the others being the sources:
```
$ ./smugcli.py sync 2016 2017 2018 remote/folder
Syncing:
  2016
  2017
  2018
to SmugMug folder "remote/folder"',
...

$ ./smugcli.py sync 201* remote/folder
...
```

Source files are synced to the destination SmugMug album and source folders are
recursively synced to the destination SmugMug folder. For source folders with a
trailing path delimiter ('/' or '\\' depending on OS), only the content of the
folder is synced, skipping the folder itself (equivalent of doing `folder/*`)
. This means that `smugcli.py sync src/album dst` is equivalent to `smugcli.py
sync src/album/ dst/album`. If no sources or destinations are specified, smugcli
defaults to syncing the current folder to the SmugMug user's root.

The sync command uses multiple threads to speed-up the file scanning and upload.
You may want to tune the number of threads used by SmugCLI depending on your
machine's performance. For instance:
```
$ ./smugcli.py sync local/folder remote/folder --folder_threads=4 --file_threads=8 --upload_threads=2
```

`folder_threads` control the number of album folders that are processed in
parallel.  `file_threads` specifies the number of files that are read from disk
and compared with the server side version in parallel. `upload_threads` controls
the number of parallel upload operations allowed when sending content to
SmugMug. Keep in mind that too many or too few threads can be harmful to
performance. Also keep in mind that increasing file_threads or upload_threads
means that more files will be loaded in memory at the same time. If you have
many large video files, loading too many in parallel could hog your system's
resources.

When you are happy with the performance using certain thread counts, you may
save these preferences so that they'd be used as defaults next time:
```
$ ./smugcli.py sync --set_defaults --folder_threads=4 --file_threads=8 --upload_threads=2
```

To exclude paths from the sync operation, run the command:
```
$ ./smugcli.py ignore local/folder/export-tmp
```

To undo this operation, you can run:
```
$ ./smugcli.py include local/folder/export-tmp
```

# Contributions

## Running from source
To run Smugcli from the source code:
```shell
# Get the source code:
git clone https://github.com/graveljp/smugcli.git

cd smugcli

# Install dependencies:
pip install -r requirements.txt

# Run smugcli module
python -m smugcli
```

## Unit tests
Unit tests are a requirement for any pull requests. All new features and bug
fixes must have test coverage. Unit testing is critical in making sure that
all features remain functional as the code evolves.

Unit tests are particularly important in pull requests since the features or
issues being fixed might not be easily reproducible by maintainers. For
instance, If smugcli fails on a particular type of media, a unit test must be
included with a sample file so that we can make sure that support for that
file format remains functional in the future. Likewise, any feature relying on
interaction with the SmugMug service must absolutely be tested since we must
have a way to detect if SmugMug ever does breaking changes on their end.

## Running unit tests
PLEASE READ, RUN UNIT TESTS AT YOUR OWN RISKS: smugcli's unit-tests use the
logged-in user account to run actual commands on SmugMug. All operations
*should* be performed in a `__smugcli_unit_tests__` subfolder in the SmugMug
account's root. This folder *should* be deleted automatically when/if the test
completes. If in doubt, do `smugcli.py logout && smugcli.py login` and use a
test account.

SmugCLI uses `tox` to run tests using all supported Python interpreter versions.
Run all tests with all Python versions by running:
```
$ tox
```

To run with only one specific Python version, for instance Python 3.9, do:
```
$ tox -e py39
```

Individual tests can be ran by doing:
```
$ tox -- tests/module[.class_name[.test_name]]
```

for instance:
```
$ tox -e py39 -- tests/end_to_end_test.py  # Runs all tests in tests/end_to_end_test.py.
$ tox -e py39 -- tests/end_to_end_test.py::EndToEndTest  # Runs all tests in class EndToEndTest.
$ tox -e py39 -- tests/end_to_end_test.py::EndToEndTest::test_sync  # Runs a single test.
```

Since the unit tests do actual operations on SmugMug, they are fairly slow. To
speed things up during development, an HTTP request cache can be enabled so that
responses from the previous run are replayed instead of re-doing the actual HTTP
requests to SmugMug. To enable this cache, set the `REUSE_RESPONSES` environment
variable to `True`:
```
$ REUSE_RESPONSES=True tox -e py39
```

Windows users can do the equivalent by doing:
```
C:\smugcli> cmd /C "set REUSE_RESPONSES=True && tox -e py39"
```

Note that if you change the code such that different HTTP requests are done, you
will have to set `REUSE_RESPONSES` to `False` on the next run to update the
cache.
