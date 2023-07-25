# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.

##############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
##############################################################################

import argparse
import numpy as np
from ..omrs.template import Template
from ..omrs import utils
filesMoved = 0
filesNotMoved = 0
global args
args = {'template': False, 'noCropping': True, 'autoAlign': False,
        'setLayout': False, 'input_dir': True, 'output_dir': ''}


def start_check(input_data, template_data):
    l1 = []
    dict1 = {}

    argparser = argparse.ArgumentParser()

    argparser.add_argument(
        "-c",
        "--noCropping",
        required=False,
        dest='noCropping',
        action='store_true',
        help="Disables page contour detection - used when page boundary is not visible"
             " e.g. document scanner.")
    argparser.add_argument(
        "-a",
        "--autoAlign",
        required=False,
        dest='autoAlign',
        action='store_true',
        help="(experimental) Enables automatic template alignment - "
             "use if the scans show slight misalignments.")
    argparser.add_argument(
        "-l",
        "--setLayout",
        required=False,
        dest='setLayout',
        action='store_true',
        help="Set up OMR template layout - modify your json file and"
             " run again until the template is set.")
    argparser.add_argument("-i", "--inputDir", required=False, action='append',
                           dest='input_dir', help="Specify an input directory.")
    argparser.add_argument("-o", "--outputDir", default='outputs', required=False,
                           dest='output_dir', help="Specify an output directory.")
    argparser.add_argument(
        "-t",
        "--template",
        required=False,
        dest='template',
        help="Specify a default template if no template file in input directories.")

    args, unknown = argparser.parse_known_args()
    args = vars(args)

    args['template'] = template_data

    args['input_dir'] = input_data

    if args['template']:
        args['template'] = Template(args['template'])

    dict1 = Main.process_dir(args['input_dir'], args['template'])
    l1.append(dict1)
    return l1


class Main():

    def process_dir(input_data, template):

        omr_files = input_data
        if omr_files:
            args_local = args.copy()

            resp = Main.process_files(omr_files, template, args_local)
            return resp

    def processOMR(template, omrResp):
        csvResp = {}

        UNMARKED_SYMBOL = ''

        for qNo, respKeys in template.concats.items():
            csvResp[qNo] = ''.join([omrResp.get(k, UNMARKED_SYMBOL)
                                    for k in respKeys])

        for qNo in template.singles:
            csvResp[qNo] = omrResp.get(qNo, UNMARKED_SYMBOL)

        return csvResp

    def process_files(omr_files, template, args):

        inOMR = np.array(omr_files)
        file_id = "sample"
        OMRresponseDict, final_marked, MultiMarked, multiroll = \
            utils.Utils.readResponse(template, inOMR,
                                     name=file_id, autoAlign=args["autoAlign"])

        resp = Main.processOMR(template, OMRresponseDict)

        return resp
