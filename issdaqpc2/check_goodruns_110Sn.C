TFile* f;
const int NRUNS = 26;
TH1D* h;
TH2D* m[3];

TF1* fpeaks[NRUNS+1];
TGraphErrors* gres[3];


void check_goodruns_110Sn(int run, int subrun){
  //  gStyle->SetOptStat(0);
  TCanvas* cc = new TCanvas("cc", "cc", 1200, 800);
  cc->cd(1);
  f = new TFile(Form("/TapeData/IS686/R%d_%d_hists.root", run, subrun));
  h = (TH1D*)f->Get("EBISMode/Ex_ebis_on");
  h->Draw();

  TCanvas* cm = new TCanvas("cm", "cm", 1500, 600);
  cm->Divide(3,1);
  for(int i = 0; i < 3; i++){
    m[i] = (TH2D*)f->Get(Form("EBISMode/module_%d/E_vs_z_ebis_on_mod%d", i, i));
    cm->cd(i+1);
    m[i]->Draw("colz");
  }
}
