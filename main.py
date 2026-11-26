#!/usr/bin/env python3
"""The World in One Page — Wednesday 25 November 2026.

A make.fun news-image entry (news-image-20261125): one 1024x1024 image that sums
up the world's news of Wednesday 25 November 2026, drawn as a poster front page
with a dotted world map whose numbered pins match the stories below it.

Every story below was reported on Wednesday 25 November 2026 and date-checked
against the wires (Reuters, AP, AFP, BBC and the outlets named in the research
notes). Labels: REPORTED = confirmed by more than one outlet or an official
source; CLAIM = one side's account, not independently confirmed; DENIAL = a
disputed point where a party rejects the claim. Two stories happened late on
Tuesday 24 November and were reported on Wednesday (the Huawei verdict and the
Riyadh tower strike); the page says so in its footer.

The program is deterministic: fixed data, fixed layout, no clock, no network,
no randomness — two runs write the same bytes. It uses Pillow when available
and falls back to a pure-standard-library PNG writer with an embedded bitmap
font, so it runs anywhere Python 3.13 does.

Output: $MAKEFUN_OUTPUT_DIR/entry.png, else /output/entry.png when /output
exists, else ./output/entry.png.
"""

import os
import sys

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 19, 16)
MUTED = (96, 90, 78)
RULE = (20, 19, 16)
RED = (179, 53, 44)
DOT = (178, 168, 148)
CHIP_REPORTED = (38, 92, 54)
CHIP_CLAIM = (176, 116, 22)
CHIP_DENIAL = (150, 44, 38)

# ---------------------------------------------------------------- stories
# (number, region, headline, summary, label, pin lon/lat or None)
TOP1 = (1, "THE DAY'S TOP STORY",
        "US Proposes New Tariffs on 14 Major Trading Partners",
        "Washington's Section 301 plan targets China, the EU, Japan, South Korea, India, "
        "Vietnam, Taiwan and seven more over 'structural excess capacity' — China would "
        "face 20% on top of existing duties. Beijing rejected the overcapacity charge "
        "as a false issue, and markets fell worldwide the same day.",
        "REPORTED", (-79, 38))
TOP2 = (2, "MIDDLE EAST",
        "Iran Says Two Tankers Struck Naval Mines in the Strait of Hormuz",
        "The Revolutionary Guards said two tankers on 'unauthorised' routes hit mines, "
        "exploded and caught fire, and warned all shipping to coordinate passage through "
        "the strait that carries a fifth of the world's oil. The US told its citizens "
        "in Iran to leave immediately. The strikes rest on Iran's statement alone.",
        "CLAIM", (56, 26))
TOP3 = (3, "NORTH AMERICA",
        "Huawei Convicted in Brooklyn on Fraud and Trade-Secret Theft",
        "A federal jury convicted Huawei and three subsidiaries on 10 of 12 counts — bank "
        "and wire fraud, sanctions violations, money-laundering conspiracy and stealing "
        "US trade secrets — acquitting it of racketeering. The verdict, returned Tuesday "
        "and reported Wednesday, caps an eight-year case; sentencing is set for 2027.",
        "REPORTED", (-71, 43))

