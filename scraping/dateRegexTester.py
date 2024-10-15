import re

# Refined pattern to capture different date formats
date_pattern = r"""(?x)                              # Enable verbose mode for better readability
(?P<relative_time>(early|mid|late))?  # Optional relative time (early, mid, late)
\s?                                # Optional space
(?P<day_start>\d{1,2})?            # Optional start day (1 or 2 digits)
\s?                                # Optional space
(?:–|-|to|and|&)?                  # Optional separator for date ranges (dash, "to", "and", or "&")
\s?                                # Optional space
(?P<day_end>\d{1,2})?              # Optional end day for date ranges
\s?                                # Optional space
(?P<month>\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\b)  # Capture the month in full or abbreviated form
\s?                                # Optional space
(?P<year>\d{4})?                   # Optional year
(?:\s*(?:-|–|—|:)\s*(?P<sentence>.*))?  # Optional separator (hyphen, en-dash, em-dash, colon) followed by the sentence
"""


if __name__ == "__main__":

    # Example sentences
    sentences = [
        "26 January: Republic Day of India",
        "26–29 January: Republic Day celebrations",
        "1 January – New Year's Day",
        "1 January: New Year’s Day",
        "Early February: Winter Olympics",
        "Early Feb — Winter Olympics",
        "Early February – Winter Olympics",
        "19 and 20 February: Event A",
        "19 & 20 February: Event B",
        "19–20 February: Event C",
        "19 to 20 February: Event D",
        "26–29 November: Thanksgiving Weekend",
        "Late May: Memorial Day",
        "Late May — Memorial Day",
        "Mid-December: Christmas preparations",
        "Mid-Dec – Christmas preparations",
        "Mid December: Holiday preparations",
        "Mid-December — Christmas preparations",
        "26–29 Nov — Thanksgiving celebrations",
        "1 January: New Year",
        "26 January – Republic Day of India",
        "26 January: Republic Day – Parade in New Delhi",
        "Mid-December — Festivities preparation",
        "Early Feb: Winter Olympics",
        "Late May: Memorial Day Celebrations",
        "Mid-Dec: Holiday Preparations",
        "1 January: Celebrating New Year’s",
        "Mid-December: Pre-Christmas activities",
        "Mid-December — Christmas Season",
        "26–29 Nov: Thanksgiving Holiday",
        "26 January — Republic Day of India",
        "19 & 20 Feb: Example Event",
        "19–20 Feb: Another Example Event",
        "19 to 20 Feb: Yet Another Event", 
        "Early-Feb Winter Olympics",
        "16 June - Janata Dal (United) quits from National Democratic Alliance led by Bharatiya Janata Party after seventeen years of association.[25]",
"20 and 21 June - Operation Amla, a terrorist-attack drill/mockup takes place in Tamil Nadu.[26]",
"Mid-June onwards: Flash floods in North India.[27]",

    ]


    for sentence in sentences:
        match = re.match(date_pattern, sentence, re.IGNORECASE)
        if match:
            print(match.groupdict())
        else:
            print(f"No match found for: {sentence}")
