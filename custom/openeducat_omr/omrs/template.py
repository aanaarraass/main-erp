# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

import cv2
import os
import numpy as np
from ..omrs import config
from ..omrs import utils


class Pt():

    def __init__(self, pt, qNo, qType, val):
        self.x = round(pt[0])
        self.y = round(pt[1])
        self.qNo = qNo
        self.qType = qType
        self.val = val


class QBlock():
    def __init__(self, dims, key, orig, traverse_pts):
        self.dims = tuple(round(x) for x in dims)
        self.key = key
        self.orig = orig
        self.traverse_pts = traverse_pts
        self.shift = 0


qtype_data = {
    'QTYPE_MED': {
        'vals': ['A', 'B', 'C', 'D', 'E'],
        'orient': 'V'
    },
    'QTYPE_ROLL': {
        'vals': range(10),
        'orient': 'V'
    },
    'QTYPE_INT': {
        'vals': range(10),
        'orient': 'V'
    },
    'QTYPE_INT_11': {
        'vals': range(11),
        'orient': 'V'
    },
    'QTYPE_INT4': {
        'vals': [1, 2, 3, 0],
        'orient': 'V'
    },
    'QTYPE_MCQ4': {
        'vals': ['A', 'B', 'C', 'D'],
        'orient': 'H'
    },
    'QTYPE_MCQ5': {
        'vals': ['A', 'B', 'C', 'D', 'E'],
        'orient': 'H'
    },

}


class Template(QBlock, Pt):

    def __init__(self, path):
        json_obj = path
        self.path = path
        self.QBlocks = []
        # throw exception on key not exist
        self.dims = json_obj["Dimensions"]
        self.bubbleDims = json_obj["BubbleDimensions"]
        self.concats = json_obj["Concatenations"]
        self.singles = json_obj["Singles"]

        # Add new qTypes from template
        if "qTypes" in json_obj:
            qtype_data.update(json_obj["qTypes"])

        # process local options
        self.options = json_obj.get("Options", {})

        self.marker = None
        self.marker_path = None
        # process markers
        if "Marker" in self.options:
            markerOps = self.options["Marker"]
            self.marker_path = os.path.join(
                os.path.dirname(path), markerOps.get(
                    "RelativePath", config.MARKER_FILE))
            if (not os.path.exists(self.marker_path)):
                exit(31)

            marker = cv2.imread(self.marker_path, cv2.IMREAD_GRAYSCALE)
            if ("SheetToMarkerWidthRatio" in markerOps):
                marker = utils.Utils.\
                    resize_util(marker,
                                config.uniform_width /
                                int(markerOps["SheetToMarkerWidthRatio"]))
            marker = cv2.GaussianBlur(marker, (5, 5), 0)
            marker = cv2.normalize(
                marker,
                None,
                alpha=0,
                beta=255,
                norm_type=cv2.NORM_MINMAX)
            self.marker = marker - cv2.erode(marker, kernel=np.ones((5, 5)),
                                             iterations=5)

        # Add QBlocks
        for name, block in json_obj["QBlocks"].items():
            self.addQBlocks(name, block)

    # Expects bubbleDims to be set already
    def addQBlocks(self, key, rect):
        assert (self.bubbleDims != [-1, -1])
        # For qType defined in QBlocks
        if 'qType' in rect:
            rect.update(**qtype_data[rect['qType']])
        else:
            rect['qType'] = {'vals': rect['vals'], 'orient': rect['orient']}
        # keyword arg unpacking followed by named args
        self.QBlocks += self.genGrid(self.bubbleDims, key, **rect)

    def genQBlock(
            self,
            bubbleDims,
            QBlockDims,
            key,
            orig,
            qNos,
            gaps,
            vals,
            qType,
            orient,
            col_orient):

        H, V = (0, 1) if (orient == 'H') else (1, 0)
        traverse_pts = []
        o = [float(i) for i in orig]

        if (col_orient == orient):
            for q in range(len(qNos)):
                pt = o.copy()
                pts = []
                for v in range(len(vals)):
                    pts.append(Pt(pt.copy(), qNos[q], qType, vals[v]))
                    pt[H] += gaps[H]
                # For diagonalal endpoint of QBlock
                pt[H] += bubbleDims[H] - gaps[H]
                pt[V] += bubbleDims[V]
                traverse_pts.append(([o.copy(), pt.copy()], pts))
                o[V] += gaps[V]
        else:
            for v in range(len(vals)):
                pt = o.copy()
                pts = []
                for q in range(len(qNos)):
                    pts.append(Pt(pt.copy(), qNos[q], qType, vals[v]))
                    pt[V] += gaps[V]
                # For diagonalal endpoint of QBlock
                pt[V] += bubbleDims[V] - gaps[V]
                pt[H] += bubbleDims[H]
                traverse_pts.append(([o.copy(), pt.copy()], pts))
                o[H] += gaps[H]
        # Pass first three args as is. only append 'traverse_pts'
        return QBlock(QBlockDims, key, orig, traverse_pts)

    def genGrid(
            self,
            bubbleDims,
            key,
            qType,
            orig,
            bigGaps,
            gaps,
            qNos,
            vals,
            orient='V',
            col_orient='V'):

        gridData = np.array(qNos)
        if (0 and len(gridData.shape) != 3 or gridData.size == 0):
            exit(32)

        orig = np.array(orig)
        numQsMax = max([max([len(qb) for qb in row]) for row in gridData])

        numDims = [numQsMax, len(vals)]

        QBlocks = []

        H, V = (0, 1) if (orient == 'H') else (1, 0)

        # orient is also the direction of making QBlocks

        qStart = orig.copy()

        origGap = [0, 0]

        # Usually single row
        for row in gridData:
            qStart[V] = orig[V]

            # Usually multiple qTuples
            for qTuple in row:
                # Update numDims and origGaps
                numDims[0] = len(qTuple)
                # bigGaps is indep of orientation
                origGap[0] = bigGaps[0] + (numDims[V] - 1) * gaps[H]
                origGap[1] = bigGaps[1] + (numDims[H] - 1) * gaps[V]
                QBlockDims = [
                    # width x height in pixels
                    gaps[0] * (numDims[V] - 1) + bubbleDims[H],
                    gaps[1] * (numDims[H] - 1) + bubbleDims[V]
                ]

                QBlocks.append(
                    self.genQBlock(
                        bubbleDims,
                        QBlockDims,
                        key,
                        qStart.copy(),
                        qTuple,
                        gaps,
                        vals,
                        qType,
                        orient,
                        col_orient))
                qStart[V] += origGap[V]
            qStart[H] += origGap[H]
        return QBlocks
