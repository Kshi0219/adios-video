import pickle
import matplotlib.pyplot as plt
from team_heatmap import teamHeatmap
from passmap import PassMap
from hasball_report import possessionReport

def main():
    with open('track-stub/tracks_name+ba.pkl','rb') as load1:
        tracks=pickle.load(load1)
    match_id='testMatch'
    base_pitch_path='test/img/nuri-futsal.png'
    heatmap_path_list=teamHeatmap().gen_team_heatmap(tracks,base_pitch_path,
                                                     match_id,'viz/heatmap-team')
    
    passmap=PassMap(f"track-stub/{match_id}-track-stub.pkl",
                    base_pitch_path)
    passmap.players_withball_data()
    passmap.player_average_coord()
    passmap.create_passmap_data(match_id,'df/passmap')
    passmap_path_list=passmap.passmap_plot('viz/passmap',match_id)

    hasball_report=possessionReport('df/heatmap/testMatch-heatmap-df.csv',
                                    base_pitch_path)
    possession_lmr_path_list=hasball_report.visual_possession(match_id,
                                                              'viz/possession')
    possession_dmr_path_list=hasball_report.visual_activate_zone(match_id,
                                                                 'viz/possession')

if __name__=='__main__':
    main()