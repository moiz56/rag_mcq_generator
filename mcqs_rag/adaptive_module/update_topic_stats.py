def update_topic_stats(topic_stats, topic, correct, learning_rate=0.1):
    """
    Update topic statistics based on student's response.

    Parameters:
    - topic_stats: dict of topic mastery and coverage
    - topic: the topic being updated
    - correct: bool, True if student answered correctly
    - learning_rate: how much to update theta (0-1)
    """
    stats = topic_stats[topic]

    # Update attempted count
    stats["attempted"] += 1

    # Update correct count
    if correct:
        stats["correct"] += 1

    # Update coverage ratio (attempted / total simulated MCQs for topic, here assume max 10)
    stats["coverage_ratio"] = min(stats["attempted"] / 10, 1.0)

    # Update theta (mastery) using simple online update
    # θ_new = θ_old + learning_rate * (reward - θ_old)
    reward = 1.0 if correct else 0.0
    stats["theta"] = stats["theta"] + learning_rate * (reward - stats["theta"])

    # Clamp theta between 0 and 1
    stats["theta"] = max(0.0, min(stats["theta"], 1.0))

    # Save back
    topic_stats[topic] = stats
