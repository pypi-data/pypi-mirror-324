"""A module to contain plotting functions for PyProBE."""

from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Tuple

import numpy as np
import plotly.graph_objects as go
import polars as pl
from deprecated import deprecated
from numpy.typing import NDArray
from plotly.express.colors import sample_colorscale
from plotly.subplots import make_subplots
from sklearn.preprocessing import minmax_scale

if TYPE_CHECKING:
    from pyprobe.result import Result

from pyprobe.units import split_quantity_unit


def _retrieve_relevant_columns(
    result_obj: "Result", args: Tuple[Any, ...], kwargs: Dict[Any, Any]
) -> pl.DataFrame:
    """Retrieve relevant columns from a Result object for plotting.

    This function analyses the arguments passed to a plotting function and retrieves the
    used columns from the Result object.

    Args:
        result_obj: The Result object.
        args: The positional arguments passed to the plotting function.
        kwargs: The keyword arguments passed to the plotting function.

    Returns:
        A dataframe containing the relevant columns from the Result object.
    """
    kwargs_values = [
        v for k, v in kwargs.items() if isinstance(v, str) and k != "label"
    ]
    args_values = [v for v in args if isinstance(v, str)]
    all_args = set(kwargs_values + args_values)
    relevant_columns = []
    for arg in all_args:
        try:
            quantity, _ = split_quantity_unit(arg)

        except ValueError:
            continue
        if quantity in result_obj._polars_cache.quantities:
            relevant_columns.append(arg)
    if len(relevant_columns) == 0:
        raise ValueError(
            f"None of the columns in {all_args} are present in the Result object."
        )
    result_obj._polars_cache.collect_columns(*relevant_columns)
    return result_obj._get_data_subset(*relevant_columns)


try:
    import seaborn as _sns
except ImportError:
    _sns = None


def _create_seaborn_wrapper() -> Any:
    """Create a wrapped version of the seaborn package."""
    if _sns is None:

        class SeabornWrapper:
            def __getattr__(self, _: Any) -> None:
                """Raise an ImportError if seaborn is not installed."""
                raise ImportError(
                    "Optional dependency 'seaborn' is not installed. Please install by "
                    "running 'pip install seaborn' or installing PyProBE with seaborn "
                    "as an optional dependency: `pip install 'PyProBE-Data[seaborn]'."
                )

        return SeabornWrapper()

    wrapped_sns = type("SeabornWrapper", (), {})()

    def wrap_function(func: Callable[..., Any]) -> Callable[..., Any]:
        """Wrap a seaborn function.

        Args:
            func (Callable): The function to wrap.
        """

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """The wrapper function.

            Modifies the 'data' argument to seaborn functions to be compatible with
            PyProBE Result objects.

            Args:
                *args: The positional arguments.
                **kwargs: The keyword arguments.

            Returns:
                The result of the wrapped function.
            """
            if "data" in kwargs:
                kwargs["data"] = _retrieve_relevant_columns(
                    kwargs["data"], args, kwargs
                ).to_pandas()
            if func.__name__ == "lineplot":
                if "estimator" not in kwargs:
                    kwargs["estimator"] = None
            return func(*args, **kwargs)

        return wrapper

    # Copy all seaborn attributes
    for attr_name in dir(_sns):
        if not attr_name.startswith("_"):
            attr = getattr(_sns, attr_name)
            if callable(attr):
                setattr(wrapped_sns, attr_name, wrap_function(attr))
            else:
                setattr(wrapped_sns, attr_name, attr)

    return wrapped_sns


seaborn = _create_seaborn_wrapper()
"""A wrapped version of the seaborn package.

Requires the seaborn package to be installed as an optional dependency. You can install
it with PyProBE by running :code:`pip install 'PyProBE-Data[seaborn]'`, or install it
seperately with :code:`pip install seaborn`.

This version of seaborn is modified to work with PyProBE Result objects. All functions
from the original seaborn package are available in this version. Where seaborn functions
accept a 'data' argument, a PyProBE Result object can be passed instead of a pandas
DataFrame. For example:

.. code-block:: python

    from pyprobe.plot import seaborn as sns

    result = cell.procedure['Sample']
    sns.lineplot(data=result, x="x", y="y")

Other modifications include:
    - The 'estimator' argument is set to None by default in the lineplot function for
    performance. This can be overridden by passing an estimator explicitly.

See the seaborn documentation for more information: https://seaborn.pydata.org/
"""


