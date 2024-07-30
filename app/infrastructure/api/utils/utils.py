import inspect
def get_class_attributes(cls):
    # Get all members of the class
    all_members = inspect.getmembers(cls)
    
    # Filter out callable and special attributes
    attributes = {name: value for name, value in all_members if not name.startswith('__') and not callable(value)}
    
    return attributes