#ifndef WRITETOFILE_H
#define WRITETOFILE_H

#include <iostream>
#include <armadillo>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <math.h>
#include "vec3.h"
#include "solarsystem.h"

class WriteToFile
{
public:
    int WritetoFile(std::string filename, double x, double y, double z);
    int WritetoFileMatrix(std::string filename, arma::mat A, int N);
    int WritetoFile_Energy_AngMom(std::string filename, double E, double time);
};

#endif // WRITETOFILE_H
