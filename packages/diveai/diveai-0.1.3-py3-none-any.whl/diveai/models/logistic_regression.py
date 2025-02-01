import numpy as np

class LogisticRegression:
    def __init__(self, learning_rate=0.01, iterations=1000, threshold=0.5,
                 regularization=None, lambda_=0.1, l1_ratio=0.5):
        """
        Enhanced Logistic Regression model with regularization support
        :param learning_rate: Step size for gradient descent
        :param iterations: Number of gradient descent iterations
        :param threshold: Decision boundary threshold (0-1)
        :param regularization: Type of regularization ('l1', 'l2', 'elastic_net')
        :param lambda_: Regularization strength
        :param l1_ratio: Mixing parameter for Elastic Net (0-1)
        """
        self.learning_rate = learning_rate
        self.iterations = iterations
        self.threshold = threshold
        self.regularization = regularization
        self.lambda_ = lambda_
        self.l1_ratio = l1_ratio
        self.weights = None
        self.bias = None
        
    def _sigmoid(self, z):
        """Numerically stable sigmoid function with clipping"""
        z = np.clip(z, -500, 500)  # Prevent overflow
        return 1 / (1 + np.exp(-z))
    
    def fit(self, X, y):
        """
        Train model with gradient descent and regularization
        """
        m, n = X.shape  # m = samples, n = features
        self.weights = np.zeros((n, 1))  # Proper shape for features
        self.bias = 0
        
        y = y.reshape(-1, 1)  # Ensure proper shape
        
        # Initialize logging
        metrics = {'weights': [], 'bias': [], 'cost': []}
        
        for _ in range(self.iterations):
            # Compute predictions and gradient
            z = X @ self.weights + self.bias
            y_pred = self._sigmoid(z)
            
            # Calculate gradients
            error = y_pred - y
            dw = (1/m) * X.T @ error  # Logistic regression gradient
            db = (1/m) * np.sum(error)
            
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
            epsilon = 1e-15  # Numerical stability
            y_pred_clipped = np.clip(y_pred, epsilon, 1 - epsilon)
            cross_entropy = -np.mean(y * np.log(y_pred_clipped) + (1 - y) * np.log(1 - y_pred_clipped))
            reg_cost = self._regularization_cost(m, n)
            total_cost = cross_entropy + reg_cost
            
            # Log metrics
            metrics['weights'].append(self.weights.copy())
            metrics['bias'].append(self.bias)
            metrics['cost'].append(total_cost)
        
        return metrics
    
    def _regularization_cost(self, m, n):
        """Calculate regularization term (identical to linear regression version)"""
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
    
    def predict_proba(self, X):
        """Return predicted probabilities"""
        return self._sigmoid(X @ self.weights + self.bias)
    
    def predict(self, X):
        """Return class predictions using threshold"""
        probabilities = self.predict_proba(X)
        return (probabilities >= self.threshold).astype(int)



# import numpy as np
# from diveai.visualization import PlotBuilder

# def sigmoid(z):
#     return 1 / (1 + np.exp(-z))

# def binary_cross_entropy(y_true, y_pred):
#     epsilon = 1e-15
#     y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
#     return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))

# def gradient_descent(X, y, initial_weights, initial_bias, learning_rate, iterations, dive):
#     weights = initial_weights
#     bias = initial_bias
#     m = X.shape[0]

#     # Logs for plotting
#     weight_log = []
#     bias_log = []
#     cost_log = []

#     if dive:
#         pb = PlotBuilder(rows=1, cols=3, title="Logistic Regression Gradient Descent", 
#                             subplot_titles=("Cost vs Iterations", "Weights and Bias vs Iterations", "Data & Decision Boundary"))

#         pb.add_plot([], [], row=0, col=0, plot_type="line", color="blue", label="Cost")
#         pb.add_plot([], [], row=0, col=1, plot_type="line", color="orange", label="Weights")
#         pb.add_plot([], [], row=0, col=1, plot_type="line", color="green", label="Bias")
#         pb.add_plot(X[:, 0], X[:, 1], row=0, col=2, plot_type="scatter", color="black", label="Data")
#         # pb.add_plot(X[:, 0], y.flatten(), row=0, col=2, plot_type="scatter", color="black", label="Data")
#         pb.add_plot([], [], row=0, col=2, plot_type="line", color="red", label="Decision Boundary")

