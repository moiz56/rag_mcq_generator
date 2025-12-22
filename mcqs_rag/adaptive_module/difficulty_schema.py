# Example difficulty level mapping
def difficulty_level(theta):
    if theta < 0.3:
        return "easy"
    elif theta < 0.7:
        return "medium"
    else:
        return "hard"