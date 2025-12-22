import random

def initialize_topic_stats(chapters):
    topic_stats = {}
    for topic in chapters:
        # Random theta between 0.2 and 0.8
        theta = round(random.uniform(0.2, 0.8), 2)
        # Random coverage ratio between 0 and 0.5
        coverage_ratio = round(random.uniform(0, 0.5), 2)

        topic_stats[topic] = {
            "attempted": int(coverage_ratio * 10),  # approximate attempts
            "correct": int(theta * coverage_ratio * 10),  # approximate correct answers
            "theta": theta,
            "coverage_ratio": coverage_ratio
        }
    return topic_stats