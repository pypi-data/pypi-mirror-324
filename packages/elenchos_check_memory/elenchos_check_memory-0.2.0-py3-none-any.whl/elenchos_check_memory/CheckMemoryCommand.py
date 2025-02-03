from elenchos.command.CheckCommand import CheckCommand

from elenchos_check_memory.MemoryPlugin import MemoryPlugin


class CheckMemoryCommand(CheckCommand):
    """
    A Élenchos command for checking total, available, used, and free memory.
    """
    name = 'check:memory'
    description = 'Test total, available, used, and free memory'

    # ------------------------------------------------------------------------------------------------------------------
    def _handle(self) -> int:
        """
        Executes this command.
        """
        plugin = MemoryPlugin()

        return plugin.check().value

# ----------------------------------------------------------------------------------------------------------------------
