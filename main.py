import cv2
import code
import apriltag

cap = cv2.VideoCapture(0)

while True:
    ret, orig = cap.read()
    gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
    options = apriltag.DetectorOptions(families="tag16h5")
    
    detector = apriltag.Detector(options)
    results = detector.detect(gray)
    output = cv2.cvtColor(src=orig, code=cv2.COLOR_BGR2RGB)
    
    # loop over the AprilTag detection results
    # print(f'Tags found: {len(results)}')
    for r in results:
        # skip low confidence images
        if r.decision_margin < 30 or r.hamming > 0:
            continue
        print(r.tag_id)
        if r.tag_id != 1:
            code.interact(local=locals())
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
        tagFamily = str(r.decision_margin)
        cv2.putText(output, tagFamily, (ptA[0], ptA[1] - 15),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        print("[INFO] tag family: {}".format(tagFamily))

    cv2.imshow('webcam', output)
    if cv2.waitKey(30) & 0xFF == ord('q'):
       break
cap.release()
cv2.destroyAllWindows()