' This is Windows-specific VBScript file used for creating or checking shortcut
' in autostart folder without a need to add winshell/pywin32 dependencies.
' The script must be invoked with the following parameters:
'   For shortcut creation:
'     0: constant value of "create", a subcommand
'     1: shortcut path (must contain filename ending with .lnk)
'     2: target executable path
'     3: executable working directory
'   For shortcut path checking:
'     0: constant value of "check", a subcommand
'     1: file to write output to
'     2: path to check shortcut path of

' Adopted and reworked from https://superuser.com/a/392082.
' Huge thanks to original answer author for saving us lots of time
' we could instead waste on messing with winshell/pywin32.

Set Shell = WScript.CreateObject("WScript.Shell")

If WScript.Arguments(0) = "create" Then
    ' Create a shortcut object for parameter 1 with target path as parameter 2
    ' and working directory as parameter 3.
    Set Shortcut = Shell.CreateShortcut(WScript.Arguments(1))
    Shortcut.TargetPath = WScript.Arguments(2)
    Shortcut.WorkingDirectory = WScript.Arguments(3)
    Shortcut.Save

Else If WScript.Arguments(0) = "check" Then
    Set FileSystem = WScript.CreateObject("Scripting.FileSystemObject")
    Const MODE_WRITE = 2

    ' Open output file for parameter 1 for writing to write shortcut for
    ' parameter 2 target path to.
    Set OutputStream = FileSystem.OpenTextFile(WScript.Arguments(1), MODE_WRITE)
    Set Shortcut = Shell.CreateShortcut(WScript.Arguments(2))
    OutputStream.WriteLine(Shortcut.TargetPath)

End If