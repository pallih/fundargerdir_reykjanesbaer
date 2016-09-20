# -*- coding: utf-8 -*-

import scraperwiki
import lxml.html
import requests
import urlparse
from dateutil import parser
from dateutil.parser import parserinfo

BASE_URL = "http://www.reykjanesbaer.is"
DATA_URL = "http://www.reykjanesbaer.is/stjornkerfi/fundargerdir?page=1&group_id=&datefrom=&dateto=&keywords="


class Icelandic(parserinfo):
    def __init__(self):
        self.WEEKDAYS = [(u"Mán", u"Mánudagur"),
                         (u"Þri", u"Þriðjudagur"),
                         (u"Mið", u"Miðvikudagur"),
                         (u"Fim", u"Fimmtudagur"),
                         (u"Fös", u"Föstudagur"),
                         (u"Lau", u"Laugardagur"),
                         (u"Sun", u"Sunnudagur")]
        self.MONTHS = [(u"Jan", u"janúar"),
                       (u"Feb", u"febrúar"),
                       (u"Mar", u"mars"),
                       (u"Apr", u"apríl"),
                       (u"maí", u"maí"),
                       (u"jún", u"júní"),
                       (u"júl", u"júlí"),
                       (u"ágú", u"ágúst"),
                       (u"sep", u"september"),
                       (u"okt", u"október"),
                       (u"nov", u"nóvember"),
                       (u"des", u"desember")]
        parserinfo.__init__(self)

    def __call__(self):
        return self


icelandic_dateutil_parserinfo = Icelandic()


r = requests.get(DATA_URL)
root = lxml.html.fromstring(r.text)
trs = root.xpath("//table[@id='fundagerd']/tbody/tr")
data = []
for tr in trs:
    meeting = {}
    meeting["nefnd"] = tr[0].text
    meeting["titill"] = tr[1][0].text
    meeting["url"] = urlparse.urljoin(BASE_URL, tr[1][0].attrib["href"])
    meeting["dagsetning"] = tr[2].text
    meeting["date"] = parser.parse(meeting["dagsetning"],
                                   icelandic_dateutil_parserinfo)
    data.append(meeting)
scraperwiki.sqlite.save(unique_keys=['url'],
                        data=data)