REGIONS = [
    ("NORTH AMERICA", [
        (4, "AI Selloff Slams Global Markets; Dow Tops 50,000",
         "Asian chip stocks cratered (KOSPI -6.16%) as Nvidia fell 5.9% a day after soaring on its CEO's return; the Dow still closed above 50,000 for the first time.", "REPORTED", (127, 37)),
        (6, "Army Calls Iowa Explosives Detonation a Success",
         "The controlled detonation of toxic bomb chemicals succeeded, the Army said, with early lead readings near the site described as promising.", "REPORTED", (-94, 42)),
        (7, "Six Dead, Two of Them Children, in Mississippi Plane Crash",
         "Divers recovered four adults and two boys, aged 8 and 10, from a plane that crashed off the Mississippi coast, the Coast Guard said.", "REPORTED", (-89, 30)),
        (8, "Wrongfully Deported Ábrego García Leaves US for Spain",
         "Kilmar Ábrego García, whose wrongful deportation to El Salvador became a flashpoint of the immigration agenda, departed the US for Spain.", "REPORTED", None),
    ]),
    ("LATIN AMERICA", [
        (9, "All Hostages Rescued in Cartagena Supermarket Siege",
         "Police and soldiers stormed an Éxito supermarket early Wednesday, freeing every hostage and killing one gunman after a failed armoured-truck robbery.", "REPORTED", (-76, 10)),
        (10, "US Targets Brazil With Aircraft and Sugar Tariff Moves",
         "Apart from the 14-partner plan, Washington proposed 10% on Brazilian Embraer aircraft and higher duties on out-of-quota Brazilian sugar.", "REPORTED", None),
        (11, "Mexico Spared in US Overcapacity Tariff Proposal",
         "Mexico and Norway were the only two of the 16 economies investigated for which no new duties were proposed at this time.", "REPORTED", None),
    ]),
    ("EUROPE", [
        (12, "Ukrainian Drones Set Two Rosneft Refineries Ablaze in Samara",
         "Fires hit the Syzran and Kuibyshev refineries overnight; the governor confirmed one death and 145+ drones downed, while a mayor claimed only minor damage.", "REPORTED", (50, 53)),
        (13, "Ukraine Says Five Russian Jets Hit at Savasleyka Airfield",
         "Kyiv said a strike on the airfield, home to jets launching hypersonic missiles and glide bombs, hit five Russian military aircraft.", "CLAIM", (43, 57)),
        (14, "Leaked Records Put Russian War Dead Near Half a Million",
         "BBC analysis of more than 11 million leaked death records indicates at least 490,334 Russian soldiers killed in Ukraine since 2022.", "REPORTED", None),
        (15, "RAF Moves Aircraft Into Hangars at Night Over Drone Fears",
         "Britain's air force is sheltering aircraft in hangars and shelters overnight to protect them from possible drone threats.", "REPORTED", None),
    ]),
    ("MIDDLE EAST", [
        (17, "Houthi Drone Hits Riyadh's Tallest Tower Again, Wounding 11",
         "A drone struck the PIF Tower for the second time in a week; the Houthis claimed it Wednesday and also claimed, unverified, a refinery attack.", "REPORTED", (47, 25)),
        (18, "Islamic State Attack Kills Two Syrian Security Personnel",
         "The attack in the north-eastern city of Hasaka also wounded five others, Syrian state television said.", "REPORTED", None),
        (19, "Israeli Strike Kills Hamas Internal Security Chief in Gaza",
         "Mohammed Abu al-Ouf was killed with his wife and two teenage daughters in Gaza City, doctors and Gaza's Interior Ministry said.", "REPORTED", (35, 33)),
        (20, "Judges Recommend Dropping Gravest Netanyahu Charges",
         "Judges in the prime minister's corruption trial said one case had little chance of conviction; Netanyahu said the trial should end.", "REPORTED", None),
        (21, "Lebanon to Open Second International Airport Next Month",
         "The new airport in the poorer north is a project long opposed by Hezbollah, whose political sway has diminished.", "REPORTED", None),
    ]),
    ("AFRICA", [
        (23, "Fuel Tanker Fire Kills at Least 31 on Cairo Ring Road",
         "A petroleum tanker overturned and exploded in Giza, engulfing other vehicles: at least 31 dead, 21 injured, 27 vehicles charred.", "REPORTED", (31, 29)),
        (24, "Saudi National Kidnapped by Suspected Islamic State Militants in Niger",
         "The man was seized over the weekend and is being held hostage, two security sources told Reuters.", "REPORTED", (9, 17)),
        (25, "Barrick CEO Meets Mali PM in First Visit Since Standoff",
         "The mining executive's Bamako meeting was the first by a foreign company chief since the dispute between Barrick and Mali began.", "REPORTED", (-8, 13)),
        (27, "Nigerian Cinema Star Pete Edochie Dies at 79",
         "The veteran Nollywood actor died after a long battle with prostate cancer, his family announced.", "REPORTED", None),
    ]),
    ("ASIA", [
        (28, "Flooded Indonesian Gold Mine Leaves Nine Dead, 17 Trapped",
         "Rescuers recovered nine bodies from the flooded Bogor shaft, where the Ciseureuh River overflowed; 325 rescuers search for 17 still trapped.", "REPORTED", (107, -7)),
        (29, "Shenzhou-24 Docks at Tiangong With First Foreign Astronaut",
         "China's crew docked 3.5 hours after launch, carrying Pakistani specialist Muhammad Zeeshan Ali, the station's first foreign visitor.", "REPORTED", (98, 40)),
        (30, "Hasina Sets December 16 Return; Dhaka Says Only in Handcuffs",
         "The ousted Bangladeshi PM asked to be flown home from exile in India; Dhaka said she can return only via extradition.", "REPORTED", (90, 24)),
        (31, "North Korea Expels Swiss Diplomat in Sanctions Row",
         "Ties will run through embassies in Bern and Beijing, Swiss officials said.", "REPORTED", None),
        (32, "China Urges Fair Business Climate in Nexperia Dispute Talks",
         "China's foreign minister pressed his Dutch counterpart in Beijing for a fair, transparent climate for Chinese firms.", "REPORTED", None),
    ]),
    ("OCEANIA", [
        (33, "Australia and Solomon Islands Sign Landmark Security Treaty",
         "The Canberra treaty makes Australia the Solomons' primary security partner, bars any foreign military base, and ends Honiara's four-year-old pact with China.", "REPORTED", (149, -35)),
    ]),
]

