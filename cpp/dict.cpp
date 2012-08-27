#include <vector>
#include <map>
#include <string>

struct genjet {

   double pt,eta,phi,lxy,ctau;

};

struct trgobj {

   std::string tag;
   double pt,eta,phi,mass;
   int id;

};

struct track {

   double pt,eta,phi,vtxpt,vtxeta,vtxphi,chi2,ip2d,ip3d,ip2dsig,ip3dsig,lxy,vlxy,vtxweight,guesslxy;
   int nHits,nPixHits,algo,exo,pdgid,momid,charge;
   int nHitsInFrontOfVert,nMissHitsAfterVert;

};

struct djcandidate {

   int idx1,idx2;
   double energy,pt,eta,phi,mass;
   double truelxy;
   double phFrac,neuHadFrac,chgHadFrac,eleFrac,muFrac,PromptEnergyFrac;
   int phN,neuHadN,chgHadN,eleN,muN;
   int nDispTracks,nPrompt,nConstituents;
   double lxy,lxysig,vtxmass,vtxpt,vtxX,vtxY,vtxZ,vtxchi2,vtxCharge,vtxdR,vtxN;
   std::vector<track> disptracks;

};

#ifdef __CINT__
#pragma link C++ class genjet+;
#pragma link C++ class track+;
#pragma link C++ class djcandidate+;
#pragma link C++ class trgobj+;
#pragma link C++ class std::vector<genjet>+;
#pragma link C++ class std::vector<track>+;
#pragma link C++ class std::vector<djcandidate>+;
#pragma link C++ class std::vector<trgobj>+;
#pragma link C++ class std::map<std::string,bool>+;
#pragma link C++ class std::map<std::string,bool>::const_iterator;
#pragma link C++ class std::pair<std::string,bool>+;
#pragma link C++ class std::map<std::string,std::string>+;
#pragma link C++ class std::map<std::string,std::string>::iterator;
#pragma link C++ class std::pair<std::string,std::string>+;
#endif
