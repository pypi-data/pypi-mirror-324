"""
This module provides functions for processing and handling images.
It includes functionalities for image rectification, disparity and depth map computation.

Functions:
    get_rect_img(data, performance_mode):
        Rectify the provided image using the camera's intrinsic and extrinsic parameters.

    get_disparity_map(camera_left, camera_right, stereo_param):
        Compute a disparity map from a pair of stereo images.

    get_depth_map(camera_left, camera_right, stereo_param):
        Generate a depth map from a pair of stereo camera images.

    disparity_to_depth(disparity_map, camera_info):
        Convert a disparity map into a depth map using camera parameters.
"""
from typing import Optional, Tuple, Union
from PIL import Image as PilImage
from coopscenes.data import CameraInformation, Camera, Image
from coopscenes.utils import Transformation
import numpy as np
import cv2


def get_rect_img(data: Union[Camera, Tuple[Image, CameraInformation]], performance_mode: bool = False) -> Image:
    """Rectify the provided image using either a Camera object or an Image with CameraInformation.

    Performs image rectification using the camera matrix, distortion coefficients, rectification matrix,
    and projection matrix. The rectified image is returned as an `Image` object.

    Args:
        data (Union[Camera, Tuple[Image, CameraInformation]]): Either a Camera object containing the image and calibration parameters,
            or a tuple of an Image object and a CameraInformation object.
        performance_mode (bool, optional): If True, faster interpolation (linear) will be used; otherwise, higher quality (Lanczos4) will be used. Defaults to False.

    Returns:
        Image: The rectified image wrapped in the `Image` class.
    """
    if isinstance(data, Camera):
        image = data._image_raw
        camera_info = data.info
    else:
        image, camera_info = data

    mapx, mapy = cv2.initUndistortRectifyMap(
        cameraMatrix=camera_info.camera_mtx,
        distCoeffs=camera_info.distortion_mtx[:-1],
        R=camera_info.rectification_mtx,
        newCameraMatrix=camera_info.projection_mtx,
        size=camera_info.shape,
        m1type=cv2.CV_16SC2
    )

    interpolation_algorithm = cv2.INTER_LINEAR if performance_mode else cv2.INTER_LANCZOS4

    rectified_image = cv2.remap(np.array(image.image), mapx, mapy, interpolation=interpolation_algorithm)

    return Image(PilImage.fromarray(rectified_image), image.timestamp)


def get_disparity_map(camera_left: Camera, camera_right: Camera,
                      stereo_param: Optional[cv2.StereoSGBM] = None) -> np.ndarray:
    """Compute a disparity map from a pair of stereo images.

    This function computes a disparity map using stereo block matching.
    The disparity map is based on the rectified grayscale images of the stereo camera pair.

    Args:
        camera_left (Camera): The left camera of the stereo pair.
        camera_right (Camera): The right camera of the stereo pair.
        stereo_param (Optional[cv2.StereoSGBM]): Optional custom StereoSGBM parameters for disparity calculation.
                                                 If not provided, default parameters will be used.

    Returns:
        np.ndarray: The computed disparity map.
    """
    img1_gray = np.array(camera_left.image.convert('L'))
    img2_gray = np.array(camera_right.image.convert('L'))

    stereo = stereo_param or _create_default_stereo_sgbm()
    disparity_map = stereo.compute(img1_gray, img2_gray).astype(np.float32)

    return disparity_map


def _create_default_stereo_sgbm() -> cv2.StereoSGBM:
    """Create default StereoSGBM parameters for disparity computation."""
    window_size = 5
    min_disparity = 0
    num_disparities = 128  # Must be divisible by 16
    block_size = window_size

    stereo = cv2.StereoSGBM_create(
        minDisparity=min_disparity,
        numDisparities=num_disparities,
        blockSize=block_size,
        P1=8 * 3 * block_size ** 2,  # P1 and P2 control the smoothness
        P2=32 * 3 * block_size ** 2,
        disp12MaxDiff=1,
        uniquenessRatio=15,
        speckleWindowSize=100,
        speckleRange=32,
        mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY
    )
    return stereo


def get_depth_map(camera_left: Camera, camera_right: Camera,
                  stereo_param: Optional[cv2.StereoSGBM] = None) -> np.ndarray:
    """Generate a depth map from a pair of stereo camera images (Experimental).

    This function computes the depth map by first calculating the disparity map between the left and right
    camera images, and then converting the disparity map to a depth map using the right camera's intrinsic parameters.

    Note: This function is experimental and has not been extensively tested on real-world data. The quality of the results may vary.

    Args:
        camera_left (Camera): The left camera of the stereo camera pair.
        camera_right (Camera): The right camera of the stereo camera pair. The intrinsic and extrinsic parameters
                               from this camera are used for disparity-to-depth conversion.
        stereo_param (Optional[cv2.StereoSGBM]): Optional StereoSGBM parameter object for controlling the stereo matching.
                                                 If not provided, default parameters will be used for disparity calculation.

    Returns:
        np.ndarray: The computed depth map.
    """
    disparity_map = get_disparity_map(camera_left, camera_right, stereo_param)

    depth_map = disparity_to_depth(disparity_map, camera_right)

    return depth_map


def disparity_to_depth(disparity_map: np.ndarray, camera_info: Union[Camera, CameraInformation]) -> np.ndarray:
    """Convert a disparity map to a depth map using camera parameters (Experimental).

    This function converts a disparity map into a depth map using the intrinsic parameters of the camera.

    Note: This function is experimental and has not been extensively tested on real-world data. The quality of the results may vary.

    Args:
        disparity_map (np.ndarray): The disparity map to convert to depth.
        camera_info (Union[Camera, CameraInformation]): The Camera object or CameraInformation object containing 
                                                   the focal length and baseline information.

    Returns:
        np.ndarray: The computed depth map, with masked areas where disparity is zero.
    """
    if hasattr(camera_info, 'info'):
        camera_info = camera_info.info
    else:
        camera_info = camera_info

    focal_length = camera_info.camera_mtx[0][0]
    stereo_tf = Transformation('stereo_right', 'stereo_left', camera_info.stereo_transform)
    baseline = abs(stereo_tf.translation[0])

    with np.errstate(divide='ignore'):
        depth_map = np.where(disparity_map > 0, (focal_length * baseline) / disparity_map, np.inf)

    return depth_map
