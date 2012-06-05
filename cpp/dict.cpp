#include <vector>

struct exotic {

   double pt,eta,phi,mass,lxy,ctau;

};

struct genjet {

   double pt,eta,phi,lxy;

};

struct track {

   double pt,eta,phi,chi2,ip2d,ip3d,ip2dsig,ip3dsig,lxy,vtxweight;
   int nHits,nPixHits,algo;

};

struct pfjet {

   double energy,pt,eta,phi,mass;
   double phFrac,neuHadFrac,chgHadFrac,eleFrac,muFrac,PromptEnergyFrac;
   int phN,neuHadN,chgHadN,eleN,muN,nPrompt;
   double lxy,lxysig,vtxmass,vtxpt,vtxchi2;
   int nDispTracks;
   std::vector<track> disptracks;

};

struct pfjetpair : pfjet {

   int idx1,idx2;

};

struct trgObj {

   double pt,eta,phi,energy,id;

};

#ifdef __CINT__
#pragma link C++ class exotic+;
#pragma link C++ class genjet+;
#pragma link C++ class track+;
#pragma link C++ class pfjet+;
#pragma link C++ class pfjetpair+;
#pragma link C++ class trgObj+;
#pragma link C++ class std::vector<exotic>+;
#pragma link C++ class std::vector<genjet>+;
#pragma link C++ class std::vector<track>+;
#pragma link C++ class std::vector<pfjet>+;
#pragma link C++ class std::vector<pfjetpair>+;
#pragma link C++ class std::vector<trgObj>+;
#endif
