def unpack(data):
    try:
        return (True, data['success'])
    except KeyError as ex:
        return (False, data['error'])
