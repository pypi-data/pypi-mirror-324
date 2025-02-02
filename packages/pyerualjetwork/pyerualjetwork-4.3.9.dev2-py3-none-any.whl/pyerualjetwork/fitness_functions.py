import numpy as np
from scipy.spatial.distance import pdist

def diversity_score(population):
    """
    Calculates the diversity score of a population based on the
    Euclidean distances between individuals in the population.
    
    :param population: That calculates the diversity score of a population based on the Euclidean distances between
    individuals in the population
    :return: The function returns the diversity score,
    which is a measure of how spread out or diverse the population is in terms of their characteristics.
    """
    if len(population) < 2:
        return 0

    distances = pdist(population, metric='euclidean')

    if np.isnan(distances).any() or np.any(distances == 0):
        distances = np.maximum(distances, 1e-10)
    avg_distance = np.mean(distances)

    if population.shape[1] == 0:
        return 0

    max_possible_distance = np.sqrt(population.shape[1])

    if max_possible_distance == 0:
        max_possible_distance = 1e-10

    diversity = avg_distance / max_possible_distance
    
    return diversity



def hybrid_accuracy_confidence(y_true, y_pred, diversity_score, accuracy, alpha=2, beta=1.5, lambda_div=0.05):
    """
    The function calculates a fitness score based on accuracy, margin loss, and diversity score using
    specified parameters.
    
    @param y_true The `y_true` parameter represents the true labels of the data points. It is an array
    or list containing the actual labels of the data points.
    @param y_pred The `y_pred` parameter in the `hybrid_accuracy_confidence` function represents the
    predicted values for a given dataset. It is a NumPy array containing the predicted values for each
    sample in the dataset.
    @param diversity_score The `diversity_score` parameter in the `hybrid_accuracy_confidence` function
    represents a measure of diversity in the predictions. It is used as a factor in calculating the
    fitness of the model. The function combines accuracy, margin loss, and diversity score to evaluate
    the overall performance of the model
    @param accuracy Accuracy is a measure of the correct predictions made by a model. It is typically
    calculated as the number of correct predictions divided by the total number of predictions. In the
    context of the `hybrid_accuracy_confidence` function, the accuracy parameter represents the accuracy
    of the model's predictions.
    @param alpha Alpha is a parameter that controls the impact of accuracy on the overall fitness score
    in the hybrid_accuracy_confidence function. It is used as an exponent to raise the accuracy value
    to, influencing its contribution to the fitness calculation.
    @param beta The `beta` parameter in the `hybrid_accuracy_confidence` function is used as an exponent
    in the fitness calculation formula. It controls the impact of the margin loss term on the overall
    fitness value. A higher value of `beta` will amplify the effect of the margin loss term, making it
    @param lambda_div The `lambda_div` parameter in the `hybrid_accuracy_confidence` function represents
    the weight given to the diversity score in calculating the fitness value. It is a hyperparameter
    that controls the impact of diversity score on the overall fitness calculation. A higher value of
    `lambda_div` will increase the importance
    @return The function `hybrid_accuracy_confidence` returns the fitness value calculated based on the
    input parameters `y_true`, `y_pred`, `diversity_score`, `accuracy`, and optional parameters `alpha`,
    `beta`, and `lambda_div`. The fitness value is computed using a formula that combines accuracy,
    margin loss, and diversity score with specified weights and coefficients.
    """
    incorrect = y_true != y_pred
    margin_loss = np.abs(y_true[incorrect] - y_pred[incorrect]).mean() if np.any(incorrect) else 0

    fitness = (accuracy ** alpha) * ((1 - margin_loss) ** beta) * (1 + lambda_div * diversity_score)
    
    return fitness