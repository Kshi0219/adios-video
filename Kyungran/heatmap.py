# 라이브러리
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from mplsoccer import Pitch

# 파일 로드
stub_path = r"C:\krpython\adios-video\adios-video\track-stub\tracks_name+ba.pkl"
with open(stub_path, 'rb') as f:
    data = pickle.load(f)


# 팀 분리된 데이터프레임 만들기
def create_player_data(data):
    player_data = []
    for player in data['players']:
        for player_id, player_info in player.items():
            row = {
                'player_id': player_id,
                'team': player_info.get('team', None),
                'bbox': player_info['bbox'],
                'team_color': player_info.get('team_color', None),
                'has_ball': player_info.get('has_ball', False),
                'kr_name': player_info.get('kr_name', None)}
            player_data.append(row)

    player_data = pd.DataFrame(player_data)

    bbox_data = player_data['bbox'].apply(lambda x: pd.Series(x) if x is not None else pd.Series([None, None, None, None]))
    bbox_data.columns = ['bbox_x1', 'bbox_y1', 'bbox_x2', 'bbox_y2']
    player_data = pd.concat([player_data, bbox_data], axis=1)
    player_data = player_data.drop(['bbox', 'team_color'], axis=1)

    return player_data


# 팀 데이터프레임 생성
player_data = create_player_data(data)


# team 값 부여
def split_team(player_data):
    # 중심좌표 계산
    player_data['center_x'] = (player_data['bbox_x1'] + player_data['bbox_x2']) / 2
    player_data['center_y'] = (player_data['bbox_y1'] + player_data['bbox_y2']) / 2

    # min-max scale
    mmscaler = MinMaxScaler()
    player_data['center_x'] = mmscaler.fit_transform(player_data['center_x'].values.reshape(-1, 1)) * 200
    player_data['center_y'] = mmscaler.fit_transform(player_data['center_y'].values.reshape(-1, 1)) * 100

    return player_data

player_data = split_team(player_data)


# 시각화 및 저장_team_a
def visual_teamA_heatmap(player_data, save_path=None):

    # 팀 분리
    team_a = player_data[player_data['team'] == 0]
    team_b = player_data[player_data['team'] == 1]

    # 시각화
    fig, ax = plt.subplots(figsize=(8, 4))
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='#c7d5cc')  # 선 색깔

    pitch.draw(ax=ax)

    # KDE 히트맵 생성
    sns.kdeplot(
        x=team_a["center_x"],
        y=team_a["center_y"],
        fill=True,
        thresh=0,
        levels=10,
        cmap="Reds",
        alpha=0.5,
        ax=ax)  # KDE 플롯을 동일한 축에 그리기 위해 ax=ax 사용

    # y축 반전
    plt.gca().invert_yaxis()

    plt.title('Team A', pad=10)

    # 저장
    if save_path:
        plt.savefig(save_path)# dpi=300, bbox_inches='tight')

    plt.show()

# 시각화 함수 호출 및 JPG 파일로 저장 예시
visual_teamA_heatmap(player_data, save_path=r"C:\krpython\adios-video\Kyungran\team_a_heatmap.jpg")



# 시각화 및 저장_team_b
def visual_teamB_heatmap(player_data, save_path=None):

    # 팀 분리
    team_b = player_data[player_data['team'] == 1]

    # 시각화
    fig, ax = plt.subplots(figsize=(8, 4))
    pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='#c7d5cc')  # 선 색깔

    pitch.draw(ax=ax)

    # KDE 히트맵 생성
    sns.kdeplot(
        x=team_b["center_x"],
        y=team_b["center_y"],
        fill=True,
        thresh=0,
        levels=10,
        cmap="Reds",
        alpha=0.5,
        ax=ax)  # KDE 플롯을 동일한 축에 그리기 위해 ax=ax 사용

    # y축 반전
    plt.gca().invert_yaxis()

    plt.title('Team B', pad=10)

    # 저장
    if save_path:
        plt.savefig(save_path)# dpi=300, bbox_inches='tight')

    plt.show()

# 시각화 함수 호출 및 JPG 파일로 저장 예시
visual_teamB_heatmap(player_data, save_path=r"C:\krpython\adios-video\Kyungran\team_b_heatmap.jpg")
