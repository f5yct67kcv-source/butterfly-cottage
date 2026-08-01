#!/usr/bin/env python3
"""Apply the round-3 content and design edits to both language versions."""
import pathlib
import sys

ROOT = pathlib.Path('/home/user/workspace/butterfly')

PDF_GREEN = 'https://www.butterfly-cottage.co.uk/images/pdf/about-us-and-green-policy.pdf'
PDF_TERMS = 'https://www.butterfly-cottage.co.uk/images/pdf/terms-and-conditions.pdf'

SOCIAL = """
            <div class="social">
              <a href="https://www.youtube.com/@scotlandbydan" rel="noopener" aria-label="{yt}" title="{yt}">
                <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.6 7.2a2.5 2.5 0 0 0-1.76-1.77C18.25 5 12 5 12 5s-6.25 0-7.84.43A2.5 2.5 0 0 0 2.4 7.2C2 8.82 2 12 2 12s0 3.18.4 4.8a2.5 2.5 0 0 0 1.76 1.77C5.75 19 12 19 12 19s6.25 0 7.84-.43a2.5 2.5 0 0 0 1.76-1.77C22 15.18 22 12 22 12s0-3.18-.4-4.8Zm-11.7 8.1V8.7l5.6 3.3-5.6 3.3Z"/></svg>
              </a>
              <a href="https://www.facebook.com/butterflygrantown/" rel="noopener" aria-label="{fb}" title="{fb}">
                <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 21v-7.5h2.6l.4-3.02h-3V8.58c0-.87.24-1.47 1.49-1.47h1.58V4.4A21.6 21.6 0 0 0 14.25 4c-2.29 0-3.86 1.4-3.86 3.96v2.52H7.8v3.02h2.59V21h3.11Z"/></svg>
              </a>
            </div>
"""

