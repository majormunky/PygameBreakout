listeners = []


def listen(cb, event_type):
    listeners.append((cb, event_type))

def post(event_type, data=None):
    for callback, e_type in listeners:
        if e_type == event_type:
            callback(data)
            
