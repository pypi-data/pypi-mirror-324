from .models import Scope

def create_scope(name, description=''):
    """
    Creates a new scope with the given name and description.

    Args:
        name (str): Name of the scope to create.
        description (str, optional): Description of the scope. Defaults to ''.

    Returns:
        Scope: The newly created scope.
    """
    scope, created = Scope.objects.get_or_create(name=name, defaults={'description': description})
    if created:
        scope.save()
    return scope

def assign_scope_to_role(role, scope_name):
    """
    Assigns a scope to a role.

    Args:
        role (Role): The role to whom the scope will be assigned.
        scope_name (str): The name of the scope to assign to the role.

    Raises:
        None

    If the scope does not exist, a message is printed indicating that the 
    specified scope does not exist.
    """
    try:
        scope = Scope.objects.get(name=scope_name)
        role.scopes.add(scope)
        role.save()
    except Scope.DoesNotExist:
        print(f"Scope {scope_name} does not exist")

def remove_scope_from_role(role, scope_name):
    """
    Removes a scope from the given role.

    Args:
        role (Role): The role from which the scope will be removed.
        scope_name (str): The name of the scope to remove from the role.

    Raises:
        None

    If the scope does not exist, a message is printed indicating that the 
    specified scope does not exist.
    """

    try:
        scope = Scope.objects.get(name=scope_name)
        role.scopes.remove(scope)
        role.save()
    except Scope.DoesNotExist:
        print(f"Scope {scope_name} does not exist")
