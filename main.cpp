#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>

using namespace cv;
using namespace std;

Mat camFrame;

int main(){
	VideoCapture cap(0);
	if (!cap.isOpened()){
		cout << "Cannot open Webcam";
	}
	
	while(1){
		cap >> camFrame;
		if (camFrame.empty()){
			cout << "Empty image from webcam.";
			break;
		}
		imshow("Web Came Image", camFrame);
		if ( waitKey(10) == 270 ) break;
	}
	return 0;
}
