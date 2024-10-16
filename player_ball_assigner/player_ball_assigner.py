import sys 
sys.path.append('../')
from utils import get_center_of_bbox, measure_distance

class PlayerBallAssigner():
    def __init__(self):
        self.max_player_ball_distance = 70
    
    # closest player to the ball is assigned in control within 70 pixels
    def assign_ball_to_player(self,players,ball_bbox):
        ball_position = get_center_of_bbox(ball_bbox)

        minimum_distance = 99999
        assigned_player=-1

        for player_id, player in players.items():   # loop through each player
            player_bbox = player['bbox']

            distance_left = measure_distance((player_bbox[0],player_bbox[-1]),ball_position)
            distance_right = measure_distance((player_bbox[2],player_bbox[-1]),ball_position)
            distance = min(distance_left,distance_right)

            if distance < self.max_player_ball_distance: # if within max distance
                if distance < minimum_distance: # if new minimum is found then update new values
                    minimum_distance = distance
                    assigned_player = player_id

        return assigned_player