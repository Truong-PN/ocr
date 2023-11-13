from typing import List

import cv2
import numpy as np


class ImageProcessing:
    thickness: int = 2
    color: tuple = (255,0,0)

    @staticmethod
    def format_rect_template(rects, crop_size_h, crop_size_w, shift_x, shift_y):
        scale_w: float = crop_size_w / 900
        scale_h: float = crop_size_h / 600
        for key, value in rects.items():
            value = np.array(value)
            rect_list = []
            shape = len(value.shape)
            if shape == 2:
                new_value = ImageProcessing.scale_rects(value, scale_w, scale_h)
                rects[key] = new_value + np.array([[shift_x, shift_y],
                                                [shift_x, shift_y],
                                                [shift_x, shift_y],
                                                [shift_x, shift_y]])
            elif shape == 3:
                for va in value:
                    new_value = ImageProcessing.scale_rects(va, scale_w, scale_h)
                    new_value = new_value + np.array([[shift_x, shift_y],
                                                [shift_x, shift_y],
                                                [shift_x, shift_y],
                                                [shift_x, shift_y]])
                    rect_list.append(new_value)
                rects[key] = rect_list
        return rects

    @staticmethod
    def get_scale_image(image)-> List[float]:
        h, w, _ = image.shape
        scale_w: float = w / 900
        scale_h: float = h / 600
        return scale_w, scale_h

    @staticmethod
    def scale_rects(rects, scale_w: int=1, scale_h: int=1)->np.ndarray:
        shape = len(np.array(rects).shape)
        if shape == 2:
            rects = rects*np.array([scale_w, scale_h])
            res = np.array(rects).astype(int)
            return res
        elif shape == 3:
            res = []
            for rect in rects:
                rect = rect*np.array([scale_w, scale_h])
                res.append(np.array(rect).astype(int))
            return res
        return np.array(rects)

    @staticmethod
    def draw_rect(image, rect):
        for i in range(len(rect)):
            cv2.line(image, rect[i],
                        rect[(i+1) % len(rect)],
                        ImageProcessing.color,
                        thickness=ImageProcessing.thickness)

    @staticmethod
    def draw(image, rect, scale_h: int=1, scale_w: int=1, text: str=''):
        if len(rect) == 0:
            return image
        rect = ImageProcessing.scale_rects(rect, scale_w, scale_h)
        draft_image = image.copy()
        ImageProcessing.draw_rect(draft_image, rect)
        if text:
            cv2.putText(draft_image, text, rect[0],
                        cv2.FONT_HERSHEY_COMPLEX, 0.7,
                        ImageProcessing.color,
                        ImageProcessing.thickness)
        return draft_image

    @staticmethod
    def crop_with_percent(image, rect, scale_h: int=1, scale_w: int=1, crop_percent: int=0):
        if len(rect) == 0:
            return image
        rect = ImageProcessing.scale_rects(rect, scale_w, scale_h)
        x, y = zip(*rect)
        width = max(x) - min(x)
        height = max(y) - min(y)
        input = np.float32([rect[3], rect[0], rect[1], rect[2]])
        output = np.float32([[0,0], [width-1,0], [width-1,height-1], [0,height-1]])
        matrix = cv2.getPerspectiveTransform(input, output)
        draft_image = image.copy()
        draft_image = cv2.warpPerspective(draft_image, matrix, (width, height))
        if crop_percent:
            pw = width // 2 // crop_percent
            ph = height // 2 // crop_percent
            draft_image = draft_image[ph:-ph, pw:-pw]
        return draft_image

    @staticmethod
    def crop_with_padding(image, rect, scale_h: int=1, scale_w: int=1, padding: int=0):
        if len(rect) == 0:
            return image
        rect = ImageProcessing.scale_rects(rect, scale_w, scale_h)
        rect = rect + np.array([[padding, -padding],
                                [padding, padding],
                                [-padding, padding],
                                [-padding, -padding]])
        x, y = zip(*rect)
        width = max(x) - min(x)
        height = max(y) - min(y)
        input = np.float32([rect[3], rect[0], rect[1], rect[2]])
        output = np.float32([[0,0], [width-1,0], [width-1,height-1], [0,height-1]])
        matrix = cv2.getPerspectiveTransform(input, output)
        draft_image = image.copy()
        draft_image = cv2.warpPerspective(draft_image, matrix, (width, height))
        return np.array(draft_image)

    @staticmethod
    def crop_group_object_without_change_axis(image, rect, scale_h: int=1, scale_w: int=1, padding: int=0):
        if len(rect) == 0:
            return image
        rect = ImageProcessing.scale_rects(rect, scale_w, scale_h)
        rect = rect + np.array([[padding, -padding],
                                [padding, padding],
                                [-padding, padding],
                                [-padding, -padding]])
        x, y = zip(*rect)
        width = max(x) - min(x)
        height = max(y) - min(y)
        input = np.float32([rect[3], rect[0], rect[1], rect[2]])
        output = np.float32([[0,0], [width-1,0], [width-1,height-1], [0,height-1]])
        matrix = cv2.getPerspectiveTransform(input, output)
        draft_image1 = image.copy()
        draft_image1 = cv2.warpPerspective(draft_image1, matrix, (width, height))

        height, width, _ = image.shape
        matrix = cv2.getPerspectiveTransform(output, input)
        draft_image2 = draft_image1.copy()
        draft_image2 = cv2.warpPerspective(draft_image2, matrix, (width, height))

        return np.array(draft_image2)