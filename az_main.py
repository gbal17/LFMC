''' 
This program runs the following scripts in the respective order:
1) a1_e_swvl.py
2) a1_ndvi.py
3) a2_1_upsampling.py
4) a2_2_coreg.py
'''
import subprocess

program_list = ['a1_e_swvl.py','a1_ndvi.py','a2_1_upsampling.py', 'a2_2_coreg.py']

for program in program_list:
    subprocess.call(['python', program])
    print("Finished:" + program)
