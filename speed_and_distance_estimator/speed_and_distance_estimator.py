import cv2
import sys
sys.path.append('../')
from utils import measure_distance, get_foot_position


class SpeedAndDistanceEstimator:
    def __init__(self):
        self.frame_window = 5
        self.frame_rate = 24 

    def add_speed_and_distance_to_tracks(self, tracks):
        total_distance = {}

        for object, object_tracks in tracks.items():
            if object == 'ball' or object == 'referees':
                continue
            number_of_frames = len(object_tracks)
            for frame_num in range(0, number_of_frames, self.frame_window): # 0, 5, 10, ...
                last_frame = min(frame_num+self.frame_window, number_of_frames-1)

                for track_id, _ in object_tracks[frame_num].items():
                    if track_id not in object_tracks[last_frame]:   # skip player if they are not in frame for the entire batch
                        continue
                    
                    start_position = object_tracks[frame_num][track_id]['position_transformed']
                    end_position = object_tracks[last_frame][track_id]['position_transformed']

                    if start_position is None or end_position is None:  # if player position is outside our transformed polygon then we can't calculate speed/distance
                        continue
                    
                    distance_covered = measure_distance(start_position, end_position)   # meters
                    time_elapsed = (last_frame-frame_num)/self.frame_rate   # per second
                    speed_meters_per_sec = distance_covered / time_elapsed
                    speed_km_per_hour = speed_meters_per_sec * 3.6  # conventional metric

                    if object not in total_distance:    # add new object to dict
                        total_distance[object] = {}

                    if track_id not in total_distance[object]:  # total distance will now start to be counted
                        total_distance[object][track_id] = 0
                    
                    total_distance[object][track_id] += distance_covered

                    for frame_num_batch in range(frame_num, last_frame):    # add speed and distance values to tracks 
                        if track_id not in tracks[object][frame_num_batch]:
                            continue
                        tracks[object][frame_num_batch][track_id]['speed'] = speed_km_per_hour
                        tracks[object][frame_num_batch][track_id]['distance'] = total_distance[object][track_id]

    def draw_speed_and_distance(self, frames, tracks):
        output_frames = []
        for frame_num, frame in enumerate(frames):
            for object, object_tracks in tracks.items():
                if object == 'ball' or object == 'referees':
                    continue
                for _, track_info in object_tracks[frame_num].items():
                    if 'speed' in track_info:
                        speed = track_info.get('speed', None)
                        distance = track_info.get('distance', None)
                        if speed is None or distance is None:   # if either is missing then skip
                            continue

                        bbox = track_info['bbox']
                        position = get_foot_position(bbox)  # position the text under ellipse ring
                        position = list(position)
                        position[1]+= 40    # buffer to prevent overlap on the overlay

                        position = tuple(map(int, position))
                        cv2.putText(frame, f"{speed:.2f} km/h", position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
                        cv2.putText(frame, f"{distance:.2f} m", (position[0], position[1]+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)

            output_frames.append(frame)
        return output_frames     