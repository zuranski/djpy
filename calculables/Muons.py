from supy import wrappedChain

class muonLooseId(wrappedChain.calculable):
	def update(self,ignored):
		self.value = []
		for i in range(len(self.source['muonPt'])):
			if self.source['muonIsPF'][i] == 0 : continue
			if self.source['muonIsTracker'][i] == 0 and self.source['muonIsGlobal'][i] == 0 : continue
			self.value.append(i)

class muonTightId(wrappedChain.calculable):
	def update(self,ignored):
		self.value = []
		for i in range(len(self.source['muonPt'])):
			if self.source['muonIsPF'][i] == 0 : continue
			if self.source['muonIsGlobal'][i] == 0 : continue
			if self.source['muonGlobalChi2'][i] > 10 : continue
			if self.source['muonGlobalTrkValidHits'][i] == 0 : continue #that's actually ValidMuonHits
			if self.source['muonStationMatches'][i] < 2 : continue
			if self.source['muonBestTrackVtxDistXY'][i] > 0.01 : continue # tigther than recommended
			if self.source['muonBestTrackVtxDistZ'][i] > 0.1 : continue # tigther than recommended
			if self.source['muonTrkPixelHits'][i] == 0 : continue
			if self.source['muonTrackLayersWithMeasurement'][i] < 6 : continue
			self.value.append(i)

class muonIso(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [(ChgHadPt + max(0,NeuHadPt + PhPt))/Pt for ChgHadPt,NeuHadPt,PhPt,PUPt,Pt in
			zip(
			self.source['muonPFIsoR04ChargedHadron'],
			self.source['muonPFIsoR04NeutralHadron'],
			self.source['muonPFIsoR04Photon'],
			self.source['muonPFIsoR04PU'],
			self.source['muonPt'],
			)]

class muonLooseIso(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [i for i in range(len(self.source['muonPt'])) if self.source['muonIso'][i] < 0.2]

class muonTightIso(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [i for i in range(len(self.source['muonPt'])) if self.source['muonIso'][i] < 0.12]

class muonLooseIdLooseIso(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [i for i in self.source['muonLooseId'] if i in self.source['muonLooseIso']]

class muonLooseIdTightIso(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [i for i in self.source['muonLooseId'] if i in self.source['muonTightIso']]

class muonTightIdLooseIso(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [i for i in self.source['muonTightId'] if i in self.source['muonLooseIso']]

class muonTightIdTightIso(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [i for i in self.source['muonTightId'] if i in self.source['muonTightIso']]
