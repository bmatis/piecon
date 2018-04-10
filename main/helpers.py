def ordinal(num):
    """Returns an ordinal of a number, e.g. 'st' in 1st or 'th' in 5th"""
    if num > 9:
        secondToLastDigit = str(num)[-2]
        if secondToLastDigit == '1':
            return 'th'
    lastDigit = num % 10
    if (lastDigit == 1):
        return 'st'
    elif (lastDigit == 2):
        return 'nd'
    elif (lastDigit == 3):
        return 'rd'
    else:
        return 'th'

def get_num_with_ordinal(num):
    """Displays a int along with its ordinal, e.g. 1st, 3rd, 28th, 101st"""
    num_with_ordinal = str(num) + ordinal(num)
    return num_with_ordinal
