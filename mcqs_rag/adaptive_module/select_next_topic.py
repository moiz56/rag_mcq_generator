
def select_next_topic(topic_stats, gamma=0.5):
    """
    Selects the next topic based on theta and coverage ratio.

    gamma: weight for balancing mastery vs coverage (0-1)
    """
    priority_scores = {}
    for topic, stats in topic_stats.items():
        mastery_gap = 1 - stats["theta"]  # higher if less mastered
        coverage_gap = 1 - stats["coverage_ratio"]  # higher if less attempted
        priority_scores[topic] = gamma * mastery_gap + (1 - gamma) * coverage_gap

    # Pick topic with highest priority
    next_topic = max(priority_scores, key=priority_scores.get)
    return next_topic
