#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import csv
import pathlib
import math
import os
import shutil
import sys
from statistics import median


# In[ ]:


# set parameterers either hard coded or from the command line

def type_of_script():
    try:
        ipy_str = str(type(get_ipython()))
        if 'zmqshell' in ipy_str:
            return 'jupyter'
        if 'terminal' in ipy_str:
            return 'ipython'
    except:
        return 'terminal'

typeScript = type_of_script()
print(typeScript)

if typeScript=='terminal':
    # get arguments from command line
    print (sys.argv[1:])

    circuitID = sys.argv[1]
    path = sys.argv[2] + '/'
    alg = sys.argv[3]
    init_state = sys.argv[4]
    final_state = sys.argv[5]
    samples_exp2 = sys.argv[6]
    n_threads = sys.argv[7]
    
else:
    # get arguments from command line
    circuitID = '19'

    #path = '~/QCircuits_BenchTest/circuits/'
    path = './'

    init_state = '0'
    final_state = '0'

    alg = 'IS'
    #alg = 'BD'
    #alg = 'BD_MIS'

    samples_exp2 = 20
    n_threads = 1


extension = '.csv'
filename_prefix = 'circuit_' + circuitID + '.data_stats_' + alg + '_' + init_state + '_' + final_state + '_' + samples_exp2 + '_' + n_threads

filename_glob = filename_prefix + '_?' + extension 
print (filename_glob)

filename_out = filename_prefix + '_average' + extension 
print (filename_out)

archive_dir = filename_prefix   
print (archive_dir)


# In[ ]:


csv_filesname = [f for f in pathlib.Path(path).glob(filename_glob)]

n_files = len(csv_filesname)
csv_f = [''] * n_files
csv_reader = [''] * n_files


# In[ ]:


for ndx,fname in enumerate(csv_filesname): 
    print ('Opening {0}'.format(fname))
    try: 
        csv_f[ndx] = open(fname, 'r')
    except OSError as error: 
        print('error %s', error) 

    csv_reader[ndx]  = csv.reader(csv_f[ndx] , delimiter=',')


# In[ ]:


try: 
    csv_fw = open(path+filename_out, 'w')
except OSError as error: 
    print('error %s', error) 

csv_writer = csv.writer (csv_fw , delimiter=',')


# In[ ]:


# REad true amplitude from the 1st csv
row = next(csv_reader[0])
csv_writer.writerow(row)
row = next(csv_reader[0])
trueR = float(row[0])
trueI = float(row[1])
csv_writer.writerow(row)
print('{0} + j {1}'.format(trueR,trueI))
# skip 3rd row
row = next(csv_reader[0])
row.append('var')
row.append('L2')
csv_writer.writerow(row)
# skip 3 rows in all remaining csv's
for ndx in range (1, n_files):
    _ = next(csv_reader[ndx])
    _ = next(csv_reader[ndx])
    _ = next(csv_reader[ndx])
    


# In[ ]:


# Read row by row on all csv
for row in csv_reader[0]:
    n_samples = row[0]
    time = row[1]
    n_paths = row[2]
    n_nonZero_paths = row[3]
    sum_estimateR = list(float(row[4]))
    sum_estimateI = list(float(row[5]))
    for ndx in range (1, n_files):
        row = next(csv_reader[ndx])
        sum_estimateR.append(float(row[4]))
        sum_estimateI.append(float(row[5]))
    estimateR = median(sum_estimateR)
    estimateI = median(sum_estimateI)
    varR = (estimateR-trueR)**2
    varI = (estimateI-trueI)**2
    variance = varR+varI
    L2 = math.sqrt(variance)

    csv_writer.writerow([n_samples, time, n_paths, n_nonZero_paths, estimateR, estimateI, varR, varI, variance, L2])

print('{0} + j {1}'.format(estimateR, estimateI))
print('variance: {0}'.format(variance))
print ('Time: {0} us'.format(time))


# In[ ]:


for fh in csv_f:
    try: 
        fh.close()
    except OSError as error: 
        print('error %s', error) 

csv_fw.close()


# In[ ]:


# archive processed files
try: 
    os.mkdir(archive_dir)
except OSError as error: 
    pass
    
for fname in csv_filesname: 
    fbasename  = os.path.basename(fname)
    os.rename (fname, archive_dir+'/'+fbasename)


# In[ ]:


print ('That\'s all , folks!')


# In[ ]:




