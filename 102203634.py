import sys
import pandas as pd
import numpy as np

def validate_inputs(data, weights, impacts):
    if len(data.columns) < 3:
        raise ValueError("Input file must have at least three columns (one for alternatives and others for criteria).")

    if len(weights) != len(data.columns) - 1:
        raise ValueError("Number of weights must match the number of criteria.")

    if len(impacts) != len(data.columns) - 1:
        raise ValueError("Number of impacts must match the number of criteria.")

    if not all(impact in ["+", "-"] for impact in impacts):
        raise ValueError("Impacts must be either '+' (beneficial) or '-' (non-beneficial).")

def normalize_matrix(matrix):
    return matrix / np.sqrt((matrix ** 2).sum(axis=0))

def calculate_ideal_solutions(weighted_matrix, impacts):
    ideal_best = np.where(np.array(impacts) == "+", weighted_matrix.max(axis=0), weighted_matrix.min(axis=0))
    ideal_worst = np.where(np.array(impacts) == "+", weighted_matrix.min(axis=0), weighted_matrix.max(axis=0))
    return ideal_best, ideal_worst

def calculate_topsis_scores(weighted_matrix, ideal_best, ideal_worst):
    dist_best = np.sqrt(((weighted_matrix - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted_matrix - ideal_worst) ** 2).sum(axis=1))
    scores = dist_worst / (dist_best + dist_worst)
    ranks = scores.argsort()[::-1] + 1
    return scores, ranks

def topsis(input_file, weights, impacts, output_file):
    data = pd.read_csv(input_file)
    validate_inputs(data, weights, impacts)
    matrix = data.iloc[:, 1:].values
    norm_matrix = normalize_matrix(matrix)
    weighted_matrix = norm_matrix * weights
    ideal_best, ideal_worst = calculate_ideal_solutions(weighted_matrix, impacts)
    scores, ranks = calculate_topsis_scores(weighted_matrix, ideal_best, ideal_worst)
    data["Topsis Score"] = scores
    data["Rank"] = ranks
    data.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python <RollNumber>.py <input_file> <weights> <impacts> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    weights = list(map(float, sys.argv[2].split(",")))
    impacts = sys.argv[3].split(",")
    output_file = sys.argv[4]

    try:
        topsis(input_file, weights, impacts, output_file)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
