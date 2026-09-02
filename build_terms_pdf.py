#!/usr/bin/env python3
"""Typesets assets/pdf/terms-and-conditions.pdf from the text below.

The old PDF lived in the Joomla media folder and went missing when that site
was replaced. The only archived copy predates both the 4pm-7pm arrival window
and the cancellation figures, so it contradicted the website and could not be
restored.

The wording here is the owners' own current text, reproduced verbatim. To
revise it, edit TEXT and run this file again:

    pip3 install reportlab
    python3 build_terms_pdf.py
"""
from pathlib import Path

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (ListFlowable, ListItem, Paragraph,
                                SimpleDocTemplate, Spacer)

OUT = Path(__file__).resolve().parent / "assets/pdf/terms-and-conditions.pdf"

INTRO = ("Please read these pages thoroughly, these terms and conditions are part of the "
         "booking conditions.")

CLAUSES = [
    "The number of guests occupying the property must not exceed the maximum set for the "
    "property, 2 Adults and maximum 2 Children up to 10.",
    "The property and all the fitments, furniture, utensils and equipment etc. must be left "
    "in a clean and tidy condition at the conclusion of the period of the holiday let.",
    "All breakages must be notified to the owner on conclusion of the rental.",
    "The rental includes all Heating, electricity and water.",
    "A full set of linen and towels is provided.",
    "If you require additional changes of linen and towels these can be provided &ndash; there "
    "is a charge of £30 per full set. Towles can be replaced on request, please ask.",
    "Smoking and vaporing is not permitted in the Butterfly cottage.",
    "Smoke detectors must not be tampered with, or batteries removed.",
    "The property is let as a holiday let and clients must vacate the property at the end of "
    "the agreed rental period as laid down in the booking and arrival instructions.",
    "We would request that you arrive at the property between 4.00 p.m. and 7.00 p.m. on the "
    "day of arrival.<br/>If you are unable to arrive at this time, we would ask that you "
    "contact one of the emergency contacts numbers as soon as possible<br/>"
    "Sarah 0044 7745 152 094<br/>Daniel 0044 7713 445 926",
    "The cottage will be ready for your arrival and the keys will be handover to you on your "
    "arrival from Sarah or Daniel.<br/>You will find them 30m up in Garden Park Guest House.",
    "Please bring with you a form of photographic identification together with your booking "
    "details to present, should it be requested.",
    "The property must be vacated by 9.30 a.m. on the day of departure to allow the "
    "housekeeping staff sufficient time to prepare the property for the next tenants in the "
    "afternoon.",
    "We reserve the right to ask any guests to vacate the property at any time if their "
    "conduct is unsuitable to that of a holiday let.",
    "Whilst we endeavour to ensure that the property is safe in all respects for use as a "
    "holiday home, we cannot be responsible for any damage caused to guest&rsquo;s property "
    "or persons whilst staying at the property unless it is as a result of our negligence.",
    "Payment of deposit or full payment constitutes the acceptance by the client of these "
    "Terms and Conditions.",
]

SERVICES = [
    "The cottages are double glazed. Please note that there is no telephone at Butterfly "
    "Cottages. There is Wi-Fi connection in the cottage (access details in information "
    "folder).",
    "Occupants are requested to inform Sarah / Daniel of any deficiencies to crockery, "
    "cutlery, light bulbs etc. and any defects such as blockages in the plumbing etc.",
    "It would be appreciated if occupants would kindly do the basic dusting and hoovering "
    "during their stay. Tenants are also requested to ensure that the property including "
    "cooker, fridge freezer, crockery and all the utensils are left in a clean and tidy "
    "condition.",
    "Note, if deep cleaning is needed, then there will be a £95 charge.",
    "Note, there is a Garden 12m x 4m, unfortunately it&rsquo;s not fenced. Feel free to use "
    "it, but please respect other people using it too.",
]

PAYMENT = [
    "A deposit of 23% of the booking total is required.",
    "The deposit will be refunded according to the cancellation conditions.",
    "Full booking balance must be paid 21 days before arrival.",
    "Payments by bacs, and the following cards: Visa, Mastercard.",
    "We reserve the right to temporarily hold an amount prior to arrival.",
]

CANCELLATION = [
    "If the booking is cancelled less than 28 days before arrival then a charge equal to 68% "
    "of the stay will be made.",
    "If the booking is cancelled 28 or more days before arrival then a charge equal to 8.6% "
    "of the stay will be made.",
    "In the event of a no show or booking reduction after the guest(s) have arrived, the full "
    "cost of the booking is charged.",
]

WARNING = ("PLEASE NOTE THAT WE STRONGLY ADVISE YOU TO TAKE OUT A HOLIDAY INSURANCE POLICY FOR "
           "YOUR HOLIDAY AS WE ARE UNABLE TO OFFER REFUNDS ON CANCELLATIONS ACCORDING TO THE "
           "CANCELLATION CONDITIONS, especially if you book the non-refundable rate.")

CLOSING = ("If you have any queries whatsoever regarding the suitability of the Butterfly "
           "Cottage, please don&rsquo;t hesitate to email us. We&rsquo;re here to help.")


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica",
                          fontSize=9.5, leading=13.5, alignment=TA_JUSTIFY,
                          spaceAfter=4)
    h1 = ParagraphStyle("h1", parent=ss["Normal"], fontName="Helvetica-Bold",
                        fontSize=15, leading=19, spaceAfter=8)
    h2 = ParagraphStyle("h2", parent=ss["Normal"], fontName="Helvetica-Bold",
                        fontSize=11, leading=15, spaceBefore=12, spaceAfter=5)
    lead = ParagraphStyle("lead", parent=body, fontName="Helvetica-Oblique",
                          spaceAfter=10)
    warn = ParagraphStyle("warn", parent=body, fontName="Helvetica-Bold", spaceBefore=8)

    def bullets(items):
        # start= carries the bullet glyph; ListItem's value= is for numbered
        # lists and would print the literal word here.
        return ListFlowable(
            [ListItem(Paragraph(x, body), leftIndent=14) for x in items],
            bulletType="bullet", start="•", bulletFontSize=8,
            bulletFontName="Helvetica", leftIndent=14, bulletOffsetY=-1,
            spaceAfter=6)

    story = [Paragraph("Butterfly Cottage &ndash; Terms and Conditions", h1),
             Paragraph(INTRO, lead),
             bullets(CLAUSES),
             Paragraph("Services and Cleaning", h2), bullets(SERVICES),
             Paragraph("Cancellation terms", h2),
             Paragraph("Payment", ParagraphStyle("h3", parent=h2, fontSize=10, spaceBefore=6)),
             bullets(PAYMENT),
             Paragraph("Cancellation conditions",
                       ParagraphStyle("h3b", parent=h2, fontSize=10, spaceBefore=6)),
             bullets(CANCELLATION),
             Paragraph(WARNING, warn),
             Spacer(1, 10),
             Paragraph(CLOSING, body),
             Paragraph("email: relax@garden-park.co.uk", body)]

    SimpleDocTemplate(str(OUT), pagesize=A4,
                      leftMargin=22 * mm, rightMargin=22 * mm,
                      topMargin=20 * mm, bottomMargin=18 * mm,
                      title="Butterfly Cottage - Terms and Conditions",
                      author="Butterfly Cottage, Grantown-on-Spey").build(story)
    print("geschrieben:", OUT, OUT.stat().st_size, "Bytes")


if __name__ == "__main__":
    build()