#         pb.set_labels(row=0, col=0, x_label="Iterations", y_label="Cost (Binary Cross-Entropy)")
#         pb.set_labels(row=0, col=1, x_label="Iterations", y_label="Value")
#         pb.set_labels(row=0, col=2, x_label="X", y_label="y")

#         pb.show()

#     for i in range(iterations):
#         z = np.dot(X, weights) + bias
#         y_pred = sigmoid(z)

#         dw = (1 / m) * np.dot(X.T, (y_pred - y))
#         db = (1 / m) * np.sum(y_pred - y)

#         weights -= learning_rate * dw
#         bias -= learning_rate * db

#         cost = binary_cross_entropy(y, y_pred)

#         weight_log.append(weights[0][0])
#         bias_log.append(bias)
#         cost_log.append(cost)

#         if dive:
#             pb.update_trace(list(range(len(cost_log))), cost_log, row=0, col=0, trace=0)
#             pb.update_trace(list(range(len(weight_log))), weight_log, row=0, col=1, trace=1)
#             pb.update_trace(list(range(len(bias_log))), bias_log, row=0, col=1, trace=2)

#             # Update decision boundary
#             x_boundary = np.array([X[:, 0].min(), X[:, 0].max()])
#             y_boundary = -(weights[0][0] * x_boundary + bias) / weights[1][0]
#             # Update decision boundary
#             # decision_boundary = -bias / weights[0][0]
#             # pb.update_trace([decision_boundary], [0.5], row=0, col=2, trace=4)
#             pb.update_trace(x_boundary, y_boundary, row=0, col=2, trace=4, auto_range=True)

#             x_min, x_max = X[:, 0].min(), X[:, 0].max()
#             y_min, y_max = -0.1, 1.1  # Slightly extend y-axis for better visibility
#             # pb.update_trace([decision_boundary, decision_boundary], [y_min, y_max], row=0, col=2, trace=4, auto_range=True)
            

#     return weights, bias


# class LogisticRegression:
#     def __init__(self, learning_rate=0.01, iterations=1000, dive=False):
#         self.learning_rate = learning_rate
#         self.iterations = iterations
#         self.dive = dive
#         self.weights = None
#         self.bias = None

#         if self.dive:
#             print("Initializing Logistic Regression Model with Dive Mode Enabled\n")
#             print("Step 1: Understanding the Logistic Function")
#             print("The logistic function (sigmoid) is used to map linear outputs to probabilities:")
#             print("σ(z) = 1 / (1 + e^(-z))")
#             print("This function maps any real number to the range (0, 1).\n")

#             print("Step 2: Cost Function for Logistic Regression")
#             print("The cost function used is Binary Cross-Entropy:")
#             print("J(w, b) = -(1/m) * Σ(y * log(y_pred) + (1 - y) * log(1 - y_pred))")
#             print("This measures the dissimilarity between true labels and predicted probabilities.\n")

#             print("Step 3: Deriving Gradients for Optimization")
#             print("The gradients for logistic regression are:")
#             print("∂J/∂w = (1/m) * X.T * (σ(X*w + b) - y)")
#             print("∂J/∂b = (1/m) * Σ(σ(X*w + b) - y)")
#             print("These gradients are used to update weights and bias in gradient descent.\n")


#     def fit(self, X, y):
#         m, n = X.shape
#         self.weights = np.zeros((n, 1))
#         self.bias = 0
#         y = y.reshape(-1, 1)

#         if self.dive:
#             print("\nStep 4: Training Process Begins")
#             print(f"Number of Training Examples: {m}, Features: {n}")
#             print(f"Learning Rate: {self.learning_rate}, Iterations: {self.iterations}")
#             print("Starting Gradient Descent...\n")

#         self.weights, self.bias = gradient_descent(
#             X, y, self.weights, self.bias, self.learning_rate, self.iterations, self.dive
#         )

#         if self.dive:
#             print("\nTraining Complete")
#             print(f"Final Weights: {self.weights.flatten()}, Final Bias: {self.bias:.6f}")

#     def predict_proba(self, X):
#         z = np.dot(X, self.weights) + self.bias
#         return sigmoid(z)

#     def predict(self, X, threshold=0.5):
#         probabilities = self.predict_proba(X)
#         return (probabilities >= threshold).astype(int)