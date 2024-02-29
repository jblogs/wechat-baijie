from datetime import datetime


def fmtfn(filename: str) -> str:
    if str:
        li = filename.index("[")
        ri = filename.index("]")
        if li < ri:
            filename = (
                filename[0:li]
                + datetime.now().strftime(filename[li + 1 : ri])
                + filename[ri + 1 :]
            )
    return filename


def is_empty_entry(thedic: dict, entry_name: str) -> bool:
    return entry_name not in thedic or not thedic[entry_name].strip()
