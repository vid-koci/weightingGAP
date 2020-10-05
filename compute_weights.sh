#This entire procedure is a mild monstrosity because Matlab has great tools for optimization but not for processing text.
#Current setup computes Wt-bias weights, refer to comments within compute_weight.py to make changes
#First, we analyse all data with compute_weights.py which generates linprog_compute_trimmed_weights.m
python compute_weights.py

#Different versions of Matlab may use different command to run from command line, e.g.
#matlab -batch "linprog_compute_trimmed_weights; exit"
#It is incredibly important that this file is run ONLY from the command line. The generated program is large (4M lines) and will crash the Matlab editor.
#Note that the script below will take a while to run (an hour or so) most of the time spent on reading the program and not on the optimization itself.
matlab -nodisplay -nosplash -nodesktop -r "linprog_compute_trimmed_weights; exit"

#This will produce linear_weights_trimmed.txt file, the list of all weights
#The script below will produce linear_weights_trimmed.json
weights_to_json.py
