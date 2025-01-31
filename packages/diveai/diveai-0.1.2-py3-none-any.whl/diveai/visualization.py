# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# from IPython.display import display

# class PlotBuilder:
#     """
#     Helper class for building interactive plots with Plotly.
#     """
#     fig_widget = None
#     traces = {}

#     def __init__(self, rows=1, cols=1, x_label=None, y_label=None, title=None, subplot_titles=None):
#         """
#         Initializes the plot with optional labels and title.
#         :param x_label: Label for the x-axis.
#         :param y_label: Label for the y-axis.
#         :param title: Title of the plot.
#         """
#         self.rows=rows
#         self.cols=cols
#         self.x_label = x_label
#         self.y_label = y_label
#         self.title = title
#         # self.figure, self.ax = plt.subplots()
#         self.fig = make_subplots(
#             rows=rows, cols=cols,
#             subplot_titles=subplot_titles
#         )

#         self.fig.update_layout(title_text=title)
#         self.fig.update_xaxes(title_text=x_label)
#         self.fig.update_yaxes(title_text=y_label)


#     def add_plot(self, x, y, row=0, col=0, plot_type="line", color="blue", label=None, **kwargs):
#         """
#         Adds a plot to the figure based on the specified type.
#         :param x: x-coordinates of the data.
#         :param y: y-coordinates of the data.
#         :param plot_type: Type of plot (e.g., "line", "scatter", "bar").
#         :param color: Color of the plot elements.
#         :param label: Label for the plot in the legend.
#         :param kwargs: Additional keyword arguments for the plot function.
#         """
#         if self.rows == 1 and self.cols == 1:
#             if x.ndim > 1:
#                 x = x.flatten()
#             if y.ndim > 1:
#                 y = y.flatten()

#         plot_types = {
#             "line": go.Scatter(x=x, y=y, mode='lines', name=label, line=dict(color=color)),
#             "scatter": go.Scatter(x=x, y=y, mode='markers', name=label, marker=dict(color=color)),
#             "bar": go.Bar(x=x, y=y, name=label, marker_color=color)
#         }

#         if plot_type not in plot_types:
#             raise ValueError(f"Unsupported plot type: {plot_type}")
        
#         final_trace = plot_types[plot_type]

#         self.fig.add_trace(final_trace, row=row+1, col=col+1)

#     def update_trace(self, x, y, row=0, col=0, trace=0, auto_range=False):
#         """
#         Updates the x and y data of a trace in the figure.
#         :param x: New x-coordinates of the data.
#         :param y: New y-coordinates of the data.
#         :param row: Row index of the subplot.
#         :param col: Column index of the subplot.
#         :param trace: Index of the trace to update.
#         """

#         if self.rows == 1 and self.cols == 1:
#             raise ValueError("Cannot update trace in a single plot.")

#         self.traces[(row, col)] = self.traces.get((row, col), []) + [(x, y)]

#         min_x, max_x = min([min(t[0]) for t in self.traces[(row, col)]]), max([max(t[0]) for t in self.traces[(row, col)]])
#         min_y, max_y = min([min(t[1]) for t in self.traces[(row, col)]]), max([max(t[1]) for t in self.traces[(row, col)]]) * 1.1

#         with self.fig_widget.batch_update():
#             if auto_range:
#                 self.fig_widget.update_xaxes(autorange=True, row=row+1, col=col+1)
#                 self.fig_widget.update_yaxes(autorange=True, row=row+1, col=col+1)
#             else:
#                 self.fig_widget.update_xaxes(range=[min_x, max_x], row=row+1, col=col+1)
#                 self.fig_widget.update_yaxes(range=[min_y, max_y], row=row+1, col=col+1)

#             self.fig_widget.data[trace]["x"] = x
#             self.fig_widget.data[trace]["y"] = y


#     # def update_plot_data(self, data):
#     #     traces = data["traces"]
#     #     axes = data["axes"]

#     #     with self.fig_widget.batch_update():
#     #         for trace, updates in traces.items():
#     #             self.fig_widget.data[trace]["x"] = updates["x"]
#     #             self.fig_widget.data[trace]["y"] = updates["y"]

#     #         for axis, updates in axes.items():
#     #             if "autorange" in updates and updates["autorange"]:
#     #                 self.fig_widget.update_xaxes(autorange=True, row=axis[0]+1, col= axis[1]+1)
#     #                 self.fig_widget.update_yaxes(autorange=True, row=axis[0]+1, col= axis[1]+1)
#     #             else:
#     #                 self.fig_widget.update_xaxes(range=updates['range']['x'], row=axis[0]+1, col= axis[1]+1)
#     #                 self.fig_widget.update_yaxes(range=updates['range']['y'], row=axis[0]+1, col= axis[1]+1)


#     def set_labels(self, row=0, col=0, x_label=None, y_label=None, title=None):
#         if x_label:
#             self.fig.update_xaxes(title_text=x_label, row=row+1, col=col+1)
#         if y_label:
#             self.fig.update_yaxes(title_text=y_label, row=row+1, col=col+1)
#         if title:
#             if self.rows == 1 and self.cols == 1:
#                 self.fig.update_layout(title_text=title)
#             else:
#                 self.fig.layout.annotations[row*self.fig.layout.grid.cols + col].text = title


#     def show(self):
#         """
#         Applies labels, legend, title, and displays the final plot.
#         """
#         if self.fig_widget is not None and self.fig_widget.comm is not None:
#             print("Already displaying an interactive plot.")
#             return

#         # Convert the figure to a FigureWidget for interactive updates
#         self.fig_widget = go.FigureWidget(self.fig)
#         # Display the interactive figure in Jupyter Notebook
#         display(self.fig_widget)
