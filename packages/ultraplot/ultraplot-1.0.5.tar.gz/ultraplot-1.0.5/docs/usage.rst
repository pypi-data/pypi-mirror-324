.. _cartopy: https://scitools.org.uk/cartopy/docs/latest/

.. _basemap: https://matplotlib.org/basemap/index.html

.. _seaborn: https://seaborn.pydata.org

.. _pandas: https://pandas.pydata.org

.. _xarray: http://xarray.pydata.org/en/stable/

.. _usage:

=============
Using ultraplot
=============

This page offers a condensed overview of ultraplot's features. It is populated
with links to the :ref:`API reference` and :ref:`User Guide <ug_basics>`.
For a more in-depth discussion, see :ref:`Why ultraplot?`.

.. _usage_background:

Background
==========

ultraplot is an object-oriented matplotlib wrapper. The "wrapper" part means
that ultraplot's features are largely a *superset* of matplotlib.  You can use
plotting commands like `~matplotlib.axes.Axes.plot`, `~matplotlib.axes.Axes.scatter`,
`~matplotlib.axes.Axes.contour`, and `~matplotlib.axes.Axes.pcolor` like you always
have. The "object-oriented" part means that ultraplot's features are implemented with
*subclasses* of the `~matplotlib.figure.Figure` and `~matplotlib.axes.Axes` classes.

If you tend to use `~matplotlib.pyplot` and are not familiar with the figure and axes
classes, check out `this guide <https://matplotlib.org/stable/api/index.html>`__.
Directly working with matplotlib classes tends to be more clear and concise than
`~matplotlib.pyplot`, makes things easier when working with multiple figures and axes,
and is certainly more "`pythonic <https://www.python.org/dev/peps/pep-0020/>`__".
Therefore, although many ultraplot features may still work, we do not officially
support the `~matplotlib.pyplot` interface.

.. _usage_import:

Importing ultraplot
=================

Importing ultraplot immediately adds several
new :ref:`colormaps <ug_cmaps>`, :ref:`property cycles <ug_cycles>`,
:ref:`color names <ug_colors>`, and :ref:`fonts <ug_fonts>` to matplotlib.
If you are only interested in these features, you may want to
import ultraplot at the top of your script and do nothing else!
We recommend importing ultraplot as follows:

.. code-block:: python

   import ultraplot as uplt

This differentiates ultraplot from the usual ``plt`` abbreviation reserved for
the `~matplotlib.pyplot` module.

.. _usage_classes:

Figure and axes classes
=======================

Creating figures with ultraplot is very similar to
matplotlib. You can either create the figure and
all of its subplots at once:

.. code-block:: python

   fig, axs = uplt.subplots(...)

or create an empty figure
then fill it with subplots:

.. code-block:: python

   fig = uplt.figure(...)
   axs = fig.add_subplots(...)  # add several subplots
   ax = fig.add_subplot(...)  # add a single subplot
   # axs = fig.subplots(...)  # shorthand
   # ax = fig.subplot(...)  # shorthand

