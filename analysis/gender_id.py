# -*- coding: utf-8 -*-

from sexmachine import detector
d = detector.Detector(case_sensitive=False)

gfile = "../data/aas227/aas227_registrants.csv"
with open(gfile,'r') as f:
    data = f.readlines()

data = [x.strip() for x in data]

m,f,a = 0,0,0
no_first_name = 0
for name in data:
    try:
        splitnames = name.split()
        namecopy = splitnames[::]
        # Check for first initial
        for sn in splitnames:
            try:
                if sn[0].isalpha() and sn[1] == ".":
                    namecopy.remove(sn)
            except IndexError:
                pass
        if len(namecopy) > 1:
            given_name = namecopy[0]
            if len(namecopy) < len(name.split()):
                print("Interpreting {0} as the first name for {1}".format(given_name,name))
            
            gender = d.get_gender(name.split()[0])

            if gender in ('male','mostly_male'):
                m += 1
            if gender in ('female','mostly_female'):
                f += 1
            if gender in ('andy',):
                a += 1
        else:
            print("Unable to determine gender for {0}".format(name))
    except SyntaxError:
        "Unable to determine gender for {0}".format(name)
        no_first_name += 1
        pass

total = len(data) - no_first_name

print("\n227th AAS - registrants")
print("Males:   {0:4.0f} ({1:2.0f} percent)".format(m,m* 1./total * 100))
print("Females: {0:4.0f} ({1:2.0f} percent)".format(f,f* 1./total * 100))
print("?????:   {0:4.0f} ({1:2.0f} percent)\n".format(a,a* 1./total * 100))

