from .models import Group, User

def create_group(name, description=''):
"""
Create a new group with the specified name and description.

If a group with the given name already exists, it will be retrieved instead
of creating a new one.

:param name: The name of the group to create.
:param description: An optional description for the group.
:return: The created or retrieved Group object.
"""

    group, created = Group.objects.get_or_create(name=name, defaults={'description': description})
    if created:
        group.save()
    return group

def add_user_to_group(user, group_name):
    """
    Add the given user to the specified group.

    If the group does not exist, the call is ignored.

    :param user: The User object to add to the group.
    :param group_name: The name of the group to add the user to.
    :return: None
    """
    try:
        group = Group.objects.get(name=group_name)
        group.members.add(user)
        group.save()
    except Group.DoesNotExist:
        print(f"Group {group_name} does not exist")

def remove_user_from_group(user, group_name):
    """
    Remove the given user from the specified group.

    If the group does not exist, the operation is ignored.

    :param user: The User object to remove from the group.
    :param group_name: The name of the group from which to remove the user.
    :return: None
    """

    try:
        group = Group.objects.get(name=group_name)
        group.members.remove(user)
        group.save()
    except Group.DoesNotExist:
        print(f"Group {group_name} does not exist")
