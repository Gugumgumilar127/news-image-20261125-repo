# stories.py - the dataset for the one-page world-news image.
# Every story happened or was first reported on Wednesday
# 25 November 2026 and was checked against the named wires
# (see research.md for the per-story sourcing and date basis).
# 50 stories total: 16 illustrated leads + a 34-story digest.
# Region counts below are recomputed from this final list.

DATE_LINE = "WEDNESDAY 25 NOVEMBER 2026"
MASTHEAD = "THE WORLD"
SUBLINE = "50 STORIES \u00b7 7 REGIONS \u00b7 ONE PAGE"
FOOTER = ("Every story on this page happened or was first "
          "reported on Wednesday 25 November 2026.")
SOURCES = ("Sources: Reuters \u00b7 AP \u00b7 BBC \u00b7 RFE/RL "
           "\u00b7 CAS \u00b7 WFP \u00b7 Daily Maverick "
           "\u00b7 wire reports")

REGION_ORDER = ["ASIA", "AMERICAS", "EUROPE", "MIDDLE EAST",
                "AFRICA", "WORLD", "OCEANIA"]
REGION_COUNTS = {"ASIA": 10, "AMERICAS": 13, "EUROPE": 9,
                 "MIDDLE EAST": 7, "AFRICA": 5, "WORLD": 2,
                 "OCEANIA": 4}
REGION_COLORS = {"ASIA": "#D97706", "AMERICAS": "#2E7D4F",
                 "EUROPE": "#3556A8", "MIDDLE EAST": "#8E44AD",
                 "AFRICA": "#B3352B", "WORLD": "#6B6252",
                 "OCEANIA": "#1F8AAD"}