These commands are modeled after `matplotlib.pyplot.subplots` and
`matplotlib.pyplot.figure` and are :ref:`packed with new features <ug_layout>`.
One highlight is the `~ultraplot.figure.Figure.auto_layout` algorithm that
:ref:`automatically adjusts the space between subplots <ug_tight>` (similar to
matplotlib's `tight layout
<https://matplotlib.org/stable/tutorials/intermediate/tight_layout_guide.html>`__)
and :ref:`automatically adjusts the figure size <ug_autosize>` to preserve subplot
sizes and aspect ratios (particularly useful for grids of map projections
and images). All sizing arguments take :ref:`arbitrary units <ug_units>`,
including metric units like ``cm`` and ``mm``.

Instead of the native `matplotlib.figure.Figure` and `matplotlib.axes.Axes`
classes, ultraplot uses the `ultraplot.figure.Figure`, `ultraplot.axes.Axes`, and
`ultraplot.axes.PlotAxes` subclasses. ultraplot figures are saved with
`~ultraplot.figure.Figure.save` or `~matplotlib.figure.Figure.savefig`,
and ultraplot axes belong to one of the following three child classes:

* `ultraplot.axes.CartesianAxes`:
  For ordinary plots with *x* and *y* coordinates.
* `ultraplot.axes.GeoAxes`:
  For geographic plots with *longitude* and *latitude* coordinates.
* `ultraplot.axes.PolarAxes`:
  For polar plots with *azimuth* and *radius* coordinates.

Most of ultraplot's features are implemented using these subclasses.
They include several new figure and axes methods and added
functionality to existing figure and axes methods.

* The `ultraplot.axes.Axes.format` and `ultraplot.figure.Figure.format` commands fine-tunes
  various axes and figure settings.  Think of this as a dedicated
  `~matplotlib.artist.Artist.update` method for axes and figures. See
  :ref:`formatting subplots <ug_format>` for a broad overview, along with the
  individual sections on formatting :ref:`Cartesian plots <ug_cartesian>`,
  :ref:`geographic plots <ug_geoformat>`, and :ref:`polar plots <ug_polar>`.
* The `ultraplot.axes.Axes.colorbar` and `ultraplot.axes.Axes.legend` commands
  draw colorbars and legends inside of subplots or along the outside edges of
  subplots. The `ultraplot.figure.Figure.colorbar` and `ultraplot.figure.Figure.legend`
  commands draw colorbars or legends along the edges of figures (aligned by subplot
  boundaries). These commands considerably :ref:`simplify <ug_guides>` the
  process of drawing colorbars and legends.
* The `ultraplot.axes.PlotAxes` subclass (used for all ultraplot axes)
  adds many, many useful features to virtually every plotting command
  (including `~ultraplot.axes.PlotAxes.plot`, `~ultraplot.axes.PlotAxes.scatter`,
  `~ultraplot.axes.PlotAxes.bar`, `~ultraplot.axes.PlotAxes.area`,
  `~ultraplot.axes.PlotAxes.box`, `~ultraplot.axes.PlotAxes.violin`,
  `~ultraplot.axes.PlotAxes.contour`, `~ultraplot.axes.PlotAxes.pcolor`,
  and `~ultraplot.axes.PlotAxes.imshow`). See the :ref:`1D plotting <ug_1dplots>`
  and :ref:`2D plotting <ug_2dplots>` sections for details.

.. _usage_integration:

Integration features
====================

ultraplot includes *optional* integration features with four external
packages: the `pandas`_ and `xarray`_ packages, used for working with annotated
tables and arrays, and the `cartopy`_ and `basemap`_ geographic
plotting packages.

* The `~ultraplot.axes.GeoAxes` class uses the `cartopy`_ or
  `basemap`_ packages to :ref:`plot geophysical data <ug_geoplot>`,
  :ref:`add geographic features <ug_geoformat>`, and
  :ref:`format projections <ug_geoformat>`. `~ultraplot.axes.GeoAxes` provides
  provides a simpler, cleaner interface than the original `cartopy`_ and `basemap`_
  interfaces. Figures can be filled with `~ultraplot.axes.GeoAxes` by passing the
  `proj` keyword to `~ultraplot.ui.subplots`.
* If you pass a `pandas.Series`, `pandas.DataFrame`, or `xarray.DataArray`
  to any plotting command, the axis labels, tick labels, titles, colorbar
  labels, and legend labels are automatically applied from the metadata. If
  you did not supply the *x* and *y* coordinates, they are also inferred from
  the metadata. This works just like the native `xarray.DataArray.plot` and
  `pandas.DataFrame.plot` commands. See the sections on :ref:`1D plotting
  <ug_1dintegration>` and :ref:`2D plotting <ug_2dintegration>` for a demonstration.

Since these features are optional,
ultraplot can be used without installing any of these packages.

.. _usage_features:

Additional features
===================

Outside of the features provided by the `ultraplot.figure.Figure` and
`ultraplot.axes.Axes` subclasses, ultraplot includes several useful
classes and :ref:`constructor functions <why_constructor>`.

* The `~ultraplot.constructor.Colormap` and `~ultraplot.constructor.Cycle`
  constructor functions can be used to :ref:`slice <ug_cmaps_mod>`,
  and :ref:`merge <ug_cmaps_merge>` existing colormaps and color
  cycles. It can also :ref:`make new colormaps <ug_cmaps_new>`
  and :ref:`color cycles <ug_cycles_new>` from scratch.
* The `~ultraplot.colors.ContinuousColormap` and
  `~ultraplot.colors.DiscreteColormap` subclasses replace the default matplotlib
  colormap classes and add several methods. The new
  `~ultraplot.colors.PerceptualColormap` class is used to make
  colormaps with :ref:`perceptually uniform transitions <ug_perceptual>`.
* The `~ultraplot.demos.show_cmaps`, `~ultraplot.demos.show_cycles`,
  `~ultraplot.demos.show_colors`, `~ultraplot.demos.show_fonts`,
  `~ultraplot.demos.show_channels`, and `~ultraplot.demos.show_colorspaces`
  functions are used to visualize your :ref:`color scheme <ug_colors>`
  and :ref:`font options <ug_fonts>` and
  :ref:`inspect individual colormaps <ug_perceptual>`.
* The `~ultraplot.constructor.Norm` constructor function generates colormap
  normalizers from shorthand names. The new
  `~ultraplot.colors.SegmentedNorm` normalizer scales colors evenly
  w.r.t. index for arbitrarily spaced monotonic levels, and the new
  `~ultraplot.colors.DiscreteNorm` meta-normalizer is used to
  :ref:`break up colormap colors into discrete levels <ug_discrete>`.
* The `~ultraplot.constructor.Locator`, `~ultraplot.constructor.Formatter`, and
  `~ultraplot.constructor.Scale` constructor functions return corresponding class
  instances from flexible input types. These are used to interpret keyword
  arguments passed to `~ultraplot.axes.Axes.format`, and can be used to quickly
  and easily modify :ref:`x and y axis settings <ug_cartesian>`.
* The `~ultraplot.config.rc` object, an instance of
  `~ultraplot.config.Configurator`, is used for
  :ref:`modifying individual settings, changing settings in bulk, and
  temporarily changing settings in context blocks <ug_rc>`.
  It also introduces several :ref:`new setings <ug_config>`
  and sets up the inline plotting backend with `~ultraplot.config.inline_backend_fmt`
  so that your inline figures look the same as your saved figures.
