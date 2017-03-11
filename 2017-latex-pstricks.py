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
def print_list_of_signatures(y,sig_list):
    #boxheight= 2
    output_list = list()
    currentx= 0
    currenty = y
    hardrightmargin = 22
    for signo in range(len(sig_list)):
        sig = sig_list[signo]
        boxwidth = orthographicsiglength(sig.affixlist)
        printlist = makesigbox(currentx,currenty,boxwidth-xmargin,boxheight,sig)
        output_list.extend(printlist)
        currentx += boxwidth
	if currentx > hardrightmargin:
		break
    return output_list

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
header2 = "\\begin{picture}(" 
 
footer1 = "\\end{picture}\n"
footer2 = "\\end{centering}\n"
footer3 = "\\end{document}\n"

sizex= 25
sizey = 20
boxwidth = 2
boxheight= 2
xmargin = .2

currentx=0
currenty=0


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
for length in range(1,10):
    if length in map_of_signatures_by_length:
        templist = list()
        for sig in map_of_signatures_by_length[length]:
            print 196 ,sig.affixlist
            templist.append(sig)
            print 202, len(templist), sig.affixlist
        lines = print_list_of_signatures(boxheight * length-4,templist)
        print 203, lines
        for i in range(0,len(lines)):
            print 205, lines[i]
            print >>outfile,  lines[i]


lines = makepspicture_end()
for line in lines:
    print >>outfile,  line
    print 197, line


print >>outfile, footer3







outfile.close()
