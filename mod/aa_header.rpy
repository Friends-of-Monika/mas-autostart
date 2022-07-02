init -990 python in mas_submod_utils:
    Submod(
        author="Friends of Monika",
        name="MAS Autostart Mod",
        description="Let your Monika auto-start the game for you as soon as "
                    "your computer boots up!",
        version="0.2.0"
    )

init -989 python:
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod="MAS Autostart Mod",
            user_name="friends-of-monika",
            repository_name="mas-autostart",
            submod_dir="/Submods/MAS Autostart Mod",
            extraction_depth=3,
            redirected_files=(
                "readme.md",
                "license.txt"
            )
        )