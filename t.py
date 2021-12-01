#Read pattern... rip first two chars off from each line as I have no
#idea what the + means....

# To shorten the RegEx ... Uppercase is assumed
import re
import pickle

calls={}
skimmer_data = {}

def skim_to_regex(skim_expression):
    skim_expression=skim_expression.replace('@','[A-Z]')
    skim_expression=skim_expression.replace('#','[0-9]')
    return r"^{0}$".format(skim_expression)

with open('patt3ch.lst','rt') as pattern:
    patt=[d[2:].upper().strip() for d in pattern.read().split('\n')[:-1]]

for p in patt:
    skimmer_data[p]={}
    skimmer_data[p]['matched_count']=0
    skimmer_data[p]['matched_calls']=[]

with open('MASTER.SCP','rt') as scp_file:
    for c in scp_file.read().upper().split('\n')[3:]:
        calls[c]={}
        calls[c]['matched_count']=0
        calls[c]['matched_patt']=[]

progress=0
for s in skimmer_data.keys():
    skim_matches=0
    pattern=re.compile(skim_to_regex(s))
    for c in calls.keys():
        m=pattern.match(c)
        if (m):
            calls[c]['matched_count'] += 1
            calls[c]['matched_patt'].append(s)
            skimmer_data[s]['matched_count'] += 1
            skimmer_data[s]['matched_calls'].append(c)
            #print(f"{c} {s}")
    progress+=1
    if (progress%1000==0):
        print(f"Done {progress}")
    #if progress>1000:
    #    break

#
#now save the results
#
with open('run1.pkl','wb') as ofp:
    pickle.dump([skimmer_data,calls],ofp)


#
# How many un-matched rules are there ?
#
c=0
for s in skimmer_data.keys():
    if skimmer_data[s]['matched_count']==0:
        #print(s)
        c+=1
print(f"We have {c} unmatched patt rules")

#
#MASTER.SCP how many calls are missing
#
cnt=0
hasslash=0
for c in calls.keys():
    if calls[c]['matched_count']==0:
        print(c)
        cnt+=1
        if c.find("/") !=-1:
            hasslash+=1
print(f"We have {cnt} unmatched calls from SCP")
print(f"of which {hasslash} has a / ")
