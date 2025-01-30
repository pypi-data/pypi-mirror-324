from django.contrib.auth import get_user_model
from .models import Role, Scope

User = get_user_model()

def create_role(name, description='', scopes=None):
    """
    Create a new role with the given name and description.

    Args:
        name (str): Name of the role
        description (str, optional): Description of the role. Defaults to ''.
        scopes (list, optional): List of scopes to assign to this role. 
            If not provided, the role will not have any scopes associated. Defaults to None.

    Returns:
        Role: The newly created role.
    """
    role = Role.objects.create(name=name, description=description)
    if scopes:
        for scope_name in scopes:
            scope, created = Scope.objects.get_or_create(name=scope_name)
            role.scopes.add(scope)
    role.save()
    return role

def assign_role_to_user(user, role_name):
    """
    Assigns a role to the given user.

    Args:
        user (User): The user to whom the role will be assigned.
        role_name (str): The name of the role to assign to the user.

    Raises:
        None

    If the role does not exist, a message is printed indicating that the 
    specified role does not exist.
    """

    try:
        role = Role.objects.get(name=role_name)
        user.roles.add(role)
        user.save()
    except Role.DoesNotExist:
        print(f"Role {role_name} does not exist")

def remove_role_from_user(user, role_name):
    """
    Removes a role from the given user.

    Args:
        user (User): The user from whom the role will be removed.
        role_name (str): The name of the role to remove from the user.

    Raises:
        None

    If the role does not exist, a message is printed indicating that the 
    specified role does not exist.
    """
    try:
        role = Role.objects.get(name=role_name)
        user.roles.remove(role)
        user.save()
    except Role.DoesNotExist:
        print(f"Role {role_name} does not exist")
