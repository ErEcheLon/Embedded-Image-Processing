#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <thread>

using namespace std;
using namespace cv;

Mat Img;
int RunningTime;

void execute(Mat kernel)
{
    for(int i = 0; i < RunningTime ; i++)
    {
        morphologyEx(Img, Img, MORPH_CLOSE, kernel);
    }
}

int main(int atgc, char ** argv)
{

    Mat img,src_gray,dst;
    Mat open, close, grad, top, black, kernel;
    int ThreadNumber = 0;

    for(int i = 1; i <= 8 ; i++)
    {
        //setUseOptimized(0);
        /*setNumThreads(4);

        cout<<getNumThreads()<<endl;
        cout<<getThreadNum()<<endl;*/

        ThreadNumber = i;

        img = imread("Dog.jpg", IMREAD_COLOR );
        imshow("img", img);

        cvtColor( img, src_gray, COLOR_BGR2GRAY );
        imshow("gray", src_gray);

        double time1 = static_cast<double>( getTickCount());

        threshold(src_gray, dst, 127, 255,THRESH_BINARY);
        imshow("threshold", dst);
        Img = dst;

        kernel = getStructuringElement(MORPH_RECT, Size(9,9), Point(-1, -1));

        RunningTime =  10000/ThreadNumber;
        thread th[ThreadNumber];
        for(int i = 0; i < ThreadNumber ; i++)
        {
            th[i] = thread(execute, kernel);
        }
        for(int i = 0; i < ThreadNumber ; i++)
        {
            th[i].join();
        }

        imshow("Img", Img);
        double time2 = (static_cast<double>( getTickCount()) - time1)/getTickFrequency();

        cout<<"Threads is "<< i <<", "<<"Cost: "<< time2 <<" Sec"<<endl;
    }

	waitKey();
	return 0;
}
