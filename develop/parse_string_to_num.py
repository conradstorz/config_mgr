import string

parseStr = lambda x: x.isalpha() and x or x.isdigit() and \
                        int(x) or x.isalnum() and x or \
                        len(set(string.punctuation).intersection(x)) == 1 and \
                        x.count('.') == 1 and float(x) or x


strings = ['123', '123.3', '3HC1', '12.e5', '12$5', '12.2.2']

for s in strings:
    value = parseStr(s)
    print '{} is of type {}'.format(value, type(value))