# Lead stories: num, region, topic, headline, summary, source,
# icon, map pin (lon, lat), tag ("" or "CLAIM").
STORIES = [
    {"num": 1, "region": "WORLD", "topic": "CLIMATE",
     "headline": "COP31 Ends Without a Deal as Producers "
                 "Block Phase-Out",
     "summary": "Nearly 200 nations leave Antalya with no final "
                "pact: oil and gas producers refuse any text "
                "naming a fossil-fuel phase-out.",
     "source": "BD Global Times \u00b7 Reuters", "icon": "leaf",
     "pin": (30.7, 36.9), "tag": ""},
    {"num": 2, "region": "EUROPE", "topic": "CONFLICT",
     "headline": "Zelenskiy Confirms Sinking of Russian "
                 "Warship Off Libya",
     "summary": "Ukraine's sea drones sank the corvette Merkury "
                "at Benghazi and hit a cargo ship in the Baltic; "
                "Moscow calls it terrorism.",
     "source": "Reuters \u00b7 RFE/RL", "icon": "drone",
     "pin": (20.1, 32.1), "tag": ""},
    {"num": 3, "region": "AMERICAS", "topic": "TRADE",
     "headline": "US Set to Unveil New Tariffs on 16 "
                 "Trading Partners",
     "summary": "A Section 301 probe into \u201cexcess factory "
                "capacity\u201d ends with fresh duties expected "
                "to stack on existing tariffs.",
     "source": "Reuters \u00b7 BBC", "icon": "crate",
     "pin": (-77.0, 38.9), "tag": ""},
    {"num": 4, "region": "AMERICAS", "topic": "TECH LAW",
     "headline": "Huawei Guilty of Stealing Trade Secrets "
                 "in US Trial",
     "summary": "A federal jury convicts the Chinese tech giant "
                "of conspiracy and bank fraud, but acquits it "
                "of racketeering.",
     "source": "AP \u00b7 BBC", "icon": "chip",
     "pin": (-74.0, 40.7), "tag": ""},
    {"num": 5, "region": "AMERICAS", "topic": "SECURITY",
     "headline": "Hackers Breach CIA's Unclassified "
                 "Computer System",
     "summary": "A cyberattack pierced an unclassified network "
                "at the agency, an AP source says; what was "
                "taken is not yet known.",
     "source": "AP", "icon": "lock",
     "pin": (-77.5, 39.2), "tag": ""},
    {"num": 6, "region": "MIDDLE EAST", "topic": "CONFLICT",
     "headline": "Houthi Strike Hits Riyadh's Tallest "
                 "Tower, 11 Hurt",
     "summary": "Saudi civil defence says the attack wounded 11 "
                "people as the Yemen war spills onto the "
                "capital's skyline.",
     "source": "Reuters", "icon": "tower",
     "pin": (46.7, 24.6), "tag": ""},
    {"num": 7, "region": "MIDDLE EAST", "topic": "ENERGY",
     "headline": "Iran Says Three Tankers Struck Mines "
                 "in Hormuz",
     "summary": "The Revolutionary Guard navy makes the claim "
                "as shipping through the world's oil chokepoint "
                "grows tenser.",
     "source": "IRGC claim \u00b7 wires", "icon": "tanker",
     "pin": (56.3, 26.5), "tag": "CLAIM"},
    {"num": 8, "region": "AMERICAS", "topic": "MARKETS",
     "headline": "AI Stocks Slide Again as Nvidia's "
                 "Bounce Fizzles",
     "summary": "Nvidia falls 7% a day after its record surge, "
                "and the attorney general dodges Congress over "
                "Trump's role in Huang's return.",
     "source": "AP \u00b7 Reuters \u00b7 BBC", "icon": "chart",
     "pin": (-73.9, 40.5), "tag": ""},
    {"num": 9, "region": "EUROPE", "topic": "JUSTICE",
     "headline": "Sarkozy and Carla Bruni Ordered to "
                 "Stand Trial",
     "summary": "French officials send the former president's "
                "corruption case to trial, with a first hearing "
                "set for 1 April 2027.",
     "source": "Reuters \u00b7 BBC", "icon": "gavel",
     "pin": (2.35, 48.85), "tag": ""},
    {"num": 10, "region": "OCEANIA", "topic": "SOCIETY",
     "headline": "Australia Apologises to LGBTQ Veterans "
                 "in Parliament",
     "summary": "Defence Minister Richard Marles says sorry for "
                "decades of discriminatory policies that harmed "
                "serving LGBTQ members.",
     "source": "Reuters", "icon": "medal",
     "pin": (149.1, -35.3), "tag": ""},
    {"num": 11, "region": "ASIA", "topic": "SPACE",
     "headline": "China Launches First Pakistani Astronaut "
                 "to Space",
     "summary": "Beijing calls the joint mission a historic "
                "journey as its crewed programme opens to a "
                "partner nation.",
     "source": "BBC", "icon": "rocket",
     "pin": (100.3, 41.0), "tag": ""},
    {"num": 12, "region": "ASIA", "topic": "POLITICS",
     "headline": "BJP and Akali Dal Reunite for Punjab's "
                 "2027 Election",
     "summary": "The two parties announce an alliance six years "
                "after splitting, reshaping the race for the "
                "Punjab assembly.",
     "source": "Indian wires", "icon": "ballot",
     "pin": (75.8, 31.1), "tag": ""},
    {"num": 13, "region": "AFRICA", "topic": "SPORT",
     "headline": "Senegal Restored as African Champions by "
                 "Sports Court",
     "summary": "CAS overturns the forfeit and confirms "
                "Senegal's 1\u20130 AFCON final win over "
                "Morocco, who say they will challenge it.",
     "source": "CAS \u00b7 Daily Maverick", "icon": "trophy",
     "pin": (-6.85, 33.97), "tag": ""},
    {"num": 14, "region": "ASIA", "topic": "EDUCATION",
     "headline": "Shortwave Lessons Reach Afghan Girls "
                 "Barred From School",
     "summary": "RFE/RL goes back to shortwave radio with "
                "classes for girls the Taliban exclude from "
                "classrooms.",
     "source": "RFE/RL", "icon": "radio",
     "pin": (69.2, 34.5), "tag": ""},
    {"num": 15, "region": "EUROPE", "topic": "WAR TOLL",
     "headline": "Analysis: 700,000 Russian Soldiers Killed "
                 "in Ukraine",
     "summary": "The new estimate passes a grim milestone; "
                "Russia's own reported figures put its war dead "
                "nearer 500,000.",
     "source": "RFE/RL \u00b7 BBC", "icon": "cross",
     "pin": (30.5, 50.4), "tag": ""},
    {"num": 16, "region": "ASIA", "topic": "DISASTER",
     "headline": "Hong Kong Marks a Year Since Fire That "
                 "Killed 168",
     "summary": "The blaze engulfed seven high-rise blocks, the "
                "city's deadliest in decades; families still "
                "await answers.",
     "source": "AP", "icon": "candle",
     "pin": (114.2, 22.3), "tag": ""},
]

DIGEST_HEADER = ("ALSO ON WEDNESDAY \u2014 34 MORE STORIES "
                 "FROM AROUND THE WORLD")

