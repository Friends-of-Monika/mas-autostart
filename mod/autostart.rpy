# NOTE: Using _masAutostart and not _mas_autostart to prevent collision
# with _mas_ prefixes used by MAS itself.

# Boolean flag indicating current autostart status.
# True if autostart was successfully enabled in the past.
define persistent._masAutostart_enabled = False

# Tuple of three items, carrying information about previous successful
# install of autostart necessities:
#   0: platform name ("windows", "linux" or "macos")
#   1: path to autostart file (shortcut, .desktop or .plist)
#   2: path to launcher script/executable (DDLC, DDLC.exe or DDLC.sh)
# Set to None when autostart is disabled. Used for cleanup of autostart
# leftovers on disable.
define persistent._masAutostart_metadata = None


init python in masAutostart_log:

    # Logging

    from store.mas_submod_utils import submod_log as log

    _LOG_PREFIX = "[MAS Autostart Mod] "

    def info(message):
        """
        Log message with info level prefixed with MAS Autostart Mod prefix.

        IN:
            message - message to write to log.
        """

        log.info(_LOG_PREFIX + message)

    def warn(message):
        """
        Log message with warning level prefixed with MAS Autostart Mod prefix.

        IN:
            message - message to write to log.
        """

        log.warning(_LOG_PREFIX + message)

    def error(message):
        """
        Log message with error level prefixed with MAS Autostart Mod prefix.

        IN:
            message - message to write to log.
        """

        log.error(_LOG_PREFIX + message)


