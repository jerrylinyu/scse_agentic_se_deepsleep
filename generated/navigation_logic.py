def decide_next_move(state):
    if state["front_blocked"] and state["left_blocked"] and state["right_blocked"]:
        return "STOP"
    if not state["front_blocked"]:
        if state["goal_ahead"]:
            return "FORWARD"
        else:
            if state["goal_on_left"] and not state["left_blocked"]:
                return "LEFT"
            elif state["goal_on_right"] and not state["right_blocked"]:
                return "RIGHT"
            else:
                if not state["left_blocked"]:
                    return "LEFT"
                elif not state["right_blocked"]:
                    return "RIGHT"
                else:
                    return "STOP"
    else:
        if state["goal_on_left"] and not state["left_blocked"]:
            return "LEFT"
        elif state["goal_on_right"] and not state["right_blocked"]:
            return "RIGHT"
        else:
            if not state["left_blocked"]:
                return "LEFT"
            elif not state["right_blocked"]:
                return "RIGHT"
            else:
                return "STOP"