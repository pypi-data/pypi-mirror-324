import os, stat, shutil

def remove_dir_with_permissions(dir_path):
    def handle_permission_error(func, path, exc_info):
        os.chmod(path, stat.S_IWUSR)
        func(path)

    if os.path.exists(dir_path):
        shutil.rmtree(dir_path, onerror=handle_permission_error)