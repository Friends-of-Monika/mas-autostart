# Using _masAutostart and not _mas_autostart to prevent collision
# with _mas_ prefixes used by MAS itself.
define persistent._masAutostart_enabled = False


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
        _AUTOSTART_DESKTOP_FILE = os.path.expandvars("%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\Monika After Story.lnk")

    elif renpy.linux:
        _LAUNCHER_PATH = os.path.join(renpy.config.renpy_base, "DDLC.sh")
        _XDG_CONFIG_HOME = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
        _AUTOSTART_DESKTOP_FILE = os.path.join(_XDG_CONFIG_HOME, "autostart", "Monika After Story.desktop")

    else:
        log.warn("Unsupported platform (not Windows or Linux.)")


    ## Helpers ##

    def is_platform_supported():
        return renpy.windows or renpy.linux


    ## Enable check functions ##

    def is_enabled():
        if renpy.windows:
            return _is_enabled_windows()

        elif renpy.linux:
            return _is_enabled_linux()

        else:
            return False

    def _is_enabled_windows():
        if not os.path.exists(_AUTOSTART_DESKTOP_FILE):
            return False

        return True

    def _is_enabled_linux():
        if not os.path.exists(_AUTOSTART_DESKTOP_FILE):
            return False

        try:
            fp = open(_AUTOSTART_DESKTOP_FILE, "r")

        except IOError as e:
            log.error("Could not open " + _AUTOSTART_DESKTOP_FILE + " for reading.")
            return False

        try:
            _desktop_file = _parse_desktop_file(fp)

            if "Desktop Entry" not in _desktop_file or "Exec" not in _desktop_file["Desktop Entry"]:
                log.error("File " + _AUTOSTART_DESKTOP_FILE + " exists, but is not a valid desktop file.")
                return False

            if _desktop_file["Desktop Entry"]["Exec"] != _LAUNCHER_PATH:
                log.error("File " + _AUTOSTART_DESKTOP_FILE + " exists, but points to wrong location.")
                return False

            return True

        except IOError as e:
            log.error("Could not read " + _AUTOSTART_DESKTOP_FILE + ".")
            return False

        finally:
            fp.close()


    ## Enable functions ##

    def enable():
        if renpy.windows:
            _enable_windows()

        elif renpy.linux:
            _enable_linux()

    def _enable_windows():
        subprocess.call((
            "cscript",
            os.path.join(renpy.config.gamedir, "Submods", "MAS Autostart Mod", "shortcut.vbs"),
            _AUTOSTART_DESKTOP_FILE,
            _LAUNCHER_PATH,
            os.path.join(*_LAUNCHER_PATH.split("\\")[:-1])
        ))


    def _enable_linux():
        desktop_file = {
            "Desktop Entry": {
                "Type": "Application",
                "Name": "Monika After Story",
                "NoDisplay": "true",
                "Exec": _LAUNCHER_PATH
            }
        }

        try:
            fp = open(_AUTOSTART_DESKTOP_FILE, "w")

        except IOError as e:
            log.error("Could not open " + _AUTOSTART_DESKTOP_FILE + " for writing.")
            return False

        try:
            _serialize_desktop_file(fp, desktop_file)
            persistent._masAutostart_enabled = True

        except OSError as e:
            log.error("Could not write to " + _AUTOSTART_DESKTOP_FILE + ".")

        finally:
            fp.close()


    ## Disable functions ##

    def disable():
        if renpy.windows:
            _disable_windows()
        elif renpy.linux:
            _disable_linux()

    def _disable_windows():
        try:
            os.remove(_AUTOSTART_DESKTOP_FILE)

        except OSError as e:
            log.error("Could not delete " + _AUTOSTART_DESKTOP_FILE + ".")

        except FileNotFoundError:
            pass



    def _disable_linux():
        try:
            os.remove(_AUTOSTART_DESKTOP_FILE)

        except OSError as e:
            log.error("Could not delete " + _AUTOSTART_DESKTOP_FILE + ".")

        except FileNotFoundError:
            pass


    ## Utility methods ##

    def _parse_desktop_file(fp):
        obj = dict()

        _group = ""
        param = dict()

        def push_group():
            obj[_group] = param
            _parse_desktop_file._group = ""
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


## Startup tasks ##

init 10 python:
    if persistent._masAutostart_enabled and not store.masAutostart_api.is_enabled():
        store.masAutostart_api.disable()
        queueEvent("masAutostart_topic_reset")