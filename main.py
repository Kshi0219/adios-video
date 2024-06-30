import pickle
from utils import read_video,save_video
from tracker import Tracker
# from keypoint_detection import *
from draw_annotation import *
from team_assigner import *
from player_ball_assigner import *
import cv2
from perspective_changer import perspectiveChanger
from video_2_frames import video2frames

def main():
    # 영상 불러오기
    '''frames_left=read_video('input-video/test-left-1q.mp4')
    frames_right=read_video('input-video/test-right-1q.mp4')[10:]
    min_frame_len=min(len(frames_left),len(frames_right))
    frames_left=frames_left[:min_frame_len]
    frames_right=frames_right[:min_frame_len]'''
    video_path_left='input-video/test-left-1q.mp4'
    pic_path_left='input-pic/1q/left'
    video_path_right='input-video/test-right-1q.mp4'
    pic_path_right='input-pic/1q/right'
    frames_path='test/frames-1q-5(10fps).pkl'
    v2f=video2frames(frames_path)
    frame_dict=v2f.get_1fps(pic_path_left,pic_path_right,
                            video_path_left,video_path_right)
    frames_left=frame_dict['left']
    frames_right=frame_dict['right']

    # 기본 경기장 규격
    base_pitch=cv2.imread('test/img/nuri-futsal.png')

    # 트래커 클래스 시작
    model_path_player='model/best-player-detector.pt'
    model_path_ball='model/best-ball-detector.pt'
    tracker=Tracker(model_path_player,
                    model_path_ball)
    track_stub_path_left='track-stub/twp-tracks-left-3.pkl'
    track_stub_path_right='track-stub/twp-tracks-right-3.pkl'
    
    # 트래킹 결과 생성
    tracks_left=tracker.tracks_generator(frames_left,
                                    read_stub=True,
                                    stub_path=track_stub_path_left)
    tracks_right=tracker.tracks_generator(frames_right,
                                    read_stub=True,
                                    stub_path=track_stub_path_right)
    tracks=tracker.concat_tracks(tracks_left,tracks_right)
    
    # homography 적용
    homography_json_path='test/homography_dict.json'
    homograph_adapter=perspectiveChanger(homography_json_path)
    tracks_changed=homograph_adapter.perspective_transformer(tracks)
    
    # real tracks gen
    tracks_tr=tracker.real_tracks_gen(tracks_changed)

    # interpolate missing ball postion
    tracks_tr['ball']=Tracker().interpolate_ball(tracks_tr['ball'])

    # 유니폼 색 기반 팀 구분
    tracks_assigned=TeamAssigner().add_2_tracks(frames_left,frames_right,tracks_tr)

    # assign ball aquisition
    tracks_assigned_2=ballAssigner().add_2_tracks(tracks_assigned)

    with open('track-stub/twp-tracks-3.pkl','wb') as s1:
        pickle.dump(tracks_assigned_2,s1)
    
    """# 팀 정보 포함된 stub 저장
    with open('track-stub/tracks-concat-1.pkl','wb') as s:
        pickle.dump(tracks_assigned_2,s)
    '''with open(track_stub_path_left,'wb') as s_left:
        pickle.dump(tracks_assigned_2_left,s_left)
    
    with open(track_stub_path_right,'wb') as s_right:
        pickle.dump(tracks_assigned_2_right,s_right)'''

    # annotate
    output_frames=annotator().annotate(base_pitch,tracks_assigned_2)
    # output_frames_left=annotator().annotate(frames_left,tracks_assigned_2_left)
    # output_frames_right=annotator().annotate(frames_right,tracks_assigned_2_right)


    # annotate한 영상 저장
    save_video(output_frames,
               'output_video/concat_1.mp4')
    save_video(output_frames_left,
               'output-video/output-l/output_left_1q(2m).avi')
    save_video(output_frames_right,
               'output-video/output-l/output_right_1q(2m).avi')"""

if __name__=='__main__':
    main()