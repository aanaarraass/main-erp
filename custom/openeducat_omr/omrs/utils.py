# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

import cv2
import numpy as np
import matplotlib.pyplot as plt
from imutils import grab_contours
from ..omrs import config

saveImgList = {}
resetpos = [0, 0]
windowX, windowY = 0, 0
plt.rcParams['figure.figsize'] = (10.0, 8.0)


class Utils():

    def normalize_util(img, alpha=0, beta=255):
        return cv2.normalize(img, alpha, beta, norm_type=cv2.NORM_MINMAX)

    def resize_util(img, u_width, u_height=None):
        if u_height is None:
            h, w = img.shape[:2]
            u_height = int(h * u_width / w)
        return cv2.resize(img, (int(u_width), int(u_height)))

    def resize_util_h(img, u_height, u_width=None):
        if u_width is None:
            h, w = img.shape[:2]
            u_width = int(w * u_height / h)
        return cv2.resize(img, (int(u_width), int(u_height)))

    def show(name, orig, pause=1, resize=False, resetpos=None):
        global windowX, windowY
        if isinstance(orig, type(None)):
            if (pause):
                cv2.destroyAllWindows()
            return
        img = Utils.resize_util(orig, config.display_width, config.display_height) \
            if resize else orig
        if (resetpos):
            windowX = resetpos[0]
            windowY = resetpos[1]

        h, w = img.shape[:2]
        margin = 25
        w += margin
        h += margin
        if (windowX + w > config.windowWidth):
            windowX = 0
            if (windowY + h > config.windowHeight):
                windowY = 0
            else:
                windowY += h
        else:
            windowX += w

        if (pause):
            cv2.destroyAllWindows()

    def drawTemplateLayout(
            img,
            template,
            shifted=True,
            draw_qvals=False,
            border=-1):
        img = Utils.resize_util(img, template.dims[0], template.dims[1])
        final_align = img.copy()
        boxW, boxH = template.bubbleDims
        for QBlock in template.QBlocks:
            s, d = QBlock.orig, QBlock.dims
            shift = QBlock.shift
            if (shifted):
                cv2.rectangle(final_align,
                              (s[0] + shift, s[1]),
                              (s[0] + shift + d[0], s[1] + d[1]),
                              config.CLR_BLACK,
                              3)
            else:
                cv2.rectangle(final_align,
                              (s[0], s[1]),
                              (s[0] + d[0], s[1] + d[1]),
                              config.CLR_BLACK
                              , 3)
            for qStrip, qBoxPts in QBlock.traverse_pts:
                for pt in qBoxPts:
                    x, y = (pt.x + QBlock.shift, pt.y) if shifted else (pt.x, pt.y)
                    cv2.rectangle(final_align,
                                  (int(x + boxW / 10),
                                   int(y + boxH / 10)),
                                  (int(x + boxW - boxW / 10),
                                   int(y + boxH - boxH / 10)),
                                  config.CLR_GRAY,
                                  border)
                    if (draw_qvals):
                        rect = [y, y + boxH, x, x + boxW]
                        cv2.putText(final_align,
                                    '%d' % (cv2.mean(img[rect[0]:rect[1],
                                                     rect[2]:rect[3]])[0]),
                                    (rect[2] + 2, rect[0] + (boxH * 2) // 3),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.6,
                                    config.CLR_BLACK,
                                    2)
            if (shifted):
                cv2.putText(final_align,
                            's%s' % (shift),
                            tuple(s - [template.dims[0] // 20, -d[1] // 2]),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            config.TEXT_SIZE,
                            config.CLR_BLACK,
                            4)
        return final_align

    def angle(p1, p2, p0):
        dx1 = float(p1[0] - p0[0])
        dy1 = float(p1[1] - p0[1])
        dx2 = float(p2[0] - p0[0])
        dy2 = float(p2[1] - p0[1])
        return (dx1 * dx2 + dy1 * dy2) / np.sqrt((dx1 * dx1 + dy1 * dy1) *
                                                 (dx2 * dx2 + dy2 * dy2) + 1e-10)

    def checkMaxCosine(approx):
        maxCosine = 0
        minCosine = 1.5
        for i in range(2, 5):
            cosine = abs(Utils.angle(approx[i % 4], approx[i - 2], approx[i - 1]))
            maxCosine = max(cosine, maxCosine)
            minCosine = min(cosine, minCosine)
        if (maxCosine >= 0.35):
            return False
        return True

    def validateRect(approx):
        return len(approx) == 4 and Utils.checkMaxCosine(approx.reshape(4, 2))

    def resetSaveImg(key):
        global saveImgList
        saveImgList[key] = []

    def appendSaveImg(key, img):
        if (config.saveimglvl >= int(key)):
            global saveImgList
            if (key not in saveImgList):
                saveImgList[key] = []
            saveImgList[key].append(img.copy())

    def findPage(image_norm):

        image_norm = Utils.normalize_util(image_norm)
        ret, image_norm = cv2.threshold(image_norm, 210, 255, cv2.THRESH_TRUNC)
        image_norm = Utils.normalize_util(image_norm)

        Utils.appendSaveImg(1, image_norm)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))

        closed = cv2.morphologyEx(image_norm, cv2.MORPH_CLOSE, kernel)

        Utils.appendSaveImg(1, closed)

        edge = cv2.Canny(closed, 185, 55)

        # findContours returns outer boundaries in CW and inner boundaries in ACW
        cnts = grab_contours(
            cv2.findContours(
                edge,
                cv2.RETR_LIST,
                cv2.CHAIN_APPROX_SIMPLE))
        # hullify to resolve disordered curves due to noise
        cnts = [cv2.convexHull(c) for c in cnts]
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
        sheet = []
        for c in cnts:
            if cv2.contourArea(c) < config.MIN_PAGE_AREA:
                continue
            peri = cv2.arcLength(c, True)

            approx = cv2.approxPolyDP(c, epsilon=0.025 * peri, closed=True)

            # check its rectangle-ness:
            if (Utils.validateRect(approx)):
                sheet = np.reshape(approx, (4, -1))
                cv2.drawContours(image_norm, [approx], -1, (0, 255, 0), 2)
                cv2.drawContours(edge, [approx], -1, (255, 255, 255), 10)
                break

        Utils.appendSaveImg(1, edge)
        if (sheet == []):
            if (config.showimglvl >= 4):
                Utils.show('Morphed Edges', np.hstack((closed, edge)), resize=1)
        return sheet

    clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(8, 8))
    thresholdCircles = []
    badThresholds = []
    veryBadPoints = []

    def getGlobalThreshold(
            QVals_orig,
            plotTitle=None,
            plotShow=True,
            sortInPlot=True,
            looseness=1):

        QVals = sorted(QVals_orig)
        ls = (looseness + 1) // 2
        lan = len(QVals) - ls
        max1, thr1 = config.MIN_JUMP, 255
        for i in range(ls, lan):
            jump = QVals[i + ls] - QVals[i - ls]
            if (jump > max1):
                max1 = jump
                thr1 = QVals[i - ls] + jump / 2

        max2, thr2 = config.MIN_JUMP, 255
        for i in range(ls, lan):
            jump = QVals[i + ls] - QVals[i - ls]
            newThr = QVals[i - ls] + jump / 2
            if (jump > max2 and abs(thr1 - newThr) > config.JUMP_DELTA):
                max2 = jump
                thr2 = newThr
        globalTHR, j_low, j_high = thr1, thr1 - max1 // 2, thr1 + max1 // 2

        if (plotTitle is not None):
            f, ax = plt.subplots()
            ax.bar(range(len(QVals_orig)), QVals if sortInPlot else QVals_orig)
            ax.set_title(plotTitle)
            thrline = ax.axhline(globalTHR, color='green', ls='--', linewidth=5)
            thrline.set_label("Global Threshold")
            thrline = ax.axhline(thr2, color='red', ls=':', linewidth=3)
            thrline.set_label("THR2 Line")

            ax.set_ylabel("Values")
            ax.set_xlabel("Position")
            ax.legend()
            if (plotShow):
                plt.title(plotTitle)
                plt.show()

        return globalTHR, j_low, j_high

    def getLocalThreshold(
            qNo,
            QVals,
            globalTHR,
            noOutliers,
            plotTitle=None,
            plotShow=True):

        QVals = sorted(QVals)

        if (len(QVals) < 3):
            thr1 = globalTHR if np.max(
                QVals) - np.min(QVals) < config.MIN_GAP else np.mean(QVals)
        else:

            lan = len(QVals) - 1
            max1, thr1 = config.MIN_JUMP, 255
            for i in range(1, lan):
                jump = QVals[i + 1] - QVals[i - 1]
                if (jump > max1):
                    max1 = jump
                    thr1 = QVals[i - 1] + jump / 2
            if (max1 < config.CONFIDENT_JUMP):
                if (noOutliers):
                    thr1 = globalTHR
                else:
                    pass

        if (plotShow and plotTitle is not None):
            f, ax = plt.subplots()
            ax.bar(range(len(QVals)), QVals)
            thrline = ax.axhline(thr1, color='green', ls=('-.'), linewidth=3)
            thrline.set_label("Local Threshold")
            thrline = ax.axhline(globalTHR, color='red', ls=':', linewidth=5)
            thrline.set_label("Global Threshold")
            ax.set_title(plotTitle)
            ax.set_ylabel("Bubble Mean Intensity")
            ax.set_xlabel("Bubble Number(sorted)")
            ax.legend()
            if (plotShow):
                plt.show()
        return thr1

    def saveImg(path, final_marked):
        cv2.imwrite(path, final_marked)

    def readResponse(template, image, name, autoAlign=False):
        global clahe
        img = image.copy()
        img = Utils.resize_util(img, template.dims[0], template.dims[1])

        if (img.max() > img.min()):
            img = Utils.normalize_util(img)
        # Processing copies
        transp_layer = img.copy()
        final_marked = img.copy()

        morph = img.copy()
        Utils.appendSaveImg(3, morph)

        # Overlay Transparencies
        alpha = 0.65

        boxW, boxH = template.bubbleDims
        OMRresponse = {}

        multimarked, multiroll = 0, 0

        if (config.showimglvl >= 5):
            allCBoxvals = {"Int": [], "Mcq": []}
            qNums = {"Int": [], "Mcq": []}

        final_align = None
        if (config.showimglvl >= 2):
            initial_align = Utils.drawTemplateLayout(img, template, shifted=False)
            final_align = Utils.drawTemplateLayout(
                img, template, shifted=True, draw_qvals=True)
            Utils.appendSaveImg(2, initial_align)
            Utils.appendSaveImg(2, final_align)
            Utils.appendSaveImg(5, img)
            if (autoAlign):
                final_align = np.hstack((initial_align, final_align))

        # Get mean vals n other stats
        allQVals, allQStripArrs, allQStdVals = [], [], []
        totalQStripNo = 0
        for QBlock in template.QBlocks:
            QStdVals = []
            for qStrip, qBoxPts in QBlock.traverse_pts:
                QStripvals = []
                for pt in qBoxPts:
                    x, y = (pt.x + QBlock.shift, pt.y)
                    rect = [y, y + boxH, x, x + boxW]
                    QStripvals.append(
                        cv2.mean(img[rect[0]:rect[1], rect[2]:rect[3]])[0])
                QStdVals.append(round(np.std(QStripvals), 2))
                allQStripArrs.append(QStripvals)
                allQVals.extend(QStripvals)
                totalQStripNo += 1
            allQStdVals.extend(QStdVals)
        globalStdTHR, jstd_low, jstd_high = Utils.getGlobalThreshold(allQStdVals)

        globalTHR, j_low, j_high = Utils.getGlobalThreshold(allQVals, looseness=4)

        perOMRThresholdAvg, totalQStripNo, totalQBoxNo = 0, 0, 0
        for QBlock in template.QBlocks:
            blockQStripNo = 1  # start from 1 is fine here
            key = QBlock.key[:3]
            for qStrip, qBoxPts in QBlock.traverse_pts:
                # All Black or All White case
                noOutliers = allQStdVals[totalQStripNo] < globalStdTHR
                perQStripThreshold = Utils.\
                    getLocalThreshold(qBoxPts[0].qNo, allQStripArrs[totalQStripNo],
                                      globalTHR, noOutliers,
                                      "Mean Intensity Histogram for " + key +
                                      "." + qBoxPts[0].qNo + '.' +
                                      str(blockQStripNo), config.showimglvl >= 6)
                perOMRThresholdAvg += perQStripThreshold

                for pt in qBoxPts:
                    # shifted
                    x, y = (pt.x + QBlock.shift, pt.y)
                    boxval0 = allQVals[totalQBoxNo]
                    detected = perQStripThreshold > boxval0

                    if (detected):
                        cv2.rectangle(final_marked,
                                      (int(x + boxW / 12),
                                       int(y + boxH / 12)),
                                      (int(x + boxW - boxW / 12),
                                       int(y + boxH - boxH / 12)),
                                      config.CLR_DARK_GRAY,
                                      3)
                    else:
                        cv2.rectangle(final_marked,
                                      (int(x + boxW / 10), int(y + boxH / 10)),
                                      (int(x + boxW - boxW / 10),
                                       int(y + boxH - boxH / 10)),
                                      config.CLR_GRAY,
                                      -1)

                    if (detected):
                        q, val = pt.qNo, str(pt.val)
                        cv2.putText(final_marked,
                                    val,
                                    (x, y),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    config.TEXT_SIZE,
                                    (20, 20, 10),
                                    int(1 + 3.5 * config.TEXT_SIZE))
                        # Only send rolls multi-marked in the directory
                        multimarkedL = q in OMRresponse
                        multimarked = multimarkedL or multimarked
                        OMRresponse[q] = (OMRresponse[q] + val) \
                            if multimarkedL else val
                        multiroll = multimarkedL and 'roll' in str(q)
                    totalQBoxNo += 1

                if (config.showimglvl >= 5):
                    if (key in allCBoxvals):
                        qNums[key].append(key[:2] + '_c' + str(blockQStripNo))
                        allCBoxvals[key].append(allQStripArrs[totalQStripNo])

                blockQStripNo += 1
                totalQStripNo += 1

        if (totalQStripNo == 0):
            exit(21)

        perOMRThresholdAvg /= totalQStripNo
        perOMRThresholdAvg = round(perOMRThresholdAvg, 2)
        cv2.addWeighted(
            final_marked,
            alpha,
            transp_layer,
            1 - alpha,
            0,
            final_marked)
        # Box types
        if (config.showimglvl >= 5):
            f, axes = plt.subplots(len(allCBoxvals), sharey=True)
            f.canvas.set_window_title(name)
            ctr = 0
            typeName = {
                "Int": "Integer",
                "Mcq": "MCQ",
                "Med": "MED",
                "Rol": "Roll"}
            for k, boxvals in allCBoxvals.items():
                axes[ctr].title.set_text(typeName[k] + " Type")
                axes[ctr].boxplot(boxvals)
                axes[ctr].set_ylabel("Intensity")
                axes[ctr].set_xticklabels(qNums[k])
                ctr += 1
            # imshow will do the waiting
            plt.tight_layout(pad=0.5)
            plt.show()

        if (config.showimglvl >= 3 and final_align is not None):
            final_align = Utils.resize_util_h(final_align,
                                              int(config.display_height))
            Utils.show("Template Alignment Adjustment", final_align, 0, 0)

        if (config.showimglvl >= 1):
            Utils.show("Final Marked Bubbles : " + name,
                       Utils.resize_util_h(final_marked,
                                           int(config.display_height * 1.3)), 1, 1)

        Utils.appendSaveImg(2, final_marked)

        return OMRresponse, final_marked, multimarked, multiroll
