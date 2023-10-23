from typing import List, Tuple


def get_confusion_matrix(
    true_labels: List[int], predicted_labels: List[int], num_classes: int,
) -> List[List[int]]:

    if len(true_labels) != len(predicted_labels):
        raise ValueError("Invalid input shapes!")

    matrix = [[0] * num_classes for _ in range(num_classes)]

    for true_label, predicted_label in zip(true_labels, predicted_labels):
        if not (0 <= true_label < num_classes) or not (0 <= predicted_label < num_classes):
            raise ValueError("Invalid prediction classes!")

        matrix[true_label][predicted_label] += 1

    return matrix


def get_quality_factors(
    true_labels: List[int],
    predicted_labels: List[int],
) -> Tuple[int, int, int, int]:
    true_negatives, false_positives, false_negatives, true_positives = 0, 0, 0, 0

    for true_label, predicted_label in zip(true_labels, predicted_labels):
        if true_label == predicted_label:
            if true_label == 0:
                true_negatives += 1
            else:
                true_positives += 1
        else:
            if true_label == 0:
                false_positives += 1
            else:
                false_negatives += 1

    return true_negatives, false_positives, false_negatives, true_positives


def accuracy_score(true_labels: List[int], predicted_labels: List[int]) -> float:
    true_negatives, false_positives, false_negatives, true_positives = get_quality_factors(true_labels, predicted_labels)
    return (true_negatives + true_positives) / (true_negatives + true_positives + false_positives + false_negatives)


def precision_score(true_labels: List[int], predicted_labels: List[int]) -> float:
    true_negatives, false_positives, false_negatives, true_positives = get_quality_factors(true_labels, predicted_labels)
    return true_positives / (true_positives + false_positives)


def recall_score(true_labels: List[int], predicted_labels: List[int]) -> float:
    true_negatives, false_positives, false_negatives, true_positives = get_quality_factors(true_labels, predicted_labels)
    return true_positives / (true_positives + false_negatives)


def f1_score(y_true: List[int], y_pred: List[int]) -> float:
    _, fp, fn, tp = get_quality_factors(y_true, y_pred)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)

    return 2 * (precision * recall) / (precision + recall) if precision + recall != 0 else 0

