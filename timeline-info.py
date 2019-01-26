#!/usr/bin/env python
#
# This script is called by timeline-info.gp -- the two scripts
# are quite tightly linked as (hopefully) indicated in the
# comments
#
from __future__ import division
from __future__ import print_function
from builtins import object
from past.utils import old_div
import re
import cmath

papers = []

#----------------------------------------------------------------------
def main():

    colours = get_colours()
    
    read_papers()
    uniq_papers = {}
    i = 0;
    # get unique list of papers
    for paper in papers:
        if (paper.arxiv in uniq_papers):
            uniq_papers[paper.arxiv].process += ", "+paper.process
        else:
            uniq_papers[paper.arxiv] = paper

    # now transfer them into an array
    sorted_papers=[]
    for arxiv in uniq_papers:        
        sorted_papers.append(uniq_papers[arxiv])

    lab=open("timeline-info.labels","w")
    pts=open("timeline-info.points","w")
    # sort and print them out
    pi = cmath.pi
    sorted_papers.sort(key = lambda paper: paper.date())
    for paper in sorted_papers:
        p    = paper.date() + 1j*(1.55-i*0.01)

        phi  = old_div(pi,2)-i*pi*0.8/(len(sorted_papers))
        dir=cmath.rect(1,phi)
        dir = dir.real*13 + 1j*dir.imag
        
        arr1 = p    + 0.008 * dir
        if   (i < 11): length = 0.5-0.04*(i%11)
        elif (i < 24): length = 0.7-0.02*(i-11)
        else         : length = 0.7-0.02*(24-11) + 0.01*(i-24)
        arr2 = arr1 + length*dir
        #print phi, arr1, arr2
        print(p.real, p.imag, i, paper.process, ";", paper.short_author(), file=pts)
        print("set arrow {} from {},{} to {},{} nohead lc rgb {}".format(i+1,arr1.real,arr1.imag,arr2.real,arr2.imag,colours[i%len(colours)]), file=lab)
        print("set label {} '{},{}' at {},{} ".format(i+101,paper.short_process(),
                                                             paper.short_author(),arr2.real+0.05,arr2.imag), file=lab)
        i += 1

#----------------------------------------------------------------------
def get_colours():
    """Extract the colours used for the palette in the gnuplot file.
    This is not super robust. We will assume that the number of colours
    that we find here is also the number we must use in the modulo operation? 
    """

    with open("timeline-info.gp") as f:
        for line in f:
            #print line
            #search = re.search(r"^ *set palette model.*\(( *[0-9.]+ *'[^']+' *)+ *\)",line)

            # first find what is in the brackets
            search = re.search(r"^ *set palette model.*\((.*)\)",line)
            if (search):
                # then extract the colours, assuming the index
                # goes in increments of 1, starting at 0
                result = []
                for g in search.group(1).split(','):
                    colour = re.sub(r'''^[^'"]+''', '', g)
                    result.append(colour)
                return result
                
    
        
#----------------------------------------------------------------------    
class Paper(object):
    def __init__(self,authors,arxiv,process):
        self.authors = authors
        self.arxiv   = arxiv
        self.process = process

    def date(self):
        year  = int(self.arxiv[:2])
        month = int(self.arxiv[2:4])
        if (year > 80): year += 1900
        else          : year += 2000
        return year + old_div((month-0.5),12.0)
        
    def short_author(self):
        if (self.authors.count(",") <= 2):
            short = re.sub(r' and ',', ',self.authors)
        else:
            short = re.sub(r',.*','',self.authors)
            short += " et al."

        short = re.sub(r'[A-Z]\. ','',short)
        return short

    def short_process(self):
        short = self.process
        short = re.sub(r'differential','diff.',short)
        short = re.sub(r'gamma','{/Symbol g}',short)
        short = re.sub(r'@[0-9]+','',short)
        return short
    
#----------------------------------------------------------------------    
def read_papers():
    with open("nnlo-refs-2017-04.tex") as f:
        lines = f.readlines()

    process=""
    just_found_bibitem = False
    for line in lines:
        #print line,;

        # identify process information
        m = re.match(r'%%---+ (.*)',line)
        if (m): process= m.group(1)

        # identify the authors
        if (just_found_bibitem):
            authors = line.replace("~"," ").rstrip()
            authors = authors.rstrip(",")
            #print authors

        # identify the arxiv
        m = re.search(r'(arXiv:|hep-ph\/)([0-9.]+)',line)
        if (m):
            #print m.group(1)
            new_paper = Paper(authors, m.group(2), process)
            papers.append(new_paper)
            #print new_paper.date()

        # identify the bibitem (should come last)
        m = re.match(r'^\\bibitem\{([^}]+)',line)
        if (m):
            just_found_bibitem = True
            bibitem = m.group(1)
        else  :
            just_found_bibitem = False

        #print m.group(1) #process= m.group(1)
    
main()
    
