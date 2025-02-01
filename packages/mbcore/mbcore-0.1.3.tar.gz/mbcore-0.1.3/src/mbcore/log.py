import logging
import logging.config
import os
import sys
from pathlib import Path
from typing_extensions import TYPE_CHECKING,Any,TypeVar,Generic,Literal
from mbcore.display import SPINNER
from mbcore._typing import dynamic


def caller(depth=1, default='__main__') -> "str | ModuleType | None":
    try:
        return sys._getframemodulename(depth + 1) or default
    except AttributeError:  # For platforms without _getframemodulename()
        pass
    try:
        return sys._getframe(depth + 1).f_globals.get('__name__', default)
    except (AttributeError, ValueError):  # For platforms without _getframe()
        pass
    return None

if TYPE_CHECKING:
    from typing_extensions import TYPE_CHECKING, Any, Dict, Generic, Literal, TypeVar
    from mbcore._typing import wraps,wrapafter
    from types import ModuleType
else: 
    wraps = lambda *args, **kwargs: lambda f: f # noqa
    wrapafter = lambda *args, **kwargs: lambda f: f # noqa

LevelT = TypeVar("LevelT", bound=Literal["DEBUG", "INFO", "WARNING", "ERROR", "FATAL"])

def parentmodule() -> "ModuleType":
    return sys.modules[caller() or "__main__"]

def parentname() -> str:
    return caller()

def parentfile() -> Path:
    return Path(sys.modules[parentname()].__file__).resolve()



def isverbose() -> bool:
    import sys
    return any(arg in sys.argv for arg in ("-v", "--verbose","-d", "--debug"))

def isvverbose() -> bool:
    import sys
    return any(arg in sys.argv for arg in ("-vv", "--vverbose","-dd", "--ddebug"))


def getlevel() -> int:
    if isverbose():
        return logging.DEBUG
    if isvverbose():
        return logging.INFO
    
    return logging.getLogger("rich").getEffectiveLevel()

log = logging.log

def getlogpath() -> Path:
    if "find_mb" not in sys.modules:
        from mbcore.traverse import find_mb
    p =  (find_mb(parentfile().parent) /  parentname()).with_suffix(".log")
    return p

SHOW_TRACEBACKS = os.getenv("TRACEBACKS_SHOW") or False
SHOW_LOCALS = os.getenv("TRACEBACKS_SHOW_LOCALS") or False
# Logging configuration dictionary
def logconfig() -> "Dict[str, Any]":
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "detailed": {
                "format": "%(message)s",
                "datefmt": "[%X]",
            },
        },
        "handlers": {
            "rich": {
                "class": "mbcore._logging.RichHandler",
                "rich_tracebacks": SHOW_TRACEBACKS,
                "tracebacks_show_locals": SHOW_LOCALS,
                "show_time": True,
                "show_level": True,
                "show_path": True,
            },
            "file": {
                "class": "logging.FileHandler",
                # "formatter": "detailed",
                "filename": getlogpath(),
                "mode": "a",
            },
        },
        "loggers": {
            "rich": {  
                "handlers": ["rich", "file"],
                "level": getlevel(),
                "propagate": False,
            },
        },
        "root": {
            "handlers": ["rich", "file"],
            "level": getlevel(),
        },
    }
def setup_logging(show_stack: bool = None, show_locals: bool =None) -> None:
    if show_stack is not None:
        global SHOW_TRACEBACKS
        SHOW_TRACEBACKS = show_stack
    if show_locals is not None:
        global SHOW_LOCALS
        SHOW_LOCALS = show_locals
    logging.config.dictConfig(logconfig())

LOGGING_CONFIG = {}
if isverbose():
    LOGGING_CONFIG.update(logconfig())  
    LOGGING_CONFIG["loggers"]["rich"]["level"] = logging.DEBUG

if isvverbose():
    SHOW_LOCALS =True
    
setup_logging()

levelmap = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "FATAL": logging.FATAL,
    logging.DEBUG: "DEBUG",
    logging.INFO: "INFO",
    logging.WARNING: "WARNING",
    logging.ERROR: "ERROR",
    logging.FATAL: "FATAL",
}


