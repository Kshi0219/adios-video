# 라이브러리
import pandas as pd
import os
from glob import glob
import matplotlib.pyplot as plt
import seaborn as sns

class teamHeatmap:
    def __init__(self):
        pass

    # 선수 위치 DataFrame 생성
    def create_player_data(self,tracks,match_id:str):
        df_path=f"df/heatmap/{match_id}-heatmap-df.csv"
        if os.path.exists(df_path):
            player_data=pd.read_csv(df_path,index_col=0)
            return player_data
        player_data = []
        for frame_num,player in enumerate(tracks['players']):
            for player_id, player_info in player.items():
                row = {
                    'frame_num':frame_num,
                    'player_id': player_id,
                    'team': player_info.get('team', None),
                    'team_color': player_info.get('team_color', None),
                    'coord_x': player_info['coord_tr'][0],
                    'coord_y': player_info['coord_tr'][1],
                    'start_pitch_side':tracks['players'][0][player_id]['pitch_side']}
                if row['coord_x']<80 and row['coord_y'] in range(80,280):
                    row['in_pa']='left_pa'
                elif row['coord_x']>680 and row['coord_y'] in range(80,280):
                    row['in_pa']='right_pa'
                else:
                    row['in_pa']='non_pa'
                player_data.append(row)

        player_data = pd.DataFrame(player_data)

        player_data.to_csv(f"df/heatmap/{match_id}-heatmap-df.csv")
        return player_data
    
    # 히트맵 생성 함수
    def gen_team_heatmap(self,tracks,base_pitch_path:str,match_id:str,heatmap_save_path:str):
        
            
        player_data=self.create_player_data(tracks,match_id)
        base_pitch=plt.imread(base_pitch_path)
        # 팀 분리
        team_split = {'Team-A':player_data.query("start_pitch_side=='left'"),
                      'Team-B':player_data.query("start_pitch_side=='right'")}
        
        for team,df in team_split.items():
            # 시각화
            fig, ax = plt.subplots()
            pitch = base_pitch.copy()

            if team=='Team-A':
                # KDE 히트맵 생성
                sns.kdeplot(
                    x=df.query("in_pa!='left_pa'")["coord_x"],
                    y=df.query("in_pa!='left_pa'")["coord_y"],
                    fill=True,
                    thresh=0,
                    levels=10,
                    cmap="Reds",
                    alpha=0.8,
                    ax=ax)
                # 이미지 배경에 그래프 추가
                ax.imshow(pitch, extent=[2.5, 802.5, 2.5, 402.5])
                # y축 반전
                plt.gca().invert_yaxis()
                plt.axis('off')
                plt.savefig(heatmap_save_path+f"/{match_id}-heatmap-team-a.png",
                            bbox_inches='tight')
            else:
                # KDE 히트맵 생성
                sns.kdeplot(
                    x=df.query("in_pa!='right_pa'")["coord_x"],
                    y=df.query("in_pa!='right_pa'")["coord_y"],
                    fill=True,
                    thresh=0,
                    levels=10,
                    cmap="Blues",
                    alpha=0.8,
                    ax=ax)
                ax.imshow(pitch, extent=[2.5, 802.5, 2.5, 402.5])
                # y축 반전
                plt.gca().invert_yaxis()
                plt.axis('off')
                plt.savefig(heatmap_save_path+f"/{match_id}-heatmap-team-b.png",
                            bbox_inches='tight')