@deprecated(
    reason="The Plot class is deprecated as a user facing class. It is kept for "
    "powering the backend of the dashboard. For user facing plotting, use the "
    "plot, hvplot or seaborn plotting integrations.",
    version="1.1.4",
)
class Plot:
    """A class for plotting result objects with plotly.

    The Plot class is deprecated as a user facing class. It is kept for
    powering the backend of the dashboard. For user facing plotting, use the
    plot, hvplot or seaborn plotting integrations."

    Args:
        layout (go.Layout): The plotly layout to use.
    """

    title_font_size = 18
    axis_font_size = 14
    default_layout = go.Layout(
        template="simple_white",
        title_font=dict(size=title_font_size),
        xaxis_title_font=dict(size=title_font_size),
        yaxis_title_font=dict(size=title_font_size),
        xaxis_tickfont=dict(size=axis_font_size),
        yaxis_tickfont=dict(size=axis_font_size),
        legend_font=dict(size=axis_font_size),
        width=800,
        height=600,
    )

    def __init__(
        self,
        layout: go.Layout = default_layout,
    ):
        """Initialize the Plot object."""
        self.layout = layout
        self._fig = make_subplots(specs=[[{"secondary_y": True}]])
        self._fig.update_layout(layout)
        self.x_min: Optional[float] = None
        self.x_max: Optional[float] = None
        self.y_min: Optional[float] = None
        self.y_max: Optional[float] = None
        self.y2_min: Optional[float] = None
        self.y2_max: Optional[float] = None

        self.xaxis_title: Optional[str] = None
        self.yaxis_title: Optional[str] = None
        self.secondary_y: Optional[str] = None

    def show(self) -> None:
        """Show the plot."""
        self.fig.show()

    def add_line(
        self,
        result: "Result",
        x: str,
        y: str,
        secondary_y: Optional[str] = None,
        color: Optional[str] = None,
        label: Optional[str] = None,
        dash: str = "solid",
        showlegend: bool = True,
    ) -> "Plot":
        """Add a line to the plot.

        Args:
            result (Result): The result object.
            x (str): The x-axis dataframe column.
            y (str): The y-axis dataframe column.
            secondary_y (str): The secondary y-axis dataframe column.
            color (str): The color of the line.
            label (str): The label of the line.
            dash (str): The dash style of the line. E.g. "dash", "dot", "dashdot".
            showlegend (bool): Whether to show the legend.
        """
        if label is None:
            if "Name" in result.info:
                label = str(result.info["Name"])
            else:
                label = "Data"
        x_data, y_data = result.get(x, y)
        self._check_limits(x_data, y_data)
        self.xaxis_title = x
        self.yaxis_title = y
        x_data, y_data = result.get(x, y)
        self._fig.add_trace(
            go.Scatter(
                x=x_data,
                y=y_data,
                mode="lines",
                line=dict(color=color, dash=dash),
                name=label,
                showlegend=showlegend,
            )
        )

        if secondary_y is not None:
            self.secondary_y = secondary_y
            self._add_secondary_y_line(result, x, secondary_y)
        return self

    def _add_secondary_y_line(
        self,
        result: "Result",
        x: str,
        y: str,
        color: Optional[str] = None,
        label: Optional[str] = None,
    ) -> "Plot":
        """Add a secondary y-axis to the plot.

        Args:
            result (Result): The result object.
            x (str): The secondary x-axis column.
            y (str): The secondary y-axis column.
            color (str): The color of the line.
            label (str): The label of the line.
        """
        if color is None:
            color = str(result.info["color"])
        if label is None:
            label = str(result.info["Name"])
        x_data, y_data = result.get(x, y)
        self._check_limits(x_data, y_data)

        self._fig.add_trace(
            go.Scatter(
                x=x_data,
                y=y_data,
                mode="lines",
                line=dict(color=color, dash="dash"),
                name=label,
                yaxis="y2",
                showlegend=False,
            ),
            secondary_y=True,
        )

        return self

    def _add_secondary_y_legend(self, secondary_y_axis: str) -> None:
        """Add a legend for the secondary y-axis.

        Args:
            secondary_y_axis (str): The label for the secondary y-axis.
        """
        self._fig.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode="lines",
                line=dict(color="black", dash="dash"),
                name=secondary_y_axis,
                showlegend=True,
            )
        )

    def add_colorscaled_line(
        self, result: "Result", x: str, y: str, color_by: str, colormap: str = "viridis"
    ) -> "Plot":
        """Add a line to the plot colored continuously by a column.

        Args:
            result (Result): The result object.
            x (str): The x-axis column.
            y (str): The y-axis column.
            color_by (str): The column to color by.
            colormap (str): The colormap to use.
        """
        x_data, y_data = result.get(x, y)
        self._check_limits(x_data, y_data)
        self.xaxis_title = x
        self.yaxis_title = y

        unique_colors = result.data[color_by].unique(maintain_order=True).to_numpy()
        colors = self.make_colorscale(unique_colors, colormap)
        for i, condition in enumerate(unique_colors):
            subset = result.data.filter(pl.col(color_by) == condition)
            self._fig.add_trace(
                go.Scatter(
                    x=subset[x],
                    y=subset[y],
                    mode="lines",
                    line=dict(color=colors[i]),
                    name=str(unique_colors[i]),
                    showlegend=False,
                )
            )
        self.add_colorbar(
            [unique_colors.min(), unique_colors.max()], color_by, colormap
        )
        return self

    @staticmethod
    def make_colorscale(
        points: NDArray[np.float64], colormap: str = "viridis"
    ) -> List[str]:
        """Create a colorscale across discrete points.

        Args:
            colormap (str): The colormap to use.
            points (NDArray): An array of colors to generate colors for.
        """
        colors = sample_colorscale(colormap, minmax_scale(points))
        return colors

    def add_colorbar(
        self, color_bounds: List[float], color_by: str, colormap: str = "viridis"
    ) -> "Plot":
        """Add a colorbar to the plot.

        Args:
            color_bounds (NDArray[np.float64]): The bounds of the color scale.
            color_by (str): The column to color by.
            colormap (str): The colormap to use.
        """
        self._fig.add_trace(
            go.Heatmap(
                z=[color_bounds],  # Set z to the range of the color scale
                colorscale=colormap,  # choose a colorscale
                colorbar=dict(title=color_by),  # add colorbar
                opacity=0,
            )
        )
        return self

    @property
    def x_range(self) -> list[float]:
        """Return the x-axis range with a buffer."""
        if self.x_min is not None and self.x_max is not None:
            x_buffer = 0.05 * (self.x_max - self.x_min)
            return [self.x_min - x_buffer, self.x_max + x_buffer]
        else:
            return [0, 1]  # default range

    @property
    def y_range(self) -> list[float]:
        """Return the y-axis range with a buffer."""
        if self.y_min is not None and self.y_max is not None:
            y_buffer = 0.05 * (self.y_max - self.y_min)
            return [self.y_min - y_buffer, self.y_max + y_buffer]
        else:
            return [0, 1]  # default range

    @property
    def y2_range(self) -> list[float]:
        """Return the secondary y-axis range with a buffer."""
        if self.y2_min is not None and self.y2_max is not None:
            y2_buffer = 0.05 * (self.y2_max - self.y2_min)
            return [self.y2_min - y2_buffer, self.y2_max + y2_buffer]
        else:
            return [0, 1]  # default range

    def _check_limits(
        self, x_data: pl.DataFrame, y_data: pl.DataFrame, secondary_y: bool = False
    ) -> None:
        """Update plot limits to newly added data.

        Args:
            x_data (pl.DataFrame): The x-axis data.
            y_data (pl.DataFrame): The y-axis data.
            secondary_y (bool): Whether the data is on the secondary y-axis.
        """
        x_max = x_data.max()
        x_min = x_data.min()
        y_max = y_data.max()
        y_min = y_data.min()

        self.x_max = x_max if self.x_max is None else max(self.x_max, x_max)
        self.x_min = x_min if self.x_min is None else min(self.x_min, x_min)
        if secondary_y is False:
            self.y_max = y_max if self.y_max is None else max(self.y_max, y_max)
            self.y_min = y_min if self.y_min is None else min(self.y_min, y_min)
        else:
            self.y2_max = y_max if self.y2_max is None else max(self.y2_max, y_max)
            self.y2_min = y_min if self.y2_min is None else min(self.y2_min, y_min)

    @property
    def fig(self) -> go.Figure:
        """Return the plotly figure."""
        self._fig.update_xaxes(range=self.x_range)
        self._fig.update_yaxes(range=self.y_range)
        self._fig.update_layout(
            xaxis_title=self.xaxis_title, yaxis_title=self.yaxis_title
        )

        if self.secondary_y is not None:  # check if secondary y-axis exists
            self._fig.update_yaxes(
                range=self.y2_range, secondary_y=True
            )  # secondary y-axis
            self._add_secondary_y_legend(self.secondary_y)
            self._fig.update_layout(
                yaxis2=dict(title=self.secondary_y, overlaying="y", side="right"),
                yaxis2_tickfont=dict(size=Plot.axis_font_size),
                yaxis2_title_font=dict(size=Plot.title_font_size),
                legend=dict(x=1.2),
            )
        self._fig.update_layout(
            self.default_layout,
        )
        return self._fig
