init -990 python in mas_submod_utils:
    Submod(
        author="Friends of Monika",
        name="MAS Autostart Mod",
        description="Let your Monika auto-start the game for you as soon as "
                    "your computer boots up!",
        version="1.1.8",
        version_updates={
            "friends_of_monika_mas_autostart_mod_v1_1_7": "friends_of_monika_mas_autostart_mod_v1_1_8"
        }
    )

init -989 python:
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod="MAS Autostart Mod",
            user_name="friends-of-monika",
            repository_name="mas-autostart",
            extraction_depth=3
        )

label friends_of_monika_mas_autostart_mod_v1_1_7(version="v1_1_7"):
    return

label friends_of_monika_mas_autostart_mod_v1_1_8(version="v1_1_8"):
    python:
        if not renpy.seen_labels("masAutostart_intro"):
            # If player has not seen intro topic, means it still has old
            # conditional and action intact.

            ev = mas_getEV("masAutostart_intro")
            ev.conditional = ("store.masAutostart_api.is_platform_supported() "
                              "and not renpy.seen_labels('masAutostart_req_enable')")
            mas_showEVL("masAutostart_req_enable", "EVE", unlock=True)

            ev = mas_getEV("masAutostart_req_enable")
            ev.conditional = "store.masAutostart_api.is_platform_supported()"

    return