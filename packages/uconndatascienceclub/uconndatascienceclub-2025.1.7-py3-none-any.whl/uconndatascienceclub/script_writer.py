import nbformat as nbf

all_scripts = dict() #nested dictionary; contains dates (key), points to 2nd dictionary (value) containing collection of scripts from that date

def write(date):
    '''Writes the scripts that were used in the given meeting date'''
    nb = all_scripts[date]['nb']

    if nb:
        for key, value in all_scripts[date]:
            pass
    
    else:
        pass

def available_dates():
    for key, value in all_scripts:
        print(key)