EDITS = {
    'index.html': [
        # ---- Inside / Sleeping ----
        ('<li>Spare set of double linen provided</li>\n                <li>Duvets and heated towel rails</li>',
         '<li>Additional set of double linen or towels on request</li>'),

        # ---- Good to know ----
        ('<dt>Arrival</dt><dd>16:00\u201317:00. Sarah or Daniel hand over the keys at Garden Park Guest House, 30 m away \u2014 please bring photo ID.</dd>',
         '<dt>Arrival</dt><dd>16:00\u201317:00. Sarah or Daniel hand over the keys at Garden Park Guest House, 30 m away \u2014 please bring photo ID or your booking overview. Your welcome package is waiting in the cottage, ready for your first breakfast.</dd>'),

        ('<dt>Dogs</dt><dd>Welcome by arrangement \u2014 please ask us before you book.</dd>',
         '<dt>Dogs</dt><dd>Welcome by arrangement. The fee is \u00a339 per booking and week.</dd>'),

        ('<dt>Included</dt><dd>All fuel, electricity and water, bed linen, towels and a spare set of double linen.</dd>',
         '<dt>Included</dt><dd>All fuel, electricity and water, bed linen and towels.</dd>'),

        ('<dt>Payment</dt><dd>A deposit confirms the booking; the balance is due before arrival.</dd>',
         '<dt>Payment</dt><dd>A deposit of 23% of the booking total confirms the booking. It is refunded in line with our cancellation conditions. The full balance is due 21 days before arrival.</dd>'),

        ('<dt>Cancellation</dt><dd>We are not able to refund cancellations, so we strongly recommend holiday insurance.</dd>',
         '<dt>Cancellation</dt><dd>We recommend taking out holiday insurance. Refunds on cancellations are only possible as set out in our <a href="' + PDF_TERMS + '" rel="noopener">cancellation policy</a>.</dd>'),

        # ---- The area ----
        ("""              Founded in the 18th century, Grantown is the historical capital of Strathspey. Since
              2003 it has sat inside the Cairngorms National Park \u2014 at 3,800 km\u00b2, the largest in
              the United Kingdom.""",
         """              Founded in the 18th century, Grantown is the historical capital of Strathspey \u2014
              and a near-perfect Highland base for day trips, whisky, nature and coast. From here
              you can comfortably explore Strathspey and Badenoch, Speyside, Morayshire,
              Nairnshire, Inverness and the Moray Firth coast on easy star-shaped drives. Since
              2003 the town has sat inside the Cairngorms National Park \u2014 at 3,800 km\u00b2, the
              largest in the United Kingdom."""),

        ("""                We don't serve lunch or dinner \u2014 but since 2025 we make our \u201cwee fancy Sandwich\u201d,
                the Br\u00fcgel, Swiss style, twice a week. Every booking receives a PDF with our own
                local favourites, whether you are vegan or love meat and fish.""",
         """                We don't serve lunch or dinner \u2014 but since 2025 we make our \u201cwee fancy sandwich\u201d,
                the Br\u00fcgel: a proper rustic sandwich, Swiss style. Every booking receives a PDF
                with all the local restaurants and caf\u00e9s. Whether you are vegan or love meat and
                fish, you will find the right place."""),

        # ---- Video ----
        ('data-video="RFKBOWaxQ0Y"', 'data-video="U91UYJeSr7w"'),
        ('<li><a href="https://www.youtube.com/watch?v=RFKBOWaxQ0Y" rel="noopener">Video tour</a></li>',
         '<li><a href="https://youtu.be/U91UYJeSr7w" rel="noopener">Video tour</a></li>\n'
         '              <li><a href="' + PDF_GREEN + '" rel="noopener">About us &amp; Green Policy (PDF)</a></li>\n'
         '              <li><a href="' + PDF_TERMS + '" rel="noopener">Terms and conditions (PDF)</a></li>'),

        # ---- Footer contact: social ----
        ("""              <li>Woodside Avenue<br />Grantown-on-Spey PH26 3JN</li>
            </ul>""",
         """              <li>Woodside Avenue<br />Grantown-on-Spey PH26 3JN</li>
            </ul>""" + SOCIAL.format(yt='YouTube \u2014 @scotlandbydan', fb='Facebook \u2014 Butterfly Cottage Grantown').rstrip()),

        # ---- Footer legal ----
        ('<span>\u00a9 <span data-year>2026</span> Butterfly Cottage \u00b7 Garden Park</span>\n          <span>Licence, Secondary Letting: HI-70001-F</span>',
         '<span>\u00a9 <span data-year>2026</span> Butterfly Cottage \u00b7 #scotlandbydan</span>\n          <span>Licence, Secondary Letting: HI-70001-R</span>'),
    ],

    'de/index.html': [
        # ---- Innen / Schlafen ----
        ('<li>Zus\u00e4tzlicher Satz Doppelbettw\u00e4sche vorhanden</li>\n                <li>Bettdecken und beheizte Handtuchhalter</li>',
         '<li>Zus\u00e4tzlicher Satz Doppelbettw\u00e4sche oder Handt\u00fccher auf Anfrage</li>'),

        # ---- Gut zu wissen ----
        ('<dt>Ankunft</dt><dd>16:00\u201317:00 Uhr. Sarah oder Daniel \u00fcbergeben die Schl\u00fcssel im Garden Park Guest House, 30 m entfernt \u2014 bitte bringen Sie einen Lichtbildausweis mit.</dd>',
         '<dt>Ankunft</dt><dd>16:00\u201317:00 Uhr. Sarah oder Daniel \u00fcbergeben die Schl\u00fcssel im Garden Park Guest House, 30 m entfernt \u2014 bitte bringen Sie einen Lichtbildausweis oder Ihre Buchungs\u00fcbersicht mit. Ihr Willkommenspaket wartet im Cottage, bereit f\u00fcr Ihr erstes Fr\u00fchst\u00fcck.</dd>'),

        ('<dt>Hunde</dt><dd>Nach Absprache willkommen \u2014 bitte fragen Sie uns vor der Buchung.</dd>',
         '<dt>Hunde</dt><dd>Nach Absprache willkommen. Die Geb\u00fchr betr\u00e4gt \u00a339 pro Buchung und Woche.</dd>'),

        ('<dt>Inklusive</dt><dd>Alle Heizkosten, Strom und Wasser, Bettw\u00e4sche, Handt\u00fccher und ein zus\u00e4tzlicher Satz Doppelbettw\u00e4sche.</dd>',
         '<dt>Inklusive</dt><dd>Alle Heizkosten, Strom und Wasser, Bettw\u00e4sche und Handt\u00fccher.</dd>'),

        ('<dt>Zahlung</dt><dd>Eine Anzahlung best\u00e4tigt die Buchung; der Restbetrag ist vor der Anreise f\u00e4llig.</dd>',
         '<dt>Zahlung</dt><dd>Eine Anzahlung von 23\u202f% des Buchungsbetrags best\u00e4tigt die Buchung. Sie wird gem\u00e4\u00df unseren Stornobedingungen zur\u00fcckerstattet. Der Restbetrag ist 21 Tage vor der Anreise f\u00e4llig.</dd>'),

        ('<dt>Stornierung</dt><dd>Wir k\u00f6nnen Stornierungen nicht erstatten, daher empfehlen wir dringend eine Reiseversicherung.</dd>',
         '<dt>Stornierung</dt><dd>Wir empfehlen eine Reiseversicherung. Erstattungen bei Stornierungen sind nur im Rahmen unserer <a href="' + PDF_TERMS + '" rel="noopener">Stornobedingungen</a> m\u00f6glich.</dd>'),

        # ---- Die Umgebung ----
        ("""              Im 18. Jahrhundert gegr\u00fcndet, ist Grantown die historische Hauptstadt von
              Strathspey. Seit 2003 liegt es im Cairngorms-Nationalpark \u2014 mit 3.800 km\u00b2 der
              gr\u00f6\u00dfte im Vereinigten K\u00f6nigreich.""",
         """              Im 18. Jahrhundert gegr\u00fcndet, ist Grantown die historische Hauptstadt von
              Strathspey \u2014 und ein nahezu perfekter Ausgangspunkt f\u00fcr Tagesausfl\u00fcge, Whisky,
              Natur und K\u00fcste. Von hier aus erkunden Sie bequem Strathspey und Badenoch,
              Speyside, Morayshire, Nairnshire, Inverness und die K\u00fcste des Moray Firth auf
              sternf\u00f6rmigen Fahrten. Seit 2003 liegt der Ort im Cairngorms-Nationalpark \u2014 mit
              3.800 km\u00b2 der gr\u00f6\u00dfte im Vereinigten K\u00f6nigreich."""),

        ("""                Mittag- oder Abendessen bieten wir nicht an \u2014 aber seit 2025 machen wir
                zweimal w\u00f6chentlich unser \u201ekleines feines Sandwich\u201c, den Br\u00fcgel, nach
                Schweizer Art. Jede Buchung erh\u00e4lt ein PDF mit unseren eigenen
                Lieblingsadressen vor Ort, egal ob Sie vegan leben oder Fleisch und Fisch
                lieben.""",
         """                Mittag- oder Abendessen bieten wir nicht an \u2014 aber seit 2025 machen wir
                unser \u201ekleines feines Sandwich\u201c, den Br\u00fcgel: ein richtig rustikales
                Sandwich nach Schweizer Art. Jede Buchung erh\u00e4lt ein PDF mit allen
                Restaurants und Caf\u00e9s vor Ort. Egal ob Sie vegan leben oder Fleisch und
                Fisch lieben \u2014 Sie finden den richtigen Platz."""),

        # ---- Video ----
        ('data-video="RFKBOWaxQ0Y"', 'data-video="U91UYJeSr7w"'),
        ('<li><a href="https://www.youtube.com/watch?v=RFKBOWaxQ0Y" rel="noopener">Videorundgang</a></li>',
         '<li><a href="https://youtu.be/U91UYJeSr7w" rel="noopener">Videorundgang</a></li>\n'
         '              <li><a href="' + PDF_GREEN + '" rel="noopener">\u00dcber uns &amp; Green Policy (PDF)</a></li>\n'
         '              <li><a href="' + PDF_TERMS + '" rel="noopener">Gesch\u00e4ftsbedingungen (PDF)</a></li>'),

        # ---- Fu\u00dfzeile Kontakt: Social ----
        ("""              <li>Woodside Avenue<br />Grantown-on-Spey PH26 3JN</li>
            </ul>""",
         """              <li>Woodside Avenue<br />Grantown-on-Spey PH26 3JN</li>
            </ul>""" + SOCIAL.format(yt='YouTube \u2014 @scotlandbydan', fb='Facebook \u2014 Butterfly Cottage Grantown').rstrip()),

        # ---- Fu\u00dfzeile rechtlich ----
        ('<span>\u00a9 <span data-year>2026</span> Butterfly Cottage \u00b7 Garden Park</span>\n          <span>Lizenz, Secondary Letting: HI-70001-F</span>',
         '<span>\u00a9 <span data-year>2026</span> Butterfly Cottage \u00b7 #scotlandbydan</span>\n          <span>Lizenz, Secondary Letting: HI-70001-R</span>'),
    ],
}

fail = False
for rel, pairs in EDITS.items():
    p = ROOT / rel
    h = p.read_text(encoding='utf-8')
    for old, new in pairs:
        n = h.count(old)
        if n != 1:
            print(f'!! {rel}: {n} matches for {old[:70]!r}')
            fail = True
            continue
        h = h.replace(old, new)
    p.write_text(h, encoding='utf-8')
    print(f'{rel}: written')

sys.exit(1 if fail else 0)
