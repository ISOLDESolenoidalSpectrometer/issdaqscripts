#include "TMath.h"
#include "TFile.h"
#include "TH1.h"
#include "TH2.h"
#include "TGraph.h"
#include "TAxis.h"
#include <sys/stat.h>
#include <math.h>
#include <vector>
#include <iostream>
#include <iomanip>
#include <cstdlib>
#include <cstring>
#include <exception>
using namespace std;



std::vector<std::vector<Double_t>> appendVector(std::vector<std::vector<Double_t>> matrix, Double_t run_number, Double_t threshold){
    std::vector<Double_t>run_threshold;
    run_threshold.push_back(run_number);
    run_threshold.push_back(threshold);
    matrix.push_back(run_threshold);
    run_threshold.clear();
    return matrix;
}
std::vector<std::vector<Double_t>>runNumbers(){
    std::vector<std::vector<Double_t>> list_run_num_vs_timethreshold;
    /**
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,218,210);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,219,208);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,220,215);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,221,217);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,222,220);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,223,223);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,224,226);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,225,229);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,226,205);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,227,202);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,228,199);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,229,196);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,230,193);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,231,190);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,232,187);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,233,185);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,234,182);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,235,179);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,237,176);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,238,173);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,239,170);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,241,167);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,242,164);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,243,161);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,244,158);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,245,155);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,246,152);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,247,149);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,248,146);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,249,143);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,250,140);

    **/
   // Small Pulse height
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,59,192);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,60,196);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,61,200);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,62,202);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,63,203);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,64,204);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,65,205);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,66,206);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,67,207);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,68,208);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,69,209);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,70,210);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,71,211);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,72,212);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,73,213);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,74,214);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,75,215);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,76,216);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,81,217);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,82,218);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,83,219);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,84,220);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,85,221);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,86,222);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,87,223);

  /**
   //Medium Pulse height
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,95,184);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,96,192);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,97,196);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,98,180);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,99,176);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,100,172);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,101,170);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,102,168);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,103,166);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,104,164);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,105,162);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,106,160);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,107,158);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,108,156);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,109,154);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,110,152);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,111,150);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,112,148);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,113,146);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,114,144);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,115,142);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,116,140);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,117,138);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,118,136);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,119,134);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,120,132);
    list_run_num_vs_timethreshold=appendVector(list_run_num_vs_timethreshold,121,130);

  **/
    return list_run_num_vs_timethreshold; 
}
std::vector<Int_t> findMaximum(TH1F* histogram){
    std::vector<Int_t>number_peaks;
    Int_t width=2;
    Double_t limitValue=50;
    Double_t difference_value=10;
    Double_t average_value;
    Double_t height;
    Double_t value;
    bool is_peak;
    for (Int_t i = width; i < histogram->GetNbinsX()-width; i++)
    {
        is_peak=false;
        height=histogram->GetBinContent(i);
        average_value=0;
        for (Int_t j = i-width; j <i+width ; j++)
        {
            if (height>histogram->GetBinContent(j)&&i!=j){
                is_peak=true;
            }
            if (height<histogram->GetBinContent(j)&&i!=j){
                is_peak=false;
                break;
            }
            if (i!=j)
            {
                average_value=average_value+histogram->GetBinContent(j);
            }
            
          
        }
        average_value=average_value/(2*(Double_t)width);
        if(is_peak&&height>limitValue&&difference_value>(value-average_value)){
            value=histogram->GetBin(i);
            number_peaks.push_back(value);
        }

        
    }
    return number_peaks;
    
}

