def can_view_all(user):
    return (
        user.is_owner or
        user.has_role("view_all") or
        user.has_role("moderator") or
        user.has_role("vip")
    )


def can_edit(user, fiche):
    return (
        user.is_owner or
        user.has_role("editor") or
        (user.has_role("creator") and fiche.author == user)
    )


def can_delete(user):
    return (
        user.is_owner or
        user.has_role("moderator")
    )
