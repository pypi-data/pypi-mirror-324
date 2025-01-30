from attrs import define, field
import matplotlib.colorbar
import matplotlib.collections
from matplotlib.ticker import MultipleLocator
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import Colormap
from mpl_toolkits.axes_grid1.axes_divider import AxesDivider
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.mpl.gridliner
import cmocean
import numpy as np

from gerg_plotting.plotting_classes.plotter import Plotter
from gerg_plotting.data_classes.bathy import Bathy


@define
class MapPlot(Plotter):
    """
    A class for plotting geographic data on maps using Cartopy and Matplotlib.

    Parameters
    ----------
    bathy : Bathy, optional
        Bathymetric data object
    grid_spacing : int, optional
        Spacing between gridlines in degrees, default is 1

    Attributes
    ----------
    sc : matplotlib.collections.PathCollection
        Scatter plot collection
    gl : cartopy.mpl.gridliner.Gridliner
        Gridliner for map coordinates
    cbar_var : matplotlib.colorbar.Colorbar
        Colorbar for plotted variable
    cbar_bathy : matplotlib.colorbar.Colorbar
        Colorbar for bathymetry
    """
    
    bathy: Bathy = field(default=None)  # Bathymetry data object
    sc: matplotlib.collections.PathCollection = field(init=False)  # Scatter plot collection
    gl: cartopy.mpl.gridliner.Gridliner = field(init=False)  # Gridliner for controlling map gridlines
    cbar_var: matplotlib.colorbar.Colorbar = field(init=False)  # Colorbar for the variable being plotted
    cbar_bathy: matplotlib.colorbar.Colorbar = field(init=False)  # Colorbar for bathymetry data
    grid_spacing: int = field(default=1)  # Spacing of the gridlines on the map in degrees


    def init_bathy(self) -> None:
        """
        Initialize bathymetry object based on map bounds.

        Creates a new Bathy object if none exists, using current map bounds.
        """
        if not isinstance(self.bathy, Bathy):
            self.bathy = Bathy(bounds=self.data.bounds)

    def set_up_map(self, fig=None, ax=None, var=None) -> tuple[str,Colormap,AxesDivider]|tuple[np.ndarray,Colormap,AxesDivider]:
        """
        Set up the base map with figure, axes, and color settings.

        Parameters
        ----------
        fig : matplotlib.figure.Figure, optional
            Figure to plot on
        ax : matplotlib.axes.Axes, optional
            Axes to plot on
        var : str, optional
            Variable name for color mapping

        Returns
        -------
        tuple
            (color, cmap, divider)
            - color : str or ndarray, Color values for plotting
            - cmap : matplotlib.colors.Colormap, Colormap for variable
            - divider : mpl_toolkits.axes_grid1.axes_divider.AxesDivider, Divider for colorbar placement
        """
        # Ensure the bounds exists
        self.data.detect_bounds(self.bounds_padding)
        # Ensure the fig and axes exist
        self.init_figure(fig=fig, ax=ax, geography=True)
        
        if var is None:
            color = 'k'  # Use black color if no variable is provided
            cmap = None
        else:
            if var == 'time':
                color_var_values = np.array(self.data.date2num())
            else:
                color_var_values = self.data[var].values.copy()
            color = color_var_values  # Color is determined by the variable data
            cmap = self.get_cmap(var)  # Get the appropriate colormap for the variable
        
        if self.data.bounds is not None:
            self.ax.set_extent([self.data.bounds.lon_min, self.data.bounds.lon_max,
                                self.data.bounds.lat_min, self.data.bounds.lat_max])  # Set map extent
        
        divider = make_axes_locatable(self.ax)  # Create a divider for colorbars
        return color, cmap, divider

    def add_coasts(self,show_coastlines) -> None:
        """
        Add coastlines to the map.

        Parameters
        ----------
        show_coastlines : bool
            Whether to display coastlines
        """
        if show_coastlines:
            self.ax.coastlines()

    def get_quiver_step(self,quiver_density) -> int|None:
        """
        Calculate step size for quiver plot density.

        Parameters
        ----------
        quiver_density : int or None
            Desired density of quiver arrows

        Returns
        -------
        int or None
            Step size for data slicing
        """
        if quiver_density is not None:
            step = round(len(self.data.u.values)/quiver_density)
        else:
            step = None
        return step

    def add_grid(self,grid:bool,show_coords:bool=True) -> None:
        """
        Add gridlines and coordinate labels to map.

        Parameters
        ----------
        grid : bool
            Whether to show gridlines
        show_coords : bool, optional
            Whether to show coordinate labels, default True
        """
        # Add gridlines if requested
        if grid:
            self.gl = self.ax.gridlines(draw_labels=True, linewidth=1, color='gray',
                                        alpha=0.4, linestyle='--')
            self.gl.xlocator = MultipleLocator(self.grid_spacing)  # Set grid spacing for x-axis
            self.gl.ylocator = MultipleLocator(self.grid_spacing)  # Set grid spacing for y-axis
        else:
            self.gl = self.ax.gridlines(draw_labels=True, linewidth=1, color='gray',
                                        alpha=0.0, linestyle='--')
            self.gl.xlocator = MultipleLocator(self.grid_spacing)  # Set grid spacing for x-axis
            self.gl.ylocator = MultipleLocator(self.grid_spacing)  # Set grid spacing for y-axis
        if show_coords:
            self.gl.top_labels = False  # Disable top labels
            self.gl.right_labels = False  # Disable right labels
            self.gl.xformatter = LONGITUDE_FORMATTER  # Format x-axis as longitude
            self.gl.yformatter = LATITUDE_FORMATTER  # Format y-axis as latitude
        else:
            self.gl.top_labels = False  # Disable top labels
            self.gl.right_labels = False  # Disable right labels
            self.gl.bottom_labels = False  # Disable top labels
            self.gl.left_labels = False  # Disable right labels

    def add_bathy(self, show_bathy, divider) -> None:
        """
        Add bathymetric contours to map.

        Parameters
        ----------
        show_bathy : bool
            Whether to display bathymetry
        divider : mpl_toolkits.axes_grid1.axes_divider.AxesDivider
            Divider for colorbar placement
        """
        if show_bathy:
            self.init_bathy()
            bathy_contourf = self.ax.contourf(self.bathy.lon, self.bathy.lat, self.bathy.depth,
                                              levels=self.bathy.contour_levels, cmap=self.bathy.cmap,
                                              vmin=self.bathy.vmin, transform=ccrs.PlateCarree(), extend='both')
            # Add a colorbar for the bathymetry
            self.cbar_bathy = self.bathy.add_colorbar(mappable=bathy_contourf, divider=divider,
                                                      fig=self.fig, nrows=self.nrows)

    def scatter(self, var: str | None = None, show_bathy: bool = True, show_coastlines:bool=True, pointsize=3, 
                linewidths=0, grid=True,show_coords=True, fig=None, ax=None) -> None:
        """
        Create scatter plot of points on map.

        Parameters
        ----------
        var : str or None, optional
            Variable name for color mapping
        show_bathy : bool, optional
            Whether to show bathymetry, default True
        show_coastlines : bool, optional
            Whether to show coastlines, default True
        pointsize : int, optional
            Size of scatter points, default 3
        linewidths : int, optional
            Width of point edges, default 0
        grid : bool, optional
            Whether to show grid, default True
        show_coords : bool, optional
            Whether to show coordinates, default True
        fig : matplotlib.figure.Figure, optional
            Figure to plot on
        ax : matplotlib.axes.Axes, optional
            Axes to plot on
        """
        color, cmap, divider = self.set_up_map(fig=fig, ax=ax, var=var)
        

        # Add bathymetry if needed
        self.add_bathy(show_bathy, divider)
        
        # Plot scatter points on the map
        self.sc = self.ax.scatter(self.data['lon'].values, self.data['lat'].values, linewidths=linewidths,
                                  c=color, cmap=cmap, s=pointsize, transform=ccrs.PlateCarree(),vmin=self.data[var].vmin,vmax=self.data[var].vmax)
        # Add a colorbar for the scatter plot variable
        self.cbar_var = self.add_colorbar(self.sc, var, divider, total_cbars=(2 if show_bathy else 1))

        self.add_coasts(show_coastlines)  # Add coastlines
        
        self.add_grid(grid=grid,show_coords=show_coords)


    def quiver(self,x:str='lon',y:str='lat',quiver_density:int=None,quiver_scale:float=None,grid:bool=True,show_bathy:bool=True,show_coastlines:bool=True,fig=None,ax=None) -> None:
        """
        Create quiver plot for vector data.

        Parameters
        ----------
        x : str, optional
            X-axis variable name, default 'lon'
        y : str, optional
            Y-axis variable name, default 'lat'
        quiver_density : int, optional
            Density of quiver arrows
        quiver_scale : float, optional
            Scaling factor for arrow length
        grid : bool, optional
            Whether to show grid, default True
        show_bathy : bool, optional
            Whether to show bathymetry, default True
        show_coastlines : bool, optional
            Whether to show coastlines, default True
        fig : matplotlib.figure.Figure, optional
            Figure to plot on
        ax : matplotlib.axes.Axes, optional
            Axes to plot on
        """
        # Ensure that data has speed
        self.data.calculate_speed(include_w=False)

        # Set up the map
        _, cmap, divider = self.set_up_map(fig=fig, ax=ax, var='speed')
        
        # Add bathymetry if needed
        self.add_bathy(show_bathy, divider)

        step = self.get_quiver_step(quiver_density)

        mappable = self.ax.quiver(self.data[x].values[::step], self.data[y].values[::step], 
                                        self.data.u.values[::step], self.data.v.values[::step], 
                                        self.data.speed.values[::step], cmap=cmap,
                                        pivot='tail', scale=quiver_scale, units='height')
        self.cbar_var = self.add_colorbar(mappable, 'speed', divider, total_cbars=(2 if show_bathy else 1))
        
        self.add_coasts(show_coastlines)  # Add coastlines

        self.add_grid(grid)
        
        
