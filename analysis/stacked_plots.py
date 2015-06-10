from __future__ import division
from matplotlib import pyplot as plt
import numpy as np
plt.ion()
import pandas as pd

def getfrac(m,f):
    return m/(f+m)

gencolors =('purple','lightgreen')
q = pd.read_csv('data.csv',names=['date','session','speaker','chair','questions'],header=None)

# Speakers
vc_speakers = q['speaker'].value_counts()

# Chairs
vc_chairs = q['chair'].value_counts()

# Questioners
qa=list(q['questions'])
try:
    qa.remove(' ')
except:
    pass
vc_questioners = pd.value_counts(list(''.join(qa)))

# First question
first = [x[1]['questions'][0] for x in q.iterrows()]
try:
    first.remove(' ')
except:
    pass
vc_firstquestion = pd.value_counts(first)

# Load into a single dataframe
data = [vc_speakers,vc_chairs,vc_questioners,vc_firstquestion][::-1]
labels = ['Speakers','Chairs','Questioners','First question'][::-1]
normdata = [x/x.sum() for x in data]


# Figure 1
# Plot stacked bar chart
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
df = pd.DataFrame(normdata,index=labels)
dfplot = df.plot(kind='barh',stacked=True,ax=ax1,color=gencolors,legend=False)

# Find data positions of the plots
patches = dfplot.patches
yc = [p.get_y() for p in patches]
yc = yc[:int(len(yc)/2)]
height = p.get_height()

ylims1 = ax1.get_ylim()
ax1.vlines(0.5,ylims1[0],ylims1[1],color='k',linestyle='-')
ax1.set_xlabel('Fraction')
#ax1.set_title('LGAstrostats 2015')

# IAU individual members
# http://www.iau.org/administration/membership/individual/distribution/
iau_frac = getfrac(9546,1803)
ax1.vlines(iau_frac,ylims1[0],yc[-1]+height,color='b',linestyle='--')
ax1.text(iau_frac*1.02,yc[-1]+0.98*height,'IAU',ha='center',va='bottom',color='b')
p,l = ax1.get_legend_handles_labels()
ax1.legend(p,l,loc='upper left')

fig1.tight_layout()
fig1.savefig('plots/stacked1.pdf', dpi=200)


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

ax5 = fig2.add_subplot(122)
mq = [len(x[1]['questions']) for x in q.iterrows() if x[1]['speaker'] == 'M']
fq = [len(x[1]['questions']) for x in q.iterrows() if x[1]['speaker'] == 'F']
ax5.hist(mq,bins=range(0,8),histtype='step',range=(0,8),linewidth=3, color=gencolors[0],label='Male speaker')
ax5.hist(fq,bins=range(0,8),histtype='step',range=(0,8),linewidth=3, color=gencolors[1],label='Female speaker')
ax5.set_ylim(ylims4)
ax5.vlines(np.mean(mq),ylims4[0],ylims4[1],linestyle='--',color=gencolors[0])
ax5.vlines(np.mean(fq),ylims4[0],ylims4[1],linestyle='--',color=gencolors[1])
ax5.set_xlabel('Questions per talk')
ax5.set_ylabel('Count')
ax5.legend(loc='upper right')

fig2.tight_layout()
fig2.savefig('plots/stacked2.pdf', dpi=200)


# Who asks questions
fig3 = plt.figure()


# When M/F speaker, who asks questions?

malespeaker_maleafter = ['M'*x[1]['questions'].count('M') for x in q.iterrows() if x[1]['speaker'] == 'M']
malespeaker_femaleafter = ['F'*x[1]['questions'].count('F') for x in q.iterrows() if x[1]['speaker'] == 'M']
femalespeaker_maleafter = ['M'*x[1]['questions'].count('M') for x in q.iterrows() if x[1]['speaker'] == 'F']
femalespeaker_femaleafter = ["F"*x[1]['questions'].count('F') for x in q.iterrows() if x[1]['speaker'] == 'F']
vc_malespeaker = pd.value_counts(list(''.join(malespeaker_maleafter+malespeaker_femaleafter)))
vc_femalespeaker = pd.value_counts(list(''.join(femalespeaker_maleafter+femalespeaker_femaleafter)))

