import numpy as np

class LinearRegression:
    def __init__(self, learning_rate=0.01, iterations=1000, dive=False,
                 regularization=None, lambda_=0.1, l1_ratio=0.5):
        """
        Enhanced Linear Regression model with regularization support
        :param learning_rate: Step size for gradient descent
        :param iterations: Number of gradient descent iterations
        :param dive: Enable detailed logging of training process
        :param regularization: Type of regularization ('l1', 'l2', 'elastic_net')
        :param lambda_: Regularization strength
        :param l1_ratio: Mixing parameter for Elastic Net (0-1)
        """
        self.learning_rate = learning_rate
        self.iterations = iterations
        self.dive = dive
        self.regularization = regularization
        self.lambda_ = lambda_
        self.l1_ratio = l1_ratio
        self.weights = None
        self.bias = None
        self.y_pred = None
        
    def fit(self, X, y):
        """
        Train model with gradient descent and regularization
        """
        m, n = X.shape  # m = samples, n = features
        self.weights = np.zeros((n, 1))  # Proper shape for multiple features
        self.bias = 0
        
        y = y.reshape(-1, 1)  # Ensure proper shape
        
        # Initialize logging
        metrics = {'weights': [], 'bias': [], 'cost': []}
        
        for _ in range(self.iterations):
            # Compute predictions and errors
            y_pred = X @ self.weights + self.bias  # Matrix multiplication
            error = y_pred - y
            
            # Compute gradients (vectorized)
            dw = (2/m) * X.T @ error  # Correct gradient calculation
            db = (2/m) * np.sum(error)
            
            # Add regularization gradients
            if self.regularization == 'l2':
                dw += (self.lambda_/m) * self.weights
            elif self.regularization == 'l1':
                dw += (self.lambda_/m) * np.sign(self.weights)
            elif self.regularization == 'elastic_net':
                l1_grad = self.lambda_ * self.l1_ratio * np.sign(self.weights)
                l2_grad = self.lambda_ * (1 - self.l1_ratio) * self.weights
                dw += (l1_grad + l2_grad)/m
            
            # Update parameters
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db
            
            # Compute cost with regularization
            mse = np.mean(error**2)
            reg_cost = self._regularization_cost(m, n)
            total_cost = mse + reg_cost
            
            # Log metrics
            metrics['weights'].append(self.weights.copy())
            metrics['bias'].append(self.bias)
            metrics['cost'].append(total_cost)
        
        return metrics
    
    def _regularization_cost(self, m, n):
        """Calculate regularization term for cost function"""
        if not self.regularization:
            return 0
            
        l1_term = np.sum(np.abs(self.weights)) 
        l2_term = np.sum(self.weights**2)
        
        if self.regularization == 'l1':
            return (self.lambda_/m) * l1_term
        elif self.regularization == 'l2':
            return (self.lambda_/(2*m)) * l2_term
        elif self.regularization == 'elastic_net':
            return (self.lambda_/m) * (self.l1_ratio * l1_term + 
                                      (1 - self.l1_ratio)/2 * l2_term)
        return 0
    
    def predict(self, X):
        """Generate predictions using learned weights"""
        return X @ self.weights + self.bias



# import numpy as np
# from diveai.visualization import PlotBuilder

# def gradient_descent(X, y, initial_weights, initial_bias, learning_rate, iterations, dive=False):
#     """
#     Perform gradient descent with optional interactive visualization and logging.

#     Args:
#         X (numpy.ndarray): Feature matrix of shape (m, n).
#         y (numpy.ndarray): Target vector of shape (m,).
#         initial_weights (numpy.ndarray): Initial weights of shape (n, 1).
#         initial_bias (float): Initial bias term.
#         learning_rate (float): Learning rate for gradient descent.
#         iterations (int): Number of iterations.
#         dive (bool): If True, display plots and print progress. If False, run silently.

#     Returns:
#         tuple: Optimized weights and bias.
#     """
#     # Initialize weights and bias
#     weights = initial_weights
#     bias = initial_bias

#     # Logs for plotting
#     weight_log = []
#     bias_log = []
#     cost_log = []

#     m = X.shape[0]  # Number of examples

#     if dive:
#         # Create a Plotly Figure with 3 subplots:
#         pb = PlotBuilder(rows=1, cols=3, title="Gradient Descent Process", subplot_titles=("Cost vs Iterations", "Weights and Bias vs Iterations", "Data & Fit Line"))

#         pb.add_plot([], [], row=0, col=0, plot_type="line", color="blue", label="Cost")
#         pb.add_plot([], [], row=0, col=1, plot_type="line", color="orange", label="Weights")
#         pb.add_plot([], [], row=0, col=1, plot_type="line", color="green", label="Bias")
#         pb.add_plot(X[:, 0], y if y.ndim == 1 else y[:, 0], row=0, col=2, plot_type="scatter", color="black", label="Data")
#         pb.add_plot([], [], row=0, col=2, plot_type="line", color="red", label="Fit Line")

