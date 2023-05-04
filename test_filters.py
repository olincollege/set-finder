"""
Test that contours are filtered correctly.
"""
import numpy as np
import pytest
from image import Image

# pylint: disable=protected-access,redefined-outer-name
@pytest.fixture
def my_class():
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    my_object = Image(img)
    return my_object


def test_filter_contours_by_area_different_and_same(my_class):
    cnt1 = np.array([[[10, 10]], [[50, 10]], [[50, 50]], [[10, 50]]])  # bad
    cnt2 = np.array([[[30, 30]], [[70, 30]], [[70, 70]], [[30, 70]]])  # bad
    cnt3 = np.array([[[60, 60]], [[90, 60]], [[90, 90]], [[60, 90]]])  # bad
    cnt4 = np.array([[[20, 20]], [[40, 20]], [[40, 40]], [[20, 40]]])  # good
    cnt5 = np.array([[[80, 80]], [[90, 80]], [[90, 90]], [[80, 90]]])  # good
    my_class.contours = [cnt1, cnt2, cnt3, cnt4, cnt5]
    my_class._filter_contours_by_area()
    assert len(my_class.contours) == 2


def test_filter_contours_by_area_all_same(my_class):
    cnt1 = np.array([[[10, 10]], [[20, 10]], [[20, 20]], [[10, 20]]])  # good
    cnt2 = np.array([[[30, 30]], [[40, 30]], [[40, 40]], [[30, 40]]])  # good
    cnt3 = np.array([[[60, 60]], [[70, 60]], [[70, 70]], [[60, 70]]])  # good
    my_class.contours = [cnt1, cnt2, cnt3]
    my_class._filter_contours_by_area()
    assert len(my_class.contours) == 3


def test_filter_contours_by_area_one_too_small(my_class):
    cnt1 = np.array([[[10, 10]], [[30, 10]], [[30, 30]], [[10, 30]]])  # good
    cnt2 = np.array([[[30, 30]], [[50, 30]], [[50, 50]], [[30, 50]]])  # good
    cnt3 = np.array([[[60, 60]], [[65, 60]], [[65, 65]], [[60, 65]]])  # bad
    my_class.contours = [cnt1, cnt3, cnt2]
    my_class._filter_contours_by_area()
    assert len(my_class.contours) == 2


def test_filter_contours_by_area_one_too_large(my_class):
    cnt1 = np.array([[[10, 10]], [[30, 10]], [[30, 30]], [[10, 30]]])  # good
    cnt2 = np.array([[[30, 30]], [[50, 30]], [[50, 50]], [[30, 50]]])  # good
    cnt3 = np.array([[[10, 10]], [[10, 60]], [[70, 70]], [[60, 10]]])  # bad
    my_class.contours = [cnt1, cnt2, cnt3]
    my_class._filter_contours_by_area()
    assert len(my_class.contours) == 2


def test_filter_by_polygon(my_class):
    cnt1 = np.array([[[10, 10]], [[50, 10]], [[50, 50]], [[10, 50]]])  # good
    cnt2 = np.array([[[30, 30]], [[70, 30]], [[70, 70]], [[60, 30]]])  # bad
    cnt3 = np.array([[[60, 60]], [[90, 60]], [[90, 90]], [[60, 90]]])  # good
    my_class.contours = [cnt1, cnt2, cnt3]
    my_class._filter_by_polygon()
    assert len(my_class.simple_contours) == 2