std::vector<Double_t> peakAreaIntegration(TH1F * histogram,Int_t centroid_bin){
    Double_t difference_value=40;
    Double_t width=4;
    std::vector<Double_t> peakAreas;
    Double_t value, average_value,low_range, high_range,peakArea;
    Int_t low_range_bin,high_range_bin;
    for (Int_t i = centroid_bin-1; i > 0; i--)
    {
        value=histogram->GetBinContent(i);
        average_value=0;
        for (Int_t j = i-1; j > i-width-1; j--)
        {
            average_value=average_value+histogram->GetBinContent(j);
          //  cout<<"j_low:"<<j<<"\n";
        }
       
        average_value=average_value/width;
        //cout<<"Value_low:"<<value<<" AverageValue:"<<average_value<<"\n";
        if ((value-average_value)<difference_value){
            low_range_bin=histogram->GetBin(i);
            //cout<<"Found! "<<"Value_low:"<<value<<" AverageValue:"<<average_value<<"\n";
           // cout<<"Bin_low:"<<low_range_bin<<"\n";
            break;

        }
        
    }
    for (Int_t i = centroid_bin+1; i < histogram->GetNbinsX()-width; i++)
    {
        value=histogram->GetBinContent(i);
        average_value=0;
        for (Int_t j = i+1; j < i+width+1; j++)
        {
            average_value=average_value+histogram->GetBinContent(j);
            //cout<<"j_high:"<<j<<"\n";
        }
        average_value=average_value/width;
        //cout<<"Value_high:"<<value<<" AverageValue:"<<average_value<<"\n";;
        if ((value-average_value)<difference_value){
         //   cout<<"Found! "<<"Value_high:"<<value<<" AverageValue:"<<average_value<<"\n";
            high_range_bin=histogram->GetBin(i);
          //  cout<<"Bin_high:"<<high_range_bin<<"\n";
            break;

        }
        
    }
    //+-200 ns timeDiffrence
    low_range_bin=281;
    high_range_bin=321;
    peakArea=histogram->Integral(low_range_bin,high_range_bin);
    low_range=histogram->GetXaxis()->GetBinCenter(low_range_bin);
    high_range=histogram->GetXaxis()->GetBinCenter(high_range_bin);
    peakAreas.push_back(peakArea);
    peakAreas.push_back(low_range);
    peakAreas.push_back(high_range);
    return peakAreas;
    
}

std::vector<Double_t> checkHistogram(std::vector<Double_t> run_num_vs_timethreshold,TH1F *histogram, Int_t mod, Int_t row ){
    std::vector<Double_t>results; 
    std::vector<Double_t> integrated_peak_area;
    Double_t run_number=run_num_vs_timethreshold[0];
    Double_t time_threshold=run_num_vs_timethreshold[1];
    std::vector<Int_t>maximums=findMaximum(histogram);
    
    for (Int_t i = 0; i < maximums.size(); i++)
    {
        cout<<"Peaks:"<<maximums[i]<<"\n";
    }

    Double_t number_peaks=(Double_t)maximums.size();

    results.push_back(run_number);
    results.push_back(time_threshold);
    results.push_back(number_peaks);
    cout<<"Number of Peaks:"<<number_peaks<<"\n"; 
    Double_t peakCentroid=0;
    Double_t peak_area=0;
    Double_t range_low=0;
    Double_t range_high=0;
    for (Int_t  i = 0; i < maximums.size(); i++)
    {
        
        integrated_peak_area=peakAreaIntegration(histogram,maximums[i]);
        //cout<<"PeakArea:"<<integrated_peak_area[0]<<"\n"; 
        peakCentroid=histogram->GetXaxis()->GetBinCenter(maximums[i]);
        results.push_back((Double_t)mod);
        results.push_back((Double_t)row);
        results.push_back(peakCentroid);
        results.push_back(integrated_peak_area[0]);
        results.push_back(integrated_peak_area[1]);
        results.push_back(integrated_peak_area[2]);
        
    }
    return results;
}

    Double_t checkNumberOfPulses(TH2F *matrix,Int_t channel  ){
    TH1F *projection_x=(TH1F*) matrix->ProjectionX();
    Double_t numberEvents=projection_x->GetBinContent(channel+1);
    return numberEvents;
}


