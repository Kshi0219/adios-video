import pandas as pd
import matplotlib.pyplot as plt

file_path = r"C:\krpython\adios-video\adios-video\Kyungran\testMatch-heatmap-df.csv"
player_data = pd.read_csv(file_path, index_col=0)


# 데이터프레임 영역 구분 지정
def create_possession_frame(player_data):
    player_data = player_data[player_data['has_ball'] == True]

    # 팀 구분
    team_a = player_data[player_data['start_pitch_side'] == 'left']
    team_b = player_data[player_data['start_pitch_side'] == 'right']

    # 구역별 점유율(가로 기준)
    categories = ['Left Side', 'Middle', 'Right Side']
    team_a['region_y'] = pd.cut(team_a['coord_y'], 
                                bins=[0, 140, 280, 420], 
                                labels=categories, ordered=True)
    team_b['region_y'] = pd.cut(team_b['coord_y'], 
                                bins=[0, 140, 280, 420], 
                                labels=categories[::-1], ordered=True)

    team_a_y = team_a['region_y'].value_counts(normalize=True).reindex(categories) * 100
    team_b_y = team_b['region_y'].value_counts(normalize=True).reindex(categories[::-1])* 100

    # 구역별 점유율(세로 기준)
    team_a['region_x'] = pd.cut(team_a['coord_x'], 
                                bins=[0, 270, 540, 810], 
                                labels=categories, ordered=True)

    team_b['region_x'] = pd.cut(team_b['coord_x'], 
                                bins=[0, 270, 540, 810], 
                                labels=categories[::-1], ordered=True)

    team_a_x = team_a['region_x'].value_counts(normalize=True).reindex(categories)*100 # 영역 비율 계산
    team_b_x = team_b['region_x'].value_counts(normalize=True).reindex(categories[::-1])*100 

    # 데이터 프레임 생성
    team_a_df = pd.DataFrame({
        'Y_Proportion': team_a_y.values,
        'X_Proportion': team_a_x.values
    })

    team_b_df = pd.DataFrame({
        'Y_Proportion': team_b_y.values,
        'X_Proportion': team_b_x.values
    })
    return team_a_df, team_b_df


# 구역별 점유율 시각화 (가로 기준)
def visual_possession(team_data, team_name, save_path=None):
    nuri_pitch=plt.imread(r"C:\krpython\adios-video\adios-video\Kyungran\nuri_pitch.png")

    fig, ax = plt.subplots()

    # 막대 너비 및 최대 길이 설정
    bar_height = 70
    max_length = 500
    bar_spacing = 130

    labels = ['Left Side', 'Middle', 'Right Side']

    # Y_Proportion 값만 사용
    y_proportions = team_data['Y_Proportion']
    swapped_distribution = y_proportions[::-1]  # Right Side와 Left Side 위치 바꾸기

    # 막대 그래프 그리기
    for idx, value in enumerate(swapped_distribution):
        y_start = 35 + (idx * bar_spacing)
        length = (value / 100) * max_length
        if team_name == 'A':
            ax.barh(y_start, length, height=bar_height, left=402, color='#FB876E', align='edge')
            ax.text(280, y_start+32, labels[idx], va='center', fontsize=10)
            ax.text(420, y_start+30, f'{value:.1f}%', va='center', fontsize=11)
        else:
            ax.barh(y_start, -length, height=bar_height, left=402, color='#7DB7DA', align='edge')
            ax.text(420, y_start+32, labels[idx], va='center', fontsize=10)
            ax.text(300, y_start+30, f'{value:.1f}%', va='center', fontsize=11)
        
        if idx < len(swapped_distribution) - 1:
            ax.axhline(y=y_start + 90, xmin=0.01, xmax=5, color='#BCBCBC', linestyle='--')

    ax.imshow(nuri_pitch, extent=[5, 802.5, 2.5, 402.5])
    ax.set_title(f'TEAM {team_name}', fontsize=12)
    ax.axis('off')
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.show()


# 구역별 점유율 시각화 (세로 기준)
def visual_activate_zone(team_a_data, team_b_data, save_path=None):
    nuri_pitch=plt.imread(r"C:\krpython\adios-video\adios-video\Kyungran\nuri_pitch.png")
    fig, ax = plt.subplots()

    # 막대 너비 및 최대 길이 설정
    bar_width = 60
    max_length = 500  # 막대 최대 길이 설정
    bar_spacing = 220  
    base_line = 180  # 기준선 설정 (축구장의 하단에 맞추기 위해 Y 좌표를 사용)

    x_proportions = team_a_data['X_Proportion']
    y_proportions = team_b_data['X_Proportion']

    # 팀 A 막대 그래프 그리기
    for idx, value in enumerate(x_proportions):
        x_start = base_line + (idx * bar_spacing)  # 막대 시작 위치 x 좌표
        length = (value / 100) * max_length  # 막대 길이 설정
        ax.bar(x_start - bar_width, length, width=bar_width, bottom=5, color='#FB876E', align='edge')  # 막대 그리기
        ax.text(x_start - bar_width / 2, length + 10, f'{value:.1f}%',  ha='center', va='bottom', fontsize=12)  # 비율 텍스트
        if idx < len(team_a_data) - 1:
            ax.axvline(x=x_start + bar_width + 45, color='#BCBCBC', linestyle='--', ymin=0.02, ymax=0.99)

    # 팀 B 막대 그래프 그리기
    for idx, value in enumerate(y_proportions):
        x_start = base_line + (idx * bar_spacing)  # 막대 시작 위치 x 좌표
        length = (value / 100) * max_length  # 막대 길이 설정
        ax.bar(x_start, length, width=bar_width, bottom=5, color='#7DB7DA', align='edge')  # 막대 그리기
        ax.text(x_start + bar_width / 2, length + 10, f'{value:.1f}%', ha='center', va='bottom', fontsize=12)  # 비율 텍스트

    # 활동 구역 텍스트 추가
    ax.text(170, 425, "Home Third", ha='center', va='center', fontsize=11)
    ax.text(400, 425, "Middle Third", ha='center', va='center', fontsize=11)
    ax.text(610, 425, "Away Third", ha='center', va='center', fontsize=11)

    ax.imshow(nuri_pitch, extent=[5, 802.5, 2.5, 402.5])
    ax.axis('off')
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.show()


# 데이터 프레임을 이용하여 팀 A, 팀 B 데이터 생성
team_a, team_b = create_possession_frame(player_data)

# 시각화 함수 호출 및 저장
visual_possession(team_a, 'A', save_path=r"C:\krpython\adios-video\adios-video\Kyungran\TEAMA_possession.jpg")
visual_possession(team_b, 'B', save_path=r"C:\krpython\adios-video\adios-video\Kyungran\TEAMA_possession.jpg")


