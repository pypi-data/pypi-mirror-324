import plotly.graph_objects as go
from IPython.display import display
from IPython import get_ipython
import sys
from itertools import cycle
import numpy as np

def is_jupyter_environment():
    """
    Checks if the code is running in a Jupyter Notebook or JupyterLab environment.
    """
    try:
        ipython = get_ipython()
        if ipython is not None:
            # If running in Jupyter environment, ipython will have a kernel
            if 'ipykernel' in sys.modules:
                return True
    except NameError:
        # Not running inside an IPython environment
        return False
    return False

class PlotBuilder:
    """
    A versatile Plotly-based plotting class that dynamically determines whether to use 2D or 3D based on the first plot.
    """
    def __init__(self, x_label=None, y_label=None, z_label=None, title=None):
        """
        Initializes the plot with optional axis labels and title.
        :param x_label: Label for the x-axis.
        :param y_label: Label for the y-axis.
        :param z_label: Label for the z-axis (for 3D plots, determined dynamically).
        :param title: Title of the overall figure.
        """
        self.x_label = x_label
        self.y_label = y_label
        self.z_label = z_label
        self.title = title
        self.is_3d = True if z_label else None  # Will be determined dynamically
        self.fig = go.Figure()
        self.set_labels(x_label=x_label, y_label=y_label, z_label=z_label, title=title)
        self.color_generator = cycle(['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan'])

    
    def add_plot(self, x, y, z=None, plot_type="line", color=None, label=None, opacity=1, size=5, colorscale="Reds", marker_symbol=None, show_scale=True):
        """
        Adds a 2D or 3D plot to the figure based on the provided data.
        :param x: x-coordinates.
        :param y: y-coordinates.
        :param z: z-coordinates (optional, determines 3D if provided in the first plot).
        :param plot_type: Type of plot ("line", "scatter", "bar").
        :param color: Color of the plot.
        :param label: Legend label.
        """
        if color is None:
            color = next(self.color_generator)
        if self.is_3d is None:
            self.is_3d = z is not None
        
        if self.is_3d:
            if z is None:
                raise ValueError("All plots must be 3D since the first plot was 3D.")
            if plot_type == "bar":
                raise ValueError("3D bar plots are not supported in Plotly.")
            if plot_type == 'surface':
                trace = go.Surface(x=x, y=y, z=z, name=label, colorscale=colorscale, opacity=opacity, showscale=show_scale, showlegend=True)
            else:
                trace = go.Scatter3d(x=x, y=y, z=z, mode='lines' if plot_type == "line" else 'markers',
                                 name=label, line=dict(color=color) if plot_type == "line" else dict(),
                                 marker=dict(color=color, size=size/2, opacity=opacity))
        else:
            if z is not None:
                raise ValueError("All plots must be 2D since the first plot was 2D.")
            if plot_type == "bar":
                trace = go.Bar(x=x, y=y, name=label, marker=dict(color=color))
            else:
                trace = go.Scatter(x=x, y=y, mode='lines' if plot_type == "line" else 'markers',
                                   name=label, line=dict(color=color) if plot_type == "line" else dict(),
                                   marker=dict(color=color, size=size, opacity=opacity), marker_symbol=marker_symbol)
        
        self.fig.add_trace(trace)
    
    def update_plot(self, x, y, z=None, trace_index=0, auto_range=True):
        """
        Updates the data of an existing plot.
        :param x: New x-coordinates.
        :param y: New y-coordinates.
        :param z: New z-coordinates (optional, required for 3D plots if first plot was 3D).
        :param trace_index: Index of the trace to update.
        """
        if trace_index < len(self.fig.data):
            with self.fig.batch_update():
                self.fig.data[trace_index].x = x
                self.fig.data[trace_index].y = y
                if self.is_3d:
                    if z is None:
                        raise ValueError("z-coordinates must be provided for 3D plots.")
                    self.fig.data[trace_index].z = z

                if auto_range:
                    def get_padded_range(values, factor=1.1):
                        min_val, max_val = min(values), max(values)
                        padding = (max_val - min_val) * (factor - 1) / 2  # Add padding symmetrically
                        return [min_val - padding, max_val + padding]

                    self.fig.update_xaxes(range=get_padded_range(x))
                    self.fig.update_yaxes(range=get_padded_range(y))

                    if self.is_3d:
                        self.fig.update_layout(scene=dict(zaxis=dict(range=get_padded_range(z)), ))


    
    def set_labels(self, x_label=None, y_label=None, z_label=None, title=None):
        """
        Sets axis labels and title.
        :param x_label: Label for x-axis.
        :param y_label: Label for y-axis.
        :param z_label: Label for z-axis (for 3D plots).
        :param title: Title for the plot.
        """
        if x_label:
            self.fig.update_layout(xaxis_title=x_label)
        if y_label:
            self.fig.update_layout(yaxis_title=y_label)
        if title:
            self.fig.update_layout(title_text=title)
        if self.is_3d and z_label:
            self.fig.update_layout(scene=dict(xaxis_title=x_label, yaxis_title=y_label, zaxis_title=z_label))
    
    def show(self):
        """
        Displays the figure.
        """
        if is_jupyter_environment():
            # If in Jupyter environment, use FigureWidget for interactivity
            self.fig = go.FigureWidget(self.fig)
            display(self.fig)

        else:
            self.fig.show()


class HeatmapPlotBuilder(PlotBuilder):
    """
    Specialized PlotBuilder for heatmap visualizations with confusion matrix support
    Maintains all original functionality while adding heatmap-specific features
    """
    
    def __init__(self, x_label="Predicted", y_label="Actual", title=None, 
                colorscale='Blues', show_scale=False):
        super().__init__(x_label=x_label, y_label=y_label, title=title)
        self.colorscale = colorscale
        self.show_scale = show_scale
        self._configure_layout()

    def _configure_layout(self):
        """Heatmap-specific layout configuration"""
        self.fig.update_layout(
            yaxis_autorange='reversed',
            plot_bgcolor='white',
            xaxis_showgrid=False,
            yaxis_showgrid=False
        )

    def add_heatmap(self, z, x_labels=None, y_labels=None, annotations=True):
        """
        Add heatmap data with automatic labels
        :param z: 2D array of values
        :param x_labels: List/array of labels for x-axis
        :param y_labels: List/array of labels for y-axis
        :param annotations: Show text annotations in cells
        """
        if len(np.array(z).shape) != 2:
            raise ValueError("Heatmap data must be 2D")

        x_labels = x_labels if x_labels is not None else [str(i) for i in range(len(z[0]))]
        y_labels = y_labels if y_labels is not None else [str(i) for i in range(len(z))]

        trace = go.Heatmap(
            z=z,
            x=x_labels,
            y=y_labels,
            colorscale=self.colorscale,
            showscale=self.show_scale,
            text=z if annotations else None,
            texttemplate="%{z}" if annotations else None,
            hoverinfo="x+y+z"
        )
        
        self.fig.add_trace(trace)
        return self

    def add_confusion_matrix(self, cm, class_labels=None):
        """
        Specialized method for confusion matrices
        :param cm: 2D confusion matrix array
        :param class_labels: List of class names (optional)
        """
        class_labels = class_labels if class_labels else [f"Class {i}" for i in range(len(cm))]
        return self.add_heatmap(cm, class_labels, class_labels)