void drawHistogramFigure(TH1F* histogram,std::vector<Double_t> outputValues,Double_t runNumber,Int_t mod, Int_t row,TString output_name ){
    TCanvas* c = new TCanvas("c","c",800,5000);
    histogram->GetXaxis()->SetRangeUser(-2000,2000);
    histogram->GetYaxis()->SetRangeUser(0,2000);
    histogram->Draw("hist");
    Int_t num_hist= outputValues.size()/6;
    TH1F** histogramClone=new TH1F *[num_hist];
    for (Int_t i = 7; i < outputValues.size()-1 ; i=i+6)
    {
        num_hist=(i-10)/6;
        histogramClone[num_hist]=(TH1F*) histogram->Clone(); 
        cout<<"Coloring Now on range: "<<outputValues[i]<<" and "<<outputValues[i+1] <<"\n";
        histogramClone[num_hist]->GetXaxis()->SetRangeUser(outputValues[i],outputValues[i+1]);
        histogramClone[num_hist]->SetFillColor(kBlue);
        histogramClone[num_hist]->Draw("Same");

    }
    TString number;
    number.Form("%.f",runNumber);
    TString name ="figureOutput/histograms/Run_";
    name.Append(number);
    name.Append("_module_");
    number.Form("%i",mod);
    name.Append(number);
    name.Append("_row_");
    number.Form("%i",row);
    name.Append(number);
    name.Append("_");
    name.Append(output_name);
    name.Append(".pdf");
    c->SaveAs(name.Data());


}
void doGraph(std::vector<Double_t>x,std::vector<Double_t>y,TString x_title, TString y_title, TString name_file ){
   TCanvas* c = new TCanvas("c","c",8000,4000);
   TGraph* gr=new TGraph();
   Double_t x_value,y_value;
   for (Int_t i = 0; i < x.size(); i++)
    {
            x_value=x[i];
            y_value=y[i];
            gr->AddPoint(x_value,y_value);
            cout<<"fileName: "<<name_file.Data()<<" x-value: "<<x_value<<" y-value: "<<y_value<<"\n";
        
    }
    gr->GetXaxis()->SetTitle(x_title.Data());
    gr->GetYaxis()->SetTitle(y_title.Data());
    TString name="figureOutput/plots/";
    name_file.Append(".pdf");
    name.Append(name_file);
    gr->SetMarkerStyle(20);
    gr->SetMarkerSize(20);
    gr->Draw("AP");
   
    c->SaveAs(name.Data());



}

