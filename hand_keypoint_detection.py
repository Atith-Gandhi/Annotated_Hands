import cv2
import os
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# For static images:
file_path = './datasets/sign_language_dataset/'
IMAGE_FILES = os.listdir(file_path)
max_image_count = 10000
print(IMAGE_FILES[0])

# font
font = cv2.FONT_HERSHEY_SIMPLEX
  
# org
org = (50, 50)
  
# fontScale
fontScale = 0.6
   
# Blue color in BGR
color = (255, 0, 0)
  
# Line thickness of 2 px
thickness = 1

with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0,
    min_tracking_confidence = 0) as hands:
  img_count = 0
  for idx, file in enumerate(IMAGE_FILES):
    
    # print(idx)
    if '.png' not in file and '.jpg' not in file:
      continue
    if(img_count == max_image_count):
      break
    # Read an image, flip it around y-axis for correct handedness output (see
    # above).
    image = cv2.flip(cv2.imread(f'{file_path}{file}'), 1)
    # print(image)
    # print(f'./datasets/one_hand/{file}')
    # Convert the BGR image to RGB before processing.
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Print handedness and draw hand landmarks on the image.
    # print('Handedness:', results.multi_handedness)
    if not results.multi_hand_landmarks:
      print(file)
      continue
    
    img_count += 1
    image_height, image_width, _ = image.shape
    annotated_image = image.copy()
    j = 0
    for hand_landmarks in results.multi_hand_landmarks:
      # if j <= 1:
      #   j += 1
      #   continue
      # print('hand_landmarks:', mp_hands.HandLandmark)
      # print(
      #     f'Index finger tip coordinates: (',
      #     f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
      #     f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
      # )
      fingertips = np.zeros((21, 3))
      
      c = 0
      for landmark in mp_hands.HandLandmark:
        # print(landmark)
        fingertips[c][0] = hand_landmarks.landmark[landmark].x
        fingertips[c][1] = hand_landmarks.landmark[landmark].y
        fingertips[c][2] = hand_landmarks.landmark[landmark].z
        # if(idx == 8):
        #   print(fingertips[c])
        c += 1
      
      # fingertips = np.asarray(fingertips)
      np.set_printoptions(suppress=True)
      # print(fingertips.shape)
      # if(idx == 8):
      #   print(np.array(fingertips))
        

      mp_drawing.draw_landmarks(
          annotated_image,
          hand_landmarks,
          mp_hands.HAND_CONNECTIONS,
          mp_drawing_styles.get_default_hand_landmarks_style(),
          mp_drawing_styles.get_default_hand_connections_style())
      
      c = 0
      for landmark in mp_hands.HandLandmark:
        org = (int(255*hand_landmarks.landmark[landmark].x), int(255*hand_landmarks.landmark[landmark].y))
        # print(org)
        # annotated_image = cv2.putText(annotated_image, str(c), org, font, fontScale, color, thickness)
        # print(fingertips[c])
        c += 1
      # print('Line 104')
    # cv2.imwrite(
    #     './One_Hand_mediapipe/annotated_image' + str(idx) + '.png', cv2.flip(annotated_image, 1))
    cv2.imwrite(
        './sign_language_annotated_images_3_channels/' + file[:-4] + '_annotated_image.png', cv2.flip(annotated_image, 1))
    
    # print(np.shape(fingertips))
    np.save('./sign_language_One_Hand_preprocessed_generated_results/fingertips_' + file[:-4]  + '.npy', np.asarray(fingertips))

    for i, hand_handedness in enumerate(results.multi_handedness):
      # print(hand_handedness.classification)
      handedness =  hand_handedness.classification[0].label
      # print(handedness)
      if handedness == 'Right':
        np.save('./sign_language_One_Hand_preprocessed_generated_results/handedness_' + file[:-4]  + '.npy', np.asarray(1))
      elif handedness == 'Left':
        np.save('./sign_language_One_Hand_preprocessed_generated_results/handedness_' + file[:-4]  + '.npy', np.asarray(0))
    # Draw hand world landmarks.
    print('Line 122')
    if not results.multi_hand_world_landmarks:
      print(file)
      continue
    # for hand_world_landmarks in results.multi_hand_world_landmarks:
    #   mp_drawing.plot_landmarks(
    #     hand_world_landmarks, mp_hands.HAND_CONNECTIONS, azimuth=5)x
