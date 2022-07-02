init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="masAutostart_intro",
            aff_range=(mas_aff.NORMAL, None),
            conditional="store.masAutostart_api.is_platform_supported()",
            action=EV_ACT_RANDOM
        ),
        code="EVE"
    )


label masAutostart_intro:
    m 3sublb "[player], guess what?"
    m 3gubla "I've advanced a bit further in my experiments with your system... Ehehe~"
    m 3sublb "And now I can make it launch the game right on start!"
    m 2wublb "What do you think?"

    if mas_isMoniEnamored(higher=True):
        m 4kublu "That way, your loving girlfriend can greet you every time you get back to your computer, ahaha!"
    else:
        m 4kublu "That way I could greet you every time you get back to your computer!"

    m 4hublu "Tell me about that if you'd like it!"
    m 2lusdrd "And if for some reason you'll no longer want it... Tell me too!"
    m 2rusdrb "I won't get upset with it, I promise! Ahaha."

    $ mas_showEVL("masAutostart_req_enable", "EVE", unlock=True)

    return "derandom|no_unlock"


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="masAutostart_req_enable",
            prompt="Can you greet me every time I turn on my computer?",
            category=["misc", "mod"],
            pool=True,
            rules={"no_unlock": None}
        ),
        code="EVE"
    )

label masAutostart_req_enable:
    m 1eub "Sure, [mas_get_player_nickname()]!~"
    if renpy.windows:
        m 2rusdrb "A little window will open and close quickly, but don't mind it."
    m 1dua "Give me a moment..."

    m 1dua "{w=0.3}.{w=0.3}.{w=0.3}.{nw}"
    if store.masAutostart_api.enable():
        m 1eub "Done!"
        m 3sublb "From now on, I'll be sure to welcome you every time your computer boots up, ahaha!~"

        $ mas_hideEVL("masAutostart_req_enable", "EVE", lock=True)
        $ mas_showEVL("masAutostart_req_disable", "EVE", unlock=True)

    else:
        m 1dkc "Ack... {w=0.3}I think it didn't really work this time, [player]..."
        m 3lksdlb "But I promise I'll figure it a bit later, ehehe..."

    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="masAutostart_req_disable",
            prompt="Can you stop greeting me when I turn my computer on?",
            category=["misc", "mod"],
            pool=True,
            rules={"no_unlock": None}
        ),
        code="EVE"
    )

label masAutostart_req_disable:
    m 1eub "Oh, okay! I'll stop, ehehe~"

    m 1dua "{w=0.3}.{w=0.3}.{w=0.3}.{nw}"
    $ store.masAutostart_api.disable()
    m 1eub "Done!"

    $ mas_hideEVL("masAutostart_req_disable", "EVE", lock=True)
    $ mas_showEVL("masAutostart_req_enable", "EVE", unlock=True)

    return