import cv2 as cv
import numpy as np
import pytest
from Image import Image


@pytest.fixture
def my_class():
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    my_object = Image(img)
    return my_object


def test_filter_contours_by_area(my_class):
    cnt1 = np.array([[[10, 10]], [[50, 10]], [[50, 50]], [[10, 50]]])
    cnt2 = np.array([[[30, 30]], [[70, 30]], [[70, 70]], [[30, 70]]])
    cnt3 = np.array([[[60, 60]], [[90, 60]], [[90, 90]], [[60, 90]]])
    my_class.contours = [cnt1, cnt2, cnt3]
    my_class._filter_contours_by_area()
    assert len(my_class.contours) == 2


def test_filter_by_polygon(my_class):
    cnt1 = np.array([[[10, 10]], [[50, 10]], [[50, 50]], [[10, 50]]])
    cnt2 = np.array([[[30, 30]], [[70, 30]], [[70, 70]], [[30, 70]]])
    cnt3 = np.array([[[60, 60]], [[90, 60]], [[90, 90]], [[60, 90]]])
    my_class.contours = [cnt1, cnt2, cnt3]
    my_class._filter_by_polygon()
    assert len(my_class.simple_contours) == 2
