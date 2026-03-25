from django.db import models

from wagtail.contrib.forms.models import AbstractFormField, AbstractEmailForm

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from modelcluster.fields import ParentalKey



class AboutPage(Page):
    body = RichTextField(
        blank=True,
        help_text="Main content of the About page"
    )
    team_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Image of the team or a representative photo"
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
        FieldPanel("team_image"),
    ]

    # This limits where this page can be created
    parent_page_types = ["home.HomePage"]
    # This page cannot have children
    subpage_types = []

class CourseCatalogPage(Page):
    introduction = RichTextField(
        blank=True,
        help_text="Introduction text shown at the top of the catalog"
    )
    catalog_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Header image for this course category"
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("catalog_image"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = ["pages.CourseDetailPage"]


class CourseDetailPage(Page):
    course_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Main image for the course"
    )
    description = RichTextField(
        help_text="Short description shown in the catalog listing"
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Price in EUR (e.g., 29.99)"
    )
    instructor = models.CharField(
        max_length=255,
        blank=True,
        help_text="Name of the course instructor"
    )
    course_content = StreamField(
        [
            ("heading", blocks.CharBlock(
                form_classname="title",
                help_text="Section heading"
            )),
            ("paragraph", blocks.RichTextBlock(
                help_text="Rich text content"
            )),
            ("image", ImageChooserBlock(
                help_text="Full-width image"
            )),
            ("learning_point", blocks.CharBlock(
                help_text="A single 'What you will learn' item"
            )),
        ],
        use_json_field=True,
        blank=True,
        help_text="Detailed course content built from blocks"
    )

    content_panels = Page.content_panels + [
        FieldPanel("course_image"),
        FieldPanel("description"),
        FieldPanel("price"),
        FieldPanel("instructor"),
        FieldPanel("course_content"),
    ]

    parent_page_types = ["pages.CourseCatalogPage"]
    subpage_types = []


class FAQPage(Page):
    introduction = RichTextField(
        blank=True,
        help_text="Optional introduction text above the FAQ list"
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        InlinePanel("faq_items", label="FAQ Item"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = []


class FAQItem(Orderable):
    page = ParentalKey(
        FAQPage,
        on_delete=models.CASCADE,
        related_name="faq_items",
    )
    question = models.CharField(
        max_length=500,
        help_text="The frequently asked question"
    )
    answer = RichTextField(
        help_text="The answer to the question"
    )

    panels = [
        FieldPanel("question"),
        FieldPanel("answer"),
    ]


class ContactFormField(AbstractFormField):
    page = ParentalKey(
        "ContactPage",
        on_delete=models.CASCADE,
        related_name="form_fields",
    )


class ContactPage(AbstractEmailForm):
    intro = RichTextField(
        blank=True,
        help_text="Text shown above the contact form"
    )
    thank_you_text = RichTextField(
        blank=True,
        help_text="Text shown after the form is submitted"
    )

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("intro"),
        InlinePanel("form_fields", label="Form Field"),
        FieldPanel("thank_you_text"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = []


class PricingPage(Page):
    introduction = RichTextField(
        blank=True,
        help_text="Introduction text for the pricing page"
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = []