# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

display_height = int(700)
display_width = int(525)
windowWidth = 525
windowHeight = 700

saveMarked = 1
saveCropped = 1
showimglvl = 4
saveimglvl = 0
PRELIM_CHECKS = 0

explain = 0
# autorotate=1

BATCH_NO = 1000
NO_MARKER_ERR = 12
MULTI_BUBBLE_WARN = 15

# name of template file
TEMPLATE_FILE = 'template.json'
MARKER_FILE = "omr_marker.jpg"

# For preProcessing
GAMMA_LOW = 0.7
GAMMA_HIGH = 1.25

ERODE_SUB_OFF = 1

# For new ways of determining threshold
MIN_GAP, MIN_STD = 30, 25
MIN_JUMP = 25
# If only not confident, take help of globalTHR
CONFIDENT_JUMP = MIN_JUMP + 15
JUMP_DELTA = 30
# MIN_GAP : worst case gap of black and gray

# Templ alignment parameters
ALIGN_RANGE = range(-5, 6, 1)

# max threshold difference for template matching
thresholdVar = 0.41

thresholdCircle = 0.3
marker_rescale_range = (35, 100)
marker_rescale_steps = 10

# Presentation variables
uniform_height = int(1231 / 1.5)
uniform_width = int(1000 / 1.5)
# Original dims are about (3527, 2494)

# Any input images should be resized to this--
uniform_width_hd = int(uniform_width * 1.5)
uniform_height_hd = int(uniform_height * 1.5)

TEXT_SIZE = 0.95
CLR_BLACK = (50, 150, 150)
CLR_WHITE = (250, 250, 250)
CLR_GRAY = (130, 130, 130)
# CLR_DARK_GRAY = (190,190,190)
CLR_DARK_GRAY = (100, 100, 100)

MIN_PAGE_AREA = 80000
