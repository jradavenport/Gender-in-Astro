from __future__ import division
from matplotlib import pyplot as plt
import numpy as np

plt.ion()
import pandas as pd

gencolors =('purple','orange')
q = pd.read_csv('question_data.csv')
c = pd.read_csv('chair_data.csv')

fig = plt.figure(1,(12,6))

# Speakers
vc_speakers = q['speaker'].value_counts()

# Speakers
qa=list(q['questions'])
qa.remove(' ')
vc_questioners = pd.value_counts(list(''.join(qa)))

# Speakers
vc_chairs = c['gender'].value_counts()

# Attendees
countrydata = pd.read_csv('map/countries.csv')
names = countrydata['name']
firstnames = [x.split(' ')[0] for x in names]

from sexmachine import detector as gender
d = gender.Detector(case_sensitive=False)
from collections import Counter
genders = [d.get_gender(fn) for fn in firstnames]
cg = Counter(genders)
attendees = list('M'*(cg['male'] + cg['mostly_male'])+'F'*(cg['female'] + cg['mostly_female']))
vc_attendees = pd.value_counts(attendees)

# First question
first = [x[1]['questions'][0] for x in q.iterrows()]
first.remove(' ')
vc_firstquestion = pd.value_counts(first)
# Load into a single dataframe

data = [vc_speakers,vc_chairs,vc_attendees,vc_questioners,vc_firstquestion][::-1]
labels = ['Speakers','Chairs','Attendees','Questioners','First question'][::-1]

normdata = [x/x.sum() for x in data]

# Plot stacked bar chart

ax1 = fig.add_subplot(121)

df = pd.DataFrame(normdata,index=labels)
dfplot = df.plot(kind='barh',stacked=True,ax=ax1,color=gencolors,legend=False)

# Find data positions of the plots

patches = dfplot.patches
yc = [p.get_y() for p in patches]
yc = yc[:int(len(yc)/2)]
height = p.get_height()

ylims1 = ax1.get_ylim()
ax1.vlines(0.5,ylims1[0],ylims1[1],color='k',linestyle='-')

def getfrac(m,f):
    return m/(f+m)

# AAS 225
aas225_speakers = getfrac(83,51)
aas225_questionaskers = getfrac(305,73)
aas225_firstquestion = getfrac(102,32)

print 'PV2015 speaker female fraction %2i' % (float(1 - getfrac(vc_speakers['M'],vc_speakers['F']))*100)
print 'PV2015 chairs female fraction %2i' % (float(1 - getfrac(vc_chairs['M'],vc_chairs['F']))*100)
print 'PV2015 attendees female fraction %2i' % (float(1 - getfrac(vc_attendees['M'],vc_attendees['F']))*100)
print 'PV2015 questioners female fraction %2i' % (float(1 - getfrac(vc_questioners['M'],vc_questioners['F']))*100)
print 'PV2015 first question female fraction %2i' % (float(1 - getfrac(vc_firstquestion['M'],vc_firstquestion['F']))*100)

print 'AAS 225 speaker female fraction %2i' % (float(1 - aas225_speakers)*100)
print 'AAS 225 questioners female fraction %2i' % (float(1 - aas225_questionaskers)*100)
print 'AAS 225 first question female fraction %2i' % (float(1 - aas225_firstquestion)*100)

ax1.vlines(aas225_speakers,yc[-1],yc[-1]+height,color='r',linestyle='--')
ax1.vlines(aas225_questionaskers,yc[-4],yc[-4]+height,color='r',linestyle='--')
ax1.vlines(aas225_firstquestion,yc[-5],yc[-5]+height,color='r',linestyle='--')

ax1.text(aas225_speakers,yc[-1]+height,'AAS 225',ha='center',va='bottom',fontsize=14,color='r')
ax1.text(aas225_questionaskers,yc[-4]+height,'AAS 225',ha='center',va='bottom',fontsize=14,color='r')
ax1.text(aas225_firstquestion,yc[-5]+height,'AAS 225',ha='center',va='bottom',fontsize=14,color='r')

ax1.set_xlabel('Fraction',fontsize=20)

p,l = ax1.get_legend_handles_labels()
ax1.legend(p,l,loc='upper left')

ax1.set_title('PV2015 vs. speakers at 225th AAS')

# IAU individual members
# http://www.iau.org/administration/membership/individual/distribution/

ax2 = fig.add_subplot(122)
dfplot2 = df.plot(kind='barh',stacked=True,ax=ax2,color=gencolors,legend=False)
iau_frac = getfrac(9546,1803)
ylims2 = ax1.get_ylim()
ax2.vlines(0.5,ylims2[0],ylims2[1],color='k',linestyle='-')
ax2.vlines(iau_frac,ylims2[0],yc[-1]+height,color='g',linestyle='-.')
ax2.text(iau_frac*1.02,yc[-1]+height,'IAU',ha='center',va='bottom',fontsize=14,color='g')

print 'IAU member female fraction %2i' % (float(1 - iau_frac)*100)

p,l = ax2.get_legend_handles_labels()
ax2.legend(p,l,loc='upper left')

ax2.set_xlabel('Fraction',fontsize=20)

ax2.set_title('PV2015 vs. IAU individual members')


