# Using _masAutostart and not _mas_autostart to prevent collision
# with _mas_ prefixes used by MAS itself.
define persistent._masAutostart_enabled = False


init in masAutostart_log:

    ## Logging ##

    _LOG_PREFIX = "[MAS Autostart] "

    def warn(message):
        store.mas_submod_utils.submod_log.warning(_LOG_PREFIX + message)

    def error(message):
        store.mas_submod_utils.submod_log.error(_LOG_PREFIX + message)


init in masAutostart_api:

    ## Initialization ##

    import os
    import store.masAutostart_log as log

    if renpy.windows:
        import _winreg

        _LAUNCHER_PATH = os.path.join(renpy.config.renpy_base, "DDLC.exe")
        _AUTORUN_KEY = "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"
        _AUTORUN_VALUE_NAME = "Monika After Story"

    elif renpy.linux:
        _LAUNCHER_PATH = os.path.join(renpy.config.renpy_base, "DDLC.sh")
        _XDG_CONFIG_HOME = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
        _AUTOSTART_DESKTOP_FILE = os.path.join(_XDG_CONFIG_HOME, "autostart", "Monika After Story.desktop")

    else:
        log.warn("Unsupported platform (not Windows or Linux.)")


    ## Conditional helper

    def is_platform_supported():
        return renpy.windows || renpy.linux


    ## Install checks ##

    def is_installed():
        if renpy.windows:
            return _is_installed_windows()

        elif renpy.linux:
            return _is_installed_linux()

        else:
            return False

    def _is_installed_windows():
        try:
            reg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
        except WindowsError as e:
            log.error("Could not open registry.")
            return False

        try:
            try:
                reg_key = _winreg.OpenKey(reg, _AUTORUN_KEY)

            except WindowsError as e:
                log.error("Could not open registry key " + _AUTORUN_KEY + ".")
                return False

            try:
                _value, _type = _winreg.QueryValueEx(reg_key, _AUTORUN_VALUE_NAME)

                if _type != _winreg.REG_SZ:
                    log.error("Registry key " + os.path.join(_AUTORUN_KEY, _AUTORUN_VALUE_NAME) + " exists, but has invalid type.")
                    return False

                if _value != _LAUNCHER_PATH:
                    log.error("Registry key " + os.path.join(_AUTORUN_KEY, _AUTORUN_VALUE_NAME) + " exists, but points to wrong location.")
                    return False

                return True

            except WindowsError as e:
                log.error("Could not query registry key " + os.path.join(_AUTORUN_KEY, _AUTORUN_VALUE_NAME) + ".")
                return False

            finally:
                _winreg.CloseKey(reg_key)

        finally:
            _winreg.CloseKey(reg)

    def _is_installed_linux():
        desktop_file = os.path.join(_AUTOSTART_DESKTOP_FILE)

        if not os.path.exists(desktop_file):
            return False

        try:
            fp = open(desktop_file, "r")

        except IOError as e:
            log.error("Could not open " + desktop_file + " for reading.")
            return False

        try:
            _desktop_file = _parse_desktop_file(fp)

            if "Desktop Entry" not in _desktop_file or "Exec" not in _desktop_file["Desktop Entry"]:
                log.error("File " + desktop_file + " exists, but is not a valid desktop file.")
                return False

            if _desktop_file["Desktop Entry"]["Exec"] != _LAUNCHER_PATH:
                log.error("File " + desktop_file + " exists, but points to wrong location.")
                return False

            return True

        except IOError as e:
            log.error("Could not read " + desktop_file + ".")
            return False

        finally:
            fp.close()


    ## Install methods ##

    def install():
        if renpy.windows:
            _install_windows()

        elif renpy.linux:
            _install_linux()

    def _install_windows():
        try:
            reg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
        except WindowsError as e:
            log.error("Could not open registry.")

        try:
            try:
                reg_key = _winreg.OpenKey(reg, _AUTORUN_KEY)

            except WindowsError as e:
                log.error("Could not open registry key " + _AUTORUN_KEY + ".")
                return

            try:
                _winreg.SetValueEx(reg_key, _AUTORUN_VALUE_NAME, 0, _winreg.REG_SZ, _LAUNCHER_PATH)

            except WindowsError as e:
                log.error("Could not save value to registry key " + os.path.join(_AUTORUN_KEY, _AUTORUN_VALUE_NAME) + ".")

            finally:
                _winreg.CloseKey(reg_key)

        finally:
            _winreg.CloseKey(reg)


    def _install_linux():
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
            log.error("Could not open " + desktop_file + " for writing.")
            return False

        try:
            _serialize_desktop_file(fp, desktop_file)

        except IOError as e:
            log.error("Could not write to " + desktop_file + ".")

        finally:
            fp.close()



    ## Utility methods

    def _parse_desktop_file(fp):
        obj = dict()

        _group = ""
        param = dict()

        def push_group():
            nonlocal _group, param

            obj[_group] = param
            _group = ""
            param = dict()

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