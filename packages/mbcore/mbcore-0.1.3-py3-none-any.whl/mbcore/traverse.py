import logging
from pathlib import Path
from typing import TYPE_CHECKING

from mbcore.cache import cache
from mbcore.import_utils import smart_import

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Union
    PathType = Union[str, Path]

PathLike = Path
logging.basicConfig(level=logging.DEBUG,force=True)

def search_parents_for_file(
    file_name: "PathType",
    max_levels=3,
    cwd: "Path | str | None | None" = None,
) -> "Path":
    """Search parent directories for a file."""
    file_name = Path(str(file_name))
    logging.debug(f"exists ? {file_name.exists()}")
    file_name = file_name.name if file_name.is_absolute() else file_name
    logging.debug(f"Searching for {file_name} in parent directories of {cwd}")
    current_dir = PathLike(cwd) if cwd else Path.cwd()
    it = 0
    target_file = current_dir / file_name
    while it <= max_levels and not target_file.exists():
        logging.debug(f"Checking {target_file}")
        current_dir = current_dir.parent
        target_file = current_dir / file_name
        it += 1

    if target_file.exists():
        return target_file
    raise FileNotFoundError(f"File '{file_name}' not found in parent directories.")



async def asearch_parents_for_file(
    file_name: "PathType",
    max_levels=3,
    cwd: "Path| str | None" = None,
) -> "Path":
    """Search parent directories for a file."""
    if TYPE_CHECKING:
        from asyncio.threads import to_thread
    else:
        to_thread = smart_import("asyncio.threads.to_thread")
    return await to_thread(search_parents_for_file, file_name, max_levels, cwd)


async def asearch_children_for_file(
    file_name: "PathType",
    max_levels=3,
    cwd: "Path | str| None" = None,
) -> "Path":
    """Search parent directories for a file."""
    if TYPE_CHECKING:
        from asyncio.threads import to_thread
    else:
        to_thread = smart_import("asyncio.threads.to_thread")
    return await to_thread(search_children_for_file, file_name, max_levels, cwd)


def search_children_for_file(
    file_name: "PathType",
    max_levels=3,
    cwd: "PathType | None" = None,
) -> "Path":
    """Search parent directories for a file."""
    if TYPE_CHECKING:
        from typing import cast
    else:
        cast = smart_import("typing.cast")
    file_name = Path(str(file_name))
    file_name = file_name.name if file_name.is_absolute() else file_name
    logging.debug(f"Searching for {file_name} in child directories of {cwd}")
    current_dir = Path(str(cwd)) if cwd else Path.cwd()
    it = 0
    visited = set()
    target_file = current_dir / file_name
    q = [current_dir]
    while it <= max_levels and not target_file.exists() and q:
        current_dir = q.pop(0)
        visited.add(current_dir)
        logging.debug(f"Checking {current_dir}")
        for child in current_dir.iterdir():
            if child not in visited:
                if child.is_dir():
                    q.append(child)
                elif child.name == file_name:
                    target_file = child
                    break
        it += 1
    if target_file.exists():
        return cast("PathLike", target_file)
    raise FileNotFoundError(f"File '{file_name}' not found in child directories.")

async def afind_file(file_name: "PathType", cwd: "PathType | None" = None, max_levels=3) -> "Path | None":
    """Find a file in parent or child directories."""
    if Path(str(file_name)).exists():
        print(f"Found {file_name} in {Path(str(file_name)).resolve()}")
        return Path(str(file_name))
    try:
        try:
            return await asearch_children_for_file(file_name, max_levels=max_levels, cwd=cwd)
        except FileNotFoundError:
            return await asearch_parents_for_file(file_name, max_levels=max_levels, cwd=cwd)
    except FileNotFoundError:
        return None
def find_file(file_name: "PathType", cwd: "PathType | None" = None, max_levels=3) -> "Path | None":
    """Find a file in parent or child directories."""
    if Path(str(file_name)).exists():
        return Path(str(file_name))
    try:
        try:
            return search_children_for_file(file_name, max_levels=max_levels, cwd=cwd)
        except FileNotFoundError:
            return search_parents_for_file(file_name, max_levels=max_levels, cwd=cwd)

    except FileNotFoundError:
        return search_parents_for_file(file_name, max_levels=max_levels, cwd=cwd)


def find_mb(cwd: "Path | None" = None):
    """Find the mb directory."""
    from pathlib import Path
    cwd = Path(cwd) if cwd else Path.cwd()
    try:
        return search_parents_for_file(".mb", cwd=cwd)
    except FileNotFoundError:
        try:
            out =  search_children_for_file(".mb", cwd=cwd)
            return out
        except FileNotFoundError:
           p = Path.home() / ".mb"
           p.mkdir(exist_ok=True)
           return p 