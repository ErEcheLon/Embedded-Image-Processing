#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <stdlib.h>
#include <stdio.h>
#include <iostream>

using namespace std;
using namespace cv;

int main(int atgc, char ** argv)
{
    //setUseOptimized(0);
    /*setNumThreads(4);

    cout<<getNumThreads()<<endl;
    cout<<getThreadNum()<<endl;*/

    Mat img,src_gray,dst;
    Mat open, close, grad, top, black, kernel;

	img = imread("Dog.jpg", IMREAD_COLOR );
	imshow("img", img);

	cvtColor( img, src_gray, COLOR_BGR2GRAY );
	imshow("gray", src_gray);

    double time1 = static_cast<double>( getTickCount());

	threshold(src_gray, dst, 127, 255,THRESH_BINARY);
    imshow("threshold", dst);


    kernel = getStructuringElement(MORPH_RECT, Size(3,3), Point(-1, -1));

    /*morphologyEx(dst, open, MORPH_OPEN, kernel);
    for(int i=0 ; i<999 ; i++)
    {
        morphologyEx(open, open, MORPH_OPEN, kernel);
    }

	imshow("open", open);
    double time2 = (static_cast<double>( getTickCount()) - time1)/getTickFrequency();

    cout<<"花費時間"<< time2 <<"秒"<<endl;*/

	morphologyEx(dst, close, MORPH_CLOSE, kernel);
    for(int i=0 ; i<999 ; i++)
    {
        morphologyEx(close, close, MORPH_CLOSE, kernel);
    }

	imshow("close", close);
    double time2 = (static_cast<double>( getTickCount()) - time1)/getTickFrequency();

    cout<<"花費時間"<< time2 <<"秒"<<endl;

	waitKey();
	return 0;
}