# Load everything into a single dataframe

speakerdata = [vc_malespeaker,vc_femalespeaker]
speakerlabels = ['Male speaker','Female speaker']
speakernormdata = [x/x.sum() for x in speakerdata]
df = pd.DataFrame(speakernormdata,index=speakerlabels)
print df

# Plot stacked bar chart
ax8 = fig3.add_subplot(311)
df.plot(kind='barh',stacked=True,ax=ax8,color=gencolors,legend=False)
ax8.set_xlabel('Fraction of total questions')
ylims8 = ax8.get_ylim()
ax8.vlines(0.5,ylims8[0],ylims8[1],color='k',linestyle='-')
p,l = ax8.get_legend_handles_labels()
ax8.legend(p,l,loc='upper left')

# Does the gender of the session chair affect the distribution of the questioners gender?

malechair_maleafter = ['M'*x[1]['questions'].count('M') for x in q.iterrows() if x[1]['chair'] == 'M']
malechair_femaleafter = ['F'*x[1]['questions'].count('F') for x in q.iterrows() if x[1]['chair'] == 'M']
femalechair_maleafter = ['M'*x[1]['questions'].count('M') for x in q.iterrows() if x[1]['chair'] == 'F']
femalechair_femaleafter = ["F"*x[1]['questions'].count('F') for x in q.iterrows() if x[1]['chair'] == 'F']
vc_malechair = pd.value_counts(list(''.join(malechair_maleafter+malechair_femaleafter)))
vc_femalechair = pd.value_counts(list(''.join(femalechair_maleafter+femalechair_femaleafter)))

# Load everything into a single dataframe

chairdata = [vc_malechair,vc_femalechair]
chairlabels = ['Male chair','Female chair']
chairnormdata = [x/x.sum() for x in chairdata]
df = pd.DataFrame(chairnormdata,index=chairlabels)
print df

# Plot stacked bar chart
ax9 = fig3.add_subplot(312)
df.plot(kind='barh',stacked=True,ax=ax9,color=gencolors,legend=False)
ax9.set_xlabel('Fraction of total questions')
ylims9 = ax9.get_ylim()
ax9.vlines(0.5,ylims9[0],ylims9[1],color='k',linestyle='-')


# Does gender of the first question affect the subsequent questions?

malefirst_maleafter = ['M'*x[1]['questions'][1:].count('M') for x in q.iterrows() if x[1]['questions'][0] == 'M']
malefirst_femaleafter = ['F'*x[1]['questions'][1:].count('F') for x in q.iterrows() if x[1]['questions'][0] == 'M']
vc_malefirst_remaining = pd.value_counts(list(''.join(malefirst_maleafter+malefirst_femaleafter)))

femalefirst_maleafter = ['M'*x[1]['questions'][1:].count('M') for x in q.iterrows() if x[1]['questions'][0] == 'F']
femalefirst_femaleafter = ["F"*x[1]['questions'][1:].count('F') for x in q.iterrows() if x[1]['questions'][0] == 'F']
vc_femalefirst_remaining = pd.value_counts(list(''.join(femalefirst_maleafter+femalefirst_femaleafter)))

# Load everything into a single dataframe
firstrdata = [vc_malefirst_remaining,vc_femalefirst_remaining]
firstrlabels = ['Man asks question 1','Woman asks question 1']
firstrnormdata = [x/x.sum() for x in firstrdata]
dfr = pd.DataFrame(firstrnormdata,index=firstrlabels)
print dfr

ax7 = fig3.add_subplot(313)
dfr.plot(kind='barh',stacked=True,ax=ax7,color=gencolors,legend=False)
ylims7 = ax7.get_ylim()
ax7.vlines(0.5,ylims7[0],ylims7[1],color='k',linestyle='-')
ax7.set_xlabel('Fraction of remaining questions')

fig3.tight_layout()
fig3.savefig('plots/stacked3.pdf', dpi=200)