fig.tight_layout()
fig.savefig('plots/stacked1.pdf', dpi=200)

# How many questions were there per talk? Did the gender of the speaker affect it?

fig2 = plt.figure(2,(12,6))
ax4 = fig2.add_subplot(121)
qpt = [len(x) for x in q['questions']]
ax4.hist(qpt,bins=range(0,8),histtype='step',range=(0,8),linewidth=3, color='k')
ax4.set_xlabel('Questions per talk')

ax5 = fig2.add_subplot(122)
mq = [len(x[1]['questions']) for x in q.iterrows() if x[1]['speaker'] == 'M']
fq = [len(x[1]['questions']) for x in q.iterrows() if x[1]['speaker'] == 'F']
ax5.hist(mq,bins=range(0,8),histtype='step',range=(0,8),linewidth=3, color='orange',label='Male speaker')
ax5.hist(fq,bins=range(0,8),histtype='step',range=(0,8),linewidth=3, color='purple',label='Female speaker')
ax5.set_xlabel('Questions per talk')
ax5.set_ylim(ax4.get_ylim())
ax5.legend(loc='upper right')

fig2.tight_layout()
fig2.savefig('plots/stacked2.pdf', dpi=200)

# When M/F is speaker, who asks questions?

fig3 = plt.figure(3,(12,6))
ax10 = fig3.add_subplot(343)
malefirst_maleafter = ['M'*x[1]['questions'].count('M') for x in q.iterrows() if x[1]['speaker'] == 'M']
malefirst_femaleafter = ['F'*x[1]['questions'].count('F') for x in q.iterrows() if x[1]['speaker'] == 'M']
pd.value_counts(list(''.join(malefirst_maleafter+malefirst_femaleafter)),normalize=True).plot(kind='bar',ax=ax10,color=gencolors)
ax10.set_ylabel('Fraction of questions')
ax10.set_title('Male speaker')
ax10.set_ylim(0,1)

ax11 = fig3.add_subplot(347)
femalefirst_maleafter = ['M'*x[1]['questions'].count('M') for x in q.iterrows() if x[1]['speaker'] == 'F']
femalefirst_femaleafter = ["F"*x[1]['questions'].count('F') for x in q.iterrows() if x[1]['speaker'] == 'F']
pd.value_counts(list(''.join(femalefirst_maleafter+femalefirst_femaleafter)),normalize=True).plot(kind='bar',ax=ax11,color=gencolors)
ax11.set_ylabel('Fraction of questions')
ax11.set_title('Female speaker')
ax11.set_ylim(0,1)

'''
# Does gender of the first speaker affect the subsequent questions?

ax7 = fig.add_subplot(3,4,12)
malefirst_percentagefemaleafter = [x[1]['questions'][1:].count('F')/len(x[1]['questions'][1:]) for x in q.iterrows() if (x[1]['questions'][0] == 'M' and len(x[1]['questions'][1:]) > 0)]
femalefirst_percentagefemaleafter = [x[1]['questions'][1:].count('F')/len(x[1]['questions'][1:]) for x in q.iterrows() if (x[1]['questions'][0] == 'F' and len(x[1]['questions'][1:]) > 0)]
ax7.hist(malefirst_percentagefemaleafter,bins=np.arange(6)/5.,histtype='step',color='orange',range=(0,1),weights=len(malefirst_percentagefemaleafter)*[1./len(malefirst_percentagefemaleafter)],lw=3,label='Male 1st Q')
ax7.hist(femalefirst_percentagefemaleafter,bins=np.arange(6)/5.,histtype='step',color='purple',range=(0,1),weights=len(femalefirst_percentagefemaleafter)*[1./len(femalefirst_percentagefemaleafter)],lw=3,label='Female 1st Q')
ax7.set_ylim(0,1.0)
ax7.set_xlabel('Fraction of subsequent questions asked by females')
ax7.set_ylabel('Fraction of all talks')
ax7.legend(loc='upper right')

# When M/F asks first question, who asks following questions?

ax8 = fig.add_subplot(344)
malefirst_maleafter = ['M'*x[1]['questions'][1:].count('M') for x in q.iterrows() if x[1]['questions'][0] == 'M']
malefirst_femaleafter = ['F'*x[1]['questions'][1:].count('F') for x in q.iterrows() if x[1]['questions'][0] == 'M']
pd.value_counts(list(''.join(malefirst_maleafter+malefirst_femaleafter)),normalize=True).plot(kind='bar',ax=ax8,color=gencolors)
ax8.set_ylabel('Fraction of remaining questions')
ax8.set_title('Male asks 1st Q')
ax8.set_ylim(0,1)

ax9 = fig.add_subplot(348)
femalefirst_maleafter = ['M'*x[1]['questions'][1:].count('M') for x in q.iterrows() if x[1]['questions'][0] == 'F']
femalefirst_femaleafter = ["F"*x[1]['questions'][1:].count('F') for x in q.iterrows() if x[1]['questions'][0] == 'F']
pd.value_counts(list(''.join(femalefirst_maleafter+femalefirst_femaleafter)),normalize=True).plot(kind='bar',ax=ax9,color=gencolors)
ax9.set_ylabel('Fraction of remaining questions')
ax9.set_title('Female asks 1st Q')
ax9.set_ylim(0,1)

'''

