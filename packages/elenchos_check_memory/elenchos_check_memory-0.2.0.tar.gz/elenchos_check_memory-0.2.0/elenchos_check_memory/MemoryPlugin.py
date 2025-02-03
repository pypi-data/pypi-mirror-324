import platform
import re
from pathlib import Path
from typing import Dict, Tuple

from elenchos.nagios.IncludeInDescription import IncludeInDescription
from elenchos.nagios.NagiosPlugin import NagiosPlugin
from elenchos.nagios.NagiosStatus import NagiosStatus
from elenchos.nagios.PerformanceData import PerformanceData


class MemoryPlugin(NagiosPlugin):
    """
    Élenchos plugin for total, available, used, and free memory.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """
        NagiosPlugin.__init__(self, 'MEMORY')

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __bytes_to_gib(n_bytes: int) -> str:
        """
        Converts bytes to GiB.

        :param n_bytes: The number of bytes to convert to GiB.
        """
        return f'{round(n_bytes / (1024 * 1024 * 1024), 1)}GiB'

    # ------------------------------------------------------------------------------------------------------------------
    def __self_check_linux(self) -> None:
        """
        Checks the memory on a Linux system.
        """
        text = Path('/proc/meminfo').read_text()
        lines = text.splitlines()
        meminfo: Dict[str, Tuple[int, str | None]] = {}
        for line in lines:
            match = re.match(r'^(?P<key>[a-zA-Z0-9_()]+):\s*(?P<value>[0-9]+)\s*(?P<unit>[a-zA-Z]+)?$', line)
            if match:
                if match['unit'] == 'kB':
                    meminfo[match['key']] = (1024 * int(match['value']), 'B')
                elif match['unit'] is None:
                    meminfo[match['key']] = (int(match['value']), None)

        meminfo['MemUsed'] = (meminfo['MemTotal'][0] - meminfo['MemAvailable'][0], 'B')

        if 'Hugepagesize' in meminfo and meminfo['Hugepagesize'][1] == 'B':
            for key in ('HugePages_Total', 'HugePages_Free', 'HugePages_Rsvd', 'HugePages_Surp'):
                if key in meminfo:
                    meminfo[key] = (meminfo[key][0] * meminfo['Hugepagesize'][0], 'B')

        self._add_performance_data(PerformanceData(name='Total Memory',
                                                   value=meminfo['MemTotal'][0],
                                                   value_in_description=self.__bytes_to_gib(meminfo['MemTotal'][0]),
                                                   min_value=0,
                                                   max_value=meminfo['MemTotal'][0],
                                                   unit='B'))
        self._add_performance_data(PerformanceData(name='Available Memory',
                                                   value=meminfo['MemAvailable'][0],
                                                   value_in_description=self.__bytes_to_gib(meminfo['MemAvailable'][0]),
                                                   min_value=0,
                                                   max_value=meminfo['MemTotal'][0],
                                                   unit='B'))
        self._add_performance_data(PerformanceData(name='Used Memory',
                                                   value=meminfo['MemUsed'][0],
                                                   value_in_description=self.__bytes_to_gib(meminfo['MemUsed'][0]),
                                                   min_value=0,
                                                   max_value=meminfo['MemTotal'][0],
                                                   unit='B'))
        self._add_performance_data(PerformanceData(name='Free Memory',
                                                   value=meminfo['MemFree'][0],
                                                   value_in_description=self.__bytes_to_gib(meminfo['MemFree'][0]),
                                                   min_value=0,
                                                   max_value=meminfo['MemTotal'][0],
                                                   unit='B'))

        for key, (value, unit) in meminfo.items():
            if key not in ('MemTotal', 'MemAvailable', 'MemUsed', 'MemFree'):
                self._add_performance_data(PerformanceData(name=key,
                                                           include_in_description=IncludeInDescription.NEVER,
                                                           value=value,
                                                           unit=unit))

    # ------------------------------------------------------------------------------------------------------------------
    def _self_check(self) -> NagiosStatus:
        """
        Checks the memory.
        """
        system = platform.system()
        if system == 'Linux':
            self.__self_check_linux()

            return NagiosStatus.OK

        self.message = f'Unknown operating system {system}'

        return NagiosStatus.UNKNOWN

# ----------------------------------------------------------------------------------------------------------------------
