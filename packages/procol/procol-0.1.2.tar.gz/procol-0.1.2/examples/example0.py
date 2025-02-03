from procol import filling_prob

if __name__ == "__main__":
    # Example usage:
    n = 10  # Number of independent discrete random variables
    m = 5   # Number of events
    probabilities = [
        [0.2, 0.3, 0.1, 0.15, 0.25],  # Probabilities for the first random variable
        [0.1, 0.2, 0.3, 0.1, 0.3],    # Probabilities for the second random variable
    ]

    result = filling_prob(n, m, probabilities)
    print(f"Filling Probability: {result}")