NUMBERS = [
    ("31", "killed in the Cairo tanker fire"),
    ("490,334", "Russian war dead, BBC count"),
    ("145+", "drones downed over Samara"),
    ("-6.16%", "South Korea's KOSPI on the day"),
    ("50,018.70", "Dow's first close above 50,000"),
    ("325", "rescuers at the Bogor mine"),
]

# ------------------------------------------------------------- world map
# Coarse continent outlines as (lon, lat) polygons; the map is drawn as a dot
# grid sampled inside them — schematic, in the style of newspaper infographics.
LAND = [
    # North & Central America
    [(-168, 66), (-145, 70), (-128, 70), (-115, 72), (-100, 73), (-92, 78), (-85, 76),
     (-80, 73), (-78, 69), (-85, 66), (-92, 63), (-95, 60), (-93, 57), (-86, 55),
     (-82, 52), (-79, 48), (-76, 45), (-71, 44), (-70, 41), (-73, 37), (-76, 35),
     (-79, 32), (-81, 27), (-83, 29), (-86, 30), (-90, 29), (-94, 29), (-97, 26),
     (-97, 23), (-95, 19), (-91, 16), (-87, 13), (-84, 10), (-79, 9), (-82, 10),
     (-87, 13), (-92, 15), (-97, 17), (-102, 19), (-106, 22), (-110, 24), (-113, 29),
     (-117, 33), (-121, 36), (-124, 42), (-124, 47), (-129, 53), (-138, 58),
     (-150, 60), (-160, 58), (-168, 66)],
    # Greenland
    [(-46, 60), (-32, 66), (-22, 70), (-19, 75), (-28, 81), (-52, 80), (-58, 74),
     (-55, 66), (-52, 61)],
    # South America
    [(-79, 9), (-73, 11), (-65, 11), (-57, 7), (-51, 3), (-46, -1), (-38, -5),
     (-35, -8), (-39, -13), (-40, -20), (-46, -24), (-51, -31), (-56, -36),
     (-60, -39), (-63, -42), (-65, -46), (-67, -51), (-69, -54), (-72, -53),
     (-74, -47), (-74, -39), (-72, -31), (-70, -21), (-74, -16), (-78, -9),
     (-81, -5), (-80, 0), (-77, 4), (-79, 9)],
    # Africa
    [(-6, 35), (0, 36), (9, 37), (11, 34), (18, 33), (25, 32), (31, 31), (33, 29),
     (35, 24), (37, 20), (39, 16), (42, 12), (47, 11), (51, 12), (49, 6), (44, 0),
     (41, -6), (40, -12), (38, -18), (36, -22), (34, -26), (30, -31), (24, -34),
     (19, -35), (17, -32), (15, -27), (13, -19), (12, -11), (13, -5), (10, -1),
     (9, 3), (5, 5), (-2, 5), (-8, 5), (-13, 8), (-17, 12), (-17, 16), (-16, 21),
     (-15, 26), (-12, 29), (-8, 32)],
    # Madagascar
    [(44, -16), (48, -14), (50, -17), (48, -22), (46, -25), (44, -24), (43, -19)],
    # Europe
    [(-9, 37), (-9, 43), (-3, 44), (-1, 46), (-4, 48), (-1, 50), (2, 51), (5, 53),
     (7, 54), (8, 56), (7, 58), (10, 59), (12, 61), (15, 65), (19, 68), (24, 70),
     (30, 70), (35, 66), (42, 65), (48, 66), (45, 62), (40, 60), (36, 58), (31, 56),
     (29, 52), (30, 49), (27, 47), (22, 45), (19, 45), (16, 44), (12, 44), (9, 44),
     (6, 43), (3, 42), (1, 39), (-1, 38), (-5, 36)],
    # Britain
    [(-5, 50), (-3, 51), (-1, 52), (-2, 55), (-4, 57), (-6, 58), (-8, 56), (-6, 54),
     (-5, 52)],
    # Asia (Siberia, Central & East Asia, India, South-East Asia)
    [(48, 66), (58, 69), (72, 71), (88, 74), (103, 77), (118, 73), (133, 72),
     (148, 70), (160, 69), (172, 66), (178, 64), (172, 61), (161, 59), (157, 52),
     (150, 50), (142, 50), (140, 46), (136, 42), (131, 42), (128, 39), (126, 41),
     (122, 38), (121, 33), (119, 29), (112, 23), (109, 20), (108, 14), (106, 9),
     (103, 6), (100, 7), (98, 11), (96, 15), (93, 17), (91, 22), (88, 22), (86, 20),
     (83, 16), (80, 14), (78, 9), (76, 11), (73, 18), (69, 22), (66, 25), (61, 25),
     (57, 27), (54, 26), (56, 25), (59, 23), (59, 22), (56, 19), (53, 16), (49, 14),
     (44, 12), (43, 13), (41, 17), (38, 21), (35, 26), (34, 29), (36, 33), (40, 36),
     (44, 38), (47, 39), (49, 42), (47, 45), (49, 49), (51, 54), (49, 60), (48, 66)],
    # Arabia (joined to Asia along the Gulf in the dot sampling)
    [(35, 29), (37, 24), (39, 20), (42, 15), (44, 12), (49, 14), (53, 16), (56, 19),
     (59, 22), (57, 25), (52, 26), (50, 29), (48, 30), (44, 29), (40, 31), (36, 34),
     (35, 31)],
    # Indonesia & New Guinea
    [(95, 5), (100, 2), (104, -2), (107, -6), (103, -5), (98, 1), (95, 4)],
    [(109, 1), (113, 3), (117, 2), (119, -1), (116, -3), (111, -3), (109, 0)],
    [(119, -1), (121, 0), (122, -3), (120, -5), (119, -3)],
    [(131, -1), (136, -2), (141, -3), (146, -6), (150, -9), (146, -8), (140, -7),
     (135, -4), (131, -3)],
    # Japan
    [(130, 31), (132, 33), (135, 34), (138, 36), (140, 38), (141, 41), (141, 44),
     (143, 43), (141, 40), (139, 37), (136, 35), (133, 34), (131, 32)],
    # Philippines
    [(120, 18), (122, 16), (122, 13), (121, 10), (120, 13), (119, 16)],
    # Australia
    [(113, -22), (114, -29), (115, -34), (118, -35), (124, -33), (130, -32),
     (133, -32), (136, -35), (138, -36), (140, -38), (144, -38), (147, -39),
     (150, -37), (153, -33), (153, -28), (151, -24), (149, -20), (146, -19),
     (143, -15), (142, -11), (140, -16), (137, -15), (136, -12), (133, -11),
     (130, -12), (127, -14), (123, -17), (119, -20), (114, -22)],
    # New Zealand
    [(173, -35), (175, -38), (174, -41), (172, -40), (171, -37)],
    [(167, -46), (169, -44), (171, -42), (169, -43), (167, -45)],
]