init python in masAutostart_api:

    # Initialization

    import os
    import errno

    import store.masAutostart_log as log
    from store import persistent as persistent

    _PLATFORM_WINDOWS = "windows"
    _PLATFORM_LINUX = "linux"
    _PLATFORM_MACOS = "macos"

    if renpy.windows:
        import subprocess

        # Startup location on Windows is standard and is documented.
        # (See FOLDERID_Startup.)
        # https://docs.microsoft.com/en-us/windows/win32/shell/knownfolderid
        #
        # It is located at %APPDATA%\Microsoft\Windows\Start menu\Programs\Startup;
        # Links and executables located there will be run on startup (it is not
        # clear if they run prior to user login or not.)
        #
        # We're using simple VBScript file (see mod/platform/shortcut.vbs)
        # in order to create shortcut without involving additional dependencies
        # (see its invocation at _enable_windows.)
        #
        # As much as we know so far, VBScript engine is added to all Windows
        # desktop distributions starting from Windows 98.
        #
        # Successful tests conducted on Windows 10 21H2.

        _LAUNCHER_PATH = os.path.join(renpy.config.renpy_base, "DDLC.exe")
        _AUTOSTART_DIR = os.path.expandvars("%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup")
        _DEFAULT_AUTOSTART_FILE = os.path.join(_AUTOSTART_DIR, "Monika After Story.lnk")
        _AUTOSTART_SHORTCUT_SCRIPT = os.path.join(renpy.config.gamedir, "Submods\\MAS Autostart Mod\\platform\\shortcut.vbs")

        _PLATFORM_CURRENT = _PLATFORM_WINDOWS

    elif renpy.linux:

        # Autostart location on Linux desktops is somewhat standard
        # (considering it so since most desktop environments comply with
        # Freedesktop standards) and is documented.
        # https://specifications.freedesktop.org/autostart-spec/autostart-spec-latest.html
        #
        # It is located at $XDG_CONFIG_HOME/autostart (note: $XDG_CONFIG_HOME
        # may easily be absent or not configured, by default it's ~/.config.)
        # .desktop files located there will be run as soon as user logs in and
        # starts their desktop session.
        #
        # We're using small .desktop file preset to parse it and populate with
        # necessary values, then write to corresponding location (see its
        # parsing and creation at _enable_linux.)
        #
        # Successful tests conducted on KDE Plasma 5.25, Arch Linux and
        # Ubuntu 22.04.

        _LAUNCHER_PATH = os.path.join(renpy.config.renpy_base, "DDLC.sh")
        _AUTOSTART_DIR = os.path.join(os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config")), "autostart")
        _DEFAULT_AUTOSTART_FILE = os.path.join(_AUTOSTART_DIR, "Monika After Story.desktop")
        _AUTOSTART_FILE_TEMPLATE = os.path.join(renpy.config.gamedir, "Submods/MAS Autostart Mod/platform/Monika After Story.desktop")

        _PLATFORM_CURRENT = _PLATFORM_LINUX

    elif renpy.macintosh:
        from xml.etree import ElementTree as xml

        # Autostart support for MacOS is implemented using s.c. 'LaunchAgent'
        # system which has documentation as well.
        # https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html
        #
        # LaunchAgent .plist files are located at ~/Library/LaunchAgents (note:
        # this directory may be missing but its absence does not indicate that
        # LaunchAgents are not supported/enabled on the system; it just needs
        # to be created.)
        # .plist files located there will be parsed and their ProgramArguments
        # will be executed as soon as user logs in.
        #
        # It is not clear what versions support this mechanism;
        # Successful tests conducted on MacOS Catalina 10.15.7.

        _LAUNCHER_PATH = os.path.join(renpy.config.renpy_base, "../../MacOS/DDLC")
        _AUTOSTART_DIR = os.path.expanduser("~/Library/LaunchAgents")
        _DEFAULT_AUTOSTART_FILE = os.path.join(_AUTOSTART_DIR, "monika.after.story.plist")
        _AUTOSTART_PLIST_TEMPLATE = os.path.join(renpy.config.gamedir, "Submods/MAS Autostart Mod/platform/monika.after.story.plist")

        _PLATFORM_CURRENT = _PLATFORM_MACOS

    else:
        log.warn(
            "Unsupported platform (not Windows, Linux or MacOS) - "
            "autostart will not be working."
        )

        _PLATFORM_CURRENT = None


    # Helpers

    def is_platform_supported():
        """
        Performs a check if platform game is currently running on is supported.

        OUT:
            True if Windows, Linux or MacOS, False otherwise.
        """

        return renpy.windows or renpy.linux or renpy.macintosh


    # Enable check functions

    def is_enabled():
        """
        Tells if autostart is currently enabled.

        OUT:
            True if autostart is enabled, False otherwise.
        """

        return persistent._masAutostart_enabled

    def _was_enabled():
        """
        Tells if autostart was enabled by player before (but it might not
        necessarily be enabled right now due to another platform, unsupported
        or deprecated platform or because autostart file is absent currently.)

        OUT:
            True if autostart was enabled, False otherwise.
        """

        return persistent._masAutostart_metadata is not None

    # Enable functions

    def enable():
        """
        Enables autostart by calling platform-specific function.

        OUT:
            True if autostart was enabled successfully, False otherwise.
            Also returns False if platform is unsupported.
        """

        if renpy.windows:
            return _enable_windows()

        elif renpy.linux:
            return _enable_linux()

        elif renpy.macintosh:
            return _enable_macos()

        else:
            return False

    def _enable_windows():
        """
        Enables autostart (Windows-specific approach.)

        OUT:
            True if autostart was enabled successfully, False otherwise.

        NOTE:
            All errors are written to log and no exceptions are raised.
        """

        # Invoke shortcut.vbs script with necessary parameters.
        # See platform/shortcut.vbs for documentation.
        exit_code = subprocess.call((
            "cscript",  # VBScript interpreter command
            _AUTOSTART_SHORTCUT_SCRIPT,  # shortcut.vbs path
            _DEFAULT_AUTOSTART_FILE,  # Path to autostart shortcut
            _LAUNCHER_PATH,  # Path to launcher executable
            os.path.dirname(_LAUNCHER_PATH)  # Working dir (DDLC folder)
        ))

        # If exited with non-zero, that shows script is either wasn't
        # interpreted at all, or wasn't able to create a shortcut.
        if exit_code != 0:
            log.error("Got non-zero exit code from shortcut script invocation ({0}.)".format(exit_code))
            return False

        # Write meta variables.
        persistent._masAutostart_enabled = True
        persistent._masAutostart_metadata = (_PLATFORM_WINDOWS, _DEFAULT_AUTOSTART_FILE, _LAUNCHER_PATH)
        return True


    def _enable_linux():
        """
        Enables autostart (Linux-specific approach.)

        OUT:
            True if autostart was enabled successfully, False otherwise.

        NOTE:
            All errors are written to log and no exceptions are raised.
        """

        # Parse template .desktop autostart file and populate Exec parameter
        # with launcher script path.
        try:
            desktop_file = _map_file(_AUTOSTART_FILE_TEMPLATE, "r", _parse_desktop_file)
            desktop_file["Desktop Entry"]["Exec"] = _LAUNCHER_PATH

        except OSError as e:
            log.error("Could not parse template desktop file {0} ({1}.)".format(_AUTOSTART_FILE_TEMPLATE, e))
            return False

        # Write actual autostart .desktop file to its respective location.
        try:
            # Create autostart location if it doesn't exist.
            try:
                os.makedirs(os.path.dirname(_DEFAULT_AUTOSTART_FILE))

            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

            # Serialize and write .desktop file; toggle status variable.
            _map_file(_DEFAULT_AUTOSTART_FILE, "w", _serialize_desktop_file, [desktop_file])

        except OSError as e:
            log.error("Could not write desktop file {0} ({1}.)".format(_DEFAULT_AUTOSTART_FILE, e))
            return False

        # Write meta variables.
        persistent._masAutostart_enabled = True
        persistent._masAutostart_metadata = (_PLATFORM_LINUX, _DEFAULT_AUTOSTART_FILE, _LAUNCHER_PATH)
        return True

    def _enable_macos():
        """
        Enables autostart (MacOS-specific approach.)

        OUT:
            True if autostart was enabled successfully, False otherwise.

        NOTE:
            All errors are written to log and no exceptions are raised.
        """

        # Parse template .plist LaunchAgent file and populate ProgramArguments
        # parameter with launcher executable path.
        try:
            plist_file = _map_file(_AUTOSTART_PLIST_TEMPLATE, "r", xml.parse)
            plist_file.find(".//array/string").text = _LAUNCHER_PATH

        except OSError as e:
            log.error("Could not parse template plist file {0} ({1}.)".format(_AUTOSTART_PLIST_TEMPLATE, e))
            return False

        # Helper function for use with _map_file that reads header (with XML
        # tag and schema) because ETree doesn't handle it.
        def dump(fp):
            fp.write(_map_file(_DEFAULT_AUTOSTART_FILE, "r", lambda fp: "".join(fp.readlines()[:2])))
            plist_file.write(fp)

        # Write actual autostart .plist LaunchAgent file to its
        # respective location.
        try:
            # Create autostart location if it doesn't exist.
            try:
                os.makedirs(os.path.dirname(_DEFAULT_AUTOSTART_FILE))

            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

            # Serialize and write .plist file.
            _map_file(_DEFAULT_AUTOSTART_FILE, "w", dump)

        except OSError as e:
            log.error("Could not write LaunchAgent file {0} ({1}.)".format(persistent._masAutostart_metadata[1], e))
            return False

        # Write meta variables.
        persistent._masAutostart_enabled = True
        persistent._masAutostart_metadata = (_PLATFORM_MACOS, _DEFAULT_AUTOSTART_FILE, _LAUNCHER_PATH)
        return True


    # Disable functions

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

        # Remove autostart file and ignore if it doesn't exist.
        try:
            os.remove(persistent._masAutostart_metadata[1])

        except OSError as e:
            # Ignore ENOENT (does not exist) error code.
            if e.errno != errno.ENOENT:
                log.error("Could not delete " + persistent._masAutostart_metadata[1] + ".")

        persistent._masAutostart_enabled = False

        # If there is metadata saved, remove all the leftovers and wipe variable.
        if persistent._masAutostart_metadata is not None:
            try:
                os.remove(persistent._masAutostart_metadata[1])

            except OSError as e:
                # Silence ENOENT (does not exist) error.
                if e.errno != errno.ENOENT:
                    log.error("Could not delete " + persistent._masAutostart_metadata[1] + ".")
                    return

            # Wipe metadata variable.
            persistent._masAutostart_metadata = None


    ## Existing autostart file detection

    def _find_autostart_files():
        """
        Scans autostart directory for current platform and returns list of
        paths that are valid autostart files for MAS.

        NOTE:
            Calling this function on an unsupported platform will lead to
            undefined behaviour. All errors are written to log and no exceptions
            are raised.

        OUT:
            List of paths of valid autostart files.
        """

        # Walk through autostart directory and check for suitable files.
        autostart_files = list()
        for cd, _, files in os.walk(_AUTOSTART_DIR):
            for _file in files:
                # Convert to absolute path and check.
                _file = os.path.join(cd, _file)
                if _check_shortcut(_file):
                    autostart_files.append(_file)

        return autostart_files

    def _update_metadata():
        """
        Scans autostart directory and updates metadata if autostart files exist.

        NOTE:
            Calling this function on an unsupported platform will lead to
            undefined behaviour.
        """

        files = _find_autostart_files()

        if len(files) > 0:
            persistent._masAutostart_metadata = (_PLATFORM_CURRENT, files[0], _LAUNCHER_PATH)
            persistent._masAutostart_enabled = True

        else:
            # Do not remove metadata in order for _was_enabled() to work.
            persistent._masAutostart_enabled = False


    # Utility methods

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

        # Root object containing root parameters and groups.
        obj = dict()

        # Current group and parameters.
        _group = None
        param = dict()

        # Build group object and push it to root object.
        def push_group():
            # If current group is not set, write to root object.
            if _group is None:
                obj.update(param)

            # Store parameters to group in root object.
            else:
                obj[_group] = param

            # Reset state.
            _parse_desktop_file._group = None
            _parse_desktop_file.param = dict()

        while True:
            # Parse file line by line.
            line = fp.readline()
            if not line:
                # Hit EOF, build and push a group and return
                # desktop file object.
                push_group()
                return obj

            # Ignore empty lines and comments
            line = line.strip()
            if not line or line[0] == "#":
                continue

            # Recognize group header enclosed in [].
            if line[0] == "[" and line[-1] == "]":
                push_group()
                _group = line[1:-1]

            # Anything that isn't a comment or a group header
            # is a key=value pair; add it to current group.
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

        # Scan keys and values in desktop file object.
        for _key, _value in desktop_file.items():
            # If value is a dictionary, it's a group.
            if type(_value) is dict:
                # Write header and output key=value pairs on next lines.
                fp.write("[{0}]\n".format(_key))
                for _param, _param_value in _value.items():
                    fp.write("{0}={1}\n".format(_param, _param_value))

                # Add empty line after group.
                fp.write("\n")

            # Else it is a root-stored parameter.
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


    ## Platform-dependent utility functions

    if renpy.windows:
        def _check_shortcut(path):
            if not path.lower().endswith(".lnk"):
                return False

            try:
                target_path = subprocess.check_output((
                    "cscript",  # VBScript interpreter command
                    "/nologo",  # Exclude Microsoft banner
                    _AUTOSTART_SHORTCUT_SCRIPT,  # shortcut.vbs path
                    path  # Path to autostart shortcut
                ))

                if target_path.strip() != _LAUNCHER_PATH:
                    return False

            except subprocess.CalledProcessError as e:
                log.error(
                    "Could not check shortcut " + path + "; "
                    "shortcut script returned non-zero exit code " + str(e.returncode)
                )
                return False

            return True

    elif renpy.linux:
        def _check_shortcut(path):
            if not path.lower().endswith(".desktop"):
                return False

            # Parse autostart .desktop file into dictionary.
            try:
                desktop_file = _map_file(path, "r", _parse_desktop_file)

            except IOError as e:
                log.error("Could not parse desktop file " + path + ".")
                return False

            # Check that desktop file is valid (has Desktop Entry and Exec)
            if "Desktop Entry" not in desktop_file or "Exec" not in desktop_file["Desktop Entry"]:
                log.error("Could not parse .desktop file {0} ({1}.)".format(path, e))
                return False

            # Check if Exec is pointing at launcher script.
            if desktop_file["Desktop Entry"]["Exec"] != _LAUNCHER_PATH:
                return False

            return True

    elif renpy.macintosh:
        def _check_shortcut(path):
            if not path.lower().endswith(".plist"):
                return False

            # Parse autostart .plist file into XML document.
            try:
                plist_file = _map_file(path, "r", xml.fromstring)

            except OSError as e:
                log.error("Could not parse LaunchAgent file {0} ({1}.)".format(path, e))
                return

            # Check if XML document has ProgramArguments with single string element.
            path = plist_file.find(".//array/string")
            if not path:
                return False

            # Check if .plist refers to launcher executable.
            if path != _LAUNCHER_PATH:
                return False

            return True


init 1000 python:

    ## Handle possible cases when user switches from supported platform to
    ## unsupported or when autostart was enabled before but this time is isn't
    ## for whatever reason.

    _metadata_updated = False

    if store.masAutostart_api._was_enabled():
        if store.masAutostart_api.is_platform_supported():
            # In case we previously hid disable topic, enable it
            # since we're on supported platform now and autostart is enabled.
            mas_showEVL("masAutostart_req_disable", "EVE", unlock=True)

        else:
            store.masAutostart_log.warn(
                "Autostart is known to be enabled, but "
                "current platform is either unsupported or its support was deprecated. "
                "Not changing enabled status, optimistically hoping this is temporare. "
                "Disable topic will be hidden."
            )

            mas_hideEVL("masAutostart_req_disable", "EVE", lock=True)

        store.masAutostart_api._update_metadata()
        _metadata_updated = True

        if not store.masAutostart_api.is_enabled():
            store.masAutostart_log.warn("Autostart is known to be enabled, but in fact it is not. Enabling it again.")

            store.masAutostart_api.disable()
            store.masAutostart_api.enable()

    ## Metadata population

    if not _metadata_updated:
        store.masAutostart_api._update_metadata()
    del _metadata_updated