# Digest stories 17-50: num, region, headline, tag.
DIGEST = [
    {"num": 17, "region": "AMERICAS",
     "headline": "Trump pardons Thanksgiving turkeys "
                 "Freedom & Feathers", "tag": ""},
    {"num": 18, "region": "AMERICAS",
     "headline": "US consumer confidence 103.3, near "
                 "two-year high", "tag": ""},
    {"num": 19, "region": "AMERICAS",
     "headline": "Radar problem delays flights at "
                 "Chicago O'Hare", "tag": ""},
    {"num": 20, "region": "AMERICAS",
     "headline": "Democrats clinch House majority, largest "
                 "in decades", "tag": ""},
    {"num": 21, "region": "AMERICAS",
     "headline": "Trump gives Medal of Freedom to "
                 "Rudy Giuliani", "tag": ""},
    {"num": 22, "region": "AMERICAS",
     "headline": "Fort Hood gunman seeks stay of execution",
     "tag": ""},
    {"num": 23, "region": "AMERICAS",
     "headline": "Car bomb in Colombian city wounds "
                 "more than 20", "tag": ""},
    {"num": 24, "region": "AMERICAS",
     "headline": "Mexico inflation hits six-month high "
                 "of 3.96%", "tag": ""},
    {"num": 25, "region": "AMERICAS",
     "headline": "Troops raid home, capture Mexican "
                 "drug lord", "tag": ""},
    {"num": 26, "region": "EUROPE",
     "headline": "NATO vows defence against Russian "
                 "space threat", "tag": ""},
    {"num": 27, "region": "EUROPE",
     "headline": "Denmark court upholds 'ghetto' "
                 "evictions law", "tag": ""},
    {"num": 28, "region": "EUROPE",
     "headline": "German business morale rises to "
                 "90.6 (Ifo)", "tag": ""},
    {"num": 29, "region": "EUROPE",
     "headline": "Russian regional governor detained",
     "tag": ""},
    {"num": 30, "region": "EUROPE",
     "headline": "Pope Francis' diary: devil encounters, "
                 "faith crisis", "tag": ""},
    {"num": 31, "region": "EUROPE",
     "headline": "Cyprus races to identify the island's "
                 "missing", "tag": ""},
    {"num": 32, "region": "MIDDLE EAST",
     "headline": "Israeli strike kills Hamas security "
                 "chief in Gaza", "tag": ""},
    {"num": 33, "region": "MIDDLE EAST",
     "headline": "Land-mine casualties soar in "
                 "post-war Syria", "tag": ""},
    {"num": 34, "region": "MIDDLE EAST",
     "headline": "US envoy unsure aid to Israel ends "
                 "this year", "tag": ""},
    {"num": 35, "region": "MIDDLE EAST",
     "headline": "Iran braces for winter gas shortages",
     "tag": ""},
    {"num": 36, "region": "MIDDLE EAST",
     "headline": "Houthis push within 60 km of Aden",
     "tag": ""},
    {"num": 37, "region": "ASIA",
     "headline": "BBC Verify: AI fakes smear Taiwan "
                 "candidates", "tag": ""},
    {"num": 38, "region": "ASIA",
     "headline": "North Koreans jailed, beaten for "
                 "their faith", "tag": ""},
    {"num": 39, "region": "ASIA",
     "headline": "Hasina: I will return to Bangladesh "
                 "16 December", "tag": ""},
    {"num": 40, "region": "ASIA",
     "headline": "India pledges $1.6bn to Nepal in "
                 "reset of ties", "tag": ""},
    {"num": 41, "region": "ASIA",
     "headline": "Explosion tears through Indonesian "
                 "sneaker shop", "tag": ""},
    {"num": 42, "region": "ASIA",
     "headline": "Persib host FC Seoul in ACL Two at "
                 "GBLA tonight", "tag": ""},
    {"num": 43, "region": "AFRICA",
     "headline": "DR Congo army plane missing; rebels "
                 "claim hit", "tag": "CLAIM"},
    {"num": 44, "region": "AFRICA",
     "headline": "Nigerian monarch, 92, suspended over "
                 "assault claims", "tag": ""},
    {"num": 45, "region": "AFRICA",
     "headline": "Zimbabwean convicted in SA over Ukraine "
                 "fight plan", "tag": ""},
    {"num": 46, "region": "AFRICA",
     "headline": "Amnesty: RSF strikes killing 37 may be "
                 "war crimes", "tag": ""},
    {"num": 47, "region": "OCEANIA",
     "headline": "England beat Australia by 8 wickets, "
                 "level T20s", "tag": ""},
    {"num": 48, "region": "OCEANIA",
     "headline": "Samoa leader sorry as 2007 Nazi-salute "
                 "video emerges", "tag": ""},
    {"num": 49, "region": "OCEANIA",
     "headline": "Study resurrects 12 'lost' Barrier Reef "
                 "corals", "tag": ""},
    {"num": 50, "region": "WORLD",
     "headline": "WFP: 266 million face acute food "
                 "insecurity", "tag": ""},
]

DATE_CHECK_TITLE = ("DATE CHECK \u2014 CHECKED & LEFT OUT "
                    "(NOT 25 NOV)")
DATE_CHECK = [
    "GTA 6 released worldwide \u2014 19 Nov",
    "Nvidia reinstates CEO Jensen Huang \u2014 23 Nov",
    "Nepal PM's state visit to India \u2014 22\u201323 Nov",
    "Israeli army suicide figures released \u2014 Monday",
]
