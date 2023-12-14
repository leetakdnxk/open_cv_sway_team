import cv2
import numpy as np

new_width = 800  # 새로운 이미지의 너비
new_height = 600  # 새로운 이미지의 높이

img1 = cv2.imread('star.jpg')  # 찾을 대상 단독 이미지
img1 = cv2.resize(img1, (new_width, new_height))  # 새로운 너비와 높이로 이미지 크기 조절
img2 = cv2.imread('mixedimg.jpg')  # 찾을 대상이 존재하는 이미지
img2 = cv2.resize(img2, (new_width, new_height))  # 새로운 너비와 높이로 이미지 크기 조절
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# 노이즈 제거 함수 정의 
def remove_noise(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ksize = (5, 5)
    blurred_image = cv2.GaussianBlur(gray_image, ksize, 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opened_image = cv2.morphologyEx(blurred_image, cv2.MORPH_OPEN, kernel)
    return opened_image

# 이미지 노이즈 제거 
img1_denoised = remove_noise(img1)
img2_denoised = remove_noise(img2)


# 멀티스케일 매칭
def multiscale_matching(img1, img2, gray1, gray2):
    ratio = 0.75
    max_matches = 0
    best_scale = 1.0

    for scale in np.linspace(0.1, 1.0, 20)[::-1]:
        resized_gray1 = cv2.resize(gray1, (int(gray1.shape[1] * scale), int(gray1.shape[0] * scale)))
        resized_gray2 = cv2.resize(gray2, (int(gray2.shape[1] * scale), int(gray2.shape[0] * scale)))

        detector = cv2.ORB_create()
        kp1, desc1 = detector.detectAndCompute(resized_gray1, None)
        kp2, desc2 = detector.detectAndCompute(resized_gray2, None)

        matcher = cv2.BFMatcher(cv2.NORM_HAMMING2)
        matches = matcher.knnMatch(desc1, desc2, 2)

        good_matches = [first for first, second in matches if first.distance < second.distance * ratio]

        if len(good_matches) > max_matches:
            max_matches = len(good_matches)
            best_scale = scale
            best_kp1 = kp1
            best_kp2 = kp2
            best_matches = good_matches

    return best_scale, best_kp1, best_kp2, best_matches

# 멀티스케일 매칭 결과 얻기 
best_scale, best_kp1, best_kp2, best_matches = multiscale_matching(img1_denoised, img2_denoised, gray1, gray2)
# ORB, BF-Hamming 으로 knnMatch  
detector = cv2.ORB_create()
kp1, desc1 = detector.detectAndCompute(gray1, None)
kp2, desc2 = detector.detectAndCompute(gray2, None)
matcher = cv2.BFMatcher(cv2.NORM_HAMMING2)
matches = matcher.knnMatch(desc1, desc2, 2)

# 이웃 거리의 75%로 좋은 매칭점 추출
ratio = 0.75
good_matches = [first for first,second in matches \
                    if first.distance < second.distance * ratio]
print('good matches:%d/%d' %(len(good_matches),len(matches)))

# 좋은 매칭점의 queryIdx로 원본 영상의 좌표 구하기 
src_pts = np.float32([ kp1[m.queryIdx].pt for m in good_matches ])
# 좋은 매칭점의 trainIdx로 대상 영상의 좌표 구하기 
dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good_matches ])
# 원근 변환 행렬 구하기 
mtrx, mask = cv2.findHomography(src_pts, dst_pts)
# 원본 영상 크기로 변환 영역 좌표 생성 
h,w, = img1.shape[:2]
pts = np.float32([ [[0,0]],[[0,h-1]],[[w-1,h-1]],[[w-1,0]] ])
# 원본 영상 좌표를 원근 변환  
dst = cv2.perspectiveTransform(pts,mtrx)
# 변환 좌표 영역을 대상 영상에 그리기 
img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)

# 좋은 매칭 그려서 출력 
res = cv2.drawMatches(img1, kp1, img2, kp2, good_matches, None, \
                    flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)
cv2.imshow('Matching Homography', res)

# 좋은 매칭 그려서 출력 
res = cv2.drawMatches(img1, kp1, img2, kp2, good_matches, None, \
                    flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)

# 좋은 매칭점의 평균 위치 계산 
average_pt1 = np.mean(np.array([kp1[m.queryIdx].pt for m in good_matches]), axis=0)
average_pt2 = np.mean(np.array([kp2[m.trainIdx].pt for m in good_matches]), axis=0)
text_position_pt1 = (int(average_pt1[0]), int(average_pt1[1] + 20))  # pt1 주변
text_position_pt2 = (int(average_pt2[0]), int(average_pt2[1] + 20))  # pt2 주변

# 좋은 매칭점 주변에 "별"이라는 글자 출력 
font_size = 1  # 폰트 크기
font_color = (255, 255, 255)  # 폰트 색상 (흰색)
font_thickness = 3 # 폰트 굵기

cv2.putText(img1, 'Star', text_position_pt1, cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)
cv2.putText(img2, 'Star', text_position_pt2, cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, font_thickness)

# 결과 이미지 출력
cv2.imshow('Matching Homography', res)
cv2.imshow('Image 1 with Star', img1)
cv2.imshow('Image 2 with Star', img2)
cv2.waitKey()
cv2.destroyAllWindows()

# cv2.imwrite('star_result.jpg',res)
