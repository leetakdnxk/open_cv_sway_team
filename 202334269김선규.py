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

best_scale, best_kp1, best_kp2, best_matches = multiscale_matching(img1, img2, gray1, gray2)