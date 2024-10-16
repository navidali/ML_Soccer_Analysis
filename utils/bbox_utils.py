def get_center_of_bbox(bbox):
    x1,y1,x2,y2 = bbox
    return int((x1+x2)/2),int((y1+y2)/2) # return x and y midpoints

def get_bbox_width(bbox):   
    return bbox[2]-bbox[0]

def measure_distance(p1,p2):    # measures the distances between 2 points as a 1d num
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5

def measure_xy_distance(p1,p2): # measures the distances between 2 points as a 2d num
    return p1[0]-p2[0],p1[1]-p2[1]

def get_foot_position(bbox):    # return bottom center point of bbox
    x1,y1,x2,y2 = bbox
    return int((x1+x2)/2),int(y2)