import csv
import os
import numpy as np
import matplotlib.pyplot as plt

os.chdir(r'C:\Users\Erin\Pictures\Documents\GitHub\Gender-in-Astro\data\aas227')

with open('genderinastro_data_revised.csv') as csvfile:
    data = list(csv.reader(csvfile, delimiter=','))

n = len(data)
chair_m = 0
chair_f = 0
speaker_m = 2
speaker_f = 2
quest_m = 0
quest_f = 0

for s in range(1,len(data)):
    if data[s][3] == 'M':
        chair_m += 1
    elif data[s][3] == 'F':
        chair_f += 1
    else:
        pass
    if data[s][4] == 'M':
        speaker_m += 1
    elif data[s][4] == 'F':
        speaker_f += 1
    else:
        pass
    mq = data[s][5].count('M')
    quest_m += mq
    fq = data[s][5].count('F')
    quest_f += fq

chair_tot = float(chair_m + chair_f)
speaker_tot = float(speaker_m + speaker_f)
quest_tot = float(quest_m + quest_f)
   
n_groups = 3

male = ((chair_m/chair_tot) * 100, (speaker_m/speaker_tot) * 100, (quest_m/quest_tot) * 100)
female = ((chair_f/chair_tot) * 100, (speaker_f/speaker_tot) * 100, (quest_f/quest_tot) * 100)

fig, ax = plt.subplots()

index = np.arange(n_groups)
bar_width = 0.35

opacity = .7

rects1 = plt.bar(index, male, bar_width,
                 alpha=opacity,
                 color='b',
                 label='Men')

rects2 = plt.bar(index + bar_width, female, bar_width,
                 alpha=opacity,
                 color='r',
                 label='Women')

plt.ylim([0,100])
plt.xlabel('Group')
plt.ylabel('Fraction')
plt.title('Percentage of Total by Group and Gender')
plt.xticks(index + bar_width, ('Session Chair', 'Speakers', 'Questioners'))
plt.legend()

plt.tight_layout()
plt.show()


