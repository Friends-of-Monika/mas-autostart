## Using _masAutostart and not _mas_autostart to prevent collision
## with _mas_ prefixes used by MAS itself.
define persistent._masAutostart_enabled = False
define persistent._masAutostart_metadata = None


init python in masAutostart_log:

    ## Logging

    from store.mas_submod_utils import submod_log as log

    _LOG_PREFIX = "[MAS Autostart] "

    def info(message):
        log.info(_LOG_PREFIX + message)

    def warn(message):
        log.warning(_LOG_PREFIX + message)

    def error(message):
        log.error(_LOG_PREFIX + message)


init python in masAutostart_api:

    ## Initialization

    import os
    import errno

    import store.masAutostart_log as log
    from store import persistent as persistent

    if renpy.windows:
        import subprocess

        ## Startup location on Windows is standard and is documented.
        ## (See FOLDERID_Startup.)
        ## https://docs.microsoft.com/en-us/windows/win32/shell/knownfolderid
        ##
        ## It is located at %APPDAT%A\Microsoft\Windows\Start menu\Programs\Startup;
        ## Links and executables located there will be run on startup (it is not
        ## clear if they run prior to user login or not.)
        ##
        ## We're using simple VBScript file (see mod/platform/shortcut.vbs)
        ## in order to create shortcut without involving additional dependencies
        ## (see its invocation at _enable_windows.)
        ##
        ## As much as we know so far, VBScript engine is added to all Windows
        ## desktop distributions starting from Windows 98.
        ##
        ## Successful tests conducted on Windows 10 21H2.

        _LAUNCHER_PATH = os.path.join(renpy.config.renpy_base, "DDLC.exe")
        _AUTOSTART_FILE = os.path.expandvars("%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\Monika After Story.lnk")
        _AUTOSTART_SHORTCUT_SCRIPT = os.path.join(renpy.config.gamedir, "Submods\\MAS Autostart Mod\\platform\\shortcut.vbs")

    elif renpy.linux:

        ## Autostart location on Linux desktops is somewhat standard
        ## (considering it so since most desktop environments comply with
        ## Freedesktop standards) and is documented.
        ## https://specifications.freedesktop.org/autostart-spec/autostart-spec-latest.html
        ##
        ## It is located at $XDG_CONFIG_HOME/autostart (note: $XDG_CONFIG_HOME
        ## may easily be absent or not configured, by default it's ~/.config.)
        ## .desktop files located there will be run as soon as user logs in and
        ## starts their desktop session.
        ##
        ## We're using small .desktop file preset to parse it and populate with
        ## necessary values, then write to corresponding location (see its
        ## parsing and creation at _enable_linux.)
        ##
        ## Successful tests conducted on KDE Plasma 5.25, Arch Linux and
        ## Ubuntu 22.04.

        _LAUNCHER_PATH = os.path.join(renpy.config.renpy_base, "DDLC.sh")
        _AUTOSTART_FILE = os.path.join(os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config/autostart/Monika After Story.desktop")))
        _AUTOSTART_FILE_TEMPLATE = os.path.join(renpy.config.gamedir, "Submods/MAS Autostart Mod/platform/Monika After Story.desktop")

    elif renpy.macintosh:
        from xml.etree import ElementTree as xml

        ## Autostart support for MacOS is implemented using s.c. 'LaunchAgent'
        ## system which has documentation as well.
        ## https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html
        ##
        ## LaunchAgent .plist files are located at ~/Library/LaunchAgents (note:
        ## this directory may be missing but its absence does not indicate that
        ## LaunchAgents are not supported/enabled on the system; it just needs
        ## to be created.)
        ## .plist files located there will be parsed and their ProgramArguments
        ## will be executed as soon as user logs in.
        ##
        ## It is not clear what versions support this mechanism;
        ## Successful tests conducted on MacOS Catalina 10.15.7.

        _LAUNCHER_PATH = os.path.join(renpy.config.renpy_base, "../../MacOS/DDLC")
        _AUTOSTART_FILE = os.path.expanduser("~/Library/LaunchAgents/monika.after.story.plist")
        _AUTOSTART_PLIST_TEMPLATE = os.path.join(renpy.config.gamedir, "Submods/MAS Autostart Mod/platform/monika.after.story.plist")

    else:
        log.warn(
            "Unsupported platform (not Windows, Linux or MacOS) - "
            "autostart will not be working."
        )


    ## Helpers

    def is_platform_supported():
        """
        Performs a check if platform game is currently running on is supported.

        OUT:
            True if Windows, Linux or MacOS, False otherwise.
        """

        return renpy.windows or renpy.linux or renpy.macintosh


    ## Enable check functions

    def is_enabled():
        """
        Performs a check if autostart is currently **in fact** enabled by
        calling corresponding platform-specific check function.

        OUT:
            True if autostart is enabled, False otherwise.
        """

        if renpy.windows:
            return _is_enabled_windows()

        elif renpy.linux:
            return _is_enabled_linux()

        elif renpy.macintosh:
            return _is_enabled_macos()

        else:
            return False

    def _is_enabled_windows():
        """
        Performs a check if autostart is enabled (Windows-specific approach.)
        Invoking this function while running on another platform results in
        an undefined behaviour.

        OUT:
            True if autostart is enabled, False otherwise.
        """

        if not os.path.exists(_AUTOSTART_FILE):
            return False

        return True

    def _is_enabled_linux():
        """
        Performs a check if autostart is enabled (Linux-specific approach.)
        Invoking this function while running on another platform results in
        an undefined behaviour.

        NOTE:
            Besides simple file presence check, this function also parses
            .desktop file and checks if Exec parameter equals actual launcher
            script path. In case of mismatch False will be returned.

        OUT:
            True if autostart is enabled, False otherwise.
        """

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
        """
        Performs a check if autostart is enabled (MacOS-specific approach.)
        Invoking this function while running on another platform results in
        an undefined behaviour.

        NOTE:
            Besides simple file presence check, this function also parses
            .plist file and checks if ProgramArguments value equals actual
            launcher script path. In case of mismatch False will be returned.

        OUT:
            True if autostart is enabled, False otherwise.
        """

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


    ## Enable functions

    def enable():
        """
        Enables autostart by calling platform-specific function.

        NOTE:
            No-op if platform is unsupported (if is_platform_supported call
            returned False.)
        """

        if renpy.windows:
            _enable_windows()

        elif renpy.linux:
            _enable_linux()

        elif renpy.macintosh:
            _enable_macos()

    def _enable_windows():
        """
        Enables autostart (Windows-specific approach.)

        NOTE:
            All errors are written to log and no exceptions are raised.
        """

        exit_code = subprocess.call((
            "cscript",
            _AUTOSTART_SHORTCUT_SCRIPT,
            _AUTOSTART_FILE,
            _LAUNCHER_PATH,
            os.path.dirname(_LAUNCHER_PATH)
        ))

        if exit_code != 0:
            log.error("Got non-zero exit code from shortcut script invocation ({0}.)".format(exit_code))
            return

        persistent._masAutostart_metadata = ("windows", _AUTOSTART_FILE, _LAUNCHER_PATH)


    def _enable_linux():
        """
        Enables autostart (Linux-specific approach.)

        NOTE:
            All errors are written to log and no exceptions are raised.
        """

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
                if e.errno != errno.EEXIST:
                    raise

            _map_file(_AUTOSTART_FILE, "w", _serialize_desktop_file, [desktop_file])
            persistent._masAutostart_enabled = True

        except OSError as e:
            log.error("Could not write desktop file {0} ({1}.)".format(_AUTOSTART_FILE, e))
            return

        persistent._masAutostart_metadata = ("linux", _AUTOSTART_FILE, _LAUNCHER_PATH)

    def _enable_macos():
        """
        Enables autostart (MacOS-specific approach.)

        NOTE:
            All errors are written to log and no exceptions are raised.
        """

        try:
            plist_file = _map_file(_AUTOSTART_PLIST_TEMPLATE, "r", xml.parse)
            plist_file.find(".//array/string").text = _LAUNCHER_PATH

        except OSError as e:
            log.error("Could not parse template plist file {0} ({1}.)".format(_AUTOSTART_PLIST_TEMPLATE, e))
            return

        def dump(fp):
            fp.write(_map_file(_AUTOSTART_FILE, "r", lambda fp: "".join(fp.readlines()[:2])))
            plist_file.write(fp)

        try:
            try:
                os.makedirs(os.path.dirname(_AUTOSTART_FILE))

            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

            _map_file(_AUTOSTART_FILE, "w", dump)

        except OSError as e:
            log.error("Could not write LaunchAgent file {0} ({1}.)".format(_AUTOSTART_FILE, e))
            return

        persistent._masAutostart_metadata = ("macos", _AUTOSTART_FILE, _LAUNCHER_PATH)


    ## Disable functions

    def disable():
        """
        Disables autostart.

        NOTE:
            No-op if platform is unsupported (if is_platform_supported call
            returned False.)
        """

        if renpy.windows or renpy.linux or renpy.macintosh:
            _disable_delete_desktop_file()

    def _disable_delete_desktop_file():
        """
        Disables autostart (currently, the approach is uniform to all platforms)
        by deleting autostart file.

        NOTE:
            All errors are written to log and no exceptions are raised.
        """

        try:
            os.remove(_AUTOSTART_FILE)

        except OSError as e:
            if e.errno != errno.ENOENT:
                log.error("Could not delete " + _AUTOSTART_FILE + ".")

        if persistent._masAutostart_metadata is not None:
            try:
                os.remove(persistent._masAutostart_metadata[1])

            except OSError as e:
                if e.errno != errno.ENOENT:
                    log.error("Could not delete " + _AUTOSTART_FILE + ".")
                    return

            persistent._masAutostart_metadata = None


    ## Utility methods

    def _parse_desktop_file(fp):
        """
        Parses .desktop file from file stream and returns it as dictionary of
        groups as keys (root/ungrouped keys are written directly to dictionary
        root like groups.)

        IN:
            fp - readable file stream (file opened with "open" function in "r"
            mode.)

        OUT:
            Parsed desktop file as dictionary.
        """

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
        """
        Serializes desktop file dictionary (parsed with _parse_desktop_file)
        to file stream.

        IN:
            fp - writable file stream (file opened with "open" function in "w"
            mode.)
            desktop_file - desktop file dictionary (parsed with
            _parse_desktop_file)
        """

        for _key, _value in desktop_file.items():
            if type(_value) is dict:
                fp.write("[{0}]\n".format(_group))
                for _key, _value in _value.items():
                    fp.write("{0}={1}\n".format(_key, _value))

            else:
                fp.write("{0}={1}\n".format(_key, _value))

    def _map_file(path, mode, fun, args=None):
        """
        Opens file at specific path in requsted mode and passes obtained
        descriptor as first argument to provided function (optionally, with
        additional parameters), closing the file after function returns,
        returning its return value.

        IN:
            path - path to file to open.
            mode - mode to open file in (see possible options in "open"
            function.)
            fun - function to pass file descriptor to.
            args - list of additional positional parameters to pass after file
            descriptor.

        OUT:
            Output of provided function.
        """

        if args is None:
            args = list()

        fp = open(path, mode)

        try:
            return fun(fp, *args)

        finally:
            fp.close()


init 1000 python:

    ## Handle possible cases when user switches from supported platform to
    ## unsupported or when autostart was enabled before but this time is isn't
    ## for whatever reason.

    if persistent._masAutostart_enabled:
        if store.masAutostart_api.is_platform_supported():
            ## In case we previously hid disable topic, enable it
            ## since we're on supported platform now and autostart is enabled.
            mas_showEVL("masAutostart_req_disable", "EVE", unlock=True)

        if not store.masAutostart_api.is_platform_supported():
            store.masAutostart_log.warn(
                "Autostart is known to be enabled, but "
                "current platform is either unsupported or its support was deprecated. "
                "Not changing enabled status, optimistically hoping this is temporare. "
                "Disable topic will be hidden."
            )

            mas_hideEVL("masAutostart_req_disable", "EVE", lock=True)

        elif not store.masAutostart_api.is_enabled():
            store.masAutostart_log.warn("Autostart is known to be enabled, but in fact it is not. Enabling it again.")

            store.masAutostart_api.disable()
            store.masAutostart_api.enable()