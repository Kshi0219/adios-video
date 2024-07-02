import cv2
import sys 
import pandas as pd
import pickle

class statGenerator:
    def __init__(self):
        self.frame_window=5
        self.frame_rate=10

    def speed_distance_to_tracks(self,tracks):
        self.tracks=tracks
        total_distance={}
        for frame_num,values in enumerate(tracks['players']):
            if frame_num in list(range(0,len(tracks['players'],self.frame_window))):
                last_frame=min(frame_num+self.frame_window,len(tracks['players'])-1)
                for track_id,_ in values.items():
                    if track_id not in tracks['players'][last_frame]:
                        continue
                    start_position=values[track_id]['coord_tr']
                    end_position=tracks['players'][last_frame][track_id]['coord_tr']

                    if start_position is None or end_position is None:
                        continue

                    # 픽셀 단위를 실제 거리 단위로 변환
                    distance_covered_x = (end_position[0] - start_position[0])/40
                    distance_covered_y = (end_position[1] - start_position[1])/40
                    distance_covered = (distance_covered_x**2 + distance_covered_y**2)**0.5 # 미터 단위

                    time_elapsed = (last_frame - frame_num) / self.frame_rate
                    speed_meters_per_second = distance_covered / time_elapsed
                    speed_km_per_hour = (speed_meters_per_second)*3.6

                    if object not in total_distance:
                        total_distance[object] = {}
                    
                    if track_id not in total_distance[object]:
                        total_distance[object][track_id] = 0
                    
                    total_distance[object][track_id] += distance_covered

                    for frame_num_batch in range(frame_num, last_frame):
                        if track_id not in tracks[object][frame_num_batch]:
                            continue
                        tracks[object][frame_num_batch][track_id]['speed'] = speed_km_per_hour
                        tracks[object][frame_num_batch][track_id]['distance'] = total_distance[object][track_id]
            else: continue
            return tracks