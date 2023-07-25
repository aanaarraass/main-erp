# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

import cv2
import numpy as np
from PIL import Image
from odoo.modules.module import get_module_resource

display_height = int(640)
display_width = int(640)
windowWidth = 1280
windowHeight = 720
uniform_height = int(1231 / 1.5)
uniform_width = int(1000 / 1.5)
saveimglvl = 0
showimglvl = 4
ERODE_SUB_OFF = 1
thresholdVar = 0.41
thresholdCircle = 0.3
marker_rescale_range = (35, 100)
marker_rescale_steps = 10
thresholdCircles = []
windowX, windowY = 0, 0
MIN_PAGE_AREA = 80000


class Cropimage():
    def appendSaveImg(key, img):
        if (saveimglvl >= int(key)):
            global saveImgList
            if (key not in saveImgList):
                saveImgList[key] = []
            saveImgList[key].append(img.copy())

    def order_points(pts):
        rect = np.zeros((4, 2), dtype="float32")

        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        # return the ordered coordinates
        return rect

    def four_point_transform(image, pts):
        rect = Cropimage.order_points(pts)
        (tl, tr, br, bl) = rect

        # compute the width of the new image, which will be the
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))

        maxWidth = max(int(widthA), int(widthB))
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")

        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

        return warped

    def resize_util(img, u_width, u_height=None):
        if u_height is None:
            h, w = img.shape[:2]
            u_height = int(h * u_width / w)
        return cv2.resize(img, (int(u_width), int(u_height)))

    def show(name, orig, pause=1, resize=False, resetpos=None):
        global windowX, windowY
        if isinstance(orig, type(None)):
            if (pause):
                cv2.destroyAllWindows()
            return
        img = Cropimage.resize_util(orig, display_width, display_height) \
            if resize else orig
        cv2.imshow(name, img)
        if (resetpos):
            windowX = resetpos[0]
            windowY = resetpos[1]
        cv2.moveWindow(name, windowX, windowY)

        h, w = img.shape[:2]
        margin = 25
        w += margin
        h += margin
        if (windowX + w > windowWidth):
            windowX = 0
            if (windowY + h > windowHeight):
                windowY = 0
            else:
                windowY += h
        else:
            windowX += w

        if (pause):
            Cropimage.waitQ()

    def resize_util_h(img, u_height, u_width=None):
        if u_width is None:
            h, w = img.shape[:2]
            u_width = int(w * u_height / h)
        return cv2.resize(img, (int(u_width), int(u_height)))

    def getBestMatch(image_eroded_sub, marker):

        descent_per_step = \
            (marker_rescale_range[1] -
             marker_rescale_range[0]) // marker_rescale_steps
        h, w = marker.shape[:2]
        res, best_scale = None, None
        allMaxT = 0

        for r0 in np.arange(
                marker_rescale_range[1],
                marker_rescale_range[0], -1 * descent_per_step):  # reverse order
            s = float(r0 * 1 / 100)
            if (s == 0.0):
                continue
            rescaled_marker = Cropimage.resize_util_h(
                marker if ERODE_SUB_OFF else marker,
                u_height=int(
                    h * s))
            image_eroded_sub.astype(np.uint8)
            rescaled_marker.astype(np.uint8)

            res = cv2.matchTemplate(
                image_eroded_sub,
                rescaled_marker,
                cv2.TM_CCOEFF_NORMED)
            maxT = res.max()
            if (allMaxT < maxT):
                best_scale, allMaxT = s, maxT

        if (allMaxT < thresholdCircle):
            if (showimglvl >= 1):
                Cropimage.show("res", res, 1, 0)

        return best_scale, allMaxT

    def normalize_util(img, alpha=0, beta=255):
        return cv2.normalize(img, alpha, beta, norm_type=cv2.NORM_MINMAX)

    def handle_markers(image_norm, marker):

        if ERODE_SUB_OFF:
            image_eroded_sub = Cropimage.normalize_util(image_norm)
        else:
            image_eroded_sub = Cropimage.\
                normalize_util(image_norm - cv2.erode(image_norm,
                                                      kernel=np.ones((5, 5)),
                                                      iterations=5))
        quads = {}
        h1, w1 = image_eroded_sub.shape[:2]
        midh, midw = h1 // 3, w1 // 2
        origins = [[0, 0], [midw, 0], [0, midh], [midw, midh]]
        quads[0] = image_eroded_sub[0:midh, 0:midw]
        quads[1] = image_eroded_sub[0:midh, midw:w1]
        quads[2] = image_eroded_sub[midh:h1, 0:midw]
        quads[3] = image_eroded_sub[midh:h1, midw:w1]

        best_scale, allMaxT = Cropimage.getBestMatch(image_eroded_sub, marker)
        if (best_scale is None):
            if (showimglvl >= 1):
                # Draw Quadlines
                image_eroded_sub[:, midw:midw + 2] = 255
                image_eroded_sub[midh:midh + 2, :] = 255
                Cropimage.show('Quads', image_eroded_sub)
            return None

        optimal_marker = Cropimage.resize_util_h(
            marker if ERODE_SUB_OFF else marker, u_height=int(
                marker.shape[0] * best_scale))
        h, w = optimal_marker.shape[:2]
        centres = []
        sumT, maxT = 0, 0
        for k in range(0, 4):
            res = cv2.matchTemplate(quads[k], optimal_marker, cv2.TM_CCOEFF_NORMED)
            maxT = res.max()
            if (maxT < thresholdCircle or abs(allMaxT - maxT) >= thresholdVar):

                if (showimglvl >= 1):
                    return None
                return None

            pt = np.argwhere(res == maxT)[0]
            pt = [pt[1], pt[0]]
            pt[0] += origins[k][0]
            pt[1] += origins[k][1]
            image_norm = cv2.rectangle(image_norm, tuple(
                pt), (pt[0] + w, pt[1] + h), (150, 150, 150), 2)
            # display:
            image_eroded_sub = cv2.rectangle(
                image_eroded_sub,
                tuple(pt),
                (pt[0] + w,
                 pt[1] + h),
                (50,
                 50,
                 50) if ERODE_SUB_OFF else (
                    155,
                    155,
                    155),
                4)
            centres.append([pt[0] + w / 2, pt[1] + h / 2])
            sumT += maxT

        thresholdCircles.append(sumT / 4)

        image_norm = Cropimage.four_point_transform(image_norm, np.array(centres))

        Cropimage.appendSaveImg(2, image_eroded_sub)
        if (showimglvl >= 2 and showimglvl < 4):
            image_eroded_sub = Cropimage.resize_util_h(image_eroded_sub,
                                                       image_norm.shape[0])
            image_eroded_sub[:, -5:] = 0
            h_stack = np.hstack((image_eroded_sub, image_norm))
            Cropimage.show("Warped: " +
                           Cropimage.resize_util(h_stack,
                                                 int(display_width * 1.6)), 0, 0,
                           [0, 0])
        return image_norm

    def resetSaveImg(key):
        global saveImgList
        saveImgList[key] = []

    def getROI(image):
        global clahe
        for i in range(saveimglvl):
            Cropimage.resetSaveImg(i + 1)
        img = image.copy()
        img = cv2.GaussianBlur(img, (3, 3), 0)
        image_norm = Cropimage.normalize_util(img)

        image_norm = Cropimage.resize_util(image_norm, uniform_width, uniform_height)

        return image_norm

    def start_crop(image):

        SheetToMarkerWidthRatio = '17'

        inOMR = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_GRAYSCALE)
        OMRCrop = Cropimage.getROI(inOMR)

        marker = get_module_resource('openeducat_omr', 'static/src/img',
                                     'omr_marker.jpg')
        marker = cv2.imread(marker, cv2.IMREAD_GRAYSCALE)
        marker = Cropimage.resize_util(marker, uniform_width /
                                       int(SheetToMarkerWidthRatio))
        marker = cv2.GaussianBlur(marker, (5, 5), 0)
        marker = cv2.normalize(
            marker,
            None,
            alpha=0,
            beta=255,
            norm_type=cv2.NORM_MINMAX)
        marker = marker - cv2.erode(marker, kernel=np.ones((5, 5)), iterations=5)

        OMRCrop = Cropimage.handle_markers(OMRCrop, marker)
        if OMRCrop is None:
            return False
        else:
            im = Image.fromarray(OMRCrop)
            new_image = im.resize((600, 700))
            return new_image
