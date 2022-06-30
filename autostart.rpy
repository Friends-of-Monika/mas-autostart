# Using _masAutostart and not _mas_autostart to prevent collision
# with _mas_ prefixes used by MAS itself.
define persistent._masAutostart_enabled = False
define persistent._masAutostart_metadata = None


init python in masAutostart_log:

    ## Logging ##

    from store.mas_submod_utils import submod_log as log

    _LOG_PREFIX = "[MAS Autostart] "

    def info(message):
        log.info(_LOG_PREFIX + message)

    def warn(message):
        log.warning(_LOG_PREFIX + message)

    def error(message):
        log.error(_LOG_PREFIX + message)


init python in masAutostart_api:

    ## Initialization ##

    import os
    import store.masAutostart_log as log
    from store import persistent as persistent

    if renpy.windows:
        import subprocess

        _LAUNCHER_PATH = os.path.join(renpy.config.renpy_base, "DDLC.exe")
        _AUTOSTART_FILE = os.path.expandvars("%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\Monika After Story.lnk")
        _AUTOSTART_SHORTCUT_SCRIPT = os.path.join(renpy.config.gamedir, "Submods", "MAS Autostart Mod", "platform", "shortcut.vbs")

    elif renpy.linux:
        _LAUNCHER_PATH = os.path.join(renpy.config.renpy_base, "DDLC.sh")
        _AUTOSTART_FILE = os.path.join(os.environ.get("XDG_CONFIG_HOME", os.path.join(os.path.expanduser("~"), ".config")), "autostart", "Monika After Story.desktop")
        _AUTOSTART_FILE_TEMPLATE = os.path.join(renpy.config.gamedir, "Submods", "MAS Autostart Mod", "platform", "Monika After Story.desktop")

    elif renpy.macintosh:
        from xml.etree import ElementTree as xml

        _LAUNCHER_PATH = os.path.join(renpy.config.renpy_base, "..", "..", "MacOS", "DDLC")
        _AUTOSTART_FILE = os.path.join(os.path.expanduser("~"), "Library", "LaunchAgents", "monika.after.story.plist")
        _AUTOSTART_PLIST_TEMPLATE = os.path.join(renpy.config.gamedir, "Submods", "MAS Autostart Mod", "platform", "monika.after.story.plist")

    else:
        log.warn("Unsupported platform (not Windows, Linux or Macintosh.)")


    ## Helpers ##

    def is_platform_supported():
        return renpy.windows or renpy.linux or renpy.macintosh


    ## Enable check functions ##

    def is_enabled():
        if renpy.windows:
            return _is_enabled_windows()

        elif renpy.linux:
            return _is_enabled_linux()

        elif renpy.macintosh:
            return _is_enabled_macos()

        else:
            return False

    def _is_enabled_windows():
        if not os.path.exists(_AUTOSTART_FILE):
            return False

        return True

    def _is_enabled_linux():
        if not os.path.exists(_AUTOSTART_FILE):
            return False

        try:
            desktop_file = _map_file(_AUTOSTART_FILE, "r", _parse_desktop_file)

        except IOError as e:
            log.error("Could not parse desktop file " + _AUTOSTART_FILE + ".")
            return False

        if "Desktop Entry" not in desktop_file or "Exec" not in desktop_file["Desktop Entry"]:
            log.error("File " + _AUTOSTART_FILE + " exists, but is not a valid desktop file.")
            return False

        if desktop_file["Desktop Entry"]["Exec"] != _LAUNCHER_PATH:
            log.error("File " + _AUTOSTART_FILE + " exists, but points to wrong location.")
            return False

        return True

    def _is_enabled_macos():
        if not os.path.exists(_AUTOSTART_FILE):
            return False

        try:
            plist_file = _map_file(_AUTOSTART_FILE, "r", xml.fromstring)

        except OSError as e:
            log.error("Could not parse LaunchAgent file {0} ({1}.)".format(_AUTOSTART_FILE, e))
            return

        path = plist_file.find(".//array/string")
        if not path:
            return False

        return path == _LAUNCHER_PATH


    ## Enable functions ##

    def enable():
        if renpy.windows:
            _enable_windows()

        elif renpy.linux:
            _enable_linux()

        elif renpy.macintosh:
            _enable_macos()

    def _enable_windows():
        subprocess.call((
            "cscript",
            _AUTOSTART_SHORTCUT_SCRIPT,
            _AUTOSTART_FILE,
            _LAUNCHER_PATH,
            os.path.dirname(_LAUNCHER_PATH)
        ))

        persistent._masAutostart_metadata = ("windows", _AUTOSTART_FILE, _LAUNCHER_PATH)


    def _enable_linux():
        try:
            desktop_file = _map_file(_AUTOSTART_FILE_TEMPLATE, "r", _parse_desktop_file)
            desktop_file["Desktop Entry"]["Exec"] = _LAUNCHER_PATH

        except OSError as e:
            log.error("Could not parse template desktop file {0} ({1}.)".format(_AUTOSTART_FILE_TEMPLATE, e))
            return

        try:
            try:
                os.makedirs(os.path.dirname(_AUTOSTART_FILE))

            except OSError as e:
                if e.errno != 17:
                    raise

            _map_file(_AUTOSTART_FILE, "w", _serialize_desktop_file, [desktop_file])
            persistent._masAutostart_enabled = True

        except OSError as e:
            log.error("Could not write desktop file {0} ({1}.)".format(_AUTOSTART_FILE, e))

        persistent._masAutostart_metadata = ("linux", _AUTOSTART_FILE, _LAUNCHER_PATH)

    def _enable_macos():
        try:
            plist_file = _map_file(_AUTOSTART_PLIST_TEMPLATE, "r", xml.fromstring)
            plist_file.find(".//array/string").text = _LAUNCHER_PATH

        except OSError as e:
            log.error("Could not parse template plist file {0} ({1}.)".format(_AUTOSTART_PLIST_TEMPLATE, e))
            return

        def dump(fp):
            fp.write(_map_file(_AUTOSTART_FILE, "r", lambda fp: "".join(fp.readlines()[:2])))
            xml.write(fp)

        try:
            try:
                os.makedirs(os.path.dirname(_AUTOSTART_FILE))

            except OSError as e:
                if e.errno != 17:
                    raise

            _map_file(_AUTOSTART_FILE, "w", dump)

        except OSError as e:
            log.error("Could not write LaunchAgent file {0} ({1}.)".format(_AUTOSTART_FILE, e))

        persistent._masAutostart_metadata = ("macos", _AUTOSTART_FILE, _LAUNCHER_PATH)


    ## Disable functions ##

    def disable():
        if renpy.windows or renpy.linux or renpy.macintosh:
            _disable_delete_desktop_file()

    def _disable_delete_desktop_file():
        try:
            os.remove(_AUTOSTART_FILE)

            if persistent._masAutostart_metadata is not None:
                try:
                    os.remove(persistent._masAutostart_metadata[1])

                except FileNotFoundError:
                    pass

        except FileNotFoundError:
            pass

        except OSError as e:
            log.error("Could not delete " + _AUTOSTART_FILE + ".")


    ## Utility methods ##

    def _parse_desktop_file(fp):
        obj = dict()

        _group = None
        param = dict()

        def push_group():
            if _group is None:
                obj.update(param)
            else:
                obj[_group] = param

            _parse_desktop_file._group = None
            _parse_desktop_file.param = dict()

        while True:
            line = fp.readline()
            if not line:
                push_group()
                return obj

            line = line.strip()
            if not line or line[0] == "#":
                continue

            if line[0] == "[" and line[-1] == "]":
                push_group()
                _group = line[1:-1]
            else:
                _key, _, _value = line.partition("=")
                param[_key] = _value

    def _serialize_desktop_file(fp, desktop_file):
        if "" in desktop_file:
            for _key, _value in desktop_file[""].items():
                fp.write("{0}={1}\n".format(_key, _value))

            fp.write("\n")

        for _group in (_group for _group in desktop_file.keys() if _group != ""):
            fp.write("[{0}]\n".format(_group))
            for _key, _value in desktop_file[_group].items():
                fp.write("{0}={1}\n".format(_key, _value))

    def _map_file(path, mode, fun, args=None):
        if args is None:
            args = list()

        fp = open(path, mode)

        try:
            return fun(fp, *args)

        finally:
            fp.close()


init 1000 python:
    if persistent._masAutostart_enabled:
        if not store.masAutostart_api.is_platform_supported():
            store.masAutostart_log.warn(
                "Autostart is known to be enabled, but "
                "current platform is either unsupported or its support was deprecated. "
                "Not changing enabled status, optimistically hoping this is temporare."
            )

        elif not store.masAutostart_api.is_enabled():
            store.masAutostart_log.warn("Autostart is known to be enabled, but in fact it is not. Enabling it again.")

            store.masAutostart_api.disable()
            store.masAutostart_api.enable()