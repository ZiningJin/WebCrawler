import re
import pandas as pd
# --------- BCI Util Functions ---------
def bci_util_concat(row):
    return pd.Series({
        'Owner Enterprise': ';'.join(row['Owner Enterprise'].map(str).unique())
    })

def bci_util_lastname(x):
    pat1 = 'Mr(.*?)\xa0'
    pat2 = 'Ms(.*?)\xa0'
    pat3 = 'Dr(.*?)\xa0'
    pat4 = 'Engr(.*?)\xa0'
    pat5 = 'Ar(.*?)\xa0'
    if re.findall(pat1, x) != []:
        return 'Mr'+re.findall(pat1, x)[0]
    elif (re.findall(pat1, x) == []) & (re.findall(pat2, x) != []):
        return 'Ms'+re.findall(pat2, x)[0]
    elif (re.findall(pat1, x) == []) & (re.findall(pat2, x) == []) & (re.findall(pat3, x) != []):
        return 'Dr'+re.findall(pat3, x)[0]
    elif (re.findall(pat1, x) == []) & (re.findall(pat2, x) == []) & (re.findall(pat3, x) == []) & (re.findall(pat4, x) != []):
        return 'Engr'+re.findall(pat4, x)[0]
    elif (re.findall(pat1, x) == []) & (re.findall(pat2, x) == []) & (re.findall(pat3, x) == []) & (re.findall(pat4, x) == []) & (re.findall(pat5, x) != []):
        return 'Ar'+re.findall(pat5, x)[0]
    else:
        return None

def bci_util_phone(x):
    pat1 = 'Phone(.*?)Fax'
    if re.findall(pat1, x) != []:
        temp = re.findall(pat1, x)[0]
        temp = temp.strip(':')
        temp = temp.lstrip() 
        temp = temp.rstrip() 
        if '/' in temp:
            temp = temp.split('/')[0]
            temp = temp.rstrip() 
            return temp
        elif ',' in temp:
            temp = temp.split(',')[0]
            temp = temp.rstrip()
            return temp
        else:
            return temp
    else:
        return None

def bci_util_email(x):
    pat1 = 'Email(.*?)\)'
    if re.findall(pat1, x) != []:
        temp = re.findall(pat1, x)[0]
        temp = temp.strip(':')
        temp = temp.strip()
        return temp
    else:
        return None

def bci_util_company(x):
    pat1 = '(.*?),'
    if re.findall(pat1, x) != []:
        temp = re.findall(pat1, x)[0]
        if ':' in temp:
            temp = temp.split(':')[1]
            temp = temp.lstrip() 
            temp = temp.rstrip() 
            return temp
        else:
            return temp

    else:
        return None
