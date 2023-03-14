
import commands

syntax = {
    # Stack manipulation
    '\\': commands.Swap(),
    'd': commands.Drop(),
    '.': commands.Dup(),
    '[': commands.Mark(),
    ']': commands.Array(),
    'p': commands.PrintLast(),
    'f': commands.PrintStack(),
    # Task manipulation
    '+': commands.Create(),
    '/': commands.Find(),
    'subtask': commands.SubtaskOf(),
    'follows': commands.Follows(),

    # Quit
    'q': commands.Quit()
}


