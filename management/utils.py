def permission_check(user):
    if user.is_authenticated():
        return user.myuser.permission > 3
    else:
        return False

def permission_check2(user):
    if user.is_authenticated():
        return user.myuser.permission > 1
    else:
        return False

def permission_check3(user):
    if user.is_authenticated():
        return user.myuser.permission > 9
    else:
        return False
