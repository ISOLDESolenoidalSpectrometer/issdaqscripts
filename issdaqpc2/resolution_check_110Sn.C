TFile* f;
const int NRUNS = 54;
TH1D* h[NRUNS+1];
TF1* fpeaks[NRUNS+1];
TGraphErrors* gres[3];

void resolution_check_110Sn(){
  gStyle->SetOptStat(0);
  TCanvas* cc = new TCanvas("cc", "cc", 1200, 800);
  cc->cd(1);
  for(int j = 0; j < 3; j++){
    gres[j] = new TGraphErrors();
  }
  int np = 0;
  for(int i = 1; i <= NRUNS; i++){
    if (i==29 || i==34 || i==36 || i==37 || i==38 || i==39 || i==40 || i==53 ) continue;
    else if (i==15 || i==54){
    cout<<"Working out 110Sn(d,p) excitation energy FWHM from R"<<i<<"_0.hist file..."<<endl;
    f = new TFile(Form("/TapeData/IS686/R%d_0_hists.root", i));
    h[i] = (TH1D*)f->Get("EBISMode/Ex_ebis_on");
    h[i]->SetLineColor(i%7);
    
    if (i==1){
      h[i]->Draw();
      h[i]->GetXaxis()->SetRangeUser(-100, 1500);
      h[i]->GetYaxis()->SetRangeUser(0, 100);
    }
    else
      h[i]->Draw("same");
    fpeaks[i] = new TF1(Form("fpeaks%d_0", i), "gaus(0)+gaus(3)+gaus(6)+pol1(9)", 0, 1400);
    fpeaks[i]->SetParameter(1, 300);
    fpeaks[i]->SetParameter(4, 750);
    fpeaks[i]->SetParameter(7, 1100);
    fpeaks[i]->SetParameter(2, 30);
    fpeaks[i]->SetParameter(5, 40);
    fpeaks[i]->SetParameter(8, 40);
    h[i]->Fit(fpeaks[i], "QN0");
    fpeaks[i]->SetLineColor(i%7);
    fpeaks[i]->Draw("same");
    
    gres[0]->SetPoint(np, i, fpeaks[i]->GetParameter(2)*2.355);
    gres[1]->SetPoint(np, i, fpeaks[i]->GetParameter(5)*2.355);
    gres[2]->SetPoint(np, i, fpeaks[i]->GetParameter(8)*2.355);
    np++;
    }
  }
  //  cc->SaveAs("is686_dp_peaks_spectra.png");
  TCanvas* cg = new TCanvas("cg", "cg", 1200, 800);
  gres[0]->SetMarkerStyle(20);
  gres[0]->GetXaxis()->SetTitle("Run");
  gres[0]->GetYaxis()->SetTitle("Peak FWHM (keV)");
  gres[1]->SetMarkerStyle(21);
  gres[1]->SetMarkerColor(2);
  gres[1]->SetLineColor(2);
  gres[2]->SetMarkerStyle(22);
  gres[2]->SetMarkerColor(4);
  gres[2]->SetLineColor(4);
  gres[0]->Draw("alp");
  gres[0]->GetYaxis()->SetRangeUser(0, 400);
  
  gres[1]->Draw("lp");
  gres[2]->Draw("lp");
  //  cg->SaveAs("is686_dp_peaks_resolution.png");
  
}
