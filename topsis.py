def run_topsis(input_file, weights_raw, impacts_raw, result_file):
    import pandas as pd
    import numpy as np
    import os

    if not os.path.isfile(input_file):
        raise FileNotFoundError("Input file not found")

    # Read file
    if input_file.endswith('.xlsx'):
        df = pd.read_excel(input_file)
    else:
        df = pd.read_csv(input_file, encoding='latin1')

    if len(df.columns) < 3:
        raise ValueError("Input file must contain three or more columns")

    data = df.iloc[:, 1:].values.astype(float)

    weights = [float(w) for w in weights_raw.split(',')]
    impacts = impacts_raw.split(',')

    if len(weights) != len(impacts) or len(weights) != data.shape[1]:
        raise ValueError("Weights, impacts, and criteria count must match")

    for i in impacts:
        if i not in ['+', '-']:
            raise ValueError("Impacts must be + or -")

    # Normalize
    norm_data = data / np.sqrt((data**2).sum(axis=0))

    # Weighted matrix
    weighted_data = norm_data * weights

    # Ideal best & worst
    p_ideal, n_ideal = [], []
    for i in range(len(impacts)):
        if impacts[i] == '+':
            p_ideal.append(weighted_data[:, i].max())
            n_ideal.append(weighted_data[:, i].min())
        else:
            p_ideal.append(weighted_data[:, i].min())
            n_ideal.append(weighted_data[:, i].max())

    s_best = np.sqrt(((weighted_data - p_ideal) ** 2).sum(axis=1))
    s_worst = np.sqrt(((weighted_data - n_ideal) ** 2).sum(axis=1))

    score = s_worst / (s_best + s_worst)

    df["Topsis Score"] = score
    df["Rank"] = df["Topsis Score"].rank(ascending=False).astype(int)

    df.to_csv(result_file, index=False)

if __name__ == "__main__":
    run_topsis()
