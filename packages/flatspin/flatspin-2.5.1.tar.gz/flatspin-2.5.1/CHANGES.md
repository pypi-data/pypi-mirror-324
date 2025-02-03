# Changelog

## Version 2.5.1

Released 2025-02-03

* Model:
    - Add to_mag_frame() and to_global_frame() helper functions
* Miscellaneous:
    - Bug fixes

## Version 2.5

Released 2024-12-20

* Model:
    - init_hc and set_hc supports 2d array for grid behaviour and 1d array to set directly
    - Support passing tablefile filename for hc and init
    - Add astroid database
    - Add model param to get astroid params from db
    - Add spin_axis="auto"
* Command-line tools:
    - flatspin-vectors: Add --style voronoi
    - flatspin-vectors: Allow indexing by [t] in --title
* Documentation
    - Add docs and reference for astroid database
* Miscellaneous:
    - Bug fixes

## Version 2.4.1

Released 2024-09-05

* Miscellaneous:
    - More fixes related to numpy 2.0

## Version 2.4

Released 2024-08-30

* Model:
    - Add flatspin.astroid module
    - Add astroid database
    - Add SpinIce.set_sw_params()
    - Clean up OpenCL code
    - Add set_hole_tile() and set_tiles() to TileLatticeSpinIce
* Encoders:
    - Add PulseTrain Encoder
* Plotting:
    - Avoid cropping of animation frames
    - Fix and improve plot_color_wheel
    - Add plot_voronoi()
    - Provide own ax and optional scaling of axes in vector plot
    - Switch to matplotlib.colormaps.register API (matplotlib 3.5+)
* Command-line tools:
    - flatspin-run: make periods work on any input type
    - flatspin-vectors: Add playback control
    - flatspin-vectors: add --dir-only, --alpha-mag
* Documentation:
    - Add dark-mode flatspin logo
    - Update python version requirement
* Miscellaneous:
    - Migrate to importlib.resources
    - More robustly handle nan params
    - Fixes for numpy 2.0
    - Fixes for matplotlib 3.9
    - Bug fixes

## Version 2.3

Released 2023-03-29

* Model:
    - Add spin_axis parameter
    - Add SpinIce.set_neighbor_distance()
    - Use NEAREST resampling when resizing spin image
* Plotting:
    - Allow setting explicit colors in plot_vectors()
    - Add plot_color_wheel()
    - Add support for plot_vector styles (arrow, rectangle, stadium)
* Miscellaneous:
    - Properly handle num_neighbors=0
    - Bug fixes

## Version 2.2

Released 2023-01-13

* Model:
    - Add LatticeSpinIce and TileLatticeSpinIce models
    - Improve LabelIndexer (model.L)
    - Fix KagomeRotated geometry for uneven sizes
* Plotting:
    - New flatspin colormap! Greatly improved visibility on white background
    - Improve look and feel of vector plots. Increased default arrow size, use
      slightly wider shaft when arrows=False.
    - Set background on axis instead of fig (cmap=peem)
* Command-line tools:
    - flatspin-run and flatspin-run-sweep: add --show-plot option
* Documentation:
    - Add changelog under Reference
* Miscellaneous:
    - Fix extent calculation for grid where spins don't perfectly align
    - Bug fixes

## Version 2.1

Released 2022-11-08

* Model:
    - Add plot_astroid() and plot_astroids()
    - Use new numpy RNG (avoid seeding np.random)
    - Add ability to change the positions and angles of a model object
* Command-line tools:
    - flatspin-plot: add --dpi
    - Auto-crop when saving animations as single images
* Miscellaneous:
    - Support latest version of numpy
    - Documentation improvements
    - Bug fixes

## Version 2.0

Released 2022-06-09

* Model:
    - New thermal model based on Arrhenius-Néel equation
    - Add ability to set all spins to 1 or -1 with init parameter
    - Add labels argument to CustomSpinIce for custom labels
    - Allow CustomSpinIce to read spin labels from table
    - Add ground option to init for Kagome
    - Add KagomeSpinIceRotated
    - Add ability to change hc with set_hc()
    - Add ability to set hc from a grid
    - Add methods for dipolar, thermal and external energy
    - Experimental CUDA support
* Documentation:
    - Brand new user guide and website!
* Encoders:
    - Rework encoder module to allow user-defined encoders with flatspin-run
    - Add phase parameter to sin/triangle/rotate based encoders
    - Add repeat to Constant and ConstantGrid encoders
    - Encoder.get_params() now returns a flat dictionary
* Datasets:
    - Add ability to filter datasets by list of values
    - Add git branch and commit to info.csv
    - Add support for functions in dataset filter
* Command-line tools:
    - flatspin-vectors and flatspin-vertices:
        - Add dark mode
        - Add ability to disable grid
        - Add peem colormap: --cmap peemX where X is a float
        - Add option to disable --grid
        - Add --dpi option
    - flatspin-run and flatspin-run-sweep:
        - Add support for time-varying parameters
        - Add support for reading params_t from file
        - Add --params-file and --sweep-file
        - Disable progress bar when run non-interactively
        - Support N-dimensional input arrays
    - Support for lists in the -i parameter
    - Add --drop-duplicates argument
    - Add --version argument
* Miscellaneous:
    - Improved vertex detection
    - Bug fixes

## Version 1.0

Released 2020-03-05

* First public release.
