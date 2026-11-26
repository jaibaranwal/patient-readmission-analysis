"""US state-to-region mapping for descriptive synthetic-data grouping."""
STATE_TO_REGION = {}
for state in ["CT","ME","MA","NH","RI","VT","NJ","NY","PA"]:
    STATE_TO_REGION[state] = "Northeast"
for state in ["IL","IN","MI","OH","WI","IA","KS","MN","MO","NE","ND","SD"]:
    STATE_TO_REGION[state] = "Midwest"
for state in ["DE","FL","GA","MD","NC","SC","VA","DC","WV","AL","KY","MS","TN","AR","LA","OK","TX"]:
    STATE_TO_REGION[state] = "South"
for state in ["AZ","CO","ID","MT","NV","NM","UT","WY","AK","CA","HI","OR","WA"]:
    STATE_TO_REGION[state] = "West"

def normalize_state(value):
    if value is None:
        return "Unknown"
    text = str(value).strip()
    if not text or text.lower() in {"nan","none","unknown","?"}:
        return "Unknown"
    return text.upper() if len(text) <= 3 else "Unknown"

def region_for_state(value):
    return STATE_TO_REGION.get(normalize_state(value), "Unknown")
