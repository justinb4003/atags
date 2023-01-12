import cv2
import code
import numpy
import apriltag

def draw_pose(overlay, camera_params, tag_size, pose, z_sign=1):

    opoints = numpy.array([
        -1, -1, 0,
         1, -1, 0,
         1,  1, 0,
        -1,  1, 0,
        -1, -1, -2*z_sign,
         1, -1, -2*z_sign,
         1,  1, -2*z_sign,
        -1,  1, -2*z_sign,
    ]).reshape(-1, 1, 3) * 0.5*tag_size

    edges = numpy.array([
        0, 1,
        1, 2,
        2, 3,
        3, 0,
        0, 4,
        1, 5,
        2, 6,
        3, 7,
        4, 5,
        5, 6,
        6, 7,
        7, 4
    ]).reshape(-1, 2)
        
    fx, fy, cx, cy = camera_params

    K = numpy.array([fx, 0, cx, 0, fy, cy, 0, 0, 1]).reshape(3, 3)

    rvec, _ = cv2.Rodrigues(pose[:3,:3])
    tvec = pose[:3, 3]

    dcoeffs = numpy.zeros(5)

    ipoints, _ = cv2.projectPoints(opoints, rvec, tvec, K, dcoeffs)

    ipoints = numpy.round(ipoints).astype(int)
    
    ipoints = [tuple(pt) for pt in ipoints.reshape(-1, 2)]

    for i, j in edges:
        cv2.line(overlay, ipoints[i], ipoints[j], (0, 255, 0), 1, 16)

# t480s properties
fx, fy, cx, cy = (9973.977159660377, 9432.229890251116, 470.03687743610527, 239.154470602995)
camera_params = (fx, fy, cx, cy)

cap = cv2.VideoCapture(0)

while True:
    ret, orig = cap.read()
    gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
    options = apriltag.DetectorOptions(families="tag16h5")
    
    detector = apriltag.Detector(options)
    results = detector.detect(gray)
    output = orig # cv2.cvtColor(src=orig, code=cv2.COLOR_BGR2RGB)
    
    # loop over the AprilTag detection results
    # print(f'Tags found: {len(results)}')
    for r in results:
        pose, e0, e1 = detector.detection_pose(r, camera_params, 1, 1)
        # skip low confidence images
        draw_pose(output, camera_params, 1, pose, 1)
        if r.decision_margin < 30 or r.hamming > 4:
            continue
        print(r.tag_id)
        # extract the bounding box (x, y)-coordinates for the AprilTag
        # and convert each of the (x, y)-coordinate pairs to integers
        (ptA, ptB, ptC, ptD) = r.corners
        ptB = (int(ptB[0]), int(ptB[1]))
        ptC = (int(ptC[0]), int(ptC[1]))
        ptD = (int(ptD[0]), int(ptD[1]))
        ptA = (int(ptA[0]), int(ptA[1]))
        # draw the bounding box of the AprilTag detection
        cv2.line(output, ptA, ptB, (0, 255, 0), 2)
        cv2.line(output, ptB, ptC, (0, 255, 0), 2)
        cv2.line(output, ptC, ptD, (0, 255, 0), 2)
        cv2.line(output, ptD, ptA, (0, 255, 0), 2)
        # draw the center (x, y)-coordinates of the AprilTag
        (cX, cY) = (int(r.center[0]), int(r.center[1]))
        cv2.circle(output, (cX, cY), 5, (0, 0, 255), -1)
        

        # Label it with something for now
        tagFamily = str(r.tag_id)
        cv2.putText(output, tagFamily, (ptA[0], ptA[1] - 15),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        print("[INFO] tag family: {}".format(tagFamily))

    cv2.imshow('webcam', output)
    if cv2.waitKey(30) & 0xFF == ord('q'):
       break
cap.release()
cv2.destroyAllWindows()
