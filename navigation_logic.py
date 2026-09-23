def navigate_to_goal(current_position, goal_position):
    if current_position == goal_position:
        return "STOP"
    # Proactive obstacle avoidance logic
    if check_obstacle_ahead():
        return "LEFT" if check_left_clear() else "RIGHT"
    return "FORWARD"

def check_obstacle_ahead():
    # Placeholder for actual obstacle detection logic
    return False

def check_left_clear():
    # Placeholder for actual left path clearance check
    return True

def check_right_clear():
    # Placeholder for actual right path clearance check
    return True