void plotCoincidences(std::vector<std::vector<Double_t>>list_run_num_vs_timethreshold,TString output_name){
std::vector<Double_t> x_value_1,x_value_2;
TString number;
std::vector<Double_t> y_area_1peaks,y_area_2peaks,numberOfCoincidences_1peaks,numberOfCoincidences_2peaks,ratios_1peaks,ratios_2peaks;
for (Int_t mod = 0; mod < 3; mod++)
{
    for (Int_t row = 0; row < 4; row++)
    {
        for (Int_t i = 0; i < list_run_num_vs_timethreshold.size(); i++)
        {
            
                if (mod==(Int_t)list_run_num_vs_timethreshold[i][3]&&row==(Int_t)list_run_num_vs_timethreshold[i][4]&&list_run_num_vs_timethreshold[i][2]==1){
                    y_area_1peaks.push_back(list_run_num_vs_timethreshold[i][6]);
                    x_value_1.push_back(list_run_num_vs_timethreshold[i][1]);
                    numberOfCoincidences_1peaks.push_back(list_run_num_vs_timethreshold[i][9]);
                    ratios_1peaks.push_back(list_run_num_vs_timethreshold[i][6]/list_run_num_vs_timethreshold[i][9]);
                


                }
                if (mod==(Int_t)list_run_num_vs_timethreshold[i][3]&&row==(Int_t)list_run_num_vs_timethreshold[i][4]&&list_run_num_vs_timethreshold[i][2]==2){
                    y_area_2peaks.push_back(list_run_num_vs_timethreshold[i][6]+list_run_num_vs_timethreshold[i][12]);
                    
                    x_value_2.push_back(list_run_num_vs_timethreshold[i][1]);
                    numberOfCoincidences_2peaks.push_back(list_run_num_vs_timethreshold[i][15]);
                    ratios_2peaks.push_back((list_run_num_vs_timethreshold[i][6]+list_run_num_vs_timethreshold[i][12])/list_run_num_vs_timethreshold[i][15]);
                }
                
                
            
            
        }
    TString name="Plot";
    name.Append("_");
    name.Append(output_name);
    name.Append("_module_");
    number.Form("%i",mod);
    name.Append(number);
    name.Append("_row_");
    number.Form("%i",row);
    name.Append(number);
    TString name_coincidence1="";
    name_coincidence1.Append(name);
    name_coincidence1.Append("coincidence_1_Peak");
    TString name_coincidence2="";
    name_coincidence2.Append(name);
    name_coincidence2.Append("coincidence_2_Peak");
    TString name_area1="";
    name_area1.Append(name);
    name_area1.Append("area_1_Peak");
    TString name_area2="";
    name_area2.Append(name);
    name_area2.Append("area_2_Peak");
    TString name_ratio1="";
    name_ratio1.Append(name);
    name_ratio1.Append("ratio_1_Peak");
    TString name_ratio2="";
    name_ratio2.Append(name);
    name_ratio2.Append("ratio_2_Peak");
    doGraph(x_value_1,y_area_1peaks,"Time threshold","Area",name_area1);
    doGraph(x_value_2,y_area_2peaks,"Time threshold","Area",name_area2);
    doGraph(x_value_1,numberOfCoincidences_1peaks,"Time threshold","Coincidences",name_coincidence1);
    doGraph(x_value_2,numberOfCoincidences_2peaks,"Time threshold","Coincidences",name_coincidence2);
    doGraph(x_value_1,ratios_1peaks,"Time threshold","Ratio",name_ratio1);
    doGraph(x_value_2,ratios_2peaks,"Time threshold","Ratio",name_ratio2);
    y_area_1peaks.clear();
    numberOfCoincidences_1peaks.clear();
    numberOfCoincidences_2peaks.clear();
    ratios_1peaks.clear();
    ratios_2peaks.clear();
    x_value_1.clear();
    x_value_2.clear();



        
    }
    
}
}


