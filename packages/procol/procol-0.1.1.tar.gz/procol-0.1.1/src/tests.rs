#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_single_event_prob() {
        let n = 10;
        let event_indices = vec![0, 1];
        let probabilities = vec![
            vec![0.2, 0.3, 0.1, 0.15, 0.25],
            vec![0.1, 0.2, 0.3, 0.1, 0.3],
        ];
        let result = single_event_prob(n, &event_indices, &probabilities);
        assert!(result >= 0.0 && result <= 1.0, "Probability out of range");
    }

    #[test]
    fn test_filling_prob() {
        let n = 10;
        let m = 5;
        let probabilities = vec![
            vec![0.2, 0.3, 0.1, 0.15, 0.25],
            vec![0.1, 0.2, 0.3, 0.1, 0.3],
            vec![0.15, 0.25, 0.2, 0.1, 0.3],
            vec![0.1, 0.3, 0.25, 0.2, 0.15],
            vec![0.2, 0.15, 0.3, 0.1, 0.25],
            vec![0.25, 0.1, 0.2, 0.3, 0.15],
            vec![0.3, 0.2, 0.1, 0.25, 0.15],
            vec![0.3, 0.2, 0.1, 0.15, 0.25],
            vec![0.25, 0.1, 0.2, 0.15, 0.3],
            vec![0.2, 0.3, 0.25, 0.15, 0.1],
        ];
        let result = filling_prob(n, m, probabilities).unwrap();
        assert!(result >= 0.0 && result <= 1.0, "Probability out of range");
    }

    #[test]
    fn test_invalid_probabilities_length() {
        let n = 10;
        let m = 5;
        let probabilities = vec![
            vec![0.2, 0.3, 0.1, 0.15, 0.25],
            vec![0.1, 0.2, 0.3, 0.1, 0.3],
        ];
        let result = filling_prob(n, m, probabilities);
        assert!(result.is_err(), "Expected an error due to invalid length");
    }

    #[test]
    fn test_invalid_inner_probabilities_length() {
        let n = 10;
        let m = 5;
        let probabilities = vec![
            vec![0.2, 0.3, 0.1, 0.15, 0.25],
            vec![0.1, 0.2, 0.3, 0.1],
            vec![0.15, 0.25, 0.2, 0.1, 0.3],
            vec![0.1, 0.3, 0.25, 0.2, 0.15],
            vec![0.2, 0.15, 0.3, 0.1, 0.25],
            vec![0.25, 0.1, 0.2, 0.3, 0.15],
            vec![0.3, 0.2, 0.1, 0.25, 0.15],
            vec![0.3, 0.2, 0.1, 0.15, 0.25],
            vec![0.25, 0.1, 0.2, 0.15, 0.3],
            vec![0.2, 0.3, 0.25, 0.15, 0.1],
        ];
        let result = filling_prob(n, m, probabilities);
        assert!(result.is_err(), "Expected an error due to invalid inner length");
    }
}

