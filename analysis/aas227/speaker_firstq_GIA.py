import csv
import os
import numpy as np
import matplotlib.pyplot as plt

os.chdir(r'C:\Users\Erin\Pictures\Documents\GitHub\Gender-in-Astro\data')

with open(r'C:\Users\Erin\Pictures\Documents\GitHub\Gender-in-Astro\data\aas223\data.csv') as csvfile:
    data2014 = list(csv.reader(csvfile, delimiter=','))
    
with open(r'C:\Users\Erin\Pictures\Documents\GitHub\Gender-in-Astro\data\aas225\data.csv') as csvfile:
    data2015 = list(csv.reader(csvfile, delimiter=','))
    
with open(r'C:\Users\Erin\Pictures\Documents\GitHub\Gender-in-Astro\data\aas227\genderinastro_data_revised.csv') as csvfile:
    data2016 = list(csv.reader(csvfile, delimiter=','))

first_quest_2014 = []
speaker_2014 = []
for s in range(1,len(data2014)):
    speaker_2014.append(data2014[s][3])
    if len(data2014[s][4]) > 0:    
        first_quest_2014.append(data2014[s][4][0])
    else:
        first_quest_2014.append(None)

first_quest_2015 = []
speaker_2015 = []
for s in range(len(data2015)): 
    speaker_2015.append(data2015[s][3])
    if len(data2015[s][4]) > 0:   
        first_quest_2015.append(data2015[s][4][0])
    else:
        first_quest_2015.append(None)

first_quest_2016 = [] 
speaker_2016 = []   
for s in range(1,len(data2016)):
    speaker_2016.append(data2016[s][4]) 
    if len(data2016[s][5]) > 0:   
        first_quest_2016.append(data2016[s][5][0])
    else:
        first_quest_2016.append(None)

fs_fq_2014 = 0
fs_mq_2014 = 0
ms_fq_2014 = 0
ms_mq_2014 = 0
fs_fq_2015 = 0
fs_mq_2015 = 0
ms_fq_2015 = 0
ms_mq_2015 = 0
fs_fq_2016 = 0
fs_mq_2016 = 0
ms_fq_2016 = 0
ms_mq_2016 = 0


for s in range(1,len(speaker_2014)):
    if first_quest_2014[s] != None:
        if speaker_2014[s] == 'M' and first_quest_2014[s] == 'M':
            ms_mq_2014 += 1
        elif speaker_2014[s] == 'M' and first_quest_2014[s] == 'F':
            ms_fq_2014 += 1
        elif speaker_2014[s] == 'F' and first_quest_2014[s] == 'F':
            fs_fq_2014 += 1
        elif speaker_2014[s] == 'F' and first_quest_2014[s] == 'M':
            fs_mq_2014 += 1
        else:
            pass
    else:
        pass

for s in range(len(speaker_2015)):
    if first_quest_2015[s] != None:
        if speaker_2015[s] == 'M' and first_quest_2015[s] == 'M':
            ms_mq_2015 += 1.
        elif speaker_2015[s] == 'M' and first_quest_2015[s] == 'F':
            ms_fq_2015 += 1.
        elif speaker_2015[s] == 'F' and first_quest_2015[s] == 'F':
            fs_fq_2015 += 1.
        elif speaker_2015[s] == 'F' and first_quest_2015[s] == 'M':
            fs_mq_2015 += 1.
        else:
            pass
    else:
        pass
        
for s in range(len(speaker_2016)):
    if first_quest_2016[s] != None:
        if speaker_2016[s] == 'M' and first_quest_2016[s] == 'M':
            ms_mq_2016 += 1.
        elif speaker_2016[s] == 'M' and first_quest_2016[s] == 'F':
            ms_fq_2016 += 1.
        elif speaker_2016[s] == 'F' and first_quest_2016[s] == 'F':
            fs_fq_2016 += 1.
        elif speaker_2016[s] == 'F' and first_quest_2016[s] == 'M':
            fs_mq_2016 += 1.
        else:
            pass
    else:
        pass
    
print 'First Q M 2014: ' + str(first_quest_2014.count('M'))
print 'First Q F 2014: ' + str(first_quest_2014.count('F'))
print 'First Q M 2015: ' + str(first_quest_2015.count('M'))
print 'First Q F 2015: ' + str(first_quest_2015.count('F'))
print 'First Q M 2016: ' + str(first_quest_2016.count('M'))
print 'First Q F 2016: ' + str(first_quest_2016.count('F'))

print 'Male S Male Q 2014: ' + str(float(ms_mq_2014))
print 'Male S Female Q 2014: ' + str(float(ms_fq_2014))
print 'Female S Female Q 2014: ' + str(float(fs_fq_2014))
print 'Female S Male Q 2014: ' + str(float(fs_mq_2014))

print 'Male S Male Q 2015: ' + str(float(ms_mq_2015))
print 'Male S Female Q 2015: ' + str(float(ms_fq_2015))
print 'Female S Female Q 2015: ' + str(float(fs_fq_2015))
print 'Female S Male Q 2015: ' + str(float(fs_mq_2015))

print 'Male S Male Q 2016: ' + str(float(ms_mq_2016))
print 'Male S Female Q 2016: ' + str(float(ms_fq_2016))
print 'Female S Female Q 2016: ' + str(float(fs_fq_2016))
print 'Female S Male Q 2016: ' + str(float(fs_mq_2016))

    
n_groups = 4

fourteen = ((151./len(speaker_2014)) * 100, (43./len(speaker_2014)) * 100, (25./len(speaker_2014)) * 100, (84./len(speaker_2014)) * 100) 
fifteen = ((109./len(speaker_2015)) * 100, (33./len(speaker_2015)) * 100, (15./len(speaker_2015)) * 100, (30./len(speaker_2015)) * 100)
sixteen = ((93./len(speaker_2016)) * 100, (27./len(speaker_2016)) * 100, (15./len(speaker_2016)) * 100, (48./len(speaker_2016)) * 100)

fig, ax = plt.subplots()

index = np.arange(n_groups)
bar_width = 0.2

opacity = .7

rects1 = plt.bar(index, fourteen, bar_width,
                 alpha=opacity,
                 color='r',
                 label='2014')

rects2 = plt.bar(index + bar_width, fifteen, bar_width,
                 alpha=opacity,
                 color='g',
                 label='2015')

rects3 = plt.bar(index + (2 * bar_width), sixteen, bar_width,
                 alpha=opacity,
                 color='b',
                 label='2016')
                 
plt.ylim([0,100])
plt.xlabel('Gender of Speaker and First Questioner')
plt.ylabel('Percentage of Total')
plt.title('Gender of Speaker and First Questioner by Year')
plt.xticks(index + bar_width, ('MS, MQ', 'MS, FQ', 'FS, FQ', 'FS, MQ'))
plt.legend()

plt.tight_layout()
plt.show()
    
    