"""
Structured document representations for office file formats with validation and rich metadata.
"""

import datetime
from typing import Annotated, Literal, Optional, Sequence, Union

import msgspec

from .contracts import Savable


# ------------------ Common Structures ------------------
class ImageSource(msgspec.Struct, frozen=True):
    """Universal image source specification for AI/user collaboration."""

    source_type: Annotated[
        Literal["user", "ai"],
        msgspec.Meta(description="Who should provide the image content"),
    ]
    description: Annotated[
        str,
        msgspec.Meta(description="Human-readable description of the required image"),
    ]
    generation_prompt: Annotated[
        Optional[str],
        msgspec.Meta(description="Detailed prompt for AI-generated images"),
    ] = None
    parameters: Annotated[
        Optional[dict],
        msgspec.Meta(description="Technical parameters for image generation/selection"),
    ] = None


class Rectangle(msgspec.Struct, frozen=True):
    """Axis-aligned bounding box representation."""

    x1: float
    y1: float
    x2: float
    y2: float

    def __post_init__(self):
        if self.x1 >= self.x2:
            raise ValueError("x2 must be greater than x1")
        if self.y1 >= self.y2:
            raise ValueError("y2 must be greater than y1")


class Color(msgspec.Struct, frozen=True):
    """Color representation with multiple format support."""

    hex: Annotated[
        Optional[str],
        msgspec.Meta(
            description="Hex color code",
            pattern=r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
            examples=["#FF0000", "#09C"],
        ),
    ] = None
    rgb: Optional[tuple[int, int, int]] = None
    cmyk: Optional[tuple[float, float, float, float]] = None


class Font(msgspec.Struct, frozen=True):
    """Detailed font specification."""

    family: str
    size: float
    color: Color = msgspec.field(default_factory=lambda: Color(hex="#000000"))
    weight: Annotated[
        Optional[Union[int, Literal["normal", "bold"]]],
        msgspec.Meta(examples=[400, "bold", 700]),
    ] = None
    style: Annotated[
        Optional[Literal["normal", "italic", "oblique"]],
        msgspec.Meta(examples=["italic"]),
    ] = None


# ------------------ PDF Structures ------------------
class PDFMetadata(msgspec.Struct, frozen=True):
    """Comprehensive PDF metadata with validation."""

    title: Annotated[
        str, msgspec.Meta(description="Document title", examples=["Annual Report 2023"])
    ]
    author: Annotated[
        Sequence[str],
        msgspec.Meta(
            description="List of authors", examples=[["John Doe", "Acme Corp"]]
        ),
    ] = ()
    subject: Optional[str] = None
    keywords: Annotated[
        Sequence[str],
        msgspec.Meta(
            description="Sorted unique keywords", examples=[["finance", "report"]]
        ),
    ] = ()
    creation_date: datetime.datetime
    modification_date: Optional[datetime.datetime] = None
    producer: Optional[str] = None
    creator: Optional[str] = None
    trapped: Optional[bool] = None
    custom: Annotated[
        dict[str, str], msgspec.Meta(description="Custom metadata properties")
    ] = msgspec.field(default_factory=dict)

    def __post_init__(self):
        if self.modification_date and self.modification_date < self.creation_date:
            raise ValueError("Modification date must be after creation date")
        if len(self.keywords) != len(set(k.lower() for k in self.keywords)):
            raise ValueError("Keywords must be unique (case-insensitive)")


class PDFPageElement(msgspec.Struct, frozen=True):
    """Base element with validated positioning."""

    bounding_box: Rectangle
    rotation: Annotated[int, msgspec.Meta(ge=0, le=360, multiple_of=90)] = 0
    opacity: Annotated[float, msgspec.Meta(ge=0.0, le=1.0)] = 1.0


class PDFTextBlock(PDFPageElement, frozen=True):
    """Rich text content with styling."""

    content: str
    font: Font
    line_height: Annotated[
        Optional[float], msgspec.Meta(description="Line spacing multiplier")
    ] = 1.2
    alignment: Annotated[
        Optional[Literal["left", "center", "right", "justify"]],
        msgspec.Meta(examples=["justify"]),
    ] = None


