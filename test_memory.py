from system.memory_manager import (
    remember_command,
    get_history
)


remember_command(
    "open nova"
)


remember_command(
    "open chrome"
)


print(
    get_history()
)