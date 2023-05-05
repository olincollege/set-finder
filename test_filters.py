"""
Test that contours are filtered correctly.
"""
import numpy as np
from image import Image

# pylint: disable=protected-access
img = np.zeros((100, 100, 3), dtype=np.uint8)
image = Image(img)


def test_filter_contours_by_area_different_and_same():
    """
    Test that a mixture of oversized and undersized contours is properly
    filtered.
    """
    cnt1 = np.array([[[10, 10]], [[50, 10]], [[50, 50]], [[10, 50]]])  # bad
    cnt2 = np.array([[[30, 30]], [[70, 30]], [[70, 70]], [[30, 70]]])  # bad
    cnt3 = np.array([[[60, 60]], [[90, 60]], [[90, 90]], [[60, 90]]])  # bad
    cnt4 = np.array([[[20, 20]], [[40, 20]], [[40, 40]], [[20, 40]]])  # good
    cnt5 = np.array([[[80, 80]], [[90, 80]], [[90, 90]], [[80, 90]]])  # good
    image.contours = [cnt1, cnt2, cnt3, cnt4, cnt5]
    image._filter_contours_by_area()
    assert len(image.contours) == 2


def test_filter_contours_by_area_all_same():
    """
    Test that contours of equal size all pass the filter.
    """
    cnt1 = np.array([[[10, 10]], [[20, 10]], [[20, 20]], [[10, 20]]])  # good
    cnt2 = np.array([[[30, 30]], [[40, 30]], [[40, 40]], [[30, 40]]])  # good
    cnt3 = np.array([[[60, 60]], [[70, 60]], [[70, 70]], [[60, 70]]])  # good
    image.contours = [cnt1, cnt2, cnt3]
    image._filter_contours_by_area()
    assert len(image.contours) == 3


def test_filter_contours_by_area_one_too_small():
    """
    Test that an undersized contour is caught by the filter.
    """
    cnt1 = np.array([[[10, 10]], [[30, 10]], [[30, 30]], [[10, 30]]])  # good
    cnt2 = np.array([[[30, 30]], [[50, 30]], [[50, 50]], [[30, 50]]])  # good
    cnt3 = np.array([[[60, 60]], [[65, 60]], [[65, 65]], [[60, 65]]])  # bad
    image.contours = [cnt1, cnt3, cnt2]
    image._filter_contours_by_area()
    assert len(image.contours) == 2


def test_filter_contours_by_area_one_too_large():
    """
    Test that an oversized contour is caught by the filter.
    """
    cnt1 = np.array([[[10, 10]], [[30, 10]], [[30, 30]], [[10, 30]]])  # good
    cnt2 = np.array([[[30, 30]], [[50, 30]], [[50, 50]], [[30, 50]]])  # good
    cnt3 = np.array([[[10, 10]], [[10, 60]], [[70, 70]], [[60, 10]]])  # bad
    image.contours = [cnt1, cnt2, cnt3]
    image._filter_contours_by_area()
    assert len(image.contours) == 2


def test_filter_by_polygon():
    """
    Test that contours with concavities fail to pass the filter.
    """
    cnt1 = np.array([[[10, 10]], [[50, 10]], [[50, 50]], [[10, 50]]])  # good
    cnt2 = np.array([[[30, 30]], [[70, 30]], [[70, 70]], [[60, 30]]])  # bad
    cnt3 = np.array([[[60, 60]], [[90, 60]], [[90, 90]], [[60, 90]]])  # good
    image.contours = [cnt1, cnt2, cnt3]
    image._filter_by_polygon()
    assert len(image.simple_contours) == 2
