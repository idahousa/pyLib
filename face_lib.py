import dlib
import numpy as np
import cv2

def rect_to_box(i_rect):
    #Convert from rectangular of box to a bounding box
    #rect = (x1,x2,x3,x4) that represent the coordinates of left,right,up,bottom points of a rect
    #Return: a box with (x,y,width,height) of a bounding box.
    _x = i_rect.left() #TOP-LEFT POSITION
    _y = i_rect.top()  #TOP-LEFT POSITION
    _width = i_rect.right() - _x + 1   #Width of face box
    _height = i_rect.bottom() - _y + 1 #Height of face box
    return _x,_y,_width,_height

def shape_to_ndarray(i_shape,i_num_points=68):
    #_shape is the list of points which specify a shape of face
    #Return an array of the points which specify the shape
    #The use of this one is just for compatible with array manupulation.
    _rtn_array = np.zeros(shape=[i_num_points,2],dtype=np.int)
    for index in range(i_num_points):
        _rtn_array[index]=(i_shape.part(index).x,i_shape.part(index).y)
    return _rtn_array

def draw_circle_on_image(i_image,i_point,i_radius = 1, i_color = 'red'):
    #i_color is the color to be draw in the circle.
    #i_point = (x,y) is the coordinate of the center point of circle.
    _shape = i_image.shape
    if len(_shape)==2: #i_image is a gray image
        for _x in range(i_radius*2):
            for _y in range(i_radius*2):
                _pos_x = i_point[0] + _x-i_radius
                _pos_y = i_point[1] + _y-i_radius
                i_image[_pos_y,_pos_x]=255
        return i_image
    elif len(_shape)==3:#i_image is a color image
        if i_color == 'red':
            for _x in range(i_radius * 2):
                for _y in range(i_radius * 2):
                    _pos_x = i_point[0] + _x - i_radius
                    _pos_y = i_point[1] + _y - i_radius
                    i_image[_pos_y, _pos_x, 0] = 255
                    i_image[_pos_y, _pos_x, 1] = 0
                    i_image[_pos_y, _pos_x, 2] = 0
            return i_image
        elif i_color == 'blue':
            for _x in range(i_radius * 2):
                for _y in range(i_radius * 2):
                    _pos_x = i_point[0] + _x - i_radius
                    _pos_y = i_point[1] + _y - i_radius
                    i_image[_pos_y, _pos_x, 0] = 0
                    i_image[_pos_y, _pos_x, 1] = 255
                    i_image[_pos_y, _pos_x, 2] = 0
            return i_image
        else:
            return i_image
    else:
        return i_image

def draw_shape_on_image(i_image,i_shape,i_radius=1,i_color='red'):
    #i_points is an ndarray with shape of [m,2] where m is numbr of points.
    if len(i_shape.shape) !=2:
        return i_image
    _num_points,_ = i_shape.shape
    for _index in range(_num_points):
        i_point = i_shape[_index,:]
        i_image = draw_circle_on_image(i_image=i_image,i_point=i_point,i_radius=i_radius,i_color=i_color)
    return i_image

def find_faces(i_image,i_detector,i_up_sample_level=1,i_rtn_box=True):
    #Find a face at a specific level of upsampling.
    #_rtn_box = True  => Return the bounding box of face with format (x,y,widht,height)
    #_rtn_box = False => Return the bounding rect of face with format (x1,y1,x2,y2)
    _faces = i_detector(i_image,i_up_sample_level)
    if i_rtn_box:
        o_rtn_faces = []
        for face in enumerate(_faces):
            _x, _y, _width, _height = rect_to_box(face)
            o_rtn_faces.append([_x, _y, _width, _height])
        return o_rtn_faces
    else:
        return _faces

def find_small_faces(i_image,i_detector,i_max_upsample_level=3,i_rtn_box=True):
    #Use this function for detect small faces in a given image.
    #This function will find a face according to up_sample_level until it sucessfully find a face
    # _rtn_box = True  => Return the bounding box of face with format (x,y,widht,height)
    # _rtn_box = False => Return the bounding rect of face with format (x1,y1,x2,y2)
    for level in range(i_max_upsample_level):
        #print('Level {}'.format(level))
        o_faces = find_faces(i_image=i_image,i_detector=i_detector,i_up_sample_level=level+1,i_rtn_box=i_rtn_box)
        if len(o_faces)>0:
            return o_faces
    return []

def find_facial_landmarks_rect(i_image,i_shape_predictor,i_face_rect):
    #Detect facial landmark points of a face using dlib.
    #Reference: https://www.pyimagesearch.com/2017/04/03/facial-landmarks-dlib-opencv-python/
    #rect = (x1,x2,x3,x4) that represent the coordinates of left,right,up,bottom points of a rect
    #Note: _face_rect is a result of face detection
    _shape = i_shape_predictor(i_image,i_face_rect)
    o_shape = shape_to_ndarray(_shape)
    return o_shape

