import cupy as cp

def pairwise_distances(X):
    """
    Pairwise Euclidean distances using CuPy.
    :param X: A (n_samples, n_features) CuPy array.
    :return: A 2D CuPy array of distances (n_samples, n_samples).
    """
    X = X.reshape(X.shape[0], -1)
    r = cp.sum(X**2, axis=1, keepdims=True)

    distances = cp.maximum(r - 2 * cp.dot(X, X.T) + r.T, 0.0)

    return cp.sqrt(distances)

def diversity_score(population):
    """
    Calculates the diversity score of a population based on the
    Euclidean distances between individuals in the population.
   
    :param population: A CuPy array of shape (n_samples, n_features).
    :return: The function returns a CuPy array of diversity scores for each matrix in the population.
    """
    if len(population) < 2:
        return cp.zeros(len(population))
    
    population = cp.nan_to_num(population, nan=0.0)
    
    distances = pairwise_distances(population)
    distances = cp.maximum(distances, 1e-10)
    
    n_samples = len(population)
    
    mask = cp.ones((n_samples, n_samples), dtype=bool)
    cp.fill_diagonal(mask, 0) 

    avg_distances = cp.sum(distances * mask, axis=1) / (n_samples - 1)

    if population.shape[1] == 0:
        return cp.zeros(len(population))
        
    max_possible_distance = cp.sqrt(population.shape[1])
    max_possible_distance = float(max(max_possible_distance, 1e-10))
    
    diversity_scores = avg_distances / max_possible_distance
    
    return diversity_scores


def multi_head_fitness(y_true, y_pred, diversity_score, accuracy, alpha=2, beta=1.5, lambda_div=0.05):
    """
    Computes a fitness score based on accuracy, margin loss, and diversity score.
    
    :param y_true: Ground truth labels (CupPy array).
    :param y_pred: Predicted labels (CupPy array).
    :param diversity_score: Diversity score for a single weight matrix.
    :param accuracy: Model accuracy.
    :param alpha: Exponent for accuracy impact.
    :param beta: Exponent for margin loss impact.
    :param lambda_div: Weight for diversity score influence.
    :return: Computed fitness value.
    """
    incorrect = y_true != y_pred
    
    if cp.any(incorrect):
        margin_loss = cp.abs(y_true[incorrect] - y_pred[incorrect]).mean()
    else:
        margin_loss = 0.0

    margin_loss = cp.nan_to_num(margin_loss, nan=0.0)
    accuracy = max(accuracy, 1e-10) 

    fitness = (accuracy ** alpha) * ((1 - margin_loss) ** beta) * (1 + lambda_div * diversity_score)
    fitness = cp.nan_to_num(fitness, nan=0.0, posinf=1e10, neginf=-1e10)
    
    return fitness