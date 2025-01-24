"""
Blocks module entry point. Used to cleanly organize blocks into
individual files based on purpose, but provide them all as a
single `blocks` module.
"""

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from wagtail import blocks

from .base_blocks import BaseBlock  # noqa
from .base_blocks import BaseLayoutBlock  # noqa
from .base_blocks import BaseLinkBlock  # noqa
from .base_blocks import ClassifierTermChooserBlock  # noqa
from .base_blocks import CoderedAdvColumnSettings  # noqa
from .base_blocks import CoderedAdvSettings  # noqa
from .base_blocks import CoderedAdvTrackingSettings  # noqa
from .base_blocks import CollectionChooserBlock  # noqa
from .base_blocks import LinkStructValue  # noqa
from .content_blocks import AccordionBlock
from .content_blocks import CardBlock
from .content_blocks import CarouselBlock
from .content_blocks import ContentWallBlock  # noqa
from .content_blocks import FilmStripBlock
from .content_blocks import ImageGalleryBlock
from .content_blocks import ModalBlock
from .content_blocks import NavDocumentLinkWithSubLinkBlock
from .content_blocks import NavExternalLinkWithSubLinkBlock
from .content_blocks import NavPageLinkWithSubLinkBlock
from .content_blocks import PriceListBlock
from .content_blocks import ReusableContentBlock
from .html_blocks import ButtonBlock
from .html_blocks import DownloadBlock
from .html_blocks import EmbedGoogleMapBlock
from .html_blocks import EmbedVideoBlock
from .html_blocks import ImageBlock
from .html_blocks import ImageLinkBlock
from .html_blocks import PageListBlock
from .html_blocks import PagePreviewBlock
from .html_blocks import QuoteBlock
from .html_blocks import RichTextBlock
from .html_blocks import TableBlock
from .layout_blocks import CardGridBlock
from .layout_blocks import GridBlock
from .layout_blocks import HeroBlock
from .stream_form_blocks import CoderedStreamFormCharFieldBlock
from .stream_form_blocks import CoderedStreamFormCheckboxesFieldBlock
from .stream_form_blocks import CoderedStreamFormCheckboxFieldBlock
from .stream_form_blocks import CoderedStreamFormDateFieldBlock
from .stream_form_blocks import CoderedStreamFormDateTimeFieldBlock
from .stream_form_blocks import CoderedStreamFormDropdownFieldBlock
from .stream_form_blocks import CoderedStreamFormFileFieldBlock
from .stream_form_blocks import CoderedStreamFormImageFieldBlock
from .stream_form_blocks import CoderedStreamFormNumberFieldBlock
from .stream_form_blocks import CoderedStreamFormRadioButtonsFieldBlock
from .stream_form_blocks import CoderedStreamFormStepBlock
from .stream_form_blocks import CoderedStreamFormTextFieldBlock
from .stream_form_blocks import CoderedStreamFormTimeFieldBlock


# Collections of blocks commonly used together.

HTML_STREAMBLOCKS = [
    ("text", RichTextBlock(icon="cr-font")),
    ("button", ButtonBlock()),
    ("image", ImageBlock()),
    ("image_link", ImageLinkBlock()),
    (
        "html",
        blocks.RawHTMLBlock(
            icon="code",
            form_classname="monospace",
            label=_("HTML"),
        ),
    ),
    ("download", DownloadBlock()),
    ("embed_video", EmbedVideoBlock()),
    ("quote", QuoteBlock()),
    ("table", TableBlock()),
    ("google_map", EmbedGoogleMapBlock()),
    ("page_list", PageListBlock()),
    ("page_preview", PagePreviewBlock()),
]

CONTENT_STREAMBLOCKS = HTML_STREAMBLOCKS

if not settings.CRX_DISABLE_FOR_PACMS:
    CONTENT_STREAMBLOCKS += [
        ("accordion", AccordionBlock()),
    ]

CONTENT_STREAMBLOCKS += [
    ("card", CardBlock()),
    ("carousel", CarouselBlock()),
]

if not settings.CRX_DISABLE_FOR_PACMS:
    CONTENT_STREAMBLOCKS += [
        ("film_strip", FilmStripBlock()),
    ]

CONTENT_STREAMBLOCKS += [
    ("image_gallery", ImageGalleryBlock()),
    ("modal", ModalBlock(HTML_STREAMBLOCKS)),
    ("pricelist", PriceListBlock()),
    ("reusable_content", ReusableContentBlock()),
]

NAVIGATION_STREAMBLOCKS = [
    ("page_link", NavPageLinkWithSubLinkBlock()),
    ("external_link", NavExternalLinkWithSubLinkBlock()),
    ("document_link", NavDocumentLinkWithSubLinkBlock()),
]

BASIC_LAYOUT_STREAMBLOCKS = [
    ("row", GridBlock(HTML_STREAMBLOCKS)),
    (
        "html",
        blocks.RawHTMLBlock(
            icon="code", form_classname="monospace", label=_("HTML")
        ),
    ),
]

LAYOUT_STREAMBLOCKS = [
    (
        "hero",
        HeroBlock(
            [
                ("row", GridBlock(CONTENT_STREAMBLOCKS)),
                (
                    "cardgrid",
                    CardGridBlock(
                        [
                            ("card", CardBlock()),
                        ]
                    ),
                ),
                (
                    "html",
                    blocks.RawHTMLBlock(
                        icon="code", form_classname="monospace", label=_("HTML")
                    ),
                ),
            ]
        ),
    ),
    ("row", GridBlock(CONTENT_STREAMBLOCKS)),
    (
        "cardgrid",
        CardGridBlock(
            [
                ("card", CardBlock()),
            ]
        ),
    ),
    (
        "html",
        blocks.RawHTMLBlock(
            icon="code", form_classname="monospace", label=_("HTML")
        ),
    ),
]

STREAMFORM_FIELDBLOCKS = [
    ("sf_singleline", CoderedStreamFormCharFieldBlock(group=_("Fields"))),
    ("sf_multiline", CoderedStreamFormTextFieldBlock(group=_("Fields"))),
    ("sf_number", CoderedStreamFormNumberFieldBlock(group=_("Fields"))),
    ("sf_checkboxes", CoderedStreamFormCheckboxesFieldBlock(group=_("Fields"))),
    ("sf_radios", CoderedStreamFormRadioButtonsFieldBlock(group=_("Fields"))),
    ("sf_dropdown", CoderedStreamFormDropdownFieldBlock(group=_("Fields"))),
    ("sf_checkbox", CoderedStreamFormCheckboxFieldBlock(group=_("Fields"))),
    ("sf_date", CoderedStreamFormDateFieldBlock(group=_("Fields"))),
    ("sf_time", CoderedStreamFormTimeFieldBlock(group=_("Fields"))),
    ("sf_datetime", CoderedStreamFormDateTimeFieldBlock(group=_("Fields"))),
    ("sf_image", CoderedStreamFormImageFieldBlock(group=_("Fields"))),
    ("sf_file", CoderedStreamFormFileFieldBlock(group=_("Fields"))),
]

STREAMFORM_BLOCKS = [
    (
        "step",
        CoderedStreamFormStepBlock(STREAMFORM_FIELDBLOCKS + HTML_STREAMBLOCKS),
    ),
]
