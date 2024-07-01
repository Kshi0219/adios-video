# 라이브러리
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch

# 한글 오류
import matplotlib
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

# pkl -> df로 만든 파일 불러오기 + 전처리
file_path = r"C:\krpython\adios-video\adios-video\Kyungran\player_data.csv"
player_data = pd.read_csv(file_path, index_col=0)

def ball_possession(player_data):
    player_data = player_data[player_data['has_ball'] == True]
    # 좌표 중앙값
    player_data['x'] = (player_data['bbox_x1'] + player_data['bbox_x2']) / 2
    player_data['y'] = (player_data['bbox_y1'] + player_data['bbox_y2']) / 2

    # 팀 구분
    team_a = player_data[player_data['team'] == 0]
    team_b = player_data[player_data['team'] == 1]

    # 영역 지정 - 구역별 볼 점유율 (가로 기준)
    team_a['region_y'] = pd.cut(team_a['y'], bins=[0, 200, 400, 600], labels=['Left Side', 'Middle', 'Right Side'])
    team_b['region_y'] = pd.cut(team_b['y'], bins=[0, 200, 400, 600], labels=['Right Side', 'Middle', 'Left Side'])

    # 영역별 비율 계산
    team_a_distribution_y = team_a['region_y'].value_counts(normalize=True) * 100  # 영역 비율 계산
    team_a_distribution_y = team_a_distribution_y.reindex(['Left Side', 'Middle', 'Right Side'])
    team_b_distribution_y = team_b['region_y'].value_counts(normalize=True) * 100
    team_b_distribution_y = team_b_distribution_y.reindex(['Right Side', 'Middle', 'Left Side'])

    # 영역 지정 - 활동 구역별 볼 점유율 (세로 기준)
    team_a['region_x'] = pd.cut(team_a['x'], bins=[0, 420, 840, 1260], labels=['Deffensive', 'Middle', 'Offensive'])
    team_b['region_x'] = pd.cut(team_b['x'], bins=[0, 420, 840, 1260], labels=['Offensive', 'Middle', 'Deffensive'])

    # 세로 기준
    team_a_distribution_x = team_a['region_x'].value_counts(normalize=True) * 100  # 영역 비율 계산
    team_a_distribution_x = team_a_distribution_x.reindex(['Deffensive', 'Middle', 'Offensive'])
    team_b_distribution_x = team_b['region_x'].value_counts(normalize=True) * 100
    team_b_distribution_x = team_b_distribution_x.reindex(['Offensive', 'Middle', 'Deffensive'])

    return team_a_distribution_y, team_b_distribution_y, team_a_distribution_x, team_b_distribution_x

def visual_ball_possession(team_a_distribution_y, team_b_distribution_y, save_path=None):
    fig, ax = plt.subplots(figsize=(8, 4))
    fig.set_facecolor('#FFFFFF')
    pitch = Pitch(pitch_type='statsbomb', pitch_color='grass', line_color='#c7d5cc')

    # 각 축구장 그리기
    pitch.draw(ax)

    # 막대 너비 및 최대 길이 설정
    bar_height = 15
    max_length = 60  # 막대 최대 길이 설정
    bar_spacing = 27  # 막대 간격 축소

    # team_a 막대 그래프 그리기
    for idx, (region, value) in enumerate(team_a_distribution_y.items()):
        y_start = 13 + (idx * bar_spacing)  # 막대 시작 위치 y 좌표
        length = (value / 100) * max_length  # 막대 길이 설정
        ax.barh(y_start, length, height=bar_height, left=60, color='#E7F0DC')  # 막대 그리기
        ax.text(61, y_start, f'{value:.1f}%', color='black', va='center', fontsize=12)  # 비율 텍스트
        if idx < len(team_a_distribution_y) - 1:
            ax.axhline(y=y_start + 13, xmin=0.05, xmax=0.96, color='white', linestyle='--')

    # team_b 막대 그래프 그리기
    for idx, (region, value) in enumerate(team_b_distribution_y.items()):
        y_start = 13 + (idx * bar_spacing)  # 막대 시작 위치 y 좌표
        length = (value / 100) * max_length  # 막대 길이 설정
        ax.barh(y_start, -length, height=bar_height, left=60, color='#B5C18E')  # 막대 그리기
        ax.text(44, y_start, f'{value:.1f}%', color='black', va='center', fontsize=12)  # 비율 텍스트

    plt.title('구역별 점유율\n', fontsize=15)
    ax.text(0.3, 1.02, 'team_a', transform=ax.transAxes, fontsize=12, ha='center')
    ax.text(0.7, 1.02, 'team_b', transform=ax.transAxes, fontsize=12, ha='center')

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

def visual_activate_zone(team_a_distribution_x, team_b_distribution_x, save_path=None):
    fig, ax = plt.subplots(figsize=(8, 4))
    fig.set_facecolor('#FFFFFF')
    pitch = Pitch(pitch_type='statsbomb', pitch_color='grass', line_color='#c7d5cc')

    # 각 축구장 그리기
    pitch.draw(ax)

    # 막대 너비 및 최대 길이 설정
    bar_height = 15
    max_length = 60  # 막대 최대 길이 설정
    bar_spacing = 27  # 막대 간격 축소

    # team_a 막대 그래프 그리기
    for idx, (region, value) in enumerate(team_a_distribution_x.items()):
        y_start = 13 + (idx * bar_spacing)  # 막대 시작 위치 y 좌표
        length = (value / 100) * max_length  # 막대 길이 설정
        ax.barh(y_start, length, height=bar_height, left=60, color='#E7F0DC')  # 막대 그리기
        ax.text(61, y_start, f'{value:.1f}%', color='black', va='center', fontsize=12)  # 비율 텍스트
        if idx < len(team_a_distribution_x) - 1:
            ax.axhline(y=y_start + 13, xmin=0.05, xmax=0.96, color='white', linestyle='--')

    # team_b 막대 그래프 그리기
    for idx, (region, value) in enumerate(team_b_distribution_x.items()):
        y_start = 13 + (idx * bar_spacing)  # 막대 시작 위치 y 좌표
        length = (value / 100) * max_length  # 막대 길이 설정
        ax.barh(y_start, -length, height=bar_height, left=60, color='#B5C18E')  # 막대 그리기
        ax.text(44, y_start, f'{value:.1f}%', color='black', va='center', fontsize=12)  # 비율 텍스트

    plt.title('활동 구역별 점유율\n', fontsize=15)
    ax.text(0.3, 1.02, 'team_a', transform=ax.transAxes, fontsize=12, ha='center')
    ax.text(0.7, 1.02, 'team_b', transform=ax.transAxes, fontsize=12, ha='center')

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

# 점유율 데이터 계산
team_a_distribution_y, team_b_distribution_y, team_a_distribution_x, team_b_distribution_x = ball_possession(player_data)

# 시각화
visual_ball_possession(team_a_distribution_y, team_b_distribution_y, save_path=r"C:\krpython\adios-video\adios-video\Kyungran\ball_possession.jpg")
visual_activate_zone(team_a_distribution_x, team_b_distribution_x, save_path=r"C:\krpython\adios-video\adios-video\Kyungran\visual_activate_zone.jpg")