class PDFImage(PDFPageElement, frozen=True):
    """Image placement specification."""

    source: ImageSource
    target_format: Annotated[
        Literal["JPEG", "PNG", "TIFF", "BMP", "GIF"],
        msgspec.Meta(description="Requested output format"),
    ]
    quality: Annotated[
        Optional[float],
        msgspec.Meta(description="Quality percentage for compression", ge=0, le=100),
    ] = None
    target_dpi: Annotated[
        Optional[tuple[int, int]],
        msgspec.Meta(description="Requested output resolution (horizontal, vertical)"),
    ] = None


class PDFAnnotation(msgspec.Struct, frozen=True):
    """Document annotation base class."""

    type: Literal["text", "link", "highlight", "stamp"]
    contents: Optional[str] = None
    author: Optional[str] = None
    modified_date: Optional[datetime.datetime] = None


class PDFPage(msgspec.Struct, frozen=True):
    """Page representation with multiple content types."""

    number: Annotated[int, msgspec.Meta(ge=1)]
    size: Annotated[
        tuple[float, float], msgspec.Meta(description="(width, height) in points")
    ]
    content: Sequence[Union[PDFTextBlock, PDFImage, PDFAnnotation]]
    bleed_box: Optional[Rectangle] = None
    trim_box: Optional[Rectangle] = None
    art_box: Optional[Rectangle] = None


class PDFOutlineItem(msgspec.Struct, frozen=True):
    """Hierarchical document outline entry."""

    title: str
    page_number: int
    children: Sequence["PDFOutlineItem"] = ()


class PDFAttachment(msgspec.Struct, frozen=True):
    """Embedded file specification."""

    name: str
    description: Annotated[
        str, msgspec.Meta(description="Detailed description of the attachment content")
    ]
    reference: Annotated[
        Optional[str],
        msgspec.Meta(description="Unique identifier for external systems"),
    ] = None
    mime_type: str


class PDFDocument(Savable, frozen=True):
    """Complete PDF document with validation."""

    metadata: PDFMetadata
    pages: Sequence[PDFPage]
    outline: Sequence[PDFOutlineItem] = ()
    attachments: Sequence[PDFAttachment] = ()
    version: Annotated[
        tuple[int, int], msgspec.Meta(description="PDF specification version")
    ] = (1, 7)

    def __post_init__(self):
        if len(self.pages) == 0:
            raise ValueError("Document must contain at least one page")
        if any(p.number != i + 1 for i, p in enumerate(self.pages)):
            raise ValueError("Page numbers must be sequential starting from 1")


# ------------------ PowerPoint Structures ------------------
class PresentationMetadata(msgspec.Struct, frozen=True):
    """Extended presentation metadata."""

    title: str
    authors: Sequence[str] = ()
    created: datetime.datetime
    modified: Optional[datetime.datetime] = None
    slide_size: Annotated[
        tuple[float, float], msgspec.Meta(description="(width, height) in points")
    ] = (9144000, 6858000)  # Default 16:9 aspect ratio
    theme: Optional[str] = None
    company: Optional[str] = None
    category: Optional[str] = None


class SlideLayout(msgspec.Struct, frozen=True):
    """Slide layout template specification."""

    name: str
    type: Literal["title", "section", "content", "comparison", "blank"]
    placeholders: Sequence[str] = ()


class SlideElement(msgspec.Struct, frozen=True):
    """Base slide element with common properties."""

    position: tuple[float, float]
    size: tuple[float, float]
    rotation: Annotated[float, msgspec.Meta(ge=0, le=360)] = 0.0
    z_order: int = 0


class SlideText(SlideElement, frozen=True):
    """Rich text content with multiple paragraphs."""

    content: Sequence[
        Annotated[
            dict,
            msgspec.Meta(
                description="Paragraphs with formatting",
                examples=[[{"text": "Hello", "font": {"size": 44}}]],
            ),
        ]
    ]
    style: Optional[str] = None
    wrap: bool = True
    margin: tuple[float, float, float, float] = (0, 0, 0, 0)


class SlideMedia(SlideElement, frozen=True):
    """Media content specification."""

    media_type: Literal["image", "video", "audio", "object"]
    source: ImageSource
    target_format: str
    link: Optional[str] = None


class SlideShape(SlideElement, frozen=True):
    """Geometric shape with styling."""

    shape_type: Literal["rectangle", "ellipse", "line", "polygon"]
    points: Sequence[tuple[float, float]] = ()
    fill: Optional[Color] = None
    stroke: Annotated[
        Optional[tuple[Color, float]], msgspec.Meta(description="(color, width) tuple")
    ] = None


