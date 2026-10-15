from generated.navigation_logic import decide_next_move

def test_goal_reached():
    state = {'target_reached': True}
    assert decide_next_move(state) == 'STOP'

def test_goal_ahead_clear():
    state = {'front_blocked': False, 'goal_ahead': True}
    assert decide_next_move(state) == 'FORWARD'

def test_front_blocked_goal_left():
    state = {'front_blocked': True, 'left_blocked': False, 'goal_on_left': True}
    assert decide_next_move(state) == 'LEFT'

def test_front_blocked_goal_right():
    state = {'front_blocked': True, 'right_blocked': False, 'goal_on_right': True}
    assert decide_next_move() == 'RIGHT'

def test_all_blocked():
    state = {'front_blocked': True, 'left_blocked': True, 'right_blocked': True}
    assert decide_next_move(state) == 'STOP'