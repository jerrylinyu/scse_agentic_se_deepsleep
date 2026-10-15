def decide_next_move(state):
    target_reached = state.get("target_reached", False)
    front_blocked = state.get("front_blocked", False)
    left_blocked = state.get("left_blocked", False)
    right_blocked = state.get("right_blocked", False)
    goal_ahead = state.get("goal_ahead", False)
    goal_on_left = state.get("goal_on_left", False)
    goal_on_right = state.get("goal_on_right", False)

    if target_reached:
        return "STOP"

    if front_blocked and left_blocked and right_blocked:
        return "STOP"

    if goal_ahead and not front_blocked:
        return "FORWARD"

    if goal_on_left and not left_blocked:
        return "LEFT"

    if goal_on_right and not right_blocked:
        return "RIGHT"

    if not front_blocked:
        return "FORWARD"

    if not left_blocked:
        return "LEFT"

    if not right_blocked:
        return "RIGHT"

    return "STOP"