class Log(Generic[LevelT]):
    """Initialize or log a message.
        
      
        Usage:
           Use `if debug()` to check if debug level is enabled.
        ```python
            from mbcore.log import debug, info, warning, error, fatal, log
  
            Examples:
                >>> debug("Processing file")  # Log a message
                >>> if debug():  # Check if debug level is enabled
                ...     print("Will only print if debug level is enabled")
                >>> debug.set()  # Set logging level to DEBUG
                >>> debug.log("Processing file")  # Log a message
                DEBUG: Processing file
        ```

    """
    @dynamic
    def level(self_or_cls) -> LevelT:
        return self_or_cls.level
    @classmethod
    def set(cls) -> "Log[LevelT]":
        """Set logging level to the specified level."""
        logging.getLogger("rich").setLevel(getattr(logging, cls.level))
        return cls
    

    @wrapafter(logging.log)
    @classmethod
    def log(cls, *args, **kwargs):
        """Log a message."""
        if args or kwargs:
            SPINNER().stop()
            logging.getLogger("rich").log(cls.level, *args, **kwargs, stack_info=SHOW_TRACEBACKS,stacklevel=3)
        return cls
    @classmethod
    def __class_getitem__(cls, level: LevelT):
        cls.level = "DEBUG" if level in ("DEBUG", logging.DEBUG) else\
        "INFO" if level in ("INFO", logging.INFO) else \
        "WARNING" if level in ("WARNING", logging.WARNING) else\
        "ERROR" if level in ("ERROR", logging.ERROR) else\
        "FATAL" if level in ("FATAL", logging.FATAL) else None
        if cls.level is None:
            raise ValueError(f"Invalid log level: {level}")
        newcls =type(cls)(cls.__name__, (cls,), {"level": cls.level})
        return newcls


    def __bool__(self=None, *args, **kwargs):
        """Check if the log level is enabled."""
        return logging.getLogger("rich").getEffectiveLevel() <= levelmap[self.level]

    def __new__(cls, *args, **kwargs):
        cls = super().__new__(cls)
        if cls.level is None:
            return cls
        return cls.__call__(*args, **kwargs)

    if TYPE_CHECKING:
        def __call__(self, *messages: object, level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "FATAL"] | None = None) -> "Log[LevelT]":
            return self.log(*messages, level)
    else:

        def __call__(
            cls=None, 
            *messages: object,
            level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "FATAL"] | None = None
        ) -> "Log[LevelT]":
                """Initialize or log a message.

                Usage:
                    Use `if debug()` to check if debug level is enabled.
                ```python
                    from mbcore.log import debug, info, warning, error, fatal, log
            
                    Examples:
                        >>> debug("Processing file")  # Log a message
                        >>> if debug():  # Check if debug level is enabled
                        ...     print("Will only print if debug level is enabled")
                        >>> debug.set()  # Set logging level to DEBUG
                        >>> debug.log("Processing file")  # Log a message
                        DEBUG: Processing file
                ```
                """
                # print(f"{cls=}, {first=}, {messages=}, {level=}")
                if cls.level is None:
                    return cls.__new__(cls)
                level_str = level or cls.level
                level_num = getattr(logging, level_str)
                if messages:
                    messages = list(messages)
                    SPINNER().stop()

                    logger = logging.getLogger("rich")
                    if isinstance(messages[0], str) and not "%" in messages[0] and len(messages) > 1:
                        messages[0] = messages[0] + (" %s" * (len(messages) - 1))
                    logger.log(level_num, *messages, stack_info=SHOW_TRACEBACKS,stacklevel=3)
                
      
                return cls

    
DEBUG:Literal["DEBUG"] = "DEBUG"
INFO:Literal["INFO"] = "INFO"
WARNING:Literal["WARNING"] = "WARNING"
ERROR:Literal["ERROR"] = "ERROR"
FATAL:Literal["FATAL"] = "FATAL"


debug = Log[DEBUG]()
info = Log[INFO]()
warning = Log[WARNING]()
error = Log[ERROR]()
fatal = Log[FATAL]()
log = Log[getlevel()]()

if __name__ == "__main__":
    debug.set()
    debug("Debug message")
    info("Info message")
    warning("Warning message")
    error("Error message")
    warning.set()
    debug("Debug message")
    info("Info message")
    warning("Warning message")

