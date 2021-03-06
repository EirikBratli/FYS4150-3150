/*
Compute the 2D ising model.
*/

#include <cmath>
#include <iostream>
#include <fstream>
#include <iomanip>
#include <cstdlib>
#include <random>
#include <armadillo>

#include "Metropolis.h"
#include "System.h"

using namespace std;
using namespace arma;


int main(int argc, char* argv[])
{


  string filename;
  int n_spin, MCs;      // number of spins and number of Monte carlo simulations
  double Temp0, Temp_final, Temp_step;
  if (argc <= 1){
    cout << "Bad usage: \n";
    cout << "type filename for output, number of cycles, size of lattice, start temperature and final temperature" << endl;
    exit(1);
  }
  else{
    filename = argv[1];
    MCs = atoi(argv[2]);
    n_spin = atoi(argv[3]);
    Temp0 = atof(argv[4]);
    Temp_final = atof(argv[5]);

  }
  
  Temp_step = 0.05;
  int choise = 0; // 0 = orderd, 1= random
  cout << "======================================================" << endl;
  cout << "The Ising model using Number of MC cycles = " << MCs << endl;
  Metropolis metroplis;
  System sys;


  clock_t start, finish;
  start = clock();

  for (double T = Temp0; T<=Temp_final; T+=Temp_step){
    vec ExpValues = zeros(5);
    metroplis.metropolis(n_spin, MCs, T, ExpValues, filename, choise);

  }
  finish = clock();
  double time_used =(double)(finish - start)/(CLOCKS_PER_SEC );
  cout << "Time used on MC calculation: " << time_used << " s." << endl;
  cout << "======================================================" << endl;
  return 0;
}
