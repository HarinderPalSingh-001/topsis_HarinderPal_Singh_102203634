import sys
import pandas as pd
import numpy as np

def calculate_topsis(input_file, weights, impacts, output_file):
    data = pd.read_csv(input_file)
    if len(data.columns) < 3:
        raise ValueError("The input file must have at least three columns (Identifier + Criteria).")
    if len(weights) != len(data.columns) - 1:
        raise ValueError("The number of weights must equal the number of criteria.")
    if len(impacts) != len(data.columns) - 1:
        raise ValueError("The number of impacts must equal the number of criteria.")
    if not set(impacts).issubset({"+", "-"}):
        raise ValueError("Impacts must only contain '+' or '-' values.")
    decision_matrix = data.iloc[:, 1:].values
    normalized_matrix = decision_matrix / np.sqrt((decision_matrix ** 2).sum(axis=0))
    weighted_matrix = normalized_matrix * weights
    ideal_best = np.where(np.array(impacts) == "+", weighted_matrix.max(axis=0), weighted_matrix.min(axis=0))
    ideal_worst = np.where(np.array(impacts) == "+", weighted_matrix.min(axis=0), weighted_matrix.max(axis=0))
    distance_best = np.sqrt(((weighted_matrix - ideal_best) ** 2).sum(axis=1))
    distance_worst = np.sqrt(((weighted_matrix - ideal_worst) ** 2).sum(axis=1))
    topsis_scores = distance_worst / (distance_best + distance_worst)
    rankings = topsis_scores.argsort()[::-1] + 1
    data["Topsis Score"] = topsis_scores
    data["Rank"] = rankings
    data.to_csv(output_file, index=False)
    print(f"TOPSIS results successfully saved to {output_file}.")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script.py <input_file> <weights> <impacts> <output_file>")
        sys.exit(1)
    
    input_file_path = sys.argv[1]
    weights_list = list(map(float, sys.argv[2].split(",")))
    impacts_list = sys.argv[3].split(",")
    output_file_path = sys.argv[4]
    
    try:
        calculate_topsis(input_file_path, weights_list, impacts_list, output_file_path)
    except Exception as error:
        print(f"Error: {error}")
        sys.exit(1)
