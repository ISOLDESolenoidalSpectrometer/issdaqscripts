//take hists of same name and put into one root file to compare more easily because I'm lazy

using namespace std;

void mult_hists( int firstrun, int subrun ){
    
    int nummods = 3, numrows = 4;
    TFile *infile;
    TH2F *pn_mult;
//    for ( int i = 0; i < numruns; i++ ){
        int run_num = firstrun;

        infile = new TFile( Form( "/TapeData/IS711/R%i_%i_events.root", run_num, subrun ) ); //read in file
        TFile *outfile = new TFile( Form( "/TapeData/IS711/anniestuff/mult_hists_run%i_%i.root" , run_num, subrun), "recreate" );

      	for ( int j = 0; j < nummods; j++ ){
            for (int k = 0; k < numrows; k++ ){

                pn_mult = (TH2F*)infile->Get( Form( "array/module_%i/pn_mult_mod%i_row%i", j, j , k ) );
                pn_mult->SetName( Form( "pn_mult_mod%i_row%i_run%i_%i", j, k, run_num, subrun ) );
                pn_mult->Write();

            } // k - rows
        } // j - modules
//    } // i - runs

    outfile->Close();

    return;
}
