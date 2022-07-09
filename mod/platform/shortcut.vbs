' This is Windows-specific VBScript file used for creating or checking shortcut
' in autostart folder without a need to add winshell/pywin32 dependencies.
' The script must be invoked with three positional parameters:
'   0: shortcut path (must contain filename ending with .lnk)
'   1: target executable path
'   2: executable working directory
' If only one positional parameter is passed (shortcut path), its target
' is written to standard output stream.

' Adopted and reworked from https://superuser.com/a/392082.
' Huge thanks to original answer author for saving us lots of time
' we could instead waste on messing with winshell/pywin32.

Set Shell = WScript.CreateObject("WScript.Shell")
Set Shortcut = Shell.CreateShortcut(WScript.Arguments(0))

If WScript.Arguments.Length = 3 Then
    Shortcut.TargetPath = WScript.Arguments(1)
    Shortcut.WorkingDirectory = WScript.Arguments(2)
    Shortcut.Save

Else
    WScript.Echo Shortcut.TargetPath

End If