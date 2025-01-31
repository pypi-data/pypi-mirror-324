"""Error codes for jobs runner."""
from enum import Enum

from move_errors.codes.base import BaseErrorCode
from move_errors.utils.codes import (
    get_default_bad_request_error_code,
    get_default_error_code,
)


class JobsRunnerErrorCodes(BaseErrorCode, Enum):
    """Error codes for jobs_runner."""

    MV_070_060_0998 = get_default_bad_request_error_code("MV_070_060_0998")
    """Describes an error code when a pydantic error occurs."""

    MV_070_060_0001 = (
        {
            "suggestions": [
                "Please ensure you have enough credits remaining",
                "1 credit is used per second of video",
            ],
        },
        "MV_070_060_0001",
        True,
        "{0}. {1}".format(
            "You do not have enough credits to process this video",
            "Upgrade your plan now to continue.",
        ),
    )

    MV_070_060_0999 = get_default_error_code("MV_070_060_0999")
    """Describes an error code when an unknown error occurs."""
