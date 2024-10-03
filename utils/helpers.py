_global_state = {}

def set_global_state(key, value):
    _global_state[key] = value

def get_global_state(key, default=None):
    return _global_state.get(key, default)
