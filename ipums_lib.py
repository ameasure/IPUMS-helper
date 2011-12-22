from xml.dom import minidom


def row_generator(datapath, ddipath):
    ''' Maps each line of the data file to the variables and values
        it represents '''
    # get mapping
    pmap = pos_map(ddipath)
    f = open(datapath, 'r')
    for line in f.readlines():
        # apply mapping
        row = {}
        for var in pmap.keys():
            start = pmap[var]['spos']
            end = pmap[var]['epos']
            dec = pmap[var]['dec']
            if dec:
                mid = end - dec
                row[var] = line[start:mid] + '.' + line[mid:end]
            else:
                row[var] = line[start : end]
        # yield mapping
        yield row


def pos_map(ddipath):
    ''' Returns a dictionary mapping the variable names to their positions
        and decimal places in the data file '''
    m = minidom.parse(ddipath)    
    vmap = {}
    varNodes = m.getElementsByTagName('var')
    for varNode in varNodes:
        locNode = varNode.getElementsByTagName('location')[0]
        name = varNode.attributes.getNamedItem('ID').value
        vmap[name] = {
            'spos' : int(locNode.attributes.getNamedItem('StartPos').value) - 1,
            'epos' : int(locNode.attributes.getNamedItem('EndPos').value),
            'dec' : int(varNode.attributes.getNamedItem('dcml').value)
            }
    return vmap
