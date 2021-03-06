#!python3

from __future__ import print_function

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
    itemsdict = dict()
    for d in items:
        if "NRAO_NAME" in d:
            keyword = d["NRAO_NAME"]
            if keyword in itemsdict:
                # Combine comments
                newcomment = d["JCMT_COMMENT"]
                if len(newcomment):
                    previtem = itemsdict[keyword]
                    previtem["JCMT_COMMENT"].add(newcomment)
            else:
                comment = d["JCMT_COMMENT"]
                d["JCMT_COMMENT"] = set()
                if len(comment):
                    d["JCMT_COMMENT"].add(comment)
                itemsdict[keyword] = d

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

def make_item_table(jcmtonly, jcmtitems, ncols=2, caption="A caption", label=None):
    # Table for JCMT only keywords.
    table = "table"
    if ncols > 1:
        table = "table*"
    print("\\begin{"+table+"}[t]")
    print("\\caption{{{}}}".format(caption))
    if label is not None:
        print("\\label{"+label+"}")
    print("\\begin{center}")
    if ncols == 1:
        print("\\begin{tabular}{lp{2.5in}}")
    elif ncols == 2:
        print("\\begin{tabular}{|lp{2.0in}|lp{2.0in}|}")
    elif ncols == 3:
        print("\\begin{tabular}{|lp{1.5in}|lp{1.5in}|lp{1.5in}|}")
    else:
        raise ValueError("Can not support {} columns.".format(ncols))
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
                commstr = " \\emph{or} ".join(info["JCMT_COMMENT"])
                thisrow += ["\\textbf{"+item+"}", commstr.replace("&","\\&")]
        rowstr = " & ".join(thisrow) + "\\\\"
        print(rowstr.replace("_", "\\_"))

    print("\\hline")
    print("\\end{tabular}")
    print("\\end{center}")
    print("\\end{"+table+"}")


# Program starts here
jcmtnames, jcmtitems = read_jcmt()
nraonames, nraoitems = read_nrao()

nraoonlydict = nraoitems
jcmtonly = []
shared = []

PRINTINFO = False

for i in jcmtnames:
    if i in nraoitems:
        if PRINTINFO:
            print("Item match: {}".format(i))
        del nraoonlydict[i]
        shared.append(i)
    else:
        if PRINTINFO:
            print("JCMT: {}".format(i))
        jcmtonly.append(i)

# Store sorted list of items for NRAO
nraoonly = []
for k in sorted(nraoonlydict.keys(), key=sortbyclassnum):
    if PRINTINFO:
        print("NRAO: {}".format(k))
    nraoonly.append(k)

make_item_table(jcmtonly[0:56], jcmtitems, label="tab:appa1",
                caption="JCMT-specific keywords from class 1 to class 4. This includes the three items that were not allocated a class.")
make_item_table(jcmtonly[57:112], jcmtitems, label="tab:appa2",
                caption="JCMT-specific keywords from class 4 to class 7.")
make_item_table(jcmtonly[112:], jcmtitems, label="tab:appa3",
                caption="JCMT-specific keywords from class 7 to class 14. Class 55 is not included here as that data was not archived.")
make_item_table( nraoonly, nraoitems, ncols=1, label="tab:noaoonly",
                 caption="Items of the GSDD model only defined for use at NRAO.")
