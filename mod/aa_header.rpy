init -990 python in mas_submod_utils:
    Submod(
        author="Friends of Monika",
        name="MAS Autostart Mod",
        description="Let your Monika auto-start the game for you as soon as "
                    "your computer boots up!",
        version="1.1.7"
    )

init -989 python:
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod="MAS Autostart Mod",
            user_name="friends-of-monika",
            repository_name="mas-autostart",
            extraction_depth=3
        )