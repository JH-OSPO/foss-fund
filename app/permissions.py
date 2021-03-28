from enum import IntFlag, auto

class Permission(IntFlag):
    ADMIN_PAGE = auto()

def is_allowed(user_perms, target_perms):
    return (user_perms & Permission[target_perms.upper()]) == Permission[target_perms.upper()]
