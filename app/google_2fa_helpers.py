import string

def parse_add_button_text(text: string):
    SECRETS = {}
    try:
        lines = text.split("\n")
        br = 0
        for i, line in enumerate(lines):
            SECRETS[lines[br].strip()] = lines[br+1].strip()
            br = br+2
    except Exception as e:
        pass
    return SECRETS

