#!python3

"""
Read JCMT and NRAO standard specification.
Compare them.

JCMT
----

Translate a JCMT storage task include file to a latex table

Include file is of form:

*
      DATA NRAO_NAME   (  1)/'C1TEL          '/
      DATA JCMT_NAME   (  1)/'TEL_NAME       '/
      DATA JCMT_COMMENT(  1)/'Telescope name                                                                  '/
      DATA FITS_TYPE   (  1)/'GENERAL '/
      DATA FITS_NAME   (  1)/'TELESCOP'/


Resulting in a dict keyed by NRAO name.

"""
import re
import math

# First read the file creating an array whose elements
# are a dict with keys NRAO_NAME, JCMT_NAME, FITS_NAME, JCMT_COMMENT, FITS_TYPE.


def read_jcmt(file="support_docs/jcmt_storage_translate_full.inc"):
    """
    Read a JCMT storage task include file and return a list
    of sorted names pointing to dict entries, and a dict
    indexed by item name.

    names, items = read_jcmt()
    """

    data_re = re.compile(r"DATA ([A-Z_]*)\s*\((\s*\d+)\)/'(.*)'/")

    items = []
    items.append( {} )

    for line in open(file):
        match_data = data_re.search(line)
        if match_data is not None:
            keyword = match_data.group(1)
            index = match_data.group(2)
            index = int(index)
            value = match_data.group(3)
            value = value.strip()
            if keyword.endswith("_NAME"):
                value = value.upper()
            try:
                this = items[index]
            except IndexError:
                items.append(dict({}))
            #value = value.replace("_","\\_")
            #value = value.replace("&","\\&")
            items[index][keyword] = value

    return list_to_dict(items)

def list_to_dict(items):
    # Convert the list to a dict so that we can order the
    # output by NRAO_NAME
    itemsdict = dict({})
    for d in items:
        if "NRAO_NAME" in d:
            itemsdict[d["NRAO_NAME"]] = d

    # but we have to be careful about C13xxx being higher than C1xxx
    names = sorted( itemsdict.keys(), key=sortbyclassnum )

    return (names, itemsdict)

def sortbyclassnum(t):
    number_re = re.compile(r"C(\d+)[A-Z]")
    sortval = 0
    match = number_re.search(t)
    if match is not None:
        sortval = int(match.group(1))
    return (sortval, t)


def read_nrao(file="support_docs/nrao-names.txt"):
    need_names = True
    unassigned = []
    items = []
    for line in open(file):
        line = line.strip()
        if len(line) == 0:
            continue
        if need_names:
            unassigned = line.split(" ")
            need_names = False
        else:
            items.append({ "NRAO_NAME": unassigned.pop(0),
                            "JCMT_COMMENT": line})
            if not len(unassigned):
                need_names = True
    return list_to_dict(items)

def make_item_table(jcmtonly, jcmtitems, ncols=2, caption="A caption"):
    # Table for JCMT only keywords.
    print("\\begin{table*}[t]")
    print("\\caption{{{}}}".format(caption))
    if ncols == 2:
        print("\\begin{tabular}{|lp{2.0in}|lp{2.0in}|}")
    else:
        print("\\begin{tabular}{|lp{1.5in}|lp{1.5in}|lp{1.5in}|}")
    print("\\hline")

    nitems = len(jcmtonly)
    nrows = int(math.ceil(nitems / ncols))

    for r in range(nrows):
        thisrow = []
        for c in range(ncols):
            idx = r + (c * nrows)
            if idx > nitems:
                thisrow += [" ", " "]
            else:
                item = jcmtonly[idx]
                info = jcmtitems[item]
                thisrow += [item, info["JCMT_COMMENT"].replace("&","\\&")]
        rowstr = " & ".join(thisrow) + "\\\\"
        print(rowstr.replace("_", "\\_"))

    print("\\hline")
    print("\\end{tabular}")
    print("\\end{table*}")


# Program starts here
jcmtnames, jcmtitems = read_jcmt()
nraonames, nraoitems = read_nrao()

nraoonly = nraoitems
jcmtonly = []

PRINTINFO = False

for i in jcmtnames:
    if i in nraoitems:
        if PRINTINFO:
            print("Item match: {}".format(i))
        del nraoonly[i]
    else:
        if PRINTINFO:
            print("JCMT: {}".format(i))
        jcmtonly.append(i)

if PRINTINFO:
    for k in sorted(nraoonly.keys(), key=sortbyclassnum):
        print("NRAO: {}".format(k))

make_item_table( jcmtonly[0:56], jcmtitems)
make_item_table( jcmtonly[57:112], jcmtitems)
make_item_table( jcmtonly[112:], jcmtitems)
