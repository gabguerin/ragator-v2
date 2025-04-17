import asyncio
from pathlib import Path


async def run_dvc_add(path: Path | str) -> None:
    process = await asyncio.create_subprocess_exec(
        "dvc",
        "add",
        path,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    if process.returncode == 0:
        print(f"DVC add successful:\n{stdout.decode()}")
    else:
        print(f"DVC add failed:\n{stderr.decode()}")
