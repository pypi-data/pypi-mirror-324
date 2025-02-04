from .log import LogFormatter


def _get_kwargs_by_verbosity(verbosity: int = 0) -> dict:
    if verbosity == 1:
        return {
            "add_name": False,
            "add_path": True,
            "before_message": "\n",
        }
    elif verbosity == 2:
        return {
            "print_traceback": True,
        }
    elif verbosity == 3:
        return {
            "print_traceback": True,
            "add_name": False,
            "add_path": True,
            "before_message": "\n",
        }
    return {}

def get_default_logging_config(verbosity: int = 0, level: str = "INFO"):
    kwargs = _get_kwargs_by_verbosity(verbosity)
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                "()": LogFormatter,
                **kwargs
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "console",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": level,
        },
    }


# Prints to a log file as well as the console
def get_dual_logging_config(log_file: str, verbosity: int = 0, level: str = "INFO"):
    kwargs = _get_kwargs_by_verbosity(verbosity)
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                "()": LogFormatter,
                **kwargs
            },
            "file": {
                "()": LogFormatter,
                **(kwargs | {"use_color": False})
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "console",
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": str(log_file),
                "formatter": "file",
            },
        },
        "root": {
            "handlers": ["console", "file"],
            "level": level,
        },
    }


# Prints to the console and two log files with different levels of verbosity
def get_triple_logging_config(
    log_file_terse: str,
    log_file_verbose: str,
    low_verbosity: int = 0,
    high_verbosity: int = 2,
    level: str = "INFO"
):
    low_kwargs = _get_kwargs_by_verbosity(low_verbosity)
    high_kwargs = _get_kwargs_by_verbosity(high_verbosity)
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                "()": LogFormatter,
                **low_kwargs
            },
            "file_terse": {
                "()": LogFormatter,
                **(low_kwargs | {"use_color": False})
            },
            "file_verbose": {
                "()": LogFormatter,
                **(high_kwargs | {"use_color": False})
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "console",
            },
            "file_terse": {
                "class": "logging.FileHandler",
                "filename": str(log_file_terse),
                "formatter": "file_terse",
            },
            "file_verbose": {
                "class": "logging.FileHandler",
                "filename": str(log_file_verbose),
                "formatter": "file_verbose",
            },
        },
        "root": {
            "handlers": ["console", "file_terse", "file_verbose"],
            "level": level,
        },
    }
