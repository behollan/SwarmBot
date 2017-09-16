#include <opencv2/aruco.hpp>

using namespace cv;

Mat markerImage;
cv::aruco::Dictionary dictionary = cv::aruco::getPredefinedDictionary(cv::aruco::DICT_6x6_250);
cv::aruco::drawMarker(dictionary, 23, 200, markerImage, 1);
