#include <opencv2/highgui.hpp>
#include <opencv2/aruco.hpp>
#include <iostream>
#include <string>
#include <fstream>
#include <istream>
#include <ostream>
#include "include/SwarmHostConfig.h"
#include "../include/arucoTest.h"
#include <readline/readline.h>
#include <readline/history.h>

#include <typeinfo>

using namespace std;
using namespace cv;


void help(std::string);

int main(int argc, char *argv[]) {
    help("brief");

    while(1){
        char * line = readline("Swarm Host>  ");
        if(!line) break;
        if(*line) add_history(line);
        
        if (std::string(line) == "help"){
            help("long");
        }
        if (std::string(line) == "arucoTest"){
            printf("Running arucoTest procedure\n"); 
            arucoDetect(0);
        }
        free(line);
    }

    return 0;
}

void printFile(std::string file){
    ifstream f;
    f.open(file);

    if (f.fail()){
        printf("Failed to open file %s.\n",file);
        exit(1);
    }
    else{
        while (f.good()){
            cout << f.rdbuf();
        }
    }
    f.close;
}

void help(std::string length){
    if (length == "long"){
        printFile("../src/helpFile.txt");
    }    

    else if (length == "brief"){
        printFile("../src/helpFile_Brief.txt");
    }
}
