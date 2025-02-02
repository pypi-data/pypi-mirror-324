import asyncio
import json
import os
from orca_driver_interface.driver_interfaces import ILabwarePlaceableDriver
import subprocess
from typing import Any, Dict, Optional

hsl_run_exe_path = r"C:\Program Files (x86)\HAMILTON\Bin\HxRun.exe"

class VenusProtocolDriver(ILabwarePlaceableDriver):


    def __init__(self, name: str):
        self._name = name
        self._exe_path: Optional[str] = None
        self._methods_folder = r"C:\Program Files (x86)\HAMILTON\Methods"
        self._is_initialized = False
        self._is_running = False
        self._params_filepath = os.path.join(os.environ["TEMP"], "CheshireLabs\\Orca\\actionConfig.json")
        self._init_protocol: Optional[str]  = None
        self._picked_protocol: Optional[str]  = None
        self._placed_protocol: Optional[str]  = None
        self._prepare_pick_protocol: Optional[str]  = None
        self._prepare_place_protocol: Optional[str]  = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_connected(self) -> bool:
        return self._is_connected

    @property
    def is_initialized(self) -> bool:
        return self._is_initialized

    async def connect(self) -> None:
        self._is_connected = True

    async def disconnect(self) -> None:
        self._is_connected = False

    def set_init_options(self, init_options: Dict[str, Any]) -> None:
        self._init_options = init_options
        if "init-protocol" in self._init_options.keys():
            self._init_protocol = self._init_options["init-protocol"]
        if "hxrun-path" in self._init_options.keys():
            self._exe_path = self._init_options["hxrun-path"]
        if "picked-protocol" in self._init_options.keys():
            self._picked_protocol = self._init_options["picked-protocol"]
        if "placed-protocol" in self._init_options.keys():
            self._placed_protocol = self._init_options["placed-protocol"]
        if "prepare-pick-protocol" in self._init_options.keys():
            self._prepare_pick_protocol = self._init_options["prepare-pick-protocol"]
        if "prepare-place-protocol" in self._init_options.keys():
            self._prepare_place_protocol = self._init_options["prepare-place-protocol"]

    async def initialize(self) -> None:
        if self._init_protocol is not None:
            await self.execute("run", {"method": self._init_protocol})
        
        # create the temporary folder for the parameters file
        os.makedirs(os.path.dirname(self._params_filepath), exist_ok=True)

        if self._exe_path is None:
            if os.path.exists(hsl_run_exe_path):
                self._exe_path = hsl_run_exe_path
            else:
                raise FileNotFoundError("The executable path for the Venus driver was not provided and could not be found in the default locations")
            
        self._is_initialized = True

    @property
    def is_running(self) -> bool:
        return self._is_running

    async def prepare_for_place(self, labware_name: str, labware_type: str, barcode: Optional[str] = None, alias: Optional[str] = None) -> None:
        if self._prepare_place_protocol is not None:
            await self.execute("run", {"method": self._prepare_place_protocol})

    async def prepare_for_pick(self, labware_name: str, labware_type: str, barcode: Optional[str] = None, alias: Optional[str] = None) -> None:
        if self._prepare_pick_protocol is not None:
            await self.execute("run", {"method": self._prepare_pick_protocol})

    async def notify_picked(self, labware_name: str, labware_type: str, barcode: Optional[str] = None, alias: Optional[str] = None) -> None:
        if self._picked_protocol is not None:
            await self.execute("run", {"method": self._picked_protocol})

    async def notify_placed(self, labware_name: str, labware_type: str, barcode: Optional[str] = None, alias: Optional[str] = None) -> None:
        if self._placed_protocol is not None:
            await self.execute("run", {"method": self._placed_protocol})

    async def execute(self, command: str, options: Dict[str, Any]) -> None:
        if command == "run":
            self._write_options_to_json_file(options)
            if 'method' not in options.keys():
                raise KeyError("The venus method was not provided in the command options.  'method' must be included with command")
            method = options["method"]
            if not os.path.exists(method):
                method = os.path.join(self._methods_folder, method)
            if not os.path.exists(method):
                raise FileNotFoundError(f"The method '{method}' does not exist")
            self._execute_protocol(method)
        else:
            raise NotImplementedError(f"The action '{command}' is unknown for {self._name} of type {type(self).__name__}")

    def _execute_protocol(self, hsl_path: str) -> None:
        self._is_running = True
        try:
            if self._exe_path is None:
                raise FileNotFoundError("The executable path for the Venus driver was not provided")
            subprocess.run([self._exe_path, "-t", hsl_path], shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
        finally:
            self._is_running = False

    def _write_options_to_json_file(self, options: Dict[str, Any]) -> None:
        json.dump(options, open(self._params_filepath, "w"))

if __name__ == "__main__":
    async def main():
        driver = VenusProtocolDriver("Venus")
        await driver.initialize()
        await driver.prepare_for_place("test", "test")
        await driver.notify_placed("test", "test")
        await driver.execute("run", {
            "method": "Cheshire Labs\\VariableAccessTesting.hsl",
            "params": {
                "strParam": "strParam value transmitted",
                "intParam": 123,
                "fltParam": 1.003
                }
            })
        await driver.prepare_for_pick("test", "test")
        await driver.notify_picked("test", "test")

    asyncio.run(main())