class SlideNotes(msgspec.Struct, frozen=True):
    """Presenter notes associated with a slide."""

    text: str
    author: Optional[str] = None
    date: Optional[datetime.datetime] = None


class Slide(msgspec.Struct, frozen=True):
    """Complete slide representation with multiple element types."""

    number: int
    layout: SlideLayout
    background: Annotated[
        Optional[Union[Color, ImageSource]],
        msgspec.Meta(description="Color or image background specification"),
    ] = None
    elements: Sequence[Union[SlideText, SlideMedia, SlideShape]]
    transitions: Annotated[
        dict, msgspec.Meta(description="Animation and transition effects")
    ] = msgspec.field(default_factory=dict)
    notes: Optional[SlideNotes] = None


class PPTXDocument(Savable, frozen=True):
    """Complete presentation structure with validation."""

    metadata: PresentationMetadata
    slides: Sequence[Slide]
    layouts: Sequence[SlideLayout] = ()
    masters: Sequence[dict] = ()
    templates: Sequence[dict] = ()

    def __post_init__(self):
        if len(self.slides) == 0:
            raise ValueError("Presentation must contain at least one slide")
        if any(s.number != i + 1 for i, s in enumerate(self.slides)):
            raise ValueError("Slide numbers must be sequential starting from 1")


# ------------------ Word Structures ------------------
class DocxMetadata(msgspec.Struct, frozen=True):
    """Word document metadata with extended properties."""

    title: str
    authors: Sequence[str] = ()
    created: datetime.datetime
    modified: Optional[datetime.datetime] = None
    company: Optional[str] = None
    subject: Optional[str] = None
    keywords: Sequence[str] = ()
    template: Optional[str] = None


class Run(msgspec.Struct, frozen=True):
    """Text run with formatting."""

    text: str
    font: Optional[Font] = None
    style: Optional[str] = None
    highlight: Optional[Color] = None


class Paragraph(msgspec.Struct, frozen=True):
    """Document paragraph with rich content."""

    runs: Sequence[Run]
    alignment: Optional[Literal["left", "center", "right", "justify"]] = None
    style: Optional[str] = None
    spacing: tuple[Optional[float], Optional[float]] = (None, None)


class TableCell(msgspec.Struct, frozen=True):
    """Table cell containing nested content."""

    content: Sequence[Union["Paragraph", "Table"]]
    style: Optional[dict] = None
    colspan: int = 1
    rowspan: int = 1


class TableRow(msgspec.Struct, frozen=True):
    """Table row containing cells."""

    cells: Sequence[TableCell]
    height: Optional[float] = None
    header: bool = False


class Table(msgspec.Struct, frozen=True):
    """Structured table representation."""

    rows: Sequence[TableRow]
    style: Optional[dict] = None
    width: Optional[float] = None


class DocxImage(msgspec.Struct, frozen=True):
    """Embedded image specification."""

    source: ImageSource
    target_format: Literal["JPEG", "PNG", "BMP"]
    width: float
    height: float
    caption: Optional[str] = None
    wrap_style: Literal["inline", "square", "tight"] = "inline"


class SectionSettings(msgspec.Struct, frozen=True):
    """Page layout settings for document sections."""

    page_width: float
    page_height: float
    margins: tuple[float, float, float, float]
    orientation: Literal["portrait", "landscape"] = "portrait"
    columns: int = 1


class DocxSection(msgspec.Struct, frozen=True):
    """Document section with content and settings."""

    content: Sequence[Union[Paragraph, Table, DocxImage]]
    settings: SectionSettings = msgspec.field(
        default_factory=lambda: SectionSettings(
            page_width=12240, page_height=15840, margins=(1440, 1440, 1440, 1440)
        )
    )


class DocxDocument(Savable, frozen=True):
    """Complete Word document structure with validation."""

    metadata: DocxMetadata
    sections: Sequence[DocxSection]
    styles: dict = msgspec.field(default_factory=dict)
    numbering: dict = msgspec.field(default_factory=dict)

    def __post_init__(self):
        if len(self.sections) == 0:
            raise ValueError("Document must contain at least one section")
        if any(len(section.content) == 0 for section in self.sections):
            raise ValueError("All sections must contain content")
