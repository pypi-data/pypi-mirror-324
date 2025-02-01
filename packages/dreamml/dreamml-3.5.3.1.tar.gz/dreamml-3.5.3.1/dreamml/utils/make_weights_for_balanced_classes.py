def make_weights_for_balanced_classes(labels, num_labels):
    total_count = len(labels)
    count_per_class = [0] * num_labels
    for label in labels:
        count_per_class[label] += 1
    weight_per_class = [total_count / c if c > 0 else 0 for c in count_per_class]
    weights = [weight_per_class[label] for label in labels]
    return weights