#         pb.set_labels(row=0, col=0, x_label="Iterations", y_label="Cost (MSE)")
#         pb.set_labels(row=0, col=1, x_label="Iterations", y_label="Value")
#         pb.set_labels(row=0, col=2, x_label="X", y_label="y")

#         pb.show()

#     # Gradient descent loop
#     for i in range(iterations):
#         # Compute predictions
#         y_pred = np.dot(X, weights) + bias

#         # Compute gradients
#         dw = -(1 / m) * np.dot(X.T, (y - y_pred))
#         db = -(1 / m) * np.sum(y - y_pred)

#         # Update weights and bias
#         weights -= learning_rate * dw
#         bias -= learning_rate * db

#         # Compute cost (Mean Squared Error)
#         cost = np.mean((y - y_pred) ** 2)

#         # Log values for plotting
#         weight_log.append(weights[0][0])  # Assuming weights is shape (1,1)
#         bias_log.append(bias)
#         cost_log.append(cost)

#         if dive:
#             pb.update_trace(list(range(len(cost_log))), cost_log, row=0, col=0, trace=0)
#             pb.update_trace(list(range(len(weight_log))), weight_log, row=0, col=1, trace=1)
#             pb.update_trace(list(range(len(bias_log))), bias_log, row=0, col=1, trace=2)
#             pb.update_trace(X[:, 0], y_pred if y_pred.ndim == 1 else y_pred[:, 0], row=0, col=2, trace=4, auto_range=True)
            
#             # Print progress (optional)
#             # print(
#             #     f"Iteration {i+1}/{iterations}, Cost: {cost:.6f}, Weight: {weights[0][0]:.6f}, Bias: {bias:.6f}"
#             # )

#     if dive:
#         print("Gradient Descent Complete!")

#     return weights, bias


# class LinearRegression:
#     def __init__(self, learning_rate=0.01, iterations=1000, dive=False):
#         """
#         Initialize the Linear Regression model with hyperparameters.
#         :param learning_rate: The step size for gradient descent.
#         :param iterations: Number of iterations to run gradient descent.
#         :param dive: If True, logs detailed information about the model derivation.
#         """
#         self.learning_rate = learning_rate
#         self.iterations = iterations
#         self.dive = dive  # Add dive parameter to the class
#         self.weights = None
#         self.bias = None

#         if self.dive:
#             print("Initializing Linear Regression Model with Dive Mode Enabled\n")
#             print("Step 1: Understanding the Cost Function")
#             print("The cost function used is Mean Squared Error (MSE):")
#             print("J(w, b) = (1/m) * Σ(y - y_pred)^2")
#             print("This measures how far our predictions are from the actual values.\n")

#             print("Step 2: Deriving Gradients for Optimization")
#             print("To minimize the cost function J(w, b), we compute its partial derivatives:")
#             print("∂J/∂w = -(1/m) * Σ(X.T * (y - y_pred))")
#             print("∂J/∂b = -(1/m) * Σ(y - y_pred)")
#             print("These gradients tell us how to adjust weights and bias to reduce the error.\n")

#             print("Step 3: Gradient Descent Update Rule")
#             print("Using the gradients, we update weights and bias as follows:")
#             print("weights = weights - learning_rate * ∂J/∂w")
#             print("bias = bias - learning_rate * ∂J/∂b\n")

#     def fit(self, X, y):
#         """
#         Train the model using gradient descent.
#         :param X: Feature matrix (numpy array of shape (m, n)).
#         :param y: Target vector (numpy array of shape (m, 1)).
#         """
#         # Number of training examples and features
#         m, n = X.shape

#         if self.dive:
#             print("\nStep 4: Training Process Begins")
#             print(f"Number of Training Examples: {m}, Features: {n}")
#             print(f"Learning Rate: {self.learning_rate}, Iterations: {self.iterations}")
#             print("Starting Gradient Descent...\n")

#         # Initialize weights and bias
#         self.weights = np.zeros((n, 1))
#         self.bias = 0

#         # Reshape y to ensure it's a column vector
#         y = y.reshape(-1, 1)

#         # Perform gradient descent with optional logging
#         self.weights, self.bias = gradient_descent(
#             X,
#             y,
#             self.weights,
#             self.bias,
#             self.learning_rate,
#             self.iterations,
#             self.dive,
#         )

#         if self.dive:
#             print("\nTraining Complete")
#             print(f"Final Weights: {self.weights.flatten()}, Final Bias: {self.bias:.6f}")

#     def predict(self, X):
#         """
#         Predict target values for given input features.
#         :param X: Feature matrix (numpy array of shape (m, n)).
#         :return: Predicted values (numpy array of shape (m, 1)).
#         """
#         return np.dot(X, self.weights) + self.bias
