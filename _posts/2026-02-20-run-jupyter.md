---
layout: post
title: Running jupyter lab locally using uv
---

A bit of a doozy of an invocation to get a jupyter notebook launched locally.

- runs with `uv` so no need to install jupyter itself and keeps packages sandboxed
- uses uv's `.venv` in current directory
- doesn't install this kernel globally, just installs it locally within the `.venv` directory
- doesn't show the native python kernel so the venv kernel is the only one that pops up
(removes need to select kernel called "venv" within jupyter lab after starting it)
- hosts on 0.0.0.0
- headless
- doesn't require token

```sh
uv run --with ipykernel python -m ipykernel install --prefix .venv --name venv && JUPYTER_DATA_DIR=.venv/share/jupyter uv run --with jupyter jupyter lab --ip 0.0.0.0 --no-browser --ServerApp.token='' --KernelSpecManager.ensure_native_kernel=False
```

I save this as an abbreviation in my `fish` config in `~/.config/fish/config.fish`:

```sh
abbr -a jupyter "uv run --with ipykernel python -m ipykernel install --prefix .venv --name venv && JUPYTER_DATA_DIR=.venv/share/jupyter uv run --with jupyter jupyter lab --ip 0.0.0.0 --no-browser --ServerApp.token='' --KernelSpecManager.ensure_native_kernel=False"
```
