#include <opencv2/aruco.hpp>
#include <opencv2/highgui.hpp>
#include <iostream>
#include <sstream>
using namespace cv;
using namespace std;
Mat markerImage;

namespace {
const char* about = "Create an ArUco marker image";
const char* keys  =
        "{d        |       | dictionary: DICT_4X4_50=0, DICT_4X4_100=1, DICT    _4X4_250=2,"
        "DICT_4X4_1000=3, DICT_5X5_50=4, DICT_5X5_100=5, DICT_5X5_250=6, DIC    T_5X5_1000=7, "
        "DICT_6X6_50=8, DICT_6X6_100=9, DICT_6X6_250=10, DICT_6X6_1000=11, D    ICT_7X7_50=12,"
        "DICT_7X7_100=13, DICT_7X7_250=14, DICT_7X7_1000=15, DICT_ARUCO_ORIG    INAL = 16}"
        "{@ids      |       | Number of Markers to Create }"
        "{ms       | 200   | Marker size in pixels }"
        "{bb       | 1     | Number of bits in marker borders }";
}


int main(int argc, char *argv[]){

	CommandLineParser parser(argc, argv, keys);
	parser.about(about);

	if (argc < 2) {
		parser.printMessage();
		return 0;
	}

	int dictID = parser.get<int>("d");
        int borderBits = parser.get<int>("bb");
        int markerSize = parser.get<int>("ms");

        int ids = parser.get<int>(0);
 
        if(!parser.check()) {
            parser.printErrors();
            return 0;
        }


	Ptr<aruco::Dictionary> dict =  aruco::getPredefinedDictionary(aruco::PREDEFINED_DICTIONARY_NAME(dictID));


	for (int i = 1; i <= ids; i++){
		aruco::drawMarker(dict, i, 200, markerImage, 1);
	
		std::ostringstream filename;
		filename <<  "ARTag/ARTag_"<< i <<".jpg";
		cout << "Writing tag "<< i<< " to: "<< filename.str()<<"\n";
		imwrite(filename.str(), markerImage);
	}
return 0;
}
