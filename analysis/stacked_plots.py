from __future__ import division,print_function
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

import os
import sys,getopt

plt.ion()

genlabels = ('Male','Female','Non-conforming')

def getfrac(m,f,n=0):
    return m/(f+m+n)

def load_data(conference):

    q = pd.read_csv('../data/%s/data.csv' % conference,names=['date','session','speaker','chair','questions'],header=None)
    # Treat missing data
    q.fillna('X', inplace=True)
    
    # Speakers
    vc_speakers = q['speaker'].value_counts().loc[['M','F','N']]
    
    # Chairs
    vc_chairs = q['chair'].value_counts().loc[['M','F','N']]
    
    # Questioners
    qa=list(q['questions'])
    vc_questioners = pd.value_counts(list(''.join(qa))).loc[['M','F','N']]
    
    # First question
    first = [x[1]['questions'][0] for x in q.iterrows()]
    vc_firstquestion = pd.value_counts(first).loc[['M','F','N']]
    
    # Load into a single dataframe
    data = [vc_speakers,vc_chairs,vc_questioners,vc_firstquestion][::-1]

    return q,data

def make_plots(q,data,conference):

    gencolors =('purple','lightgreen','darkorange')
    plotdir = "./plots"
    if not os.path.exists(plotdir):
        os.makedirs(plotdir)

    print("\nAnalyzing data for %s\n" % conference)

    # Figure 1
    # Plot stacked bar chart
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    normdata = [x/x.sum() for x in data]
    labels = ['Speakers','Chairs','Questioners','First question'][::-1]
    df = pd.DataFrame(normdata,index=labels)
    dfplot = df.plot(kind='barh',stacked=True,ax=ax1,color=gencolors,legend=False)
    
    # Find data positions of the plots
    patches = dfplot.patches
    yc = [p.get_y() for p in patches]
    yc = yc[:int(len(yc)/2)]
    height = p.get_height()
    
    ylims1 = ax1.get_ylim()
    ax1.vlines(0.5,ylims1[0],ylims1[1],color='k',linestyle='-')
    
    # IAU individual members - note no data on non-binary (M/F) gender types
    # http://www.iau.org/administration/membership/individual/distribution/
    iau_frac = getfrac(9546,1803,0)
    ax1.vlines(iau_frac,ylims1[0],yc[-1]+height,color='b',linestyle='--')
    ax1.text(iau_frac*1.02,yc[-1]+0.98*height,'IAU',ha='center',va='bottom',color='b')
    p,l = ax1.get_legend_handles_labels()
    ax1.legend(p,l,loc='upper left')

    ax1.set_xlabel('Fraction')
    ax1.set_title(conference,fontsize=12)
    
    fig1.tight_layout()
    fig1.savefig('%s/%s_demographics.pdf' % (plotdir,conference), dpi=200)
    
    # Figure 2
    # How many questions were there per talk? Did the gender of the speaker affect it?
    fig2 = plt.figure()
    ax4 = fig2.add_subplot(121)
    qpt = [len(x) for x in q['questions']]
    ax4.hist(qpt,bins=range(0,8),histtype='step',range=(0,8),linewidth=3, color='k')
    ylims4 = ax4.get_ylim()
    ax4.vlines(np.mean(qpt),ylims4[0],ylims4[1],linestyle='--',color='k')

    ax4.set_xlabel('Questions per talk')
    ax4.set_ylabel('Count')
    ax4.set_title(conference,fontsize=12)
    
    ax5 = fig2.add_subplot(122)

    question_list = []
    for gender in ('M','F','N'):
        question_list.append([len(x[1]['questions']) for x in q.iterrows() if x[1]['speaker'] == gender])

    for ql,label,gcolor in zip(question_list,genlabels,gencolors):
        if len(ql) > 0:
            ax5.hist(ql,bins=range(0,8),histtype='step',range=(0,8),linewidth=3, color=gcolor,label='%s speaker' % label)
            ax5.vlines(np.mean(ql),ylims4[0],ylims4[1],linestyle='--',color=gcolor)

    ax5.set_ylim(ylims4)
    ax5.legend(loc='upper right')

    ax5.set_xlabel('Questions per talk')
    ax5.set_ylabel('Count')
    
    fig2.tight_layout()
    fig2.savefig('%s/%s_histogram_questions.pdf' % (plotdir,conference), dpi=200)
    
    # Who asks questions?
    fig3 = plt.figure()
    
    # When M/F/N speaker, who asks questions?
    
    malespeaker_maleafter = ['M'*x[1]['questions'].count('M') for x in q.iterrows() if x[1]['speaker'] == 'M']
    malespeaker_femaleafter = ['F'*x[1]['questions'].count('F') for x in q.iterrows() if x[1]['speaker'] == 'M']
    malespeaker_noncomafter = ['N'*x[1]['questions'].count('N') for x in q.iterrows() if x[1]['speaker'] == 'M']
    femalespeaker_maleafter = ['M'*x[1]['questions'].count('M') for x in q.iterrows() if x[1]['speaker'] == 'F']
    femalespeaker_femaleafter = ["F"*x[1]['questions'].count('F') for x in q.iterrows() if x[1]['speaker'] == 'F']
    femalespeaker_noncomafter = ['N'*x[1]['questions'].count('N') for x in q.iterrows() if x[1]['speaker'] == 'F']
    noncomspeaker_maleafter = ['M'*x[1]['questions'].count('M') for x in q.iterrows() if x[1]['speaker'] == 'N']
    noncomspeaker_femaleafter = ["F"*x[1]['questions'].count('F') for x in q.iterrows() if x[1]['speaker'] == 'N']
    noncomspeaker_noncomafter = ['N'*x[1]['questions'].count('N') for x in q.iterrows() if x[1]['speaker'] == 'N']
    vc_malespeaker = pd.value_counts(list(''.join(malespeaker_maleafter+malespeaker_femaleafter+malespeaker_noncomafter)))
    vc_femalespeaker = pd.value_counts(list(''.join(femalespeaker_maleafter+femalespeaker_femaleafter+femalespeaker_noncomafter)))
    vc_noncomspeaker = pd.value_counts(list(''.join(noncomspeaker_maleafter+noncomspeaker_femaleafter+noncomspeaker_noncomafter)))
    
    # Load everything into a single dataframe
    
    speakerdata = [vc_malespeaker,vc_femalespeaker,vc_noncomspeaker]
    speakerlabels = ['Male speaker','Female speaker','Non-conforming speaker']
    speakernormdata = [x/x.sum() for x in speakerdata]
    df = pd.DataFrame(speakernormdata,index=speakerlabels)
    print("Questions based on gender of speakers")
    print(df)
    
    # Plot stacked bar chart
    ax8 = fig3.add_subplot(311)
    df.plot(kind='barh',stacked=True,ax=ax8,color=gencolors,legend=False)
    ylims8 = ax8.get_ylim()
    ax8.vlines(0.5,ylims8[0],ylims8[1],color='k',linestyle='-')
    p,l = ax8.get_legend_handles_labels()
    ax8.legend(p,l,loc='upper left')
    ax8.set_xlabel('Fraction of total questions')
    ax8.set_title(conference,fontsize=12)
    
    # Does the gender of the session chair affect the distribution of the questioners gender?
    
    malechair_maleafter = ['M'*x[1]['questions'].count('M') for x in q.iterrows() if x[1]['chair'] == 'M']
    malechair_femaleafter = ['F'*x[1]['questions'].count('F') for x in q.iterrows() if x[1]['chair'] == 'M']
    malechair_noncomafter = ['N'*x[1]['questions'].count('N') for x in q.iterrows() if x[1]['chair'] == 'M']
    femalechair_maleafter = ['M'*x[1]['questions'].count('M') for x in q.iterrows() if x[1]['chair'] == 'F']
    femalechair_femaleafter = ["F"*x[1]['questions'].count('F') for x in q.iterrows() if x[1]['chair'] == 'F']
    femalechair_noncomafter = ['N'*x[1]['questions'].count('N') for x in q.iterrows() if x[1]['chair'] == 'F']
    noncomchair_maleafter = ['M'*x[1]['questions'].count('M') for x in q.iterrows() if x[1]['chair'] == 'N']
    noncomchair_femaleafter = ["F"*x[1]['questions'].count('F') for x in q.iterrows() if x[1]['chair'] == 'N']
    noncomchair_noncomafter = ['N'*x[1]['questions'].count('N') for x in q.iterrows() if x[1]['chair'] == 'N']
    vc_malechair = pd.value_counts(list(''.join(malechair_maleafter+malechair_femaleafter+malechair_noncomafter)))
    vc_femalechair = pd.value_counts(list(''.join(femalechair_maleafter+femalechair_femaleafter+femalechair_noncomafter)))
    vc_noncomchair = pd.value_counts(list(''.join(noncomchair_maleafter+noncomchair_femaleafter+noncomchair_noncomafter)))
    
    # Load everything into a single dataframe
    
    chairdata = [vc_malechair,vc_femalechair,vc_noncomchair]
    chairlabels = ['Male chair','Female chair','Non-conforming chair']
    chairnormdata = [x/x.sum() for x in chairdata]
    df = pd.DataFrame(chairnormdata,index=chairlabels)
    print("Questions based on gender of chairs")
    print(df)
    
    # Plot stacked bar chart
    ax9 = fig3.add_subplot(312)
    df.plot(kind='barh',stacked=True,ax=ax9,color=gencolors,legend=False)
    ylims9 = ax9.get_ylim()
    ax9.vlines(0.5,ylims9[0],ylims9[1],color='k',linestyle='-')
    ax9.set_xlabel('Fraction of total questions')
    
    # Does gender of the first question affect the subsequent questions?
    
    malefirst_maleafter = ['M'*x[1]['questions'][1:].count('M') for x in q.iterrows() if x[1]['questions'][0] == 'M']
    malefirst_femaleafter = ['F'*x[1]['questions'][1:].count('F') for x in q.iterrows() if x[1]['questions'][0] == 'M']
    malefirst_noncomafter = ['N'*x[1]['questions'][1:].count('N') for x in q.iterrows() if x[1]['questions'][0] == 'M']
    vc_malefirst_remaining = pd.value_counts(list(''.join(malefirst_maleafter+malefirst_femaleafter+malefirst_noncomafter)))
    
    femalefirst_maleafter = ['M'*x[1]['questions'][1:].count('M') for x in q.iterrows() if x[1]['questions'][0] == 'F']
    femalefirst_femaleafter = ["F"*x[1]['questions'][1:].count('F') for x in q.iterrows() if x[1]['questions'][0] == 'F']
    femalefirst_noncomafter = ['N'*x[1]['questions'][1:].count('N') for x in q.iterrows() if x[1]['questions'][0] == 'F']
    vc_femalefirst_remaining = pd.value_counts(list(''.join(femalefirst_maleafter+femalefirst_femaleafter+femalefirst_noncomafter)))
    
    noncomfirst_maleafter = ['M'*x[1]['questions'][1:].count('M') for x in q.iterrows() if x[1]['questions'][0] == 'N']
    noncomfirst_femaleafter = ["F"*x[1]['questions'][1:].count('F') for x in q.iterrows() if x[1]['questions'][0] == 'N']
    noncomfirst_noncomafter = ['N'*x[1]['questions'][1:].count('N') for x in q.iterrows() if x[1]['questions'][0] == 'N']
    vc_noncomfirst_remaining = pd.value_counts(list(''.join(noncomfirst_maleafter+noncomfirst_femaleafter+noncomfirst_noncomafter)))
    
    # Load everything into a single dataframe
    firstrdata = [vc_malefirst_remaining,vc_femalefirst_remaining,vc_noncomfirst_remaining]
    firstrlabels = ['Male asks question 1','Female asks question 1','Non-conforming asks question 1']
    firstrnormdata = [x/x.sum() for x in firstrdata]
    dfr = pd.DataFrame(firstrnormdata,index=firstrlabels)
    print("Questions based on gender of person asking the first question")
    print(dfr)
    
    ax7 = fig3.add_subplot(313)
    dfr.plot(kind='barh',stacked=True,ax=ax7,color=gencolors,legend=False)
    ylims7 = ax7.get_ylim()
    ax7.vlines(0.5,ylims7[0],ylims7[1],color='k',linestyle='-')
    ax7.set_xlabel('Fraction of remaining questions')
    
    fig3.tight_layout()
    fig3.savefig('%s/%s_mf_effects.pdf' % (plotdir,conference), dpi=200)

def usage():

    print("Usage: python stacked_plots.py -c <conference>")

    w = os.walk("../data")
    clist = [x[0].split('/')[-1] for x in w][1:]
    print("\nConferences with data:")
    for c in clist:
        print("\t%s" % c)

def main(argv):

    conference = "aas225"

    try:
        opts,args = getopt.getopt(argv,"hc:d", ["help","conference="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt,arg in opts:
        if opt in ("-h","--help"):
            usage()
            sys.exit()
        elif opt == "-d":
            global _debug
            _debug = 1
        elif opt in ("-c","--conference"):
            conference = arg

    q,data = load_data(conference)
    make_plots(q,data,conference)

if __name__ == "__main__":

    main(sys.argv[1:])
