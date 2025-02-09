import cv2
import numpy as np


def extract_lined_paper(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, 190], dtype=np.uint8)
    upper_white = np.array([180, 50, 255], dtype=np.uint8)

    mask = cv2.inRange(hsv, lower_white, upper_white)

    mask = cv2.GaussianBlur(mask, (5, 5), 0)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    largest_contour = max(contours, key=cv2.contourArea)

    epsilon = 0.02 * cv2.arcLength(largest_contour, True)
    approx = cv2.approxPolyDP(largest_contour, epsilon, True)

    if len(approx) == 4:
        x, y, w, h = cv2.boundingRect(approx)
    else:
        x, y, w, h = cv2.boundingRect(largest_contour)

    cropped = image[y:y+h, x:x+w]
    return cropped


def increase_contrast(image, alpha=1.3, beta=0):
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)


def deskew_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Detect lines using Hough Line Transform
    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=100)  # Adjusted threshold

    if lines is not None:
        angles = []
        for line in lines:
            rho, theta = line[0]  # Correct unpacking
            angle = (theta * 180 / np.pi) - 90  # Convert to degrees
            if -15 < angle < 15:  # Keep only near-horizontal lines
                angles.append(angle)

        if angles:
            median_angle = np.median(angles)  # Get the median angle

            # Rotate only if skew is significant (>1 degree)
            if abs(median_angle) > 1:
                h, w = image.shape[:2]
                center = (w // 2, h // 2)
                rotation_matrix = cv2.getRotationMatrix2D(center, median_angle, 1.0)
                rotated = cv2.warpAffine(image, rotation_matrix, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
            else:
                rotated = image  # No rotation needed
        else:
            rotated = image  # No valid lines found
    else:
        rotated = image  # No lines found

    return rotated


def lil_extra_crop(image):
    h, w = image.shape[:2]
    crop_x = int(w * 0.15)
    crop_y = int(h * 0.15)

    cropped = image[crop_y:h - crop_y, crop_x:w - crop_x]
    return cropped


def output_final(image_path):
    deskewed_image = deskew_image(image_path)
    contrasted_image = increase_contrast(deskewed_image)
    cropped_paper = extract_lined_paper(contrasted_image)

    # Apply additional cropping
    final_cropped = lil_extra_crop(cropped_paper)

    # Save and show images
    cv2.imwrite("final_output.jpg", final_cropped)
    cv2.imshow("Deskewed Image", deskewed_image)
    cv2.imshow("Contrast Enhanced", contrasted_image)
    cv2.imshow("Final Output", final_cropped)
    cv2.waitKey(0)

output_final("winghack.png")

