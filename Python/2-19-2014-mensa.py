
orig = ['ARTWORK','KJBZOK','NVKKWYK','FBJB','OBJTERK','BQJVUABOEK','TVNNRR ZQUK','XBKRXBYY TBAFK']
trans = {'J':'T',
         'F':'D',
         'B':'A',
         'K':'S',
         'Z':'M',
         'O':'P',
         'T':'C',
         'E':'H',
         'R':'E',
         'A':'R',
         'W':'I',
         'Q':'U',
         'V':'O',
         'U':'G',
         'N':'F',
         'Y':'L',
         'X':'B'}

def transform(orig_list, transform_dict):
    for phrase in orig_list:
        for letter in phrase:
            try:
                print(transform_dict[letter],end='')
            except KeyError:
                print(letter, end='')
        print('')

transform(orig,trans)
