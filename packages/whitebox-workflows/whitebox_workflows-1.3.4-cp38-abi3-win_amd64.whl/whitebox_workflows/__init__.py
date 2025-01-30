import os
from math import ceil
from typing import Tuple
from .whitebox_workflows import *
from .scripts.horton_ratios import horton_ratios
from .scripts.improved_ground_point_filter import improved_ground_point_filter
from .scripts.nibble import nibble
from .scripts.ridge_and_valley_vectors import ridge_and_valley_vectors
from .scripts.sieve import sieve
from whitebox_workflows import Raster, Vector

__doc__ = whitebox_workflows.__doc__
if hasattr(whitebox_workflows, "__all__"):
    __all__ = whitebox_workflows.__all__
    
def _install_package(*args):
    try:
        pip_packages = os.popen("pip list").read()
    except Exception:
        print("Error: Couldn not install package, pip is not installed")

    for arg in args:
        if pip_packages.find(arg) == -1:
            print(f"Installing {arg}...")
            os.system(f"pip install {arg}")
   
def show(obj, ax=None, title=None, figsize=None, skip=None, clip_percent=None, plot_as_surface=False, vert_exaggeration=None, colorbar_kwargs=None, **kwargs):
    """Display a Raster, Vector, or Lidar dataset using matplotlib. This function requires
    that matplotlib is installed and will use an automatic pip install of the library if it 
    is not already available.

    Parameters
    ----------
    obj : Raster | Vector | Lidar, required
        Dataset to be displayed on the plot axes. Can be of Raster, Vector or Lidar type.
    ax : matplotlib.axes.Axes, optional
        Axes to plot on, otherwise uses current axes.
    title : str | dict, optional
        Either a string representing the title for the figure, or a dict containing keyword
        and value pairs sent to the `matplotlib.axes.Axes.set_title` function, e.g.:
        `title='My Title'`
        `title={'label': 'My Title', 'pad': 12, 'fontsize': 10, 'fontweight': 'bold', 'fontstyle': 'italic'}`
    figsize : Tuple[float, float], optional
        Defines the size (width, height) of the figure to which the Axes is to be added.
    skip : int, optional
        Determines the stride for reading Raster and Lidar obj types when displaying. skip=1
        indicates that every pixel/point is read, while skip=2 would indicate that every second
        pixel/point is read. This argument can strongly impact the amount of time required to
        display the resulting figure but larger values may impact the quality of the resulting
        image. For larger raster images, values in the range of 2-10 may be advisable while for
        lidar datasets, values in the range of 500-1000 may be suitable.
    clip_percent : float | Tuple[float, float], optional
        Continuous Raster datasets (i.e. non-RGB images) will use the Raster.configs.display_min and
        Raster.configs.display_max values to determine the assignment of colours from the colormap.
        By default, these values are set to the raster min/max values when the raster is read. If
        a clip_percent value > 0 is provided, the show function will call the Raster.clip_display_min_max
        function to clip the tails of the raster histogram. Seperate clip percentages can also be provided 
        for the lower and upper tails respectively as a tuple of floats. Depending on the size of the 
        raster, this function can significantly increase time to display. If the same raster is being
        added to multiple Axes in a multi-part figure, it may be advisable to only set the clip_percent 
        function (or call the clip_display_min_max seperately) one time.
    plot_as_surface : bool, optional, default = False
        Continuous Raster datasets can be plotted on a Axes3D using the 
        `mpl_toolkits.mplot3d.axes3d.Axes3D.plot_surface` function, rather than the usual 2D representation
        using the `matplotlib.pyplot.imshow` function when this optional argument is set to True.
    vert_exaggeration : float, optional
        This optional argument determines the vertical exaggeration used in displaying 3D plots for either
        rasters (plotted with `plot_as_surface=True`) and Lidar datasets. Generally, `vert_exaggeration > 1.0`
        is advisable and for lower-relief sites, values much larger than 1.0 are likely suitable otherwise
        the resulting plot may appear quite flat.
    colorbar_kwargs : key-value pairings, optional
        Dictionary of key-value pairs that are sent to the `matplotlib.pyplot.colorbar` function. These
        arguments are only used when a `cmap` key exists in the **kwargs argument. That is, leaving this
        argument unspecified will result in no colorbar being displayed in the resulting image. 

        `ax = show(hs, title='Hillshade', skip=2, cmap='gray', colorbar_kwargs={'location': "right", 'shrink': 0.5}, figsize=(7.0,4.7))`
    **kwargs : key, value pairings, optional
        These will be passed to the `matplotlib.pyplot.scatter`, `matplotlib.pyplot.fill`, `matplotlib.pyplot.imshow`, 
        or `mpl_toolkits.mplot3d.axes3d.Axes3D.plot_surface` functions depending on obj type.

    Returns
    -------
    ax : matplotlib.axes.Axes
        Axes with plot.

    """
    
    # Plotting operations require numpy, matplotlib, and mpl_interactions (to allow zooming into plots via scrolling).
    _install_package('numpy', 'matplotlib') #, 'mpl_interactions')

    import matplotlib as mpl
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap
    # from matplotlib.colors import LightSource
    import numpy as np

    show_plot = False

    if ax is None:
        show_plot = True
        if plot_as_surface or isinstance(obj, Lidar):
            # fig = plt.gcf()
            fig = plt.figure() 
            ax = fig.add_subplot(projection='3d')
        else:
            fig, ax = plt.subplots()
    else:
        fig = plt.gcf()

    if figsize is not None:
        fig.set_size_inches(figsize[0], figsize[1])

    # fig.tight_layout()

    show_colorbar = False
    if colorbar_kwargs is not None:
        show_colorbar = True


    # Has the user presented a WbPalette for a colormap?
    if 'cmap' in kwargs:
        pal = kwargs['cmap']
        if isinstance(pal, WbPalette):
            kwargs['cmap'] = LinearSegmentedColormap.from_list('palette', WbPalette.get_normalized_palette(pal), N=1024)
        elif isinstance(pal, list):
            kwargs['cmap'] = LinearSegmentedColormap.from_list('palette', pal, N=1024)

    # This is where the heavy lifting comes in.
    if isinstance(obj, Vector):
        # is it a point, line or polygon file?
        if obj.header.shape_type.base_shape_type() == VectorGeometryType.Point:
            xs = []
            ys = []
            for rec in obj:
                x, y = rec.get_xy_data()
                xs.append(x)
                ys.append(y)
            
            ax.scatter(xs, ys, **kwargs)

        elif obj.header.shape_type.base_shape_type() == VectorGeometryType.PolyLine:
            xs = []
            ys = []
            for rec in obj:
                parts = rec.parts
                num_parts = rec.num_parts
                part_num = 1 # actually the next part
                x, y = rec.get_xy_data()
                for i in range(len(x)):
                    if part_num < num_parts and i == parts[part_num]:
                        xs.append(np.nan) # discontinuity
                        ys.append(np.nan) # discontinuity
                        part_num += 1

                    xs.append(x[i])
                    ys.append(y[i])
                xs.append(np.nan) # discontinuity
                ys.append(np.nan) # discontinuity
            
            ax.plot(xs, ys, **kwargs)

        else: # Polygon

            xs = []
            ys = []
            for rec in obj:
                parts = rec.parts
                num_parts = rec.num_parts
                part_num = 1 # actually the next part
                x, y = rec.get_xy_data()
                for i in range(len(x)):
                    if part_num < num_parts and i == parts[part_num]:
                        xs.append(np.nan) # discontinuity
                        ys.append(np.nan) # discontinuity
                        part_num += 1

                    xs.append(x[i])
                    ys.append(y[i])

                xs.append(np.nan) # discontinuity
                ys.append(np.nan) # discontinuity
            
            ax.fill(xs, ys, **kwargs)

    elif isinstance(obj, Raster):
        if skip is None:
            skip = 1

        rows = int(ceil(obj.configs.rows / skip))
        columns = int(ceil(obj.configs.columns / skip))
        nodata = obj.configs.nodata

        # Figure out the extent, if it's not present
        if 'extent' not in kwargs:
            left = obj.configs.west
            right = obj.configs.east
            bottom = obj.configs.south
            top = obj.configs.north
            kwargs['extent'] = (left, right, bottom, top)
        
        if plot_as_surface:
            if 'extent' in kwargs:
                del kwargs['extent']

        # This can happen if the raster has never been saved to file before.
        if obj.configs.minimum == float("inf") or obj.configs.maximum == float("-inf"):
            obj.update_min_max()

        minVal = obj.configs.display_min
        maxVal = obj.configs.display_max

        is_clipped = False
        if clip_percent is not None:
            is_clipped = True
            

        if obj.configs.photometric_interp != PhotometricInterpretation.RGB and not plot_as_surface: # A continuous image, e.g. a DEM
            arr = np.full([rows, columns], np.nan) # Initialize with nodata

            if is_clipped:
                if isinstance(clip_percent, float):
                    if clip_percent > 0.0 and clip_percent < 50.0:
                        obj.clip_display_min_max(clip_percent)
                        minVal = obj.configs.display_min
                        maxVal = obj.configs.display_max
                elif isinstance(clip_percent, Tuple):
                    if clip_percent[0] > 0.0 and clip_percent[0] < 50.0:
                        obj.clip_display_min(clip_percent[0])
                        minVal = obj.configs.display_min
                    if clip_percent[1] > 0.0 and clip_percent[1] < 50.0:
                        obj.clip_display_max(clip_percent[1])
                        maxVal = obj.configs.display_max

            
            r = 0
            for row in range(0, obj.configs.rows, skip):
                values = obj.get_row_data(row)
                c = 0
                for col in range(0, obj.configs.columns, skip):
                    value = values[col]
                    if value != nodata:
                        # if is_clipped:
                        if value < minVal:
                            value = minVal
                        elif value > maxVal:
                            value = maxVal

                        arr[r, c] = value

                    c += 1
                r += 1

            im = ax.imshow(arr, **kwargs)

        elif obj.configs.photometric_interp != PhotometricInterpretation.RGB and plot_as_surface: # A surface plot
            X = np.zeros([rows, columns])
            Y = np.zeros([rows, columns])
            Z = np.zeros([rows, columns])
            mask = np.zeros([rows, columns])

            if is_clipped:
                if isinstance(clip_percent, float):
                    if clip_percent > 0.0 and clip_percent < 50.0:
                        obj.clip_display_min_max(clip_percent)
                        minVal = obj.configs.display_min
                        maxVal = obj.configs.display_max
                elif isinstance(clip_percent, Tuple):
                    if clip_percent[0] > 0.0 and clip_percent[0] < 50.0:
                        obj.clip_display_min(clip_percent[0])
                        minVal = obj.configs.display_min
                    if clip_percent[1] > 0.0 and clip_percent[1] < 50.0:
                        obj.clip_display_max(clip_percent[1])
                        maxVal = obj.configs.display_max

            r = 0
            for row in range(0, obj.configs.rows, skip):
                y = obj.get_y_from_row(row)
                values = obj.get_row_data(row)
                c = 0
                for col in range(0, obj.configs.columns, skip):
                    x = obj.get_x_from_column(col)
                    z = values[col]
                    if z != nodata:
                        # if is_clipped:
                        if z < minVal:
                            z = minVal
                        elif z > maxVal:
                            z = maxVal
                    else:
                        z = minVal
                        mask[r, c] = 1
                    
                    X[r, c] = x
                    Y[r, c] = y
                    Z[r, c] = z

                    c += 1
                r += 1

            Z = np.ma.masked_array(Z, mask=mask)

            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')

            kwargs['vmin'] = obj.configs.display_min
            kwargs['vmax'] = obj.configs.display_max


            if vert_exaggeration is not None:
                z_range = np.ptp(Z)
                x_range = np.ptp(X)
                aspect = float(vert_exaggeration) * (1.0 / x_range) * z_range
                ax.set_box_aspect((1.0, 1.0, float(aspect)))
            
            if 'cmap' in kwargs:
                cmap = kwargs['cmap']
                if isinstance(cmap, str):
                    cmap = mpl.cm.get_cmap(cmap)
                
                if 'shade' in kwargs and kwargs['shade'] == True:
                    norm = mpl.colors.Normalize(vmin=Z.min(), vmax=Z.max(), clip=False)
                    # colors = norm(Z)
                    # kwargs['norm'] = norm
                    kwargs['facecolors'] = cmap(norm(Z))

                    if show_colorbar:
                        m = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
                        m.set_array([])
                        fig.colorbar(m, ax=ax, **colorbar_kwargs)
                        show_colorbar = False
            
            # if 'shade' in kwargs and 'cmap' in kwargs:
            #     # To use a custom hillshading mode, override the built-in shading and pass
            #     # in the rgb colors of the shaded surface calculated from "shade".
            #     ls = mpl.colors.LightSource(315.0, 45.0)
            #     cm = kwargs['cmap']
            #     if isinstance(cm, str):
            #         cm = mpl.cm.get_cmap(cm)
            #     rgb = ls.shade(Z, cmap = cm, vert_exag = 1.0, blend_mode = 'overlay', dx=obj.configs.resolution_x, dy=obj.configs.resolution_y, fraction = 1.2)
            #     kwargs['facecolors'] = rgb
            # #     del kwargs['cmap']
            # #     del kwargs['shade']
            # #     if 'color' in kwargs:
            # #         del kwargs['color']

            # Plot the surface.
            im = ax.plot_surface(X, Y, Z, **kwargs)

        else: # An RGB image
            # ax = plt.gca()
            show_colorbar = False # colorbars don't make sense for RGB images
            arr = np.zeros([rows, columns, 4], dtype=np.uint8)

            # start2 = time()
            r = 0
            for row in range(0, obj.configs.rows, skip):
                values = obj.get_row_data_as_rgba(row)
                c = 0
                for col in range(0, obj.configs.columns, skip):
                    arr[r, c, 0] = values[col][0]
                    arr[r, c, 1] = values[col][1]
                    arr[r, c, 2] = values[col][2]
                    arr[r, c, 3] = values[col][3]

                    c += 1
                r += 1

            # for row in range(rows):
            #     values = obj.get_row_data_as_rgba(row)
            #     for col in range(columns):
            #         arr[row, col, 0] = values[col][0]
            #         arr[row, col, 1] = values[col][1]
            #         arr[row, col, 2] = values[col][2]
            #         arr[row, col, 3] = values[col][3]

            # end2 = time()
            # print(f"Elapsed time: {end2 - start2} seconds")      

            im = ax.imshow(arr, **kwargs)

        
        if show_colorbar:
            # Set up some things for a potential colorbar
            if colorbar_kwargs is None:
                colorbar_kwargs = {}

            if 'not specified' not in obj.configs.z_units and 'label' not in colorbar_kwargs:
                colorbar_kwargs['label'] = obj.configs.z_units

            if is_clipped or minVal > obj.configs.minimum or maxVal < obj.configs.maximum:
                if 'extend' not in colorbar_kwargs:
                    colorbar_kwargs['extend'] = 'both'

            fig.colorbar(im, ax=ax, **colorbar_kwargs)
    
    elif isinstance(obj, Lidar):
        if skip is None:
            skip = 1000

        num_points = obj.header.get_num_points()
        xs = []
        ys = []
        zs = []
        for i in range(0, num_points, skip):
            x, y, z = obj.get_transformed_xyz(i)
            xs.append(x)
            ys.append(y)
            zs.append(z)
            

        if 'cmap' in kwargs and ('color' not in kwargs and 'c' not in kwargs): # don't override an existing 'c' kw
            kwargs['c'] = zs
        
        scatter = ax.scatter(xs, ys, zs, **kwargs)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        if vert_exaggeration is not None:
            z_range = np.ptp(zs)
            x_range = np.ptp(xs)
            aspect = float(vert_exaggeration) * (1.0 / x_range) * z_range
            ax.set_box_aspect((1.0, 1.0, float(aspect)))

        if show_colorbar:
            # Set up some things for a potential colorbar
            if colorbar_kwargs is None:
                colorbar_kwargs = {}

            fig.colorbar(scatter, ax=ax, **colorbar_kwargs)
    
    else:
        raise TypeError("Object must be a Vector, Raster, or Lidar type")

    if title:
        if isinstance(title, dict):
            ax.set_title(**title)
        else:
            ax.set_title(title)

    if show_plot:
        if "label" in kwargs:
            ax.legend()

        plt.show()

    return ax



