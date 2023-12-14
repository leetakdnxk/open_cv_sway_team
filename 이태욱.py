# 별들의 평균 위치 계산 
average_pt1 = np.mean(np.array([kp1[m.queryIdx].pt for m in good_matches]), axis=0)
average_pt2 = np.mean(np.array([kp2[m.trainIdx].pt for m in good_matches]), axis=0)
text_position_pt1 = (int(average_pt1[0]), int(average_pt1[1] + 20))  
text_position_pt2 = (int(average_pt2[0]), int(average_pt2[1] + 20))  

# 평균 위치에 "별"이라는 글자 출력
font_size = 1  # 폰트 크기
font_color = (255, 255, 255)  # 폰트 색상 (흰색)
font_thickness = 2 # 폰트 굵기

cv2.putText(img1, 'Star', text_position_pt1, cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
cv2.putText(img2, 'Star', text_position_pt2, cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)

# 결과 이미지 출력(사진1,사진2, 최종 sifo 사진 출력)
cv2.imshow('Matching Homography', res)
cv2.imshow('Image 1 with Star', img1)
cv2.imshow('Image 2 with Star', img2)