void checkCoincidencesEventsRatio(){

cout<<"Here"<<"\n";
TFile *fileEvents;
TFile *fileCoincidence;
std::vector<std::vector<Double_t>> list_run_num_vs_timethreshold=runNumbers();
// list_maximums_for_run=<<run_number,timethreshold,number_peaks,peak_centroid_1,peak_area_1,range_low_1,range_high_1,peak_centroid_2,peak_area_2,range_low_2,range_high_2...>...>
std::vector<std::vector<Double_t>> list_pp_ratios;
std::vector<std::vector<Double_t>> list_nn_ratios;
TString nameFileEvents,nameFileCoincidence,number,histogramEventName,coincidenceEventsName;
TH2F *histogramEvents;
TH1F *histogramCoincidence;
Int_t n_module=3;
Int_t n_row=4;
Int_t channel_pp_1=15;
Int_t channel_pp_2=111;
Int_t channel_nn_1=14;
Int_t channel_nn_2=15;
Int_t channel_nn_3=110;
Int_t channel_nn_4=111;
Int_t numberPeaks;
Int_t value;
Double_t numberEvents;
TString path="/TapeData/calAug23/sorted/";
std::cout<<"Size:"<<list_run_num_vs_timethreshold.size()<<"\n";
for (Int_t i = 0; i < list_run_num_vs_timethreshold.size(); i++)
{
    nameFileEvents=path.Copy();
    nameFileEvents.Append("R");
    number.Form("%.f",list_run_num_vs_timethreshold[i][0]);
    nameFileEvents.Append(number.Data());
    nameFileCoincidence=nameFileEvents.Copy();
    nameFileEvents.Append("_0.root");
    nameFileCoincidence.Append("_0_events.root");
    fileEvents=TFile::Open(nameFileEvents,"read");
    fileCoincidence=TFile::Open(nameFileCoincidence,"read");
    
    fileEvents->ls();
    for (Int_t j = 0; j < n_module; j++)
    {
        for (Int_t k = 0; k < n_row; k++)
        {
            coincidenceEventsName="array/module_";
            number.Form("%i",j);
            coincidenceEventsName.Append(number);
            coincidenceEventsName.Append("/pp_td_mod");
            coincidenceEventsName.Append(number);
            coincidenceEventsName.Append("_row");
            number.Form("%i",k);
            coincidenceEventsName.Append(number);
            histogramCoincidence=(TH1F *)fileCoincidence->Get(coincidenceEventsName.Data());

            histogramEventName="asic_hists/module_";
            number.Form("%i",j);
            histogramEventName.Append(number);
            histogramEventName.Append("/asic_");
            histogramEventName.Append(number);
            histogramEventName.Append("_");
           
            if(k==0){
                number.Form("%i",k);
            }
            if (k==1){
                number="2";
            }
            if (k==2){
                number="3";
            }
             if (k==3){
                number="5";
            }
            histogramEventName.Append(number);
            histogramEventName.Append("_cal");
            histogramEvents=(TH2F *)fileEvents->Get(histogramEventName.Data());



            cout<<"Histogram name: "<<histogramEvents->GetName()<<"\n";
            cout<<"Histogram name: "<<histogramCoincidence->GetName()<<"\n";
            std::vector<Double_t> output=checkHistogram(list_run_num_vs_timethreshold[i],histogramCoincidence,j,k);
            cout<<"CheckedHistogram! "<<"\n";
            numberEvents=checkNumberOfPulses(histogramEvents, channel_pp_1 );
            cout<<"Number of Events1: "<<numberEvents<<"\n";
            output.push_back(numberEvents);
            numberEvents=checkNumberOfPulses(histogramEvents, channel_pp_2 );
            cout<<"Number of Events2: "<<numberEvents<<"\n";
            output.push_back(numberEvents);

            list_pp_ratios.push_back(output);
            //drawHistogramFigure(histogram,output,list_run_num_vs_timethreshold[i][0],j,k,output_name);
            output.clear();
        }
        
    }
    
     for (Int_t j = 0; j < n_module; j++)
    {
        for (Int_t k = 0; k < n_row; k++)
        {
            coincidenceEventsName="array/module_";
            number.Form("%i",j);
            coincidenceEventsName.Append(number);
            coincidenceEventsName.Append("/nn_td_mod");
            coincidenceEventsName.Append(number);
            coincidenceEventsName.Append("_row");
            number.Form("%i",k);
            coincidenceEventsName.Append(number);
            histogramCoincidence=(TH1F *)fileCoincidence->Get(coincidenceEventsName.Data());

            histogramEventName="asic_hists/module_";
            number.Form("%i",j);
            histogramEventName.Append(number);
            histogramEventName.Append("/asic_");
            histogramEventName.Append(number);
            histogramEventName.Append("_");
           
            if(k==0||k==1){
                number="1";
            }
            if(k==2||k==3){
                number="4";
            }
            
            histogramEventName.Append(number);
            histogramEventName.Append("_cal");
            histogramEvents=(TH2F *)fileEvents->Get(histogramEventName.Data());



            cout<<"Histogram name: "<<histogramEvents->GetName()<<"\n";
            std::vector<Double_t> output=checkHistogram(list_run_num_vs_timethreshold[i],histogramCoincidence,j,k);
            numberEvents=checkNumberOfPulses(histogramEvents, channel_nn_1 );
            output.push_back(numberEvents);
            numberEvents=checkNumberOfPulses(histogramEvents, channel_nn_2 );
            output.push_back(numberEvents);
            numberEvents=checkNumberOfPulses(histogramEvents, channel_nn_3 );
            output.push_back(numberEvents);
            numberEvents=checkNumberOfPulses(histogramEvents, channel_nn_4 );
            output.push_back(numberEvents);

            list_nn_ratios.push_back(output);
            //drawHistogramFigure(histogram,output,list_run_num_vs_timethreshold[i][0],j,k,output_name);
            output.clear();
        }
        
    }
    
   
    

    fileEvents->Close();
    fileCoincidence->Close();
}
 for (Int_t i = 0; i < list_nn_ratios.size(); i++)
    {
        cout<<"nn"<<"\n";
        cout<<"Run Number:"<<list_nn_ratios[i][0]<<"\n";
        cout<<"Time Threshold:"<<list_nn_ratios[i][1]<<"\n";
        cout<<"Number of Peaks:"<<list_nn_ratios[i][2]<<"\n";
        numberPeaks=(Int_t)list_nn_ratios[i][2];
        for (Int_t j = 3; j < 3+numberPeaks*6; j++)
        {
            cout<<"Module :"<<list_nn_ratios[i][j]<<"\n";
             ++j;
            cout<< "Row : "<<list_nn_ratios[i][j]<<"\n";
             ++j;
            cout<<"Centroid:"<<list_nn_ratios[i][j]<<"\n";
            ++j;
            cout<<"Area:"<<list_nn_ratios[i][j]<<"\n";
            ++j;
            cout<<"Range_low:"<<list_nn_ratios[i][j]<<"\n";
            ++j;
            cout<<"Range_high:"<<list_nn_ratios[i][j]<<"\n";

        }
        value=3+numberPeaks*6;
        cout<<"Number events 1:"<<list_nn_ratios[i][value]<<"\n";;
        cout<<"Number events 2:"<<list_nn_ratios[i][value+1]<<"\n";;
        cout<<"Number events 3:"<<list_nn_ratios[i][value+2]<<"\n";;
        cout<<"Number events 4:"<<list_nn_ratios[i][value+3]<<"\n";;

       
    }

    for (Int_t i = 0; i < list_pp_ratios.size(); i++)
    {
        cout<<"pp"<<"\n";
        cout<<"Run Number:"<<list_pp_ratios[i][0]<<"\n";
        cout<<"Time Threshold:"<<list_pp_ratios[i][1]<<"\n";
        cout<<"Number of Peaks:"<<list_pp_ratios[i][2]<<"\n";
        numberPeaks=(Int_t)list_pp_ratios[i][2];
        for (Int_t j = 3; j < 3+numberPeaks*6; j++)
        {
            cout<<"Module :"<<list_pp_ratios[i][j]<<"\n";
             ++j;
            cout<< "Row : "<<list_pp_ratios[i][j]<<"\n";
             ++j;
            cout<<"Centroid:"<<list_pp_ratios[i][j]<<"\n";
            ++j;
            cout<<"Area:"<<list_pp_ratios[i][j]<<"\n";
            ++j;
            cout<<"Range_low:"<<list_pp_ratios[i][j]<<"\n";
            ++j;
            cout<<"Range_high:"<<list_pp_ratios[i][j]<<"\n";

        }
        value=3+numberPeaks*6;
        cout<<"Number events 1:"<<list_pp_ratios[i][value]<<"\n";;
        cout<<"Number events 2:"<<list_pp_ratios[i][value+1]<<"\n";;
        

       
    }
    
    plotCoincidences(list_pp_ratios,"Small_Pulse");
    //plotCoincidences(list_nn_ratios,"Intermediate_Pulse_nn");
    //histogramName="array/module_0/pp_td_mod0_row0";
}

