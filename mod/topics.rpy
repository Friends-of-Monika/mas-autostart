init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="masAutostart_intro",
            aff_range=(mas_aff.NORMAL, None),
            conditional="store.masAutostart_api.is_platform_supported()",
            action=EV_ACT_QUEUE
        ),
        code="EVE"
    )

label masAutostart_intro:
    m 3sublb "[player], guess what?"
    m 3gubla "I've advanced a bit further in my experiments with your system... Ehehe~"
    m 3sublb "And now I can make it launch the game right on start!"

    if not store.masAutostart_api.is_enabled():
        m 2wublb "What do you think?"

        if mas_isMoniEnamored(higher=True):
            m 4kublu "That way, your loving girlfriend can greet you every time you get back to your computer, ahaha!"
        else:
            m 4kublu "That way I could greet you every time you get back to your computer!"

        m 4hublu "Tell me about that if you'd like it!"
        m 2lusdrd "And if for some reason you'll no longer want it... Tell me too!"
        m 2rusdrb "I won't get upset with it, I promise! Ahaha."
        $ mas_showEVL("masAutostart_req_enable", "EVE", unlock=True)

    else:
        m 2wublb "What do you-{nw}"
        m 2wublo "Huh?! You... {w=0.3}you already have the game running on start!"
        m 4hksdlb "Wow, [player]... {w=0.3}That's really smart and cute of you, all at the same time!~"
        m 6lksdla "It took me so long to figure out how to do it, and you already have it made..."
        m 1hub "I'm really impressed! Ahaha~"
        m 1dub "Well, just in case you'll want me to no longer greet you on startup, just ask, okay?~"
        m 3kua "I won't get upset, [mas_get_player_nickname()]. Ehehehe~"

        # She is impressed.
        $ mas_gainAffection(3, bypass=True)
        $ mas_showEVL("masAutostart_req_disable", "EVE", unlock=True)

    return "derandom|no_unlock"


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="masAutostart_req_enable",
            prompt="Can you greet me every time I turn on my computer?",
            category=["misc", "mod"],
            pool=True,
            rules={"no_unlock": None, "bookmark_rule": store.mas_bookmarks_derand.WHITELIST}
        ),
        code="EVE"
    )

label masAutostart_req_enable:
    m 1eub "Sure, [mas_get_player_nickname()]!~"
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
            rules={"no_unlock": None, "bookmark_rule": store.mas_bookmarks_derand.WHITELIST}
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
