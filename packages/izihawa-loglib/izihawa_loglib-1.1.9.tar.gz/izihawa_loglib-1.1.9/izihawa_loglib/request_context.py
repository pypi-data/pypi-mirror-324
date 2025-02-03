import logging
from typing import Any

from izihawa_loglib import error_log
from izihawa_utils.random import generate_request_id


class RequestContext:
    request_id_length: int = 12

    def __init__(
        self, **kwargs: dict[str, Any],
    ):
        self.default_fields = kwargs
        if "request_id" not in self.default_fields:
            self.default_fields["request_id"] = RequestContext.generate_request_id(
                self.request_id_length
            )

    def __getattr__(self, name: str) -> Any:
        return self.default_fields[name]

    def __setattr__(self, key: str, value: Any):
        self.default_fields[key] = value

    @staticmethod
    def generate_request_id(length):
        return generate_request_id(length)

    def add_default_fields(self, **fields: dict) -> None:
        self.default_fields.update(fields)

    def statbox(self, **kwargs: dict) -> None:
        logging.getLogger("statbox").info(msg={**self.default_fields, **kwargs})

    def user_log(self, **kwargs: dict) -> None:
        logging.getLogger("user").info(msg={**self.default_fields, **kwargs})

    def debug_log(self, **kwargs: dict) -> None:
        logging.getLogger("debug").debug(msg={**self.default_fields, **kwargs})

    def error_log(self, e, level=logging.ERROR, **fields) -> None:
        all_fields = {**self.default_fields, **fields}
        error_log(e, level=level, **all_fields)
