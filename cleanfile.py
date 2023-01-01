filename = input('File: ')
word = input('What are we looking for: ')
toDelete = []

with open(r'./' + filename, 'r') as fp:
    for l_no, line in enumerate(fp):
        # search string
        if word in line:
            print('string found in a file')
            print('Line Number:', l_no)
            print('Line:', line)
            toDelete.append(l_no)
    for tdl in toDelete:
        with open(filename) as file:
            dLines = file.readlines()
            try:
                del dLines[tdl]
            except:
                continue
        with open(filename, 'w') as file:
            for lineF in dLines:
                file.write(lineF)
        toDelete.remove(tld)
print(toDelete)