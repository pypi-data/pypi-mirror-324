import numpy as np
from diveai.visualization import PlotBuilder

def gradient_descent(X, y, initial_weights, initial_bias, learning_rate, iterations, dive=False):
    """
    Perform gradient descent with optional interactive visualization and logging.

    Args:
        X (numpy.ndarray): Feature matrix of shape (m, n).
        y (numpy.ndarray): Target vector of shape (m,).
        initial_weights (numpy.ndarray): Initial weights of shape (n, 1).
        initial_bias (float): Initial bias term.
        learning_rate (float): Learning rate for gradient descent.
        iterations (int): Number of iterations.
        dive (bool): If True, display plots and print progress. If False, run silently.

    Returns:
        tuple: Optimized weights and bias.
    """
    # Initialize weights and bias
    weights = initial_weights
    bias = initial_bias

    # Logs for plotting
    weight_log = []
    bias_log = []
    cost_log = []

    m = X.shape[0]  # Number of examples

    if dive:
        # Create a Plotly Figure with 3 subplots:
        pb = PlotBuilder(rows=1, cols=3, title="Gradient Descent Process", subplot_titles=("Cost vs Iterations", "Weights and Bias vs Iterations", "Data & Fit Line"))

        pb.add_plot([], [], row=0, col=0, plot_type="line", color="blue", label="Cost")
        pb.add_plot([], [], row=0, col=1, plot_type="line", color="orange", label="Weights")
        pb.add_plot([], [], row=0, col=1, plot_type="line", color="green", label="Bias")
        pb.add_plot(X[:, 0], y if y.ndim == 1 else y[:, 0], row=0, col=2, plot_type="scatter", color="black", label="Data")
        pb.add_plot([], [], row=0, col=2, plot_type="line", color="red", label="Fit Line")

        pb.set_labels(row=0, col=0, x_label="Iterations", y_label="Cost (MSE)")
        pb.set_labels(row=0, col=1, x_label="Iterations", y_label="Value")
        pb.set_labels(row=0, col=2, x_label="X", y_label="y")

        pb.show()

    # Gradient descent loop
    for i in range(iterations):
        # Compute predictions
        y_pred = np.dot(X, weights) + bias

        # Compute gradients
        dw = -(1 / m) * np.dot(X.T, (y - y_pred))
        db = -(1 / m) * np.sum(y - y_pred)

        # Update weights and bias
        weights -= learning_rate * dw
        bias -= learning_rate * db

        # Compute cost (Mean Squared Error)
        cost = np.mean((y - y_pred) ** 2)

        # Log values for plotting
        weight_log.append(weights[0][0])  # Assuming weights is shape (1,1)
        bias_log.append(bias)
        cost_log.append(cost)

        if dive:
            pb.update_trace(list(range(len(cost_log))), cost_log, row=0, col=0, trace=0)
            pb.update_trace(list(range(len(weight_log))), weight_log, row=0, col=1, trace=1)
            pb.update_trace(list(range(len(bias_log))), bias_log, row=0, col=1, trace=2)
            pb.update_trace(X[:, 0], y_pred if y_pred.ndim == 1 else y_pred[:, 0], row=0, col=2, trace=4, auto_range=True)
            
            # Print progress (optional)
            # print(
            #     f"Iteration {i+1}/{iterations}, Cost: {cost:.6f}, Weight: {weights[0][0]:.6f}, Bias: {bias:.6f}"
            # )

    if dive:
        print("Gradient Descent Complete!")

    return weights, bias


class LinearRegression:
    def __init__(self, learning_rate=0.01, iterations=1000, dive=False):
        """
        Initialize the Linear Regression model with hyperparameters.
        :param learning_rate: The step size for gradient descent.
        :param iterations: Number of iterations to run gradient descent.
        :param dive: If True, logs detailed information about the model derivation.
        """
        self.learning_rate = learning_rate
        self.iterations = iterations
        self.dive = dive  # Add dive parameter to the class
        self.weights = None
        self.bias = None

        if self.dive:
            print("Initializing Linear Regression Model with Dive Mode Enabled\n")
            print("Step 1: Understanding the Cost Function")
            print("The cost function used is Mean Squared Error (MSE):")
            print("J(w, b) = (1/m) * Σ(y - y_pred)^2")
            print("This measures how far our predictions are from the actual values.\n")

            print("Step 2: Deriving Gradients for Optimization")
            print("To minimize the cost function J(w, b), we compute its partial derivatives:")
            print("∂J/∂w = -(1/m) * Σ(X.T * (y - y_pred))")
            print("∂J/∂b = -(1/m) * Σ(y - y_pred)")
            print("These gradients tell us how to adjust weights and bias to reduce the error.\n")

            print("Step 3: Gradient Descent Update Rule")
            print("Using the gradients, we update weights and bias as follows:")
            print("weights = weights - learning_rate * ∂J/∂w")
            print("bias = bias - learning_rate * ∂J/∂b\n")

    def fit(self, X, y):
        """
        Train the model using gradient descent.
        :param X: Feature matrix (numpy array of shape (m, n)).
        :param y: Target vector (numpy array of shape (m, 1)).
        """
        # Number of training examples and features
        m, n = X.shape

        if self.dive:
            print("\nStep 4: Training Process Begins")
            print(f"Number of Training Examples: {m}, Features: {n}")
            print(f"Learning Rate: {self.learning_rate}, Iterations: {self.iterations}")
            print("Starting Gradient Descent...\n")

        # Initialize weights and bias
        self.weights = np.zeros((n, 1))
        self.bias = 0

        # Reshape y to ensure it's a column vector
        y = y.reshape(-1, 1)

        # Perform gradient descent with optional logging
        self.weights, self.bias = gradient_descent(
            X,
            y,
            self.weights,
            self.bias,
            self.learning_rate,
            self.iterations,
            self.dive,
        )

        if self.dive:
            print("\nTraining Complete")
            print(f"Final Weights: {self.weights.flatten()}, Final Bias: {self.bias:.6f}")

    def predict(self, X):
        """
        Predict target values for given input features.
        :param X: Feature matrix (numpy array of shape (m, n)).
        :return: Predicted values (numpy array of shape (m, 1)).
        """
        return np.dot(X, self.weights) + self.bias
