import pickle
import matplotlib.pyplot as plt
from team_heatmap import teamHeatmap
from passmap import PassMap

def main():
    with open('track-stub/tracks_name+ba.pkl','rb') as load1:
        tracks=pickle.load(load1)
    match_id='testMatch'
    heatmap_path_list=teamHeatmap().gen_team_heatmap(tracks,'test/img/nuri-futsal.png',
                                                     match_id,'viz/heatmap-team')
    
    passmap=PassMap(f"track-stub/{match_id}-track-stub.pkl",
                    'test/img/nuri-futsal.png')
    passmap.players_withball_data()
    passmap.player_average_coord()
    passmap.create_passmap_data(match_id,'df/passmap')
    passmap.passmap_plot('viz/passmap',match_id)

if __name__=='__main__':
    main()