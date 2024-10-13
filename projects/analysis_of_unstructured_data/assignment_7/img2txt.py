#!/usr/bin/env python

import sys
from typing import Iterator, Self

import cv2
import fire
import numpy as np
import pytesseract


class Image:
    img: cv2.typing.MatLike

    def __init__(self, b: bytes):
        arr = np.frombuffer(b, dtype=np.uint8)
        self.img = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    def _grayscale(self) -> Self:
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        return self

    def _threshold(self) -> Self:
        _, self.img = cv2.threshold(self.img, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        return self

    def _dilate(self) -> Self:
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        self.img = cv2.dilate(self.img, kernel, iterations=1)
        return self

    def _invert(self) -> Self:
        self.img = cv2.bitwise_not(self.img)
        return self

    def to_bytes(self) -> bytes:
        return cv2.imencode(".jpg", self.img)[1].tobytes()

    def _add_contours(self) -> Self:
        contours, hierarchy = cv2.findContours(self.img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            self.img = cv2.rectangle(self.img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return self

    def pipeline(self) -> Self:
        return self._grayscale()._threshold()._invert()._dilate()._add_contours()

    def get_text(self) -> Iterator[str]:
        contours, hierarchy = cv2.findContours(self.img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cropped = self.img[y : y + h, x : x + w]
            yield pytesseract.image_to_string(cropped)


def main(to_processed_image: bool = False):
    data = sys.stdin.buffer.read()
    result = Image(data).pipeline()

    if to_processed_image:
        sys.stdout.buffer.write(result.to_bytes())
        return

    for text in result.get_text():
        sys.stdout.buffer.write(text.encode("utf-8"))


if __name__ == "__main__":
    # cat fanta.jpg | ./img2txt.py > test.txt
    # cat fanta.jpg | ./img2txt.py -t > test.jpg
    fire.Fire(main)
