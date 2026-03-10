import os

AUTOMATIONS_PATH = "automations"


def list_automations():

    automations = []

    for name in os.listdir(AUTOMATIONS_PATH):

        path = os.path.join(AUTOMATIONS_PATH, name)

        main_file = os.path.join(path, "main.py")

        if os.path.isdir(path) and os.path.exists(main_file):

            automations.append(name)
            # Removed prepare() call to avoid creating directories for all automations on list

    return automations