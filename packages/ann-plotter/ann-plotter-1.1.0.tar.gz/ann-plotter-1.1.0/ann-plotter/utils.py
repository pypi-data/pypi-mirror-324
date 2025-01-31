def normalize_data(data):
    """Normalize data to range [0,1]."""
    min_val = min(data)
    max_val = max(data)
    return [(x - min_val) / (max_val - min_val) for x in data] if max_val > min_val else data
