import pickle
import matplotlib.pyplot as plt
from team_heatmap import teamHeatmap

def main():
    with open('track-stub/tracks_name+ba.pkl','rb') as load1:
        tracks=pickle.load(load1)

    heatmap_path_list=teamHeatmap().gen_team_heatmap(tracks,'test/img/nuri-futsal.png',
                                                     'testMatch','viz/heatmap-team')

if __name__=='__main__':
    main()