def find_facial_landmarks_image(i_image,i_face_detector,i_face_shape_detector):
    #Detect any face from input image
    _faces = find_small_faces(i_image=i_image,i_detector=i_face_detector,i_rtn_box=False)
    _num_face = len(_faces)
    if _num_face<=0:
        return
    o_shapes = np.zeros(shape=[_num_face,68,2],dtype=np.int)
    for _index,_face in enumerate(_faces):
        _shape = find_facial_landmarks_rect(i_image=i_image,i_shape_predictor=i_face_shape_detector,i_face_rect=_face)
        o_shapes[_index]=_shape
    return o_shapes

def rotate_image(i_image,i_center,i_angle):
    #Rotate the i_image around i_center with i_angle degree.
    #i_angle is the rotation angle in degree
    _height,_width,_nchannel = i_image.shape
    _rotate_matrix = cv2.getRotationMatrix2D(center=i_center,angle=i_angle,scale=1)
    i_image = cv2.warpAffine(src=i_image,M=_rotate_matrix,dsize=(_width,_height))
    return i_image,_rotate_matrix

def find_center_of_point_sequence(i_shape,i_start=0,i_stop=68):
    #i_shape is the (68,2) landmark points
    _x = 0
    _y = 0
    _cnt = 0
    for _index in range(68):
        if (_index>=i_start) and (_index<i_stop):
            _x += i_shape[_index, 0]
            _y += i_shape[_index, 1]
            _cnt +=1
    _x /= _cnt
    _y /= _cnt
    return _x,_y

def normalize_face(i_image,i_shape):
    #i_shape is an numpy.ndarray of the shape of (68,2) that specifies the landmark coordinate of landmark points
    _left_eye_x, _left_eye_y = find_center_of_point_sequence(i_shape=i_shape, i_start=36, i_stop=42)
    _right_eye_x, _right_eye_y = find_center_of_point_sequence(i_shape=i_shape, i_start=42, i_stop=48)
    _center_face_x, _center_face_y = find_center_of_point_sequence(i_shape=i_shape, i_start=31, i_stop=36)
    _diff_x = _right_eye_x - _left_eye_x
    _diff_y = _right_eye_y - _left_eye_y
    _rotate_angle = np.arctan(_diff_y/_diff_x) #Return as the angle from [-pi/2 pi/2]
    _rotate_angle *= (180./np.pi)
    o_image,rot_matrix = rotate_image(i_image=i_image,i_center=(_center_face_y,_center_face_x),i_angle=_rotate_angle)
    o_shape = np.zeros_like(i_shape)
    for _index in range(68):
        o_shape[_index, 0] = i_shape[_index, 0] * rot_matrix[0, 0] + i_shape[_index, 1] * rot_matrix[0, 1] + rot_matrix[0, 2]
        o_shape[_index, 1] = i_shape[_index, 0] * rot_matrix[1, 0] + i_shape[_index, 1] * rot_matrix[1, 1] + rot_matrix[1, 2]
    return o_image,o_shape

def extract_face_region(i_image,i_shape,i_dsize=(224,224),i_extend_size = 10):
    #Extract an face from image.
    #Resize to a specific size
    _height,_width,_nchannel = i_image.shape
    o_image, o_shape = normalize_face(i_image=i_image,i_shape=i_shape)
    _min_x,_min_y = o_shape.min(axis=0)
    _max_x,_max_y = o_shape.max(axis=0)
    _min_x -= i_extend_size
    _max_x += i_extend_size
    _min_y -= i_extend_size
    _max_y += i_extend_size
    if _min_x<0:
        _min_x=0
    if _min_y<0:
        _min_y=0
    if _max_x>_width:
        _max_x=_width
    if _max_y>_height:
        _max_y=_height
    _face_roi = o_image[_min_y:_max_y,_min_x:_max_x,:]
    return cv2.resize(src=_face_roi,dsize=i_dsize)

if __name__=='__main__':
    face_detector = dlib.get_frontal_face_detector()
    shape_predictor = dlib.shape_predictor('face_shape_predictor/shape_predictor_68_face_landmarks.dat')
    image = dlib.load_rgb_image('images/image2.jpg')
    height,width,channel = image.shape
    image,_ = rotate_image(i_image=image,i_center=(height/2,width/2),i_angle=30)
    face_shapes = find_facial_landmarks_image(i_image=image,i_face_detector=face_detector,i_face_shape_detector=shape_predictor)
    [num_faces,num_point,num_coordinate] = face_shapes.shape
    for index in range(num_faces):
        shape = face_shapes[index,:,:].reshape((num_point,num_coordinate))
        face_roi = extract_face_region(i_image=image,i_shape=shape,i_extend_size=0)
        dlib.save_image(face_roi, 'face_roi.jpg')
        draw_shape_on_image(i_image=image, i_shape=shape, i_radius=2, i_color='blue')
        image,new_shape = normalize_face(i_image=image,i_shape=shape)
        draw_shape_on_image(i_image=image, i_shape=new_shape, i_radius=2)
    dlib.save_image(image,'shape2.jpg')

