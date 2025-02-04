## v3.6.0 (2025-02-03)

### ✨ Features

- add support for Python 3.13, closes [#58](https://github.com/kmnhan/erlabpy/issues/58) ([df4f479](https://github.com/kmnhan/erlabpy/commit/df4f479b5a388d111f397e1d999ae8a4f995d427))

- **explorer:** add a new interactive tool for browsing file systems ([a70b222](https://github.com/kmnhan/erlabpy/commit/a70b222b4113b97697b30c376095295056bd928f))

  Adds a `explorer` GUI window that provides a view of the file system with a summary of selected ARPES data files.

  The window can be started within ImageTool Manager from the File menu, or as a standalone application with `python -m erlab.interactive.explorer`.

  Closes [#83](https://github.com/kmnhan/erlabpy/issues/83).

- **misc:** add function to open directory in system's file manager ([7d3db3f](https://github.com/kmnhan/erlabpy/commit/7d3db3ff5674bfc88e2a99cc0f662286ca79f795))

### 🐞 Bug Fixes

- **io.exampledata:** replace `sph_harm` deprecated in scipy 1.15.0 with `sph_harm_y` ([eba902c](https://github.com/kmnhan/erlabpy/commit/eba902c9d4dacd682207e456fe744ebe5b6486d5))

- **interactive.utils:** ignore all other arguments for separator actions in `DictMenuBar` ([5c94b92](https://github.com/kmnhan/erlabpy/commit/5c94b9286fe11501dc2b5e9a4dc9deb46387cabf))

  This fixes unintended text showing alongside menubar separators in some operating systems.

- **imagetool.manager:** fix archived files being deleted after a few days ([7d93442](https://github.com/kmnhan/erlabpy/commit/7d93442376f90d5f9e48d2666fc2db0691247aad))

### ♻️ Code Refactor

- **io.exampledata:** update sph_harm usage to match scipy 1.15.0 changes ([1dde195](https://github.com/kmnhan/erlabpy/commit/1dde195b556a91e92b0445a33c46c134a02bc901))

- replace direct `typing` imports with namespace imports ([fc2825d](https://github.com/kmnhan/erlabpy/commit/fc2825d2a0459ae81a5d3791051807449dd5e361))

- **imagetool:** update type hints and preload fastbinning module ([ab0b3fd](https://github.com/kmnhan/erlabpy/commit/ab0b3fdd2668fe126135f197f7cc74cd6c307f69))

- **io:** improve docs structure by reorganizing namespace ([5e2d7e5](https://github.com/kmnhan/erlabpy/commit/5e2d7e51e62d11a292da4747076ac8316b9c71fd))

- **io:** improve error messages for folders ([8d63c09](https://github.com/kmnhan/erlabpy/commit/8d63c095cb8595860c8700fbf4354845b0d2f2a8))

[main 567dfc8] bump: version 3.5.1 → 3.6.0
 2 files changed, 2 insertions(+), 2 deletions(-)

