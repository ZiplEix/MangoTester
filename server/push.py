import os
from program.print import print_error, print_successful
from program.check import has_mango_db, has_mango_folder

MANGO_DB = os.path.expanduser("~/.mango/mangodb")
MANGO_LOCAL = "./mango"


def remove_folder(path: str):
    if ".." in path:
        return 1
    os.system(f"rm -rf {path}")


def delete_user_tests(category: str):
    name = os.getlogin() + "_"
    for test in os.listdir(os.path.join(MANGO_DB, category)):
        if test.startswith(name):
            remove_folder(os.path.join(MANGO_DB, category, test))


def push(flags):
    name = os.getlogin() + "_"
    # For all the category on the mango folder
    if not has_mango_folder() or not has_mango_db():
        return
    for category in os.listdir(MANGO_LOCAL):
        category_folder = os.path.join(MANGO_LOCAL, category)
        # Ignore files
        if not os.path.isdir(category_folder):
            continue

        print("On category:", category)

        # If category don't exist on remote:
        if not os.path.exists(os.path.join(MANGO_DB, category)):
            # Create it.
            os.mkdir(os.path.join(MANGO_DB, category))
        else:
            # Delete all old tests.
            delete_user_tests(category)

        # Put all the new tests on the remote
        for test in os.listdir(category_folder):
            if not test.startswith(name):
                continue
            test_folder = os.path.join(category_folder, test)
            print("-", test)
            os.system(
                f"cp -r {test_folder} {os.path.join(MANGO_DB, category, test)}")

    # Update remote db
    status = os.system(
        f'cd {MANGO_DB} && git pull && git add --all && git commit -m "autocommit" && git push'
    )
    if status != 0:
        print_error("Some error happend during push...")
        return
    print_successful("Pushed successfully!")
