from typing import AnyStr, List

import os


def stringify(string_list: List[AnyStr]) -> AnyStr:
    """Function that turns list of strings into a joined string

    Parameters
    ----------
    List[AnyStr]
        List of strings to be joined together

    Returns
    -------
    AnyStr
        A joined string
    """
    bold_list = ["<b>" + string + "</b>" for string in string_list]
    return ", ".join(bold_list[:-1]) + f" and {bold_list[-1]}"


def check_folder(folder_path: AnyStr) -> None:
    """If folder does not exist, creates the folder

    Parameters
    ----------
    folder_path : AnyStr
        The folder path to create
    """
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)


def get_report_folder_path():
    return os.path.abspath(os.path.join(__file__, "../.."))
