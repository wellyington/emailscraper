from googlesearch import search
gquery = input('Search Term: ')
gtotal = 10
gurls = []
for j in search(gquery, tld="com", num=int(gtotal), stop=int(gtotal), pause=2):
    gurls.append(j)
print(gurls)
