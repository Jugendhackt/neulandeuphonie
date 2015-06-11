import json
import sys
import linecache
changes = {}
def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)
with open("tag_replace/de2.json","r") as myfile:
    changes = json.load(myfile)
print(changes)
original = "blub"
while original != "":
    original = raw_input("Original:")
    if original != "":
        replacements = []
        replacement = "blub"
        while replacement != "":
            replacement = raw_input("Replacement:")
            if replacement != "":
                replacements.append(replacement)
        changes[original] = replacements
with open("tag_replace/de2.json","w") as myfile:
    myfile.write(json.dumps(changes,indent=4))