def _inside(lon, lat, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > lat) != (yj > lat)) and (lon < (xj - xi) * (lat - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside


def land_dots(step=2.6):
    dots = []
    lat = 80.0
    row = 0
    while lat > -58:
        lon = -168.0 + (step / 2 if row % 2 else 0.0)
        while lon < 192:
            l = lon - 360 if lon > 180 else lon
            if any(_inside(l, lat, p) for p in LAND):
                dots.append((lon, lat))
            lon += step
        lat -= step
        row += 1
    return dots

# ------------------------------------------------------------- rendering
def _wrap(draw, text, font, width):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if draw.textlength(trial, font=font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def render_pil():
    from PIL import Image, ImageDraw, ImageFont

    FD = "/usr/share/fonts/truetype/dejavu"
    def F(name, size):
        return ImageFont.truetype(os.path.join(FD, name), size)
    SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
    SANS = lambda s: F("DejaVuSans.ttf", s)
    SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)
    SANS_I = lambda s: F("DejaVuSans-Oblique.ttf", s) if os.path.exists(os.path.join(FD, "DejaVuSans-Oblique.ttf")) else F("DejaVuSans.ttf", s)

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    def chip(x, y, label):
        col = {"REPORTED": CHIP_REPORTED, "CLAIM": CHIP_CLAIM, "DENIAL": CHIP_DENIAL}[label]
        f = SANS_B(9)
        w = d.textlength(label, font=f) + 12
        d.rounded_rectangle([x, y, x + w, y + 15], 3, fill=col)
        d.text((x + 6, y + 2.5), label, font=f, fill=(255, 255, 255))
        return w

    # masthead
    d.text((28, 22), "THE WORLD IN ONE PAGE", font=SERIF_B(41), fill=INK)
    d.text((996, 34), "make.fun · picture of the day", font=SANS_I(11), fill=MUTED, anchor="ra")
    d.line([28, 78, 996, 78], fill=RED, width=3)
    d.line([28, 83, 996, 83], fill=INK, width=1)
    d.text((28, 92), "WEDNESDAY 25 NOVEMBER 2026", font=SANS_B(13), fill=INK)
    d.text((996, 92), "29 STORIES · 7 REGIONS · ONE PAGE", font=SANS_B(13), fill=RED, anchor="ra")

    # lead story (left)
    lx, lw = 28, 434
    y = 122
    d.text((lx, y), "THE DAY'S TOP STORY", font=SANS_B(11), fill=RED)
    chip(lx + d.textlength("THE DAY'S TOP STORY", font=SANS_B(11)) + 10, y - 1, TOP1[4])
    y += 20
    for line in _wrap(d, TOP1[2], SERIF_B(26), lw):
        d.text((lx, y), line, font=SERIF_B(26), fill=INK)
        y += 31
    y += 4
    for line in _wrap(d, TOP1[3], SANS(12), lw):
        d.text((lx, y), line, font=SANS(12), fill=INK)
        y += 16.5

    # map (right)
    mx0, my0, mx1, my1 = 482, 118, 996, 316
    lon0, lon1, lat0, lat1 = -170.0, 192.0, 84.0, -60.0
    def proj(lon, lat):
        return (mx0 + (lon - lon0) / (lon1 - lon0) * (mx1 - mx0),
                my0 + (lat0 - lat) / (lat0 - lat1) * (my1 - my0))
    for lon, lat in land_dots():
        x, yy = proj(lon, lat)
        d.ellipse([x - 1.6, yy - 1.6, x + 1.6, yy + 1.6], fill=DOT)
    pins = []
    for story in [TOP1, TOP2, TOP3]:
        if story[5]:
            pins.append((story[0], story[5]))
    for _name, stories in REGIONS:
        for s in stories:
            if s[4]:
                pins.append((s[0], s[4]))
    for num, (lon, lat) in pins:
        x, yy = proj(lon, lat)
        d.ellipse([x - 9, yy - 9, x + 9, yy + 9], fill=RED, outline=(255, 255, 255), width=1)
        d.text((x, yy - 5.5), str(num), font=SANS_B(10), fill=(255, 255, 255), anchor="ma")
    d.text((482, 322), "Where the day happened — the pins carry the story numbers used below.",
           font=SANS_I(10.5), fill=MUTED)

    # feature cards
    fy = 348
    for i, story in enumerate([TOP2, TOP3]):
        cx = 28 if i == 0 else 522
        cw = 474
        d.rectangle([cx, fy, cx + cw, fy + 130], fill=(240, 235, 222), outline=RULE, width=1)
        d.text((cx + 12, fy + 9), f"{story[0]} · {story[1]}", font=SANS_B(10.5), fill=RED)
        chip(cx + cw - 12 - 74, fy + 7, story[4])
        yy = fy + 27
        for line in _wrap(d, story[2], SANS_B(15), cw - 24)[:2]:
            d.text((cx + 12, yy), line, font=SANS_B(15), fill=INK)
            yy += 19
        for line in _wrap(d, story[3], SANS(10.8), cw - 24)[:4]:
            d.text((cx + 12, yy + 1), line, font=SANS(10.8), fill=INK)
            yy += 14.2

    # region columns
    cols = [
        [REGIONS[0], REGIONS[1]],
        [REGIONS[2], REGIONS[3]],
        [REGIONS[4], REGIONS[5], REGIONS[6]],
    ]
    col_x = [28, 354, 680]
    col_w = 316
    top, bottom = 494, 900

    def draw_column(x, blocks, scale):
        yy = top
        hf = SANS_B(int(11.5 * scale))
        bf = SANS_B(int(11 * scale))
        tf = SANS(int(10.2 * scale))
        for name, stories in blocks:
            d.text((x, yy), name, font=hf, fill=RED)
            d.line([x, yy + 15 * scale, x + col_w, yy + 15 * scale], fill=RULE, width=1)
            yy += 20 * scale
            for s in stories:
                head = f"{s[0]} · {s[1]}"
                hl = _wrap(d, head, bf, col_w)
                for line in hl:
                    d.text((x, yy), line, font=bf, fill=INK)
                    yy += 13.5 * scale
                for line in _wrap(d, s[2], tf, col_w):
                    d.text((x, yy), line, font=tf, fill=INK)
                    yy += 12.3 * scale
                yy += 5.5 * scale
            yy += 6 * scale
        return yy

    scale = 1.0
    while scale > 0.8:
        # measure on a scratch draw
        scratch = ImageDraw.Draw(Image.new("RGB", (8, 8)))
        def measure(x, blocks, sc):
            yy = top
            hf = SANS_B(int(11.5 * sc)); bf = SANS_B(int(11 * sc)); tf = SANS(int(10.2 * sc))
            for name, stories in blocks:
                yy += 20 * sc
                for s in stories:
                    yy += 13.5 * sc * len(_wrap(scratch, f"{s[0]} · {s[1]}", bf, col_w))
                    yy += 12.3 * sc * len(_wrap(scratch, s[2], tf, col_w))
                    yy += 5.5 * sc
                yy += 6 * sc
            return yy
        if max(measure(0, b, scale) for b in cols) <= bottom:
            break
        scale -= 0.04
    for x, blocks in zip(col_x, cols):
        draw_column(x, blocks, scale)

    # day in numbers
    ny = 908
    d.rectangle([28, ny, 996, ny + 56], fill=INK)
    d.text((42, ny + 7), "THE DAY IN NUMBERS", font=SANS_B(10.5), fill=(247, 243, 234))
    cell_w = (996 - 42) / 6
    for i, (fig, label) in enumerate(NUMBERS):
        cx = 42 + i * cell_w
        d.text((cx, ny + 22), fig, font=SANS_B(15), fill=(255, 255, 255))
        for j, line in enumerate(_wrap(d, label, SANS(8.2), cell_w - 10)[:2]):
            d.text((cx, ny + 41 + j * 9.5), line, font=SANS(8.2), fill=(214, 208, 192))

    # footer
    d.line([28, 976, 996, 976], fill=RULE, width=1)
    foot = ("REPORTED = confirmed by more than one outlet or an official source · CLAIM = one side's account, "
            "not independently confirmed. Every story was reported on Wednesday 25 November 2026 and date-checked "
            "against Reuters, AP, AFP and BBC reporting; the Huawei verdict and the Riyadh tower strike happened "
            "late Tuesday and were reported Wednesday. Figures are as reported by the outlets named in each story.")
    yy = 982
    for line in _wrap(d, foot, SANS(9), 968):
        d.text((28, yy), line, font=SANS(9), fill=MUTED)
        yy += 12
    return img


def render_fallback():
    """Pure-stdlib PNG with a 3x5 micro font (only used if Pillow is absent)."""
    import struct
    import zlib

    px = [[PAPER for _ in range(W)] for _ in range(H)]

    def set_px(x, y, col):
        if 0 <= x < W and 0 <= y < H:
            px[y][x] = col

    glyphs = {
        "A": (2, 5, 7, 5, 5), "B": (6, 5, 6, 5, 6), "C": (3, 4, 4, 4, 3),
        "D": (6, 5, 5, 5, 6), "E": (7, 4, 6, 4, 7), "F": (7, 4, 6, 4, 4),
        "G": (3, 4, 5, 5, 3), "H": (5, 5, 7, 5, 5), "I": (7, 2, 2, 2, 7),
        "J": (1, 1, 1, 5, 2), "K": (5, 5, 6, 5, 5), "L": (4, 4, 4, 4, 7),
        "M": (5, 7, 7, 5, 5), "N": (5, 7, 7, 7, 5), "O": (2, 5, 5, 5, 2),
        "P": (6, 5, 6, 4, 4), "Q": (2, 5, 5, 6, 3), "R": (6, 5, 6, 5, 5),
        "S": (3, 4, 2, 1, 6), "T": (7, 2, 2, 2, 2), "U": (5, 5, 5, 5, 7),
        "V": (5, 5, 5, 5, 2), "W": (5, 5, 7, 7, 5), "X": (5, 5, 2, 5, 5),
        "Y": (5, 5, 2, 2, 2), "Z": (7, 1, 2, 4, 7),
        "0": (7, 5, 5, 5, 7), "1": (2, 2, 2, 2, 2), "2": (6, 1, 2, 4, 7),
        "3": (6, 1, 2, 1, 6), "4": (5, 5, 7, 1, 1), "5": (7, 4, 6, 1, 6),
        "6": (3, 4, 6, 5, 2), "7": (7, 1, 1, 2, 2), "8": (2, 5, 2, 5, 2),
        "9": (2, 5, 3, 1, 6), " ": (0, 0, 0, 0, 0), "-": (0, 0, 7, 0, 0),
        ".": (0, 0, 0, 0, 2), ",": (0, 0, 0, 2, 4), ":": (0, 2, 0, 2, 0),
        "'": (2, 2, 0, 0, 0), "/": (1, 1, 2, 4, 4), "(": (1, 2, 2, 2, 1),
        ")": (4, 2, 2, 2, 4), "+": (0, 2, 7, 2, 0), "%": (5, 1, 2, 4, 5),
        "$": (2, 7, 6, 3, 2),
    }

    def draw_text(x, y, text, col, s=2):
        cx = x
        for ch in text.upper():
            g = glyphs.get(ch, glyphs[" "])
            for r in range(5):
                for c in range(3):
                    if (g[r] >> (2 - c)) & 1:
                        for dx in range(s):
                            for dy in range(s):
                                set_px(cx + c * s + dx, y + r * s + dy, col)
            cx += 4 * s
        return cx

    draw_text(28, 24, "THE WORLD IN ONE PAGE", INK, 6)
    draw_text(28, 66, "Wednesday 25 November 2026 - 29 stories - 7 regions", MUTED, 3)
    yy = 118
    for t in (TOP1, TOP2, TOP3):
        draw_text(28, yy, f"{t[0]}. {t[2]} ({t[4]})", INK, 3)
        yy += 36
    yy += 8
    for name, stories in REGIONS:
        draw_text(28, yy, name, RED, 3)
        yy += 30
        for s in stories:
            draw_text(28, yy, f"{s[0]}. {s[1]} ({s[3]})", INK, 2)
            yy += 23
        yy += 8
        if yy > H - 130:
            break
    draw_text(28, H - 118, "Day in numbers: 31 dead Cairo - 490334 war dead - 145+ drones - KOSPI -6.16%", RED, 2)
    draw_text(28, H - 88, "Labels: REPORTED confirmed - CLAIM one side's account", MUTED, 2)
    draw_text(28, H - 58, "Date check: only items reported on 25 Nov 2026 are included.", MUTED, 2)

    raw = b""
    for row in px:
        raw += b"\x00" + b"".join(bytes(p) for p in row)

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, 9))
    png += chunk(b"IEND", b"")
    return png


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        out_dir = "/output" if os.path.isdir("/output") else os.path.join(".", "output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    try:
        img = render_pil()
        img.save(out_path, format="PNG", optimize=False)
    except ImportError:
        with open(out_path, "wb") as f:
            f.write(render_fallback())
    print("wrote", out_path)


if __name__ == "__main__":
    sys.exit(main())
