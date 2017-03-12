def orthographicsiglength(affixlist):
    length = 0
    for affix in affixlist:
        length += len(affix)+1
    return 1 +length/7.0
#--------------------------------------------------------------------##
#		makebox
#--------------------------------------------------------------------##
def makebox(x,y,width,height,title='this title'):
    outlist = list()
    x1 = x+width
    y1 = y + height
    parameters= "[linewidth=2pt,framearc=.3,fillstyle=solid,fillcolor=yellow]"
    thisstring = "\\psframe"+parameters + "(" + str(x) + "," + str(y)+")("+str(x1)+","+str(y1)+ ")"
    outlist.append(thisstring)
    x2 = x + width/2
    y2 = y + height/2
    thisstring = "\\rput(" + str(x2) + "," + str(y2) + "){"+title+ "}"

    outlist.append(thisstring)
    return outlist

def makesigbox(x,y,width,height,sig):
    outlist = list()
    title="-".join(sig.affixlist)
    #print title
    x1 = x + width
    y1 = y + height
    parameters= "[linewidth=2pt,framearc=.3,fillstyle=solid,fillcolor=yellow]"
    thisstring = "\\psframe" + parameters + "(" + str(x) + "," + str(y) + ")(" + str(x1) + "," + str(y1)+ ")"
    outlist.append(thisstring)

    x2 = x + width/2
    y2 = y + height-.5
    thisstring = "\\rput(" + str(x2) + "," + str(y2) + "){" + "-".join(sig.affixlist) + "}"
    outlist.append(thisstring)


    x3= x2
    y3 = y2 - .5
    thisstring = "\\rput(" + str(x3) + "," + str(y3) + "){" + sig.examplestem + "}"
    outlist.append(thisstring)

    x4= x2
    y4 = y3 - .5
    thisstring = "\\rput(" + str(x4) + "," + str(y4) + "){" + str(sig.stemcount) + "}"
    outlist.append(thisstring)


    return outlist
def print_list_of_signatures(outfile, y,sig_list, hardrightmargin):
    #boxheight= 2
    output_list = list()
    currentx= 0
    currenty = y
    for signo in range(len(sig_list)):
        sig = sig_list.pop(0)
        boxwidth = orthographicsiglength(sig.affixlist)
        printlist = makesigbox(currentx,currenty,boxwidth-xmargin,boxheight,sig)
        for line in printlist:
            print >>outfile, line
        currentx += boxwidth
        if currentx > hardrightmargin:
		    break

def makepspicture_start(x,y,width,height):
    outlist = list()
    x1= x + width
    y1 = y + height
    thisstring= "\\begin{pspicture}("+str(x)+","+str(y)+")("+str(x1)+","+str(y1)+ ")"
    outlist.append(thisstring)

    outlist.append("\\psgrid")
    return outlist

def makepspicture_end():
    outlist  = list()
    thisstring="\\end{pspicture}"
    outlist.append(thisstring)
    return outlist
#--------------------------------------------------------------------##
#		class signature 
#--------------------------------------------------------------------##

class signature:
    def __init__(self, thisaffixlist, thisstemlist, stemcount, robustness, stem):
        self.affixlist = thisaffixlist
        self.stemlist = thisstemlist
        self.stemcount = stemcount
        self.robustness = robustness
        self.examplestem=stem

#--------------------------------------------------------------------##
#		Files in and out
#--------------------------------------------------------------------##
def readfile():
    folder = "/home/jagoldsm/Dropbox/data/"
    folder +=   "english/lxa/"
    infilename = folder +   "Signatures.txt"
    list_of_sigs=list()
    with open(infilename) as infile:
        signatures = infile.readlines()
        for line in signatures:

            if "==" in line:
                break
            if '=' in line:
                pieces = line.split()
                sig = pieces[0]
                sig_list = sig.split('=')
                stemcount = int(pieces[1])
                robustness = int(pieces[2])
                stem = pieces[5]
                thissig = signature(sig_list, list(), stemcount, robustness, stem)
                #print sig_list, stemcount
                list_of_sigs.append(thissig)

    return list_of_sigs
#--------------------------------------------------------------------##
#		Main program 
#--------------------------------------------------------------------##

 
infolder = ''	
outfolder = infolder
tablelines = []
datalines = []
 
 
outfilename = outfolder + "latextable.tex"


 
outfile = open (outfilename,mode='w')
#--------------------------------------------------------------------##
#		input
#--------------------------------------------------------------------##
longestitem = 1
numberofcolumns = 0
 








#--------------------------------------------------------------------##
#		output
#--------------------------------------------------------------------##
start1 = """\\documentclass{article}\n"""
start2 =  """\\usepackage{pstricks}\n"""
start3 =  """\\usepackage{geometry}\n"""
start4= """\\usepackage[letterpaper, landscape, margin=.5in]{geometry}\n"""
start5 = """\\begin{document}\n"""

start_a_1="""\\documentclass[a4paper,12pt]{article}\n"""
start_a_2="""\\usepackage{xspace,colortbl}\n"""                                          
start_a_3="""\\usepackage[screen, paneltoc]{pdfscreen}\n"""
start_a_4="""\\margins{.5in}{.5in}{.5in}{.5in}\n"""                     
start_a_5="""\\screensize{6.25in}{11in}\n""" 
start_a_6 =  """\\usepackage{pstricks}\n"""

if True:
	print >>outfile, start1
	print >>outfile, start2
	print >>outfile, start4
	print >>outfile, start5
else:
	print >>outfile, start_a_1
	print >>outfile, start_a_2
	print >>outfile, start_a_3
	print >>outfile, start_a_4
	print >>outfile, start_a_5
	print >>outfile, start_a_6

#bullet = """\\newcommand\cb{\makebox(0,0){$\\bullet$}}\n"""
header1 = """\\begin{centering}"""  
#header2 = "\\begin{pspicture}"
 
footer1 = "\\end{pspicture}\n"
footer2 = "\\end{centering}\n"
footer3 = "\\end{document}\n"

sizex= 25
sizey = 15
boxwidth = 2
boxheight= 2
xmargin  = .2

currentx=0
currenty=0
hardrightmargin = 22

readfile()
 
docstart = makepspicture_start(0,0,sizex,sizey)
for line in docstart:
    print >>outfile, line


	
list_of_sigs = readfile()
#list_of_sigs.sort(key= lambda sig: len(sig.affixlist) ) #signatures are sorted in increasing number of affixes
map_of_signatures_by_length = dict()
# first we create a dict whose keys are signature lengths, and whose values are lists of those signatures
for sig in list_of_sigs:
    siglength = len(sig.affixlist)
    if siglength not in map_of_signatures_by_length:
        map_of_signatures_by_length[siglength] = list()
    map_of_signatures_by_length[siglength].append(sig)

# Now we print each list of signatures
# we will break this up into separate pages, though
Maximum_signature_length = 10

while (True):
    Finished_flag = True
   
    for length in range(1,Maximum_signature_length):
        if length in map_of_signatures_by_length:
            lines = print_list_of_signatures(outfile, boxheight * length-4,map_of_signatures_by_length[length], hardrightmargin)
            if len(map_of_signatures_by_length[length]) > 0:
                Finished_flag = False
    print >>outfile, footer1
    if Finished_flag == True:
            break
    else:
        print >>outfile, "\n\\newpage"
        print >>outfile, "\\begin{pspicture}(10,15)"

  

lines = makepspicture_end()
for line in lines:
    print >>outfile,  line


print >>outfile, footer3







outfile.close()
