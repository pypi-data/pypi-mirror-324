from typing import Dict


class WPIError(Exception):
    def __init_subclass__(cls, **kwargs) -> None:
        cls.__module__ = "aiowpi.error"

    def __init__(self, error: Dict) -> None:
        self.code = error["code"]
        self.message = error["message"]
        self.field = error["field"]
        self.value = error["value"]

    def __str__(self) -> str:
        return f"WpiError:\nerror code: {self.code}\nerror message: {self.message}\nerror field: {self.field}\nerror value: {self.value}"


class WPIGetInstanceError(Exception):
    def __init_subclass__(cls, **kwargs) -> None:
        cls.__module__ = "aiowpi.error"

    def __str__(self) -> str:
        return f"Can't get that instance init it first"


class WPIInstanceInitError(Exception):
    def __init_subclass__(cls, **kwargs) -> None:
        cls.__module__ = "aiowpi.error"

    def __str__(self) -> str:
        return f"Can't init instance check your args"


async def check_wg_response(resp_json: Dict):
    if error := resp_json.get("error", False):
        raise WPIError(error)
    return True