class WbEnvironment(WbEnvironmentBase):
    """The WbEnvironment class can be used to configure WbW settings (e.g. the working
directory, number of processors used, and verbose mode). It is also used to call
the various tool functions, which appear as methods of this class, and to read/write
spatial data."""
    def __init__(self, user_id: str = None):
        """Initializes a new WbEnvironment object with an optional user_id, i.e. a floating
license ID string used in WbW-Pro licenses.
        """
        # WbEnvironmentBase(user_id)

    def available_functions(self) -> None:
        """This function will list all of the available functions associated with a
WbEnvironment (wbe). The functions that are accessible will depend on the 
license level (WbW or WbWPro).
        """

        # Are we running a pro license?
        pro_license = self.license_type == LicenseType.WbWPro

        # Get all the non-dunder methods of WbEnvironment
        method_list = [func for func in dir(WbEnvironment) if callable(getattr(WbEnvironment, func)) and not func.startswith("__")]

        print(f"Available Methods ({self.license_type}):")

        j = 0
        s = ''
        for i in range(len(method_list)):
            val = method_list[i]
            val_len = len(f"{j}. {val}")
            is_pro_func = whitebox_workflows.is_wbw_pro_function(val)
            
            added = True
            if not is_pro_func and j % 2 == 0:
                s += f"{j+1}. {val}{' '* (50 - val_len)}"
                j += 1
            elif not is_pro_func and j % 2 == 1:
                s += f"{j+1}. {val}"
                j += 1
            elif (is_pro_func and pro_license) and j % 2 == 0:
                s += f"{j+1}. {val}{' '* (50 - val_len)}"
                j += 1
            elif (is_pro_func and pro_license) and j % 2 == 1:
                s += f"{j+1}. {val}"
                j += 1
            else:
                added = False
                

            if added and (j % 2 == 0 or i == len(method_list)-1):
                print(s)
                s = ''


    def horton_ratios(self, dem: Raster, streams_raster: Raster) -> Tuple[float, float, float, float]:
        '''This function can be used to calculate Horton's so-called laws of drainage network composition for a
input stream network. The user must specify an input DEM (which has been suitably hydrologically pre-processed
to remove any topographic depressions) and a raster stream network. The function will output a 4-element 
tuple containing the bifurcation ratio (Rb), the length ratio (Rl), the area ratio (Ra), and the slope ratio
(Rs). These indices are related to drainage network geometry and are used in some geomorphological analysis.
The calculation of the ratios is based on the method described by Knighton (1998) Fluvial Forms and Processes: 
A New Perspective.

# Code Example

```python
from whitebox_workflows import WbEnvironment

# Set up the WbW environment
wbe = WbEnvironment()
wbe.verbose = True
wbe.working_directory = '/path/to/data'

# Read the inputs
dem = wbe.read_raster('DEM.tif')
streams = wbe.read_raster('streams.tif')

# Calculate the Horton ratios
(bifurcation_ratio, length_ratio, area_ratio, slope_ratio) = wbe.horton_ratios(dem, streams)

# Outputs
print(f"Bifurcation ratio (Rb): {bifurcation_ratio:.3f}")
print(f"Length ratio (Rl): {length_ratio:.3f}")
print(f"Area ratio (Ra): {area_ratio:.3f}")
print(f"Slope ratio (Rs): {slope_ratio:.3f}")
```

# See Also
<a href="tool_help_wbwpro.md#horton_stream_order">horton_stream_order</a>

# Function Signature
```python
def horton_ratios(self, dem: Raster, streams_raster: Raster) -> Tuple[float, float, float, float]: ...
```
'''
        return horton_ratios(self, dem, streams_raster)


    def nibble(self, input_raster: Raster, mask: Raster, use_nodata: bool = False, nibble_nodata: bool = True) -> Raster:
        '''Use of this function requires a license for Whitebox Workflows for Python Professional (WbW-Pro).
Please visit www.whiteboxgeo.com to purchase a license.

The nibble function assigns areas within an input class map raster that are coincident with a mask the value 
of their nearest neighbour. Nibble is typically used to replace erroneous sections in a class map. Cells in the mask
raster that are either NoData or zero values will be replaced in the input image with their nearest non-masked
value. All input raster values in non-mask areas will be unmodified.

There are two input parameters that are related to how NoData cells in the input raster are handled during
the nibble operation. The use_nodata Boolean determines whether or not input NoData cells, not contained within masked
areas, are treated as ordinary values during the nibble. It is False by default, meaning that NoData cells 
in the input raster do not extend into nibbled areas. When the nibble_nodata parameter is True, any NoData cells
in the input raster that are within the masked area are also NoData in the output raster; when nibble_nodata is False
these cells will be nibbled.

# See Also:
<a href='https://www.whiteboxgeo.com/manual/wbw-user-manual/book/tool_help_wbwpro.html#sieve'>sieve</a>

# Function Signature
```python
def nibble(self, input_raster: Raster, mask: Raster, use_nodata: bool = False, nibble_nodata: bool = True) -> Raster:
```
'''
        return nibble(self, input_raster, mask, use_nodata, nibble_nodata)


    def ridge_and_valley_vectors(self, dem: Raster, filter_size: int = 11, ep_threshold: float = 30.0, slope_threshold: float = 0.0, min_length: int = 20) -> Tuple[Vector, Vector]:
        '''Use of this function requires a license for Whitebox Workflows for Python Professional (WbW-Pro).
Please visit www.whiteboxgeo.com to purchase a license.

This function can be used to extract ridge and channel vectors from an input digital elevation model (DEM).
The function works by first calculating elevation percentile (EP) from an input DEM using a neighbourhood size set by
the user-specified filter_size parameter. Increasing the value of filter_size can result in more continuous mapped ridge
and valley bottom networks. A thresholding operation is then applied to identify cells that have an EP less than the 
user-specified ep_threshold (valley bottom regions) and a second thresholding operation maps regions where EP is 
greater than 100 - ep_threshold (ridges). Each of these ridge and valley region maps are also multiplied by a slope 
mask created by identify all cells with a slope greater than the user-specified slope_threshold value, which is set 
to zero by default. This second thresholding can be helpful if the input DEM contains extensive flat areas, which 
can be confused for valleys otherwise. The filter_size and ep_threshold parameters are somewhat dependent on one 
another. Increasing the filter_size parameter generally requires also increasing the value of the ep_threshold. The 
ep_threshold can take values between 5.0 and 50.0, where larger values will generally result in more extensive and 
continuous mapped ridge and valley bottom networks. For many DEMs, a value on the higher end of the scale tends to 
work best.

After applying the thresholding operations, the function then applies specialized shape generalization, line thinning, 
and vectorization alorithms to produce the final ridge and valley vectors. The user must also specify the value of the
min_length parameter, which determines the minimum size, in grid cells, of a mapped line feature. The function outputs
a tuple of two vector, the first being the ridge network and the second vector being the valley-bottom network.

![](./img/ridge_and_valley_vectors.jpeg)

# Code Example

```python
from whitebox_workflows import WbEnvironment

# Set up the WbW environment
license_id = 'my-license-id' # Note, this tool requires a license for WbW-Pro
wbe = WbEnvironment(license_id)
try:
    wbe.verbose = True
    wbe.working_directory = '/path/to/data'

    # Read the input DEM
    dem = wbe.read_raster('DEM.tif')

    # Run the operation
    ridges, valleys = wbe.ridge_and_valley_vectors(dem, filter_size=21, ep_threshold=45.0, slope_threshold=1.0, min_length=25)
    wbe.write_vector(ridges, 'ridges_lines.shp')
    wbe.write_vector(valley, 'valley_lines.shp')

    print('Done!')
except Exception as e:
  print("Error: ", e)
finally:
    wbe.check_in_license(license_id)
```

# See Also:
<a href='https://www.whiteboxgeo.com/manual/wbw-user-manual/book/tool_help.html#extract_valleys'>extract_valleys</a>

# Function Signature
```python
def ridge_and_valley_vectors(self, dem: Raster, filter_size: int = 11, ep_threshold: float = 30.0, slope_threshold: float = 0.0, min_length: int = 20) -> Tuple[Raster, Raster]:
```
'''
        return ridge_and_valley_vectors(self, dem, filter_size, ep_threshold, slope_threshold, min_length)


    def sieve(self, input_raster: Raster, threshold: int = 1, zero_background: bool = False) -> Raster:
        '''Use of this function requires a license for Whitebox Workflows for Python Professional (WbW-Pro).
Please visit www.whiteboxgeo.com to purchase a license.

The sieve function removes individual objects in a class map that are less than a threshold
area, in grid cells. Pixels contained within the removed small polygons will be replaced with the nearest
remaining class value. This operation is common when generalizing class maps, e.g. those derived from an
image classification. Thus, this tool provides a similar function to the <a href='https://www.whiteboxgeo.com/manual/wbw-user-manual/book/tool_help_wbwpro.html#generalize_classified_raster'>generalize_classified_raster</a> and
<a href='https://www.whiteboxgeo.com/manual/wbw-user-manual/book/tool_help_wbwpro.html#generalize_with_similarity'>generalize_with_similarity</a> functions.

# See Also:
<a href='https://www.whiteboxgeo.com/manual/wbw-user-manual/book/tool_help_wbwpro.html#generalize_classified_raster'>generalize_classified_raster</a>, <a href='https://www.whiteboxgeo.com/manual/wbw-user-manual/book/tool_help_wbwpro.html#generalize_with_similarity'>generalize_with_similarity</a>

# Function Signature
```python
def sieve(self, input_raster: Raster, threshold: int = 1, zero_background: bool = False) -> Raster: ...
```
        '''
        return sieve(self, input_raster, threshold, zero_background)
    
    def improved_ground_point_filter(self, input: Lidar, block_size: float = 1.0, max_building_size: float = 150.0, slope_threshold: float = 15.0, elev_threshold: float = 0.15, classify: bool = False, preserve_classes: bool = False) -> Lidar:
        '''Use of this function requires a license for Whitebox Workflows for Python Professional (WbW-Pro).
Please visit www.whiteboxgeo.com to purchase a license.

This function provides a faster alternative to the `lidar_ground_point_filter` algorithm, provided in the free
version of Whitebox Workflows, for the extraction of ground points from within a LiDAR point cloud. The algorithm
works by placing a grid overtop of the point cloud of a specified resolution (`block_size`, in xy-units) and identifying the
subset of lidar points associated with the lowest position in each block. A raster surface is then created by 
TINing these points. The surface is further processed by removing any off-terrain objects (OTOs), including buildings
smaller than the `max_building_size` parameter (xy-units). Removing OTOs also requires the user to specify the value of
a `slope_threshold`, in degrees. Finally, the algorithm then extracts all of the points in the input LiDAR point cloud 
(`input`) that are within a specified absolute vertical distance (`elev_threshold`) of this surface model.

Conceptually, this method of ground-point filtering is somewhat similar in concept to the cloth-simulation approach of 
Zhang et al. (2016). The difference is that the cloth is first fitted to the minimum surface with infinite flexibility 
and then the rigidity of the cloth is subsequently increased, via the identification and removal of OTOs from the minimal 
surface. The `slope_threshold` parameter effectively controls the eventual rigidity of the fitted surface.

By default, the tool will return a point cloud containing only the subset of points in the input dataset that coincide
with the idenfitied ground points. Setting the `classify` parameter to True modifies this behaviour such that the output
point cloud will contain all of the points within the input dataset, but will have the classification value of identified
ground points set to '2' (i.e., the ground class value) and all other points will be set to '1' (i.e., the unclassified
class value). By setting the `preserve_classes` paramter to True, all non-ground points in the output cloud will have
the same classes as the corresponding point class values in the input dataset.

Compared with the `lidar_ground_point_filter` algorithm, the `improved_ground_point_filter` algorithm is generally far faster and is
able to more effectively remove points associated with larger buildings. Removing large buildings from point clouds with the 
`lidar_ground_point_filter` algorithm requires use of very large search distances, which slows the operation considerably.

As a comparison of the two available methods, one test tile of LiDAR containing numerous large buildings and abundant 
vegetation required 600.5 seconds to process on the test system using the `lidar_ground_point_filter` algorithm 
(removing all but the largest buildings) and 9.8 seconds to process using the `improved_ground_point_filter` algorithm 
(with complete building removal), i.e., 61x faster.

The original test LiDAR tile, containing abundant vegetation and buildings:

![](./img/improved_ground_point_filter1.png)

The result of applying the `lidar_ground_point_filter` function, with a search radius of 25 m and max inter-point slope of 
15 degrees:

![](./img/improved_ground_point_filter2.png)

The result of applying the `improved_ground_point_filter` method, with `block_size` = 1.0 m, `max_building_size` = 150.0 m, 
`slope_threshold` = 15.0 degrees, and `elev_threshold` = 0.15 m:

![](./img/improved_ground_point_filter3.png)

# References:
Zhang, W., Qi, J., Wan, P., Wang, H., Xie, D., Wang, X., & Yan, G. (2016). An easy-to-use airborne LiDAR data filtering 
method based on cloth simulation. Remote sensing, 8(6), 501.

# See Also:
<a href='https://www.whiteboxgeo.com/manual/wbw-user-manual/book/tool_help.html#lidar_ground_point_filter'>lidar_ground_point_filter</a>

# Function Signature
```python
def improved_ground_point_filter(self, input: Lidar, block_size = 1.0, max_building_size = 150.0, slope_threshold = 15.0, elev_threshold = 0.15, , classify = False, preserve_classes = False) -> Lidar: ...
```
        '''
        return improved_ground_point_filter(self, input, block_size, max_building_size, slope_threshold, elev_threshold, classify, preserve_classes)