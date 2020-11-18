import config as cfg


def connect_db(user, password):

    if user == cfg.mysql['user'] and password == cfg.mysql['password']:
        return True
    else:
        return False

    # host - mysql.connector.errors.InterfaceError
    # pwd - mysql.connector.errors.ProgrammingError
    # user - mysql.connector.errors.NotSupportedError
