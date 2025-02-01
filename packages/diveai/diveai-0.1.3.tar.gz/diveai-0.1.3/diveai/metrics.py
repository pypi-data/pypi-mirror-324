import numpy as np

def mean_squared_error(y_true, y_pred):
    """
    Calculate Mean Squared Error (MSE).
    :param y_true: True target values.
    :param y_pred: Predicted target values.
    :return: MSE value.
    """
    return np.mean((y_true - y_pred) ** 2)

def r2_score(y_true, y_pred):
    """
    Calculate R-squared score. (same as scikit-learn's r2_score)
    :param y_true: True target values.
    :param y_pred: Predicted target values.
    :return: R-squared score.
    """
    ss_total = np.sum((y_true - np.mean(y_true)) ** 2)
    ss_residual = np.sum((y_true - y_pred) ** 2)
    return 1 - (ss_residual / ss_total)

def accuracy_score(y_true, y_pred):
    """
    Calculate accuracy score.
    :param y_true: True target values.
    :param y_pred: Predicted target values.
    :return: Accuracy score.
    """
    correct = sum(a == b for a, b in zip(y_true, y_pred))
    total = len(y_true)
    return correct / total

def accuracy_score(y_true, y_pred):
    correct = np.sum(y_true == y_pred)
    return correct / len(y_true)

def precision_score(y_true, y_pred):
    tp = np.sum((y_true == 1) & (y_pred == 1))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    return tp / (tp + fp) if (tp + fp) > 0 else 0

def recall_score(y_true, y_pred):
    tp = np.sum((y_true == 1) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    return tp / (tp + fn) if (tp + fn) > 0 else 0

def f1_score(y_true, y_pred):
    p = precision_score(y_true, y_pred)
    r = recall_score(y_true, y_pred)
    return 2 * (p * r) / (p + r) if (p + r) > 0 else 0

def roc_auc_score(y_true, y_proba, n_thresholds=100):
    # Sort probabilities and corresponding true labels
    indices = np.argsort(y_proba)[::-1]
    y_proba_sorted = y_proba[indices]
    y_true_sorted = y_true[indices]
    
    # Initialize variables
    tpr, fpr = [0], [0]
    auc = 0
    prev_fpr, prev_tpr = 0, 0
    total_pos = np.sum(y_true == 1)
    total_neg = np.sum(y_true == 0)
    
    # Calculate ROC curve points
    for i in range(1, len(y_proba_sorted)):
        threshold = y_proba_sorted[i]
        y_pred_thresh = y_proba >= threshold
        
        tp = np.sum((y_true == 1) & y_pred_thresh)
        fp = np.sum((y_true == 0) & y_pred_thresh)
        
        current_tpr = tp / total_pos if total_pos > 0 else 0
        current_fpr = fp / total_neg if total_neg > 0 else 0
        
        # Add area segment
        auc += (current_fpr - prev_fpr) * (current_tpr + prev_tpr) / 2
        
        tpr.append(current_tpr)
        fpr.append(current_fpr)
        prev_tpr = current_tpr
        prev_fpr = current_fpr
    
    return max(auc, 0)  # Ensure non-negative

def confusion_matrix(y_true, y_pred, labels=None):
    """
    Compute confusion matrix to evaluate the accuracy of a classification.

    Parameters:
    y_true : array-like of shape (n_samples,)
        Ground truth (correct) target values.
    y_pred : array-like of shape (n_samples,)
        Estimated targets as returned by a classifier.
    labels : array-like of shape (n_classes), default=None
        List of labels to index the matrix. If None, the unique values in y_true and y_pred are used.

    Returns:
    confusion_matrix : ndarray of shape (n_classes, n_classes)
        Confusion matrix whose i-th row and j-th column entry indicates the number of samples with 
        true label i and predicted label j.
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)

    if labels is None:
        labels = np.sort(np.unique(np.concatenate((y_true, y_pred))))
    else:
        labels = np.asarray(labels)

    n_labels = labels.size
    matrix = np.zeros((n_labels, n_labels), dtype=int)

    for i, true_label in enumerate(labels):
        for j, pred_label in enumerate(labels):
            matrix[i, j] = np.sum((y_true == true_label) & (y_pred == pred_label))

    return matrix
