from boggle import *
import matplotlib.pyplot as plt
import pickle

logbook = pickle.load(open("pickles/final_data.pkl", "rb"))


generate_path_gif(logbook, 'path_animation.gif')
generate_evolution_gif(logbook, 'evolve_animation.gif')