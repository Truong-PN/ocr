import cv2

refPt = []
final_boundaries = []
image = None

def horizontal_to_rect(horizontal: list) -> list:
    l,r,t,b = horizontal
    tr = [r,t]
    br = [r,b]
    bl = [l,b]
    tl = [l,t]
    rect = [tr, br, bl, tl]
    return rect

def click_and_crop(event, x, y, flags, param):
    global refPt, image
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x, y))
        final_boundaries.append((refPt[0],refPt[1]))
        rect = [refPt[0][0],refPt[1][0], refPt[0][1], refPt[1][1]]
        rects = horizontal_to_rect(rect)
        print(rects)
        cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow("image", image)
    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        clone = image.copy()
        cv2.rectangle(clone, refPt[0], (x, y), (0, 255, 0), 2)
        cv2.imshow("image", clone)


def main(path):
    global image
    image = cv2.imread(path) #convert to image boundary
    image = cv2.resize(image, [900, 600])
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_and_crop)
    cv2.imshow("image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return (final_boundaries)

if __name__ == "__main__":
    path = "crop.jpg"
    main(path)