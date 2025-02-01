import pytest
from mbcore import log
from mbcore.log import debug, info, warning, error, fatal
import logging
import sys

@pytest.fixture(autouse=True)
def capture_logs(caplog):
    """Ensure all logs are captured at DEBUG level"""
    caplog.set_level(logging.DEBUG, logger="rich")
    return caplog

def test_log_levels():
    # Test different log levels
    assert log.Log["DEBUG"].level == "DEBUG"
    assert log.Log["INFO"].level == "INFO"
    assert log.Log["WARNING"].level == "WARNING"
    assert log.Log["ERROR"].level == "ERROR"
    assert log.Log["FATAL"].level == "FATAL"

def test_log_bool_check():
    """Test boolean checks for log levels"""
    debug.set()

    assert bool(log.Log["DEBUG"])
    assert bool(log.Log["INFO"]())
    
    info.set()
    assert not bool(log.Log["DEBUG"]())
    assert bool(log.Log["INFO"]())

def test_log_set():
    # Test setting log level
    log.Log["DEBUG"].set()
    assert logging.getLogger("rich").getEffectiveLevel() == logging.DEBUG
    
    log.Log["INFO"].set()
    assert logging.getLogger("rich").getEffectiveLevel() == logging.INFO

def test_log_call(caplog):
    """Test logging messages"""
    debug.set()
    logger = log.Log["DEBUG"]
    import io
    from contextlib import redirect_stdout
    out = io.TextIOWrapper(io.BytesIO(), encoding="utf-8")
    with redirect_stdout(out):
        logger("Debug message")
        logger("Info message")
    out = out.buffer.getvalue().decode("utf-8")
    logger = log.Log["INFO"]
    logger("Info message")
    assert "Debug message" in out
    assert "Info message" in out
    
def test_convenience_functions():
    """Test convenience logging functions"""
    import contextlib
    from io import StringIO
    out = StringIO()
    error.set()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
        debug("Debug message")
        info("Info message")
        warning("Warning message")
        error("Error message")
        fatal("Fatal message")
    from mbcore.display import safe_str
    from rich.ansi import AnsiDecoder,re_ansi
    from rich.text import Text
    out = "".join(str(Text.from_ansi(o,end="")) for o in out.getvalue().splitlines())
    assert "Error message" in out
    assert "Fatal message" in out

    warning.set()
    out = StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
        debug("Debug message")
        info("Info message")
        warning("Warning message")
        error("Error message")
        fatal("Fatal message")
    out = "".join(str(Text.from_ansi(o,end="")) for o in out.getvalue().splitlines())
    assert "Warning message" in out
    assert "Error message" in out
    assert "Fatal message" in out

    debug.set()
    out = StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
        debug("Debug message")
        info("Info message")
        warning("Warning message")
        error("Error message")
        fatal("Fatal message")
    out = "".join(str(Text.from_ansi(o,end="")) for o in out.getvalue().splitlines())
    assert "Debug message" in out
    assert "Info message" in out
    assert "Warning message" in out
    assert "Error message" in out
    assert "Fatal message" in out




def test_verbose_flags():
    # Test verbose flag detection
    sys.argv = []
    assert not log.isverbose()
    
    sys.argv = ["-v"]
    assert log.isverbose() == True
    
    sys.argv = ["--verbose"] 
    assert log.isverbose() == True

if __name__ == "__main__":
    pytest.main(["-v", __file__])