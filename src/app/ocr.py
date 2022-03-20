'''
@author     : Ali Mustofa HALOTEC
@module     : OCR Container Number
@Created on : 29 April 2021
'''

import cv2
import torch
import easyocr
from PIL import Image, ImageDraw

from config import ISO_CODE

class OpticalCharacterRecognition:
    '''
    Setup configuration EasyOCR
    '''
    def __init__(self):
        self.device                         = True if torch.cuda.is_available() else False
        self.list_langs                     = ['en', 'id']
        self.recog_network_container_number = 'latin_g2'
        self.recog_network_iso_code         = 'latin_g1'
        self.reader_container_number        = easyocr.Reader(self.list_langs, gpu=self.device, recog_network=self.recog_network_container_number)
        if ISO_CODE: self.reader_iso_code   = easyocr.Reader(self.list_langs, gpu=self.device, recog_network=self.recog_network_iso_code)

    def detect_char(self, image):
        '''
        Detection character in image
        '''
        return self.reader_container_number.detect(image)

    def ocr_image(self, image, config, clasess_name='container_number'):
        '''
        Read text in image with library easy ocr
        with configuration in param config
        '''
        if clasess_name == 'container_number':
            results = self.reader_container_number.readtext(
                image,
                detail          = config.detail,
                decoder         = config.decoder,
                beamWidth       = config.beam_width,
                batch_size      = config.batch_size,
                workers         = config.workers,
                allowlist       = config.allow_list,
                blocklist       = config.blocklist,
                paragraph       = config.paragraph,
                min_size        = config.min_size,
                rotation_info   = config.rotation_info,
                # Contrast
                contrast_ths    = config.contrast_ths,
                adjust_contrast = config.adjust_contrast,
                # Text detection
                text_threshold  = config.text_threshold + 0.1 if self.device else config.text_threshold,
                low_text        = config.low_text,
                link_threshold  = config.link_threshold,
                canvas_size     = config.canvas_size,
                mag_ratio       = config.mag_ratio
            )
        elif clasess_name == 'iso_code':
             results = self.reader_iso_code.readtext(
                image,
                detail          = config.detail,
                decoder         = config.decoder,
                beamWidth       = config.beam_width,
                batch_size      = config.batch_size,
                workers         = config.workers,
                allowlist       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
                blocklist       = config.blocklist,
                paragraph       = config.paragraph,
                min_size        = config.min_size,
                rotation_info   = config.rotation_info,
                # Contrast
                contrast_ths    = config.contrast_ths,
                adjust_contrast = config.adjust_contrast,
                # Text detection
                text_threshold  = config.text_threshold + 0.1 if self.device else config.text_threshold,
                low_text        = config.low_text,
                link_threshold  = config.link_threshold,
                canvas_size     = config.canvas_size,
                mag_ratio       = config.mag_ratio
            )
        return results
    
    def draw_boxes(self, image, bounds, color='yellow', width=2):
        text = []
        confidence = []
        image = Image.fromarray(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(image)

        for bound in bounds:
            if bound[2] > 0.0:
                confidence.append(bound[2])
                text.append(bound[1])
                p0, p1, p2, p3 = bound[0]
                draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
        
        # Calculate AVG confidence level
        avgConf = sum(confidence)/len(confidence)
        return image, text, avgConf