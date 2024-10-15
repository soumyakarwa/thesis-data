import re 
import dateRegexTester
from datetime import datetime
from fuzzywuzzy import process

month_days = {
    'january': 31, 'february': 28, 'march': 31, 'april': 30,
    'may': 31, 'june': 30, 'july': 31, 'august': 31,
    'september': 30, 'october': 31, 'november': 30, 'december': 31
}
month_abbreviations = {
    'jan': 'January', 'feb': 'February', 'mar': 'March', 'apr': 'April',
    'may': 'May', 'jun': 'June', 'jul': 'July', 'aug': 'August',
    'sep': 'September', 'sept': 'September', 'oct': 'October', 'nov': 'November',
    'dec': 'December'
}
FUZZY_THRESHOLD = 80

def correct_month(month):
    # First, check for exact match in abbreviations
    month = month.lower()
    if month in month_abbreviations:
        return month_abbreviations[month]

    # If no exact match, use fuzzy matching to find the closest month
    potential_matches = process.extractOne(month, list(month_abbreviations.keys()), score_cutoff=FUZZY_THRESHOLD)
    if potential_matches:
        best_match = potential_matches[0]
        return month_abbreviations[best_match]

def splitSentence(sentence):
    # Updated regex to match patterns like "1 January", "26–29 Nov", "early Feb", "late May", "mid-Dec", etc.
    # date_pattern = r"((\d{1,2})(–|-|:)?(\d{1,2})?\s(\w+)|(early|late|mid)(-)?\s\w+|\d{1,2}\s\w+)\s*–\s*(.*)"
    
    match = re.match(dateRegexTester.date_pattern, sentence, re.IGNORECASE)
    # print(sentence)
    if match:
        # Safely access the groups based on the existing structure of your pattern
        # Extract the date part (the combined information from named groups)
        relative_time = match.group('relative_time')  # 'early', 'mid', 'late'
        day_start = match.group('day_start')  # Start day, if available
        day_end = match.group('day_end')  # End day, if available
        month = match.group('month')  # Month (e.g., January, Feb)
        year = match.group('year')  # Year (if available)
        
        # Construct the date part based on what is available
        date_part = ''
        if relative_time:
            date_part += relative_time.capitalize() + ' '
        if day_start:
            date_part += day_start
            if day_end:
                date_part += '–' + day_end  # Add day range if available
        if month:
            date_part += ' ' + month.capitalize()
        if year:
            date_part += ' ' + year
        
        # Extract the content part after the date
        content_part = match.group('sentence') if match.group('sentence') else sentence  # Fallback to original sentence
        if date_part and content_part:
            return date_part.strip(), content_part.strip()
        elif date_part and not content_part:
            return date_part.strip(), sentence
        elif not date_part and content_part:
            return None, content_part.strip()
    else:
        return None, sentence

def extractDayMonth(date_part):
    # Convert the date_part to lowercase for easier matching
    date_part = date_part.lower()

    # Handle cases like "26–29 November" or "26–29 Nov"
    range_match = re.search(r"(\d{1,2})(–|-)?(\d{1,2})?\s(\w+)", date_part)
    if range_match:
        start_day = range_match.group(1)
        end_day = range_match.group(3)  # This is optional, could be None
        month = range_match.group(4)  # Extract the month

        # Correct any typos or abbreviations in the month
        corrected_month = correct_month(month)
        if corrected_month is None:
            return None, None  # Invalid month or typo that can't be corrected

        # Validate the day against the full corrected month name
        if corrected_month.lower() in month_days:
            max_day = month_days[corrected_month.lower()]
            
            # Validate the day range (start_day and end_day)
            if int(start_day) > max_day or (end_day and int(end_day) > max_day):
                return None, corrected_month  # Invalid day, set day as None
            else:
                # Return the valid day or range
                if end_day:
                    return f"{start_day}–{end_day}", corrected_month
                else:
                    return start_day, corrected_month
        else:
            return None, corrected_month

    # Handle special cases for "early", "mid", "late" before months
    if 'early' in date_part or 'late' in date_part or 'mid' in date_part:
        # Extract the month name (allowing for optional hyphen)
        month_name = re.search(r"(early|mid|late)(-)?\s+(\w+)", date_part, re.IGNORECASE)
        if month_name:
            relative_time = month_name.group(1).capitalize()  # "Early", "Mid", "Late"
            month = month_name.group(3).capitalize()  # e.g., "December"
            
            # Correct the month
            corrected_month = correct_month(month)
            if corrected_month is None:
                return None, None  # Invalid month or typo that can't be corrected

            return relative_time, corrected_month
    
    # Handle cases like "1 January" or "1 Jan"
    else:
        try:
            # Check for full or abbreviated month using datetime.strptime
            parsed_date = datetime.strptime(date_part.capitalize(), "%d %b")  # Handle abbreviated months as well
            day = parsed_date.day
            month = parsed_date.strftime("%B")  # Full month name
            return day, month
        except ValueError:
            try:
                parsed_date = datetime.strptime(date_part.capitalize(), "%d %B")  # Handle full month names
                day = parsed_date.day
                month = parsed_date.strftime("%B")  # Full month name
                return day, month
            except ValueError:
                return None, None
    # single_match = re.search(r"(\d{1,2})?\s*(\w+)", date_part)
    # print(single_match)
    # if single_match:
    #     day = single_match.group(1)  # This is the day (e.g., "1")
    #     month = single_match.group(2)  # This could be None

    #     if month:
    #         corrected_month = correct_month(month)
    #         if corrected_month:
    #             # Validate the day
    #             if corrected_month.lower() in month_days:
    #                 max_day = month_days[corrected_month.lower()]
    #                 if int(day) <= max_day:
    #                     return day, corrected_month
    #                 else:
    #                     return None, corrected_month
    #             else:
    #                 return None, corrected_month
    #     else:
    #         # If no month, return day and None for the month
    #         return day, "unknown"

    # If no valid day or month is found
    return None, None

# Function to create the initial JSON structure for a given year and month
def create_yearly_structure(year):
    return {
        year: {
            "january": [],
            "february": [],
            "march": [],
            "april": [],
            "may": [],
            "june": [],
            "july": [],
            "august": [],
            "september": [],
            "october": [],
            "november": [],
            "december": [],
            "unknown": [],
        }
    }

# Function to add a month dynamically to an existing year
def addEvent(dataset, year, event):
    # if year not in eventsData.year:
    #     eventsData.update(create_yearly_structure(year))
    
    datePart, titlePart = splitSentence(event)
    if datePart:
        date, month = extractDayMonth(datePart)
    
        if not date:
            date = None
        if not month:
            month = "unknown"

        dataset[year][month.lower()].append({
            "title": titlePart,
            "date": date,
            "location": None,
            "theHindu": None,
            "timesOfIndia": None,
            "theIndianExpress": None,
            "theHindustanTimes": None,
        })

    
    