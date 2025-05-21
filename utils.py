import os 
import sys

def create_standard_dirs(root_folder=r"C:\Users\shawk\Desktop\a.1"):
    """
    Creates standard subdirectories for the application.
    Based on user-provided one-liner (adapted for clarity in docstring):
    import os; [os.makedirs(os.path.join("C:/Users/shawk/Desktop/a.1", d), exist_ok=True) for d in ["Input_PDFs", "Output_Labels", "Output_SetupDocs", "Application_Templates", "Logs"]]
    """
    subdirs = ["Input_PDFs", "Output_Labels", "Output_SetupDocs", "Application_Templates", "Logs"]
    created_paths = []
    errors = []
    
    # Ensure root folder itself is handled correctly
    # This path might not be valid on all systems, so robust error handling is good.
    try:
        if not os.path.exists(root_folder):
            os.makedirs(root_folder, exist_ok=True)
            print(f"Created root folder: {root_folder}")
        else:
            print(f"Root folder already exists: {root_folder}")
    except OSError as e:
        # Catch specific OS errors like permission denied or invalid path
        errors.append(f"Error creating or accessing root folder {root_folder}: {e}")
        print(f"\nError creating or accessing root folder {root_folder}: {e}")
        # If root cannot be created/accessed, it might not be possible to create subdirs.
        # Depending on the error, you might want to stop here.
        # For this example, we'll let it try to create subdirs, 
        # but they will likely fail if root_folder is problematic.


    for d in subdirs:
        path = os.path.join(root_folder, d)
        try:
            os.makedirs(path, exist_ok=True)
            created_paths.append(path)
        except Exception as e:
            errors.append(f"Error creating {path}: {e}")
    
    if created_paths and not errors: # Only print success if no errors related to subdirs
        print("\nSuccessfully created/verified the following subdirectories:")
        for p in created_paths:
            print(f" - {p}")
    
    if errors:
        print("\nErrors occurred during directory creation:")
        for error in errors:
            print(error)
        # Suggest to the user to check the root path or permissions.
        print(f"\nPlease ensure the root path '{root_folder}' is valid and you have write permissions.")
        return False
    
    print(f"\nStandard application directories ensured under: {root_folder}")
    return True