from . import encoder, decoder

from lxml import etree  # type: ignore

import io
from warnings import warn
from pathlib import Path
from typing import Any, BinaryIO, TextIO, Union


def dump(data: Any, file: Union[Path | TextIO | BinaryIO]) -> None:
    """
    Serialize data as JSOML XML to file (a pathlib.Path, file or file-like object).
    """

    if isinstance(file, str):
        raise ValueError("file must be file-like object or pathlib.Path")
    lxml_param: Any
    if isinstance(file, Path):
        lxml_param = str(file)
    elif isinstance(file, io.TextIOBase):
        lxml_param = file.buffer
    else:
        lxml_param = file
    tree = etree.ElementTree(encoder.xml_from_data(data))
    tree.write(lxml_param, encoding="utf-8", xml_declaration=True)


def dumps(data: Any) -> str:
    buf = io.BytesIO()
    dump(data, buf)
    return buf.getvalue().decode("utf-8")


def load(source: Union[str, Path, BinaryIO]) -> decoder.JsonData:
    """
    Deserialize JSOML XML from source.

    source can be a file, file-like object, or pathlib.Path.

    Return like json.load.
    """

    if isinstance(source, str):
        raise ValueError("file must be file-like object or pathlib.Path")
    if isinstance(source, Path):
        source = str(source)
    root = etree.parse(source).getroot()
    if "key" in root.attrib:
        warn("Root XML element should not have key attribute", SyntaxWarning)
    return decoder.data_from_xml(root)


def loads(text: str) -> Any:
    return load(io.BytesIO(text.encode('utf-8')))
