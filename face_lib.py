import dlib
import numpy as np

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

def draw_circle_on_image(i_image,i_point,i_radius = 1):
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
        for _x in range(i_radius * 2):
            for _y in range(i_radius * 2):
                _pos_x = i_point[0] + _x - i_radius
                _pos_y = i_point[1] + _y - i_radius
                i_image[_pos_y, _pos_x, 0] = 255
                i_image[_pos_y, _pos_x, 1] = 0
                i_image[_pos_y, _pos_x, 2] = 0
        return i_image
    else:
        return i_image

def draw_shape_on_image(i_image,i_shape,i_radius=1):
    #i_points is an ndarray with shape of [m,2] where m is numbr of points.
    if len(i_shape.shape) !=2:
        return i_image
    _num_points,_ = i_shape.shape
    for _index in range(_num_points):
        i_point = i_shape[_index,:]
        i_image = draw_circle_on_image(i_image=i_image,i_point=i_point,i_radius=i_radius)
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
        print('Level {}'.format(level))
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

if __name__=='__main__':
    face_detector = dlib.get_frontal_face_detector()
    shape_predictor = dlib.shape_predictor('face_shape_predictor/shape_predictor_68_face_landmarks.dat')
    image = dlib.load_rgb_image('images/image2.jpg')
    face_shapes = find_facial_landmarks_image(i_image=image,i_face_detector=face_detector,i_face_shape_detector=shape_predictor)
    print(face_shapes)
    print(face_shapes.shape)
    [num_faces,num_point,num_coordinate] = face_shapes.shape
    for index in range(num_faces):
        shape = face_shapes[index,:,:].reshape((num_point,num_coordinate))
        draw_shape_on_image(i_image=image,i_shape=shape,i_radius=2)
    dlib.save_image(image,'shape2.jpg')
