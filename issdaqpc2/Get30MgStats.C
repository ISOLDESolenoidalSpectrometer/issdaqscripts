#include <fstream>
#include <iostream>
#include <string>

#include <TFile.h>
#include <TH1F.h>
#include <TH2F.h>

void Get30MgStats( std::string file_name, std::string subrun, double time ){
	// Various numbers
	const int NUM_SECTORS = 4;
	int Ex_integral = -1;
	int Ex_integral_lower_excited_states = -1;
	int elum_sector_peak[NUM_SECTORS];
	int recoil_sector_peak[NUM_SECTORS];
	
	// File and pointers
	TFile *f = new TFile( file_name.data(), "READ" );
	TH1F *h1;
	TH2F* h2;
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
	
	// Excitation energy counts
	h1 = (TH1F*)f->Get("RecoilMode/Ex_recoil");
	Ex_integral = h1->Integral();
	Ex_integral_lower_excited_states = h1->Integral( h1->FindBin( -1000 ), h1->FindBin( 2000 ) );
	
	// Elum sectors
	for ( int i = 0; i < NUM_SECTORS; ++i ){
		h1 = (TH1F*)f->Get( Form( "ElumDetector/sector_%d/elum_ebis_on_sec%d", i, i ) );
		elum_sector_peak[i] = h1->Integral( h1->FindBin( 1000 ), h1->FindBin( 1600 ) );
		
		h2 = (TH2F*)f->Get( Form( "RecoilDetector/sector_%d/recoil_EdE_sec%d", i, i ) );
		recoil_sector_peak[i] = h2->Integral();
		
	}
	
	// Get the hist information desired
	out_file <<
		subrun << "\t" <<
		time << "\t" <<
		Ex_integral << "\t" <<
		Ex_integral_lower_excited_states << "\t" <<
		elum_sector_peak[0] << "\t" <<
		elum_sector_peak[1] << "\t" <<
		elum_sector_peak[2] << "\t" <<
		elum_sector_peak[3] << "\t" <<
		recoil_sector_peak[0] << "\t" <<
		recoil_sector_peak[1] << "\t" <<
		recoil_sector_peak[2] << "\t" <<
		recoil_sector_peak[3] << "\t" <<
		std::endl;
	
	// Close files
	out_file.close();
	f->Close();

	return;
}
