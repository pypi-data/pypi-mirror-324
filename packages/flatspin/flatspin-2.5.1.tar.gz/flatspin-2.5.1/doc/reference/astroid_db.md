---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.6
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Astroid database

flatspin includes an astroid database with switching parameters for a range of different magnet shapes and sizes.
These parameters have been estimated from [mumax](https://mumax.github.io/) simulations.
The table below shows the full contents of the astroid database.

```{code-cell} ipython3
:tags: [hide-input]

from flatspin.astroid import db
db = db.sort_values(['shape', 'thickness', 'height', 'width'], ignore_index=True)
db.style \
  .hide() \
  .format(subset='hc', precision=4) \
  .format(subset=['b', 'c'], precision=3) \
  .format(subset=['beta', 'gamma'], precision=2)
```
