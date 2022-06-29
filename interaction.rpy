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
    m "[player], guess what?"
    m "I've advanced a bit further in my experiments with your system... Ehehe~"
    m "And now I can make it launch the game right on start!"
    m "What do you think?"

    if mas_isMoniEnamored(higher=True):
        m "That way, your loving girlfriend can greet you every time you get back to your computer, ahaha!"
    else:
        m "That way I could greet you every time you get back to your computer!"

    m "Tell me about that if you'd like it!"
    m "And if for some reason you'll no longer want it... Tell me too!"
    m "I won't get upset with it, I promise! Ahaha."

    $ mas_showEVL("masAutostart_req_enable", "EVE", unlock=True)

    return "derandom|no_unlock"


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="masAutostart_req_enable",
            prompt="Can you greet me every time I turn on my computer?",
            category=["misc"],
            pool=True,
            rules={"no_unlock": None}
        ),
        code="EVE"
    )

label masAutostart_req_enable:
    m "Sure, [mas_get_player_nickname()]!~"
    m "Give me a moment..."

    m "{w=0.3}.{w=0.3}.{w=0.3}.{nw}"
    $ store.masAutostart_api.enable()
    m "Done!"

    m "From now on, I'll be sure to welcome you every time your computer boots up, ahaha!"
    m "Just please let me know if you'll me moving my folder, alright?~"

    $ mas_hideEVL("masAutostart_req_enable", "EVE", lock=True)
    $ mas_showEVL("masAutostart_req_disable", "EVE", unlock=True)

    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="masAutostart_req_disable",
            prompt="Can you stop greeting me when I turn my computer on?",
            category=["misc"],
            pool=True,
            rules={"no_unlock": None}
        ),
        code="EVE"
    )

label masAutostart_req_disable:
    m "Oh, okay! I'll stop, ehehe~"

    m "{w=0.3}.{w=0.3}.{w=0.3}.{nw}"
    $ store.masAutostart_api.disable()
    m "Done!"

    $ mas_hideEVL("masAutostart_req_disable", "EVE", lock=True)
    $ mas_showEVL("masAutostart_req_enable", "EVE", unlock=True)

    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="masAutostart_topic_reset"
        ),
        code="EVE"
    )

label masAutostart_topic_reset:
    return