#include <fstream>
#include <iostream>
#include <string>

#include <TFile.h>
#include <TH1F.h>
#include <TH2F.h>
#include <TH1D.h>
#include <TCanvas.h>


void Get92KrStats( std::string file_name, std::string subrun, double time ){
	// Various numbers
	int elum_peak;
    int recoil_peak1, recoil_peak2;
    float ratio;
    
//    char subrun = subrun.c_str();
    
	// File and pointers
	TFile *f = new TFile( file_name.data(), "READ" );
	TH1F *h1;
//    TH1D *h3;
    TH2F *h2;
	ofstream out_file;
	out_file.open("output_numbers.dat", ios::app);
	
	// Check files are open
	if ( !f->IsOpen() ){
		std::cerr << "FILE FAILED TO OPEN" << std::endl;
		std::exit(1);
	}
	if ( !out_file.is_open() ){
		std::cerr << "FILE FAILED TO OPEN" << std::endl;
		std::exit(1);
	}
		
	// Elum
    h1 = (TH1F*)f->Get( "ElumDetector/elum_ebis_on" );
    elum_peak = h1->Integral( 430, 550 );
		
	//Recoil Rb/Kr ratio stuff for sync tests
    h2 = (TH2F*)f->Get( "RecoilDetector/sector_0/recoil_bragg_sec0" );
    TH1D *h3 = h2->ProjectionY( Form( "projY_%s", subrun.c_str() ), 7, 7 );
    
    new TCanvas();
    h3->Draw();
    
    
    recoil_peak1 = h3->Integral(488,570);
    recoil_peak2 = h3->Integral(570,700);
    ratio = (float)recoil_peak1/(float)recoil_peak2;
    
	// Get the hist information desired
	out_file <<
		subrun << "\t" <<
		time << "\t" <<
		elum_peak << "\t" <<
        recoil_peak1 << "\t" <<
        recoil_peak2 << "\t" <<
        ratio << "\t" <<
		std::endl;
	
	// Close files
	out_file.close();
    
    TFile *outfile = new TFile( Form( "/TapeData/IS711/output_%s.root", subrun.c_str() ), "recreate" );
    
    h3->Write();
    outfile->Close();
    
	f->Close();

	return;
}

