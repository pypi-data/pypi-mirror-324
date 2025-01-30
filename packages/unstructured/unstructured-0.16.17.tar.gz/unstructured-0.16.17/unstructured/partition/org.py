from __future__ import annotations

from typing import IO, Any

from unstructured.documents.elements import Element
from unstructured.file_utils.file_conversion import convert_file_to_html_text_using_pandoc
from unstructured.file_utils.model import FileType
from unstructured.partition.common.common import exactly_one
from unstructured.partition.common.metadata import get_last_modified_date
from unstructured.partition.html import partition_html

DETECTION_ORIGIN: str = "org"


def partition_org(
    filename: str | None = None,
    *,
    file: IO[bytes] | None = None,
    metadata_filename: str | None = None,
    metadata_last_modified: str | None = None,
    **kwargs: Any,
) -> list[Element]:
    """Partitions an org document. The document is first converted to HTML and then
    partitioned using partition_html.

    Parameters
    ----------
    filename
        A string defining the target filename path.
    file
        A file-like object using "rb" mode --> open(filename, "rb").
    metadata_last_modified
        The last modified date for the document.
    """
    exactly_one(filename=filename, file=file)

    last_modified = get_last_modified_date(filename) if filename else None

    html_text = convert_file_to_html_text_using_pandoc(
        source_format="org", filename=filename, file=file
    )

    return partition_html(
        text=html_text,
        metadata_filename=metadata_filename or filename,
        metadata_file_type=FileType.ORG,
        metadata_last_modified=metadata_last_modified or last_modified,
        detection_origin=DETECTION_ORIGIN,
        **kwargs,
    )
