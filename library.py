
import commands
import commands_dot
from db import Db

tasks_db = Db()

library = {
    # Stack manipulation
    '\\': commands.Swap(),
    'd': commands.Drop(),
    '.': commands.Dup(),
    '[': commands.Mark(),
    ']': commands.Array(),
    'p': commands.PrintLast(),
    'f': commands.PrintStack(),
    # Task manipulation
    '+': commands.Create(tasks_db),
    '/': commands.Find(tasks_db),
    'subtask': commands.SubtaskOf(tasks_db),
    'follows': commands.Follows(tasks_db),

    # Process
    '!': commands.Commit(tasks_db),
    'dot': commands_dot.DotCommand(tasks_db),
    'q': commands.Quit()
}


