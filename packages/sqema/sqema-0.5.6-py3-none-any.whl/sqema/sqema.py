#!/usr/bin/env/python3

"""Software for generating species abundance distributions from eDNA metabarcoding data"""

import sys
import os
import argparse
import time
import bisect
import numpy as np
import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt
from scipy.special import logit, expit
import bisect
from pathlib import Path

#Add to path
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))


def RRA(df,OTUs,samples):
	RRAs={}
	for a in OTUs:
		RRAs[a]=[]
	for a in samples:
		sample=df[a]
		total=sum(sample)
		for b in range(0,len(sample)):
			RRAs[OTUs[b]]=RRAs[OTUs[b]]+[sample[b]/total]
	mRRAs=[]
	for a in OTUs:
		mRRAs.append(np.mean(RRAs[a]))
	maxProp=max(mRRAs)
	scaledRRAs={}
	for a in range(0,len(mRRAs)):
		scaled=mRRAs[a]/maxProp
		scaledRRAs[OTUs[a]]=scaled
	return scaledRRAs
	
#RRA scaled to R of the sample - more items is more complete sampling
def RwRRA(df,OTUs,samples):
	RRAs={}
	for a in OTUs:
		RRAs[a]=[]
	for a in samples:
		sample=df[a]
		weight=np.count_nonzero(sample)/len(sample)
		total=sum(sample)
		for b in range(0,len(sample)):
			RRAs[OTUs[b]]=RRAs[OTUs[b]]+[(sample[b]/total)*weight]
	mRRAs=[]
	for a in OTUs:
		mRRAs.append(np.mean(RRAs[a]))
	maxProp=max(mRRAs)
	scaledRRAs={}
	for a in range(0,len(mRRAs)):
		scaled=mRRAs[a]/maxProp
		scaledRRAs[OTUs[a]]=scaled
	return scaledRRAs
	
def POO(df,OTUs,samples):
	POOs={}
	nsamples=len(samples)
	for a in range(len(OTUs)):
		line=(df.iloc[a]).tolist()
		zeros=line.count(0)
		POO=(nsamples-zeros)/nsamples
		POOs[OTUs[a]]=POO
	total=0
	for a in POOs:
		total=total+POOs[a]
	for a in POOs:
		POOs[a]=POOs[a]/total
	return POOs

def wPOO(df,OTUs,samples):
	nOTUs=len(OTUs)
	nSamples=len(samples)
	wPOOs={}
	for a in OTUs:
		wPOOs[a]=0
	for a in samples:
		column=df[a].tolist()
		zeros=column.count(0)
		w=nOTUs-zeros
		for b in range(nOTUs):
			if column[b]>0:
				wPOOs[OTUs[b]]=wPOOs[OTUs[b]]+w
	for a in wPOOs:
		wPOOs[a]=wPOOs[a]/nSamples
	return wPOOs

def dataTransforms(df,transform):
	if transform=='prop':
		df = df.apply(lambda x: x/max(x), axis=0)
	if transform=='arcsin_sqrt':
		df = df.apply(lambda x: x/max(x), axis=0)
		df=df.transform(lambda x: np.arcsin(np.sqrt(x)))
		df = df.apply(lambda x: x/max(x), axis=0)
	if transform=='expit_lim':
		df = df.apply(lambda x: x/(max(x)*1.0001)+0.000001, axis=0)
		df=df.apply(lambda x:expit(x))
		df=df.apply(lambda x: rescale(0,1,x),axis=0)
	return df

def scoreReadAbundance(df,OTUs,samples,metric):
	#Get relative read abundance, rank them and make new lists for OTUs and data	
	if metric=='RRA':
		scores=RRA(df,OTUs,samples)
	if metric=='RwRRA':
		scores=RwRRA(df,OTUs,samples)
	if metric=='POO':
		scores=POO(df,OTUs,samples)
	if metric=='wPOO':
		scores=wPOO(df,OTUs,samples)
	ranker=[]
	for a in OTUs:
		ranker.append((scores[a],a))
	ranker.sort()
	ranker.reverse()
	rankedOTUs=[]
	estimates=[]
	for a in ranker:
		rankedOTUs.append(a[1])
		estimates.append(a[0]) # These are the ordered estimates of abundance, in parallel with a list of names - rankedOTUs
	sumE=sum(estimates)
	propEstimates=[]
	for a in estimates:
		if sum(estimates):
			propEstimates.append(a/sumE)
		else:
			propEstimates.append(a)
	return rankedOTUs,propEstimates
	
	
#Fits curves for SADs to a list of ranked OTUs and measures of DNA abundance
def modelFit(rankedOTUs,scores,model):	
	counts=relToCounts(scores)

	if model=='logser':
		dist = sp.stats.logser
		bounds = {'p': (0,10),'loc':(0,5)} 
		res = sp.stats.fit(dist, counts, bounds)
		fz_logser=sp.stats.logser(res.params[0],res.params[1])
		xs=range(1,len(scores)+1)
		pmf=(fz_logser.pmf(xs)).tolist()
		parameters={'p':res.params[0],'loc':res.params[1]}
			
	if model=='zipf':
		dist = sp.stats.zipf
		bounds = {'a': (1, 20),'loc':(0,5)} 
		res = sp.stats.fit(dist, counts, bounds)
		fz_zipf=sp.stats.zipf(res.params[0],res.params[1])
		xs=range(1,len(scores)+1)
		pmf=(fz_zipf.pmf(xs)).tolist()
		parameters={'a':res.params[0],'loc':res.params[1]}

	if model=='genpareto':
		dist = sp.stats.genpareto
		bounds = {'c': (0, 10),'loc':(0,0.9),'scale':(0.1,10)} 
		res = sp.stats.fit(dist, counts, bounds)
		fz_genpareto=sp.stats.genpareto(res.params[0],res.params[1],res.params[2])
		xs=range(1,len(scores)+1)
		pmf=(fz_genpareto.pdf(xs)).tolist()
		parameters={'c':res.params[0],'loc':res.params[1],'scale':res.params[2]}

	if model=='lognorm':
		dist = sp.stats.lognorm
		bounds = {'s': (0, 10),'loc':(0,0.9),'scale':(0.1,10)}
		res = sp.stats.fit(dist, counts, bounds)
		fz_lognorm=sp.stats.lognorm(res.params[0],res.params[1],res.params[2])
		xs=range(1,len(scores)+1)
		pmf=(fz_lognorm.pdf(xs)).tolist()
		parameters={'s':res.params[0],'loc':res.params[1],'scale':res.params[2]}
		
	if model=='geom':
		dist = sp.stats.geom
		bounds = {'p': (0, 1),'loc':(0,5)}
		res = sp.stats.fit(dist, counts, bounds)
		fz_geom=sp.stats.geom(res.params[0],res.params[1])
		xs=range(1,len(scores)+1)
		pmf=(fz_geom.pmf(xs)).tolist()
		parameters={'p':res.params[0],'loc':res.params[1]}
		
	if model=='nbinom':
		dist = sp.stats.nbinom
		bounds = {'p':(0,1),'n': (0, 5),'loc':(0.0,5)}#,'scale':(0,10)} 
		res = sp.stats.fit(dist, counts, bounds)
		fz_nbinom=sp.stats.nbinom(res.params[0],res.params[1],res.params[2])
		xs=range(1,len(scores)+1)
		pmf=(fz_nbinom.pmf(xs)).tolist()
		parameters={'p':res.params[0],'n':res.params[1],'loc':res.params[2]}
		
	if model=='linear':
		xs=range(1,len(scores)+1)
		res = sp.stats.linregress(xs, scores)
		pmf=[]
		for a in xs:
			pmf.append((res.slope*a)+res.intercept)
		parameter=res.slope
		parameters={'slope':res.slope,'y_intercept':res.intercept}
		
	ll=loglikelihood(pmf,scores)
	return pmf,parameters,ll


	
#Compares two lists, measures the difference in logs between items, sums differences to return -LL
def loglikelihood(l1,l2):
	l=0
	for a in range(len(l1)):
		if l2[a]:
			d=np.log(abs(l1[a])/abs(l2[a]))
			if d<0:
				d=d*-1
		else:
			d=0
		l=l-d
	return l
	
#rescales a list to a new min and max
def rescale(nMin,nMax,x):
	oMin=min(x)
	oMax=max(x)
	oRange=(oMax-oMin)
	nRange=(nMax-nMin)
	out=[]
	for a in x:
		new=(((a-oMin)*nRange)/oRange)+nMin
		out.append(new)
	return out
		
#Change proportional lists to counts
def relToCounts(rel):
	if min(rel):
		multiplier=(1/min(rel))
	else:
		multiplier=10
	counts=[]
	for a in range(len(rel)):
		counts=counts+[a+1]*int(rel[a]*multiplier)
	counts.append(0)
	return counts
		
#Creates pseudoreplicated dataframes for bootstrapping
def pseudoreplicate(df):
	samples=list(df.columns.values)
	rs=[]
	for b in range(len(samples)):
		rs.append(np.random.choice(samples))
	newDF = df[rs]
	pseudoNames=[]
	for c in range(len(samples)):
		pseudoNames.append('Pseudo_'+str(c+1))
	newDF.columns=pseudoNames
	return newDF,pseudoNames
	
#Bootstrapping function for determining rank difference significance
def bootstrap(df,pseudoreplicates,pmf,OTUs,displayOTUs,metric):
	bData={}
	for a in OTUs:
		bData[a]=[]
	for r in range(pseudoreplicates):
		pseudoDF,pseudoNames=pseudoreplicate(df)
		rankedOTUs,scores=scoreReadAbundance(pseudoDF,OTUs,pseudoNames,metric)
		for p in range(len(rankedOTUs)):
			bData[rankedOTUs[p]]=bData[rankedOTUs[p]]+[scores[p]]
	boots=[]
	for a in displayOTUs:
		boots.append(bData[a])
	return boots
	
#Overall change in proportions of species between two samples
def prop_m_1(d1,d2):
	score=0
	for a in d1.keys():
		if a not in d2:
			d2[a]=0.0
	for a in d2.keys():
		if a not in d1:
			d1[a]=0.0
	for a in d1:
		diff=abs(d1[a]-d2[a])/2
		score=score+diff
	return score
	
#Calculate Simpson diversity index for one sample
def SimpsonDI(sample):
	#proportionalise
	t=sum(sample)
	props=[]
	for a in sample:
		props.append(a/t)
	squares=[]
	for a in props:
		squares.append(a**2)
	l=sum(squares)
	return l
	
	
#Calculate Shannon-Weaver diversity index for one sample
def ShannonDI(sample):
	t=sum(sample)
	plps=[]
	for a in sample:
		if a:
			p1=a/t
			plps.append(p1*np.log(p1))
	l=sum(plps)*-1
	return l
	
#Calculates the mean squared error for two lists 0f counts, expected and observed
def MSE(exp,counts):
	total=0
	for a in range(len(exp)):
		e=counts[a]-exp[a]
		se=e*e
		total=total+se
	return total*(1/len(exp))
	
#Calculates the mean absoluteerror for two lists 0f counts, expected and observed
def MAE(exp,counts):
	total=0
	for a in range(len(exp)):
		ae=abs(counts[a]-exp[a])
		total=total+ae
	return total/len(exp)
	
#Makes a cumulative distribution function for a model given its shape parameters and r species
def modelCDF(model,shape,r):	
	cdf=[]
	if model=='logser':
		for a in range(1,r):
			cdf.append(sp.stats.logser.cdf(a,shape))
	# if model=='zipf':
	# if model=='genpareto':
	if model=='lognorm':
		for a in range(1,r):
			cdf.append(sp.stats.lognorm.cdf(a,shape))
	# if model=='geom':
	# if model=='nbinom':
	# if model=='linear':
	return cdf

#Take n samples from a CDF and assign them to categories, returning counts for each
def sampleCDF(cdf,n,patchiness):
	#Cut a proportion of the cdf based on patchiness - 0.1 means 1 in ten taxa lost
	richness=len(cdf)
	nLoss=int(richness*patchiness)
	newcdf=cdf.copy()
	for a in range(nLoss):
		i=np.random.randint(len(cdf))
		if i>0:
			newcdf[i]=newcdf[i-1]
		else:
			newcdf[0]=0
	counts=[0]*(richness+1)
	for a in range(n):
		r=np.random.random()
		i = bisect.bisect_left(newcdf,r)
		counts[i]=counts[i]+1
	return counts
	
#Gives the expected counts for a sample size n in each category of a cdf
def expectedCountsCDF(cdf,n):
	exp=[]
	last=0
	for a in cdf:
		bit=a-last
		exp.append(int(bit*n))
		last=a
	return exp


#Remove zero-only rows and columns
def dataCuration(df):
	#Remove zero only rows
	removal=[]
	for a in range(1,df.shape[0]):
		row=list(df.iloc[a][1:])
		if sum(row)==0:
			removal.append(a)
	df=df.drop(index=removal)
	df.reset_index(drop=True, inplace=True)
	removed=''
	if removal:
		for a in removal:
			removed=removed+str(a)+','
	else:
		removed='None'
	print('Zero only rows removed: '+removed)
	
	#Remove the first column from the data frame and get OTU list, sample list
	OTUs=df.iloc[:, 0].tolist()
	df = df.drop(df.columns[[0,]], axis=1) 
	df.reset_index(drop=True, inplace=True)
	
	#Remove zero only columns
	removal=[]
	for col in df.columns:
		values=df[col].to_list()
		c=values.count(0)
		if len(values)==c:
			removal.append(col)
	df=df.drop(columns=removal)
	df.reset_index(drop=True, inplace=True)
	samples=list(df.columns.values[0:])
	removed=''
	if removal:
		for a in removal:
			removed=removed+str(a)+','
	else:
		removed='None'
	print('\nZero only columns removed: '+removed+'\n')
	
	#Identify identical sample and OTU names
	duplicate_samples = [i for i in set(samples) if samples.count(i) > 1]
	duplicate_OTUs = [i for i in set(OTUs) if OTUs.count(i) > 1]
	d_samples=''
	for a in duplicate_samples:
		d_samples=d_samples+str(samples[a])+', '
	d_OTUs=''
	for a in duplicate_OTUs:
		d_OTUs=d_OTUs+str(OTUs[a])+', '
	
	#Duplicate sample, OTU name alerts
	if duplicate_samples:
		print ('\nSamples with identical names present: '+d_samples)
		print('\nEdit file to remove duplicates and reload\n')
		exit()
	if duplicate_OTUs:
		print ('\nOTUs with identical names present: '+d_OTUs)
		print('\nEdit file to remove duplicates and reload\n')
		exit()
		
	#Remove spaces from OTU and sample names
	samples2=[]
	OTUs2=[]
	for a in samples:
		b=a.replace(' ','_')
		samples2.append(b)
	for a in OTUs:
		b=a.replace(' ','_')
		OTUs2.append(b)
	return df,samples2,OTUs2

	
###### transform, metric, model fitting #####
	
def fit_SAD(df,OTUs,samples,args):
	#Analyse data
	out='Metrics fitted, Fit log likelihood'
	fixedOTUs,fixedScores=scoreReadAbundance(df,OTUs,samples,args.metric)
	allStore=[]
	for t_transform in args.test_transforms:
		print('Testing transform: '+t_transform)
		for t_metric in args.test_metrics:
			print('Testing metric: '+t_metric)
			for t_model in args.test_models:
				print('Testing model: '+t_model)
				df=dataTransforms(df,t_transform)
				rankedOTUs,scores=scoreReadAbundance(df,OTUs,samples,t_metric)
				pmf, parameters,llFit=modelFit(rankedOTUs,scores,t_model)
				llFit=loglikelihood(pmf,fixedScores)
				k=len(parameters)
				AIC=2*k-2*llFit
				allStore.append((llFit,t_transform,t_metric,t_model,pmf,parameters,AIC))
	allStore.sort(reverse=True)
		
	#AIC analysis
	AIC_Store=sorted(allStore, key=lambda tup: tup[6])
	bestAIC=AIC_Store[0][6]
	AICsorter=[]
	for a in AIC_Store:
		AICdiff=bestAIC-a[6]
		if AICdiff:
			relative_likelihood=np.exp(AICdiff/2)
		else:
			relative_likelihood=0
		AICsorter.append((relative_likelihood,a[6],a[1],a[2],a[3]))

	AIClabels=['Untransformed OTU read data as '+args.metric]
	AICtext='AIC scores, relative likelihood'
	for a in AICsorter:
		AIClabels=AIClabels+[str(round(a[1],6))+', '+str(a[0])]
	AIClabels=AIClabels[:args.max_fit_plot]
		
	out='Log likelihood,Transform,Metric,Model,Model parameters,AIC,Relative Likelihood'
	for (L,A) in zip(allStore, AICsorter):
		parameters=L[5]
		parText=''
		for a in parameters:
			parText=parText+a+': '+str(parameters[a])+'; '
		out=out+'\n'+str(L[0])+', '+str(L[1])+', '+str(L[2])+', '+str(L[3])+', '+parText+', '+str(A[1])+', '+str(A[0])
		
	#Plot results
	xs=np.arange(0,len(scores))
	fig, ax = plt.subplots(figsize=(10, 10))
	plt.set_cmap('Set1')
	ax.set_title(label='Fitting for '+args.in_file)
	ax.set_axisbelow(True)
	ax.set_facecolor("linen")
	ax.grid(color='white', linestyle='-', linewidth=1)
	ax.scatter(xs,fixedScores,marker='o',facecolors='red', edgecolors='black', label='Untransformed OTU read data as '+args.metric, zorder=3)

	colorstyles=['blue','darkorange','purple','darkgreen']
	linestyles=['dashed','dashdot','dotted']
	ls=0
	cs=0
	if len(allStore) < args.max_fit_plot:
		max_fit_plot=len(allStore)
	for fit in allStore[:args.max_fit_plot]:
		lsChoice=linestyles[ls]
		csChoice=colorstyles[cs]
		ls=ls+1
		cs=cs+1
		if ls==len(linestyles):
			ls=0
		if cs==len(colorstyles):
			cs=0
		ax.plot(xs,fit[4],zorder=2,linestyle=lsChoice,color=csChoice,label=str(round(fit[0],6))+' = log likelihood: '+str(fit[1])+', '+str(fit[2])+', '+str(fit[3]))

	#Axes
	xt=np.arange(0,len(scores))
	xtext=[]
	for a in range(len(rankedOTUs)):
		xtext.append(str(a+1)+' '+rankedOTUs[a])
	ax.set_xticks(xt)
	ax.set_xticklabels(xtext,rotation=-30,ha='left',size=6)
	if args.plot_yaxis=='log':
		ax.set_yscale('log')
	plt.xlabel('OTUs in abundance order')
	plt.ylabel('Model PMF or PDF fitted to DNA abundance')
	
	#Legends
	legText='Best transform, metric, model combinations'
	legend1=ax.legend(title=legText,prop={'size': 8},loc='upper right')
	ax.add_artist(legend1)
	if args.plot_yaxis=='log':
		legend2=ax.legend(title=AICtext,prop={'size': 8},loc='lower left',labels=AIClabels)
	else:
		legend2=ax.legend(title=AICtext,prop={'size': 8},loc='right',labels=AIClabels)
	ax.add_artist(legend2)
		
	#File outputs

	plotTitle=args.out_dir+args.out_file+'_fit_SAD'+args.graph_format
	ax.plot(xs,fixedScores,color='red',drawstyle='steps-mid',linewidth=0.5, zorder=3,label=None)
	plt.savefig(plotTitle,dpi=300)
	print('\nFile saved: '+plotTitle)
	
	outputTitle=args.out_dir+args.out_file+'_fit_SAD.csv'
	f = open(outputTitle, "w")
	f.write(out)
	f.close()
	print('\nFile saved: '+outputTitle+'\n')
	

###### Estimate abundance from fitted SAD #####


def quantify(df,OTUs,samples,args):
	#Analyse data
	if args.transform!="untransf":
		df=dataTransforms(df,args.transform)
	rankedOTUs,scores=scoreReadAbundance(df,OTUs,samples,args.metric)
	pmf, parameters,llFit=modelFit(rankedOTUs,scores,args.model)
	boots=bootstrap(df,args.pseudoreplicates,pmf,OTUs,rankedOTUs,args.metric)
	end=[pmf[len(pmf)-1]]
	pmf=pmf[1:]+end
	
	#Test for significant differences in rank based on bootstrap results
	bmps=[]
	for a in range(len(rankedOTUs)-1):
		w, p = sp.stats.brunnermunzel(boots[a],boots[a+1],distribution='normal',nan_policy='omit')
		if p:
			bmps.append((p,w))
		else:
			bmps.append((0,0))
	bmps.append((1,-1))
	
	#Plot results of bootstrapping
	xs=np.arange(0,len(scores))
	fig, ax = plt.subplots(figsize=(10, 10))
	ax.set_title(label='Estimates of relative abundance from OTU table')
	ax.set_facecolor("linen")
	ax.grid(color='white', linestyle='-', linewidth=1)
	bxplt=ax.boxplot(boots,0,'', positions=xs,patch_artist=True)
	ax.plot(xs,pmf,color='red',linestyle='dashed',label='Fit of '+args.model+' model')
	ax.plot(xs,scores,color='black',linestyle='dashed',label='Measured relative DNA abundance')

	#Axes
	xt=np.arange(0,len(scores))
	xtext=[]
	for a in range(len(rankedOTUs)):
		xtext.append(str(a+1)+' '+rankedOTUs[a])
	ax.set_xticks(xt)
	ax.set_xticklabels(xtext,rotation=-30,ha='left',size=6)
	if args.plot_yaxis=='log':
		ax.set_yscale('log')
	plt.xlabel('OTUs in abundance order')
	plt.ylabel('Estimated relative abundance and model PMF/PDF')
	
	#Legend
	legText='Transform = '+args.transform+'\nMetric = '+args.metric
	legText=legText+'\nModel = '+args.model+'\nBootstrap pseudoreplicates = '+str(args.pseudoreplicates)
	ax.legend(title=legText,loc='upper right')
	

	#Plot graph and save it
	plotTitle=args.out_dir+args.out_file+'_quantify_boots'+args.graph_format
	plt.savefig(plotTitle,dpi=300)
	print('\nFile saved: '+plotTitle)
	
	
	##### Analysis for Whittaker plot  #####
	#Get tied ranks
	ranks=[]
	rank=[]
	for a in range(len(rankedOTUs)):
		rank=rank+[(rankedOTUs[a],pmf[a])]
		if bmps[a][0]<args.p_value:
			ranks=ranks+[rank]
			rank=[]
	if rank:
		ranks=ranks+[rank]

	#Get all OTUs into dictionary of OTUs: values for tied ranks
	tiedOTUs={}
	newRanks=[]
	newRank=0
	for a in ranks:
		newRank=newRank+1
		if len(a)==1:
			tiedOTUs[a[0][0]]=a[0][1]
			newRanks.append(str(newRank))
		if len(a)>1:
			tValues=0
			for b in range(len(a)):
				tValues=tValues+a[b][1]
			tValues=tValues/(b+1)
			for b in range(len(a)):
				tiedOTUs[a[b][0]]=tValues
			newRanks=newRanks+[str(newRank)+'\n~']*len(a)
				
	#Put data into vectors for Whittaker plotting
	WhittakerXs=[]
	x=1
	WhittakerYs=[]
	WhittakerLabels=[]
	WhittakerLabels2=[]
	for a in tiedOTUs:
		WhittakerXs.append(x)
		x=x+1
		WhittakerYs.append(tiedOTUs[a])
		WhittakerLabels.append('  '+a)
		WhittakerLabels2.append(str(round(tiedOTUs[a],5))+'    ')  ###
	for a in range(1,len(WhittakerLabels2)):
		if WhittakerLabels2[a-1]==WhittakerLabels2[a]:
			b=a
			while WhittakerLabels2[b]==WhittakerLabels2[a-1]:
				WhittakerLabels2[b]=' '
				if b<len(WhittakerLabels2)-1:
					b=b+1
				else:
					break
					
	#Plot Whittaker-type graph
	fig, ax = plt.subplots(figsize=(10, 10))
	ax.set_title(label='Estimated relative abundance')
	ax.set_facecolor("linen")
	ax.grid(color='white', linestyle='-', linewidth=1)
	ax.plot(WhittakerXs,pmf,color='red',linestyle='solid',label='Model fit')
	ax.plot(WhittakerXs,WhittakerYs,color='darkblue',drawstyle='steps-mid',linewidth=0.8,zorder=2)
	ax.scatter(WhittakerXs,WhittakerYs,color='darkblue',zorder=2,label='Estimated abundance')
	for (x, y, z) in zip(WhittakerXs, WhittakerYs, WhittakerLabels):
		ax.text(x, y, z, va='bottom', ha='left',rotation=30,size=7)
	for (x, y, z) in zip(WhittakerXs, WhittakerYs, WhittakerLabels2):
		ax.text(x, y, z, va='top', ha='right',rotation=00,size=6)
	
	#Axes
	xt=np.arange(1,len(WhittakerXs)+1)
	xr=ax.get_xlim()
	ax.set_xlim(xr[0]-(xr[1]*0.05), xr[1]*1.05)
	yr=ax.get_ylim()
	if args.plot_yaxis=='linear':
		ax.set_ylim(yr[0],yr[1]*1.05)
	ax.set_xticks(xt)
	ax.set_xticklabels(newRanks, size=7)

	if args.plot_yaxis=='log':
		ax.set_yscale('log')
	plt.xlabel('OTUs in abundance order')
	plt.ylabel('Relative abundance estimates')
	
	#Legend
	legText='Transform = '+args.transform+'\nMetric = '+args.metric
	legText=legText+'\nModel = '+args.model+'\nBootstrap pseudoreplicates = '+str(args.pseudoreplicates)
	legText=legText+'\np-value for Brunner-Munzel rank tests = '+str(args.p_value)
	legText=legText+'\nValues for tied ranks are means'    
	ax.legend(title=legText,loc='upper right')
	
	
	#Log results of primary estimation and bootstrapping for a .csv file
	factors=''
	for b in parameters:
		factors=factors+b+' = '+str(parameters[b])+'; '
	out='OTUs ranked by abundance,Measured DNA abundance,Estimated relative abundance,Relative abundance with means for tied ranks, Mean bootstrap estimate,Std bootstrap estimate'
	for a in range(len(rankedOTUs)-1):
		out=out+'\n'+rankedOTUs[a]+','+str(scores[a])+','+str(pmf[a])##pmf is 1-indexed
		mn=np.mean(boots[a])
		sd=np.std(boots[a])
		out=out+','+str(WhittakerYs[a])
		out=out+','+str(mn)+','+str(sd)
		
	out=out+'\n\nAbundance estimates based on OTU read counts from file,'+args.in_file
	out=out+'\nData transformation,'+args.transform
	out=out+'\nMetric for DNA abundance,'+args.metric
	out=out+'\nModel for estimating species abundance distribution,' +args.model
	out=out+'\nModel parameters,'+str(factors)
	out=out+'\nLog likelihood of model fit to DNA abundance,'+str(llFit)


	#File output 2
	#Save Whittaker plot
	plotTitle=args.out_dir+args.out_file+'_quantify_est'+args.graph_format		
	plt.savefig(plotTitle,dpi=300)
	print('\nFile saved: '+plotTitle)

	#Save analyses to .csv file
	outTitle=args.out_dir+args.out_file+'_quantify_scores.csv'
	f = open(outTitle, "w")
	f.write(out)
	f.close()
	print('\nFile saved: '+outTitle+'\n')

	
###### Get standard biodiversity metrics for an OTU table #####

def bdiv_metrics(df,samples,args):
	#Get Rs and ts
	Rs=[]
	ts=[]
	#l = Simpson, H = Shannon, R D1, D2 Hill numbers
	ls=[]
	Hs=[]
	BPs=[]
	D1s=[]
	D2s=[]
	for col in df.columns:
		values=df[col].to_list()
		t=sum(values)
		ts.append(t)
		c=values.count(0)
		R=len(values)-c
		ts.append(t)
		Rs.append(R)
		l=SimpsonDI(values)
		ls.append(l)
		D2s.append(1/l)
		H=ShannonDI(values)
		Hs.append(H)
		D1s.append(np.exp(H))
		BPs.append(max(values)/t)

	out='Sample'
	for a in range(len(samples)):
		out=out+','+samples[a]
	out=out+'\nN reads'
	for a in range(len(samples)):
		out=out+','+str(ts[a])
	out=out+'\nRichness (R)'
	for a in range(len(samples)):
		out=out+','+str(Rs[a])
	out=out+'\nSimpson index (lambda)'
	for a in range(len(samples)):
		out=out+','+str(ls[a])
	out=out+'\nGini-Simpson index'
	for a in range(len(samples)):
		out=out+','+str(1-ls[a])
	out=out+"\nShannon-Weaver diversity (H')"
	for a in range(len(samples)):
		out=out+','+str(Hs[a])
	out=out+"\nBerger-Parker index"
	for a in range(len(samples)):
		out=out+','+str(BPs[a])
	out=out+"\nHill D0"
	for a in range(len(samples)):
		out=out+','+str(Rs[a])
	out=out+"\nHill D1"
	for a in range(len(samples)):
		out=out+','+str(D1s[a])
	out=out+"\nHill D2"
	for a in range(len(samples)):
		out=out+','+str(D2s[a])
	
	#File output
	outTitle=args.out_dir+args.out_file+'_bdiv_metrics.csv'
	file1 = open(outTitle, "w") 
	file1.write(out)
	file1.close()
	print('\n\nFile saved: '+outTitle+'\n')
	

###### Get measures of dispersion for counts in a table given expected, model-based counts #####


def dispersions(df,samples,args):
	
	print ("\n\nDispersal testing with model "+ args.model+'\nShape parameter ' +str(args.shape_par))
	
	sampleN=len(df.columns)
	speciesN=len(df[df.columns[0]])
	print(sampleN,speciesN)
	
	#Get expected counts given model distribution
	cdf=[]
	if args.model=='logser':
		for a in range(1,speciesN):
			cdf.append(sp.stats.logser.cdf(a,args.shape_par))
	if args.model=='zipf':
		for a in range(1,speciesN):
			if args.shape_par<1 and args.model=='zipf':
				print ('\nzipf distribution requires a shape parameter greater than 1\n')
				return
			cdf.append(sp.stats.zipf.cdf(a,args.shape_par))

	# if model=='genpareto':

	if args.model=='lognorm':
		for a in range(1,speciesN):
			cdf.append(sp.stats.lognorm.cdf(a,args.shape_par))
		
	# if model=='geom':

	#if model=='nbinom':

	# if model=='linear':
	
	out='\nModel:,'+args.model+',Shape parameters:,'+str(args.shape_par)
	out=out+'\nCumulative frequency distribution: '
	for a in cdf:
		out=out+str(a)+','
	
	#Get data
	maes=[]
	mses=[]
	rmsds=[]
	for col in df.columns:
		values=df[col].to_list()
		total=sum(values)
		#Convert cdf to expected counts
		exp=[]
		last=0
		for a in cdf:
			bit=a-last
			exp.append(int(bit*total))
			last=a
		mae=MAE(exp,values)
		maes.append(mae)
		mse=MSE(exp,values)
		mses.append(mse)
		rmsd=np.sqrt(mse)
		rmsds.append(rmsd)
		
	#Write dispersions file
	out=out+'\n\nOTU table mean dispersions\n\n'
	m_maes=np.mean(maes)
	out=out+'mean MAE,'+str(m_maes)
	m_mses=np.mean(mses)
	out=out+'\nmean MSE,'+str(m_mses)
	m_rmsds=np.mean(rmsds)
	out=out+'\nmean RMSD,'+str(m_rmsds)+'\n\nSample dispersions\n,'
		
	out=out+'\nSample'
	for a in range(len(samples)):
		out=out+','+samples[a]
	out=out+'\nMAE,'
	for a in maes:
		out=out+str(a)+','
	out=out+'\nMSE,'
	for a in mses:
		out=out+str(a)+','
	out=out+'\nRMSD,'
	for a in rmsds:
		out=out+str(a)+','
	
	#File output
	outTitle=args.out_dir+args.out_file+'_dispersions.csv'
	file1 = open(outTitle, "w") 
	file1.write(out)
	file1.close()
	
	print('\n\nFile saved: '+outTitle+'\n')
	

###### Simulate a df and save as a .csv formatted OTU table #####

def sim_samples(args):
	cdf=modelCDF(args.model,args.shape_par,args.sim_richness)
	samples=[]
	dispersions='Measures of dispersion for simulated OTU table\nSpecies richness,'+str(args.sim_richness)+'\nSamples,'+str(args.sim_samples)+'\nCounts per sample,'+str(args.sim_counts)+'\n\nDataset means\n'
	maes=[]
	mses=[]
	rmsds=[]
	sampleNames=[]
	for a in range(args.sim_samples):
		sampleNames.append('Sample_'+str(a+1))
		sample=sampleCDF(cdf,args.sim_counts,args.patchiness)
		samples=samples+[sample]
		#Measure dispersion
		exp=expectedCountsCDF(cdf,args.sim_counts)
		mae=MAE(exp,sample)
		maes.append(mae)
		mse=MSE(exp,sample)
		mses.append(mse)
		rmsd=np.sqrt(mse)
		rmsds.append(rmsd)
	sf=pd.DataFrame(samples)
	sf=sf.transpose()
	indexNames=[]
	for a in range(args.sim_richness):
		indexNames.append('Species_'+str(a+1))
	sf.index=indexNames
	sf.columns=sampleNames
	
	#Write dispersions file
	m_maes=np.mean(maes)
	dispersions=dispersions+'mean MAE,'+str(m_maes)
	m_mses=np.mean(mses)
	dispersions=dispersions+'\nmean MSE,'+str(m_mses)
	m_rmsds=np.mean(rmsds)
	dispersions=dispersions+'\nmean RMSD,'+str(m_rmsds)+'\n\nSample dispersions\n,'
	
	for a in range(args.sim_samples):
		dispersions=dispersions+str(a+1)+','
	dispersions=dispersions+'\nMAE,'
	for a in range(args.sim_samples):
		dispersions=dispersions+str(maes[a])+','
	dispersions=dispersions+'\nMSE,'
	for a in range(args.sim_samples):
		dispersions=dispersions+str(mses[a])+','
	dispersions=dispersions+'\nRMSD,'
	for a in range(args.sim_samples):
		dispersions=dispersions+str(rmsds[a])+','
		
	#File output
	outTitle=args.out_dir+args.out_file+'_simulated.csv'
	outTitle2=args.out_dir+args.out_file+'_simulates_disp_metrics.csv'
	sf.to_csv(outTitle, index=False)
	file2 = open(outTitle2, "w") 
	file2.write(dispersions)
	file2.close()
	
	print('\n\nFile saved: '+outTitle)
	print('\nFile saved: '+outTitle2+'\n')


###### Drop samples/columns from a df and save as a new file #####

def rm_columns(df,args):
	
	#Remove samples by name
	if args.basis=='names':
		column_names = df.columns.tolist()
		removal=[]
		not_listed=[]
		for a in args.rm_names:
			if a!='':
				if a in column_names:
					removal.append(str(a))
				else:
					not_listed.append(a)
		df=df.drop(removal,axis=1)
		df.reset_index(drop=True, inplace=True)
		removed=''
		for a in removal:
			removed=removed+a+','
		print('\nSamples removed: \n')
		print(removed+'\n')
		if not_listed:
			nl=''
			for a in not_listed:
				nl=nl+a+','
			print('\nSamples names given, but not in table: \n')
			print(nl+'\n')
		
	#Remove low R samples
	if args.basis=='richness':
		column_names = df.columns.tolist()
		removal=[]
		for col in column_names[1:]:
			values=df[col].to_list()
			c=values.count(0)
			R=len(values)-c
			if R<args.minimum_R:
				removal.append(col)
		df=df.drop(columns=removal)
		df.reset_index(drop=True, inplace=True)
		removed=''
		for a in removal:
			removed=removed+a+','
		print('\nLow-R samples removed: '+removed)
		
	#Remove low read samples
	if args.basis=='low_reads':
		column_names = df.columns.tolist()
		removal=[]
		for col in column_names[1:]:
			t=sum(df[col])
			if t<args.minimum_reads:
				removal.append(col)
		df=df.drop(columns=removal)
		df.reset_index(drop=True, inplace=True)
		removed=''
		for a in removal:
			removed=removed+a+','
		print('\nLow read samples removed: '+removed)
		
	#Remove zero only rows
	removal=[]
	for a in range(1,df.shape[0]):
		row=list(df.iloc[a][1:])
		if sum(row)==0:
			removal.append(a)
	df=df.drop(index=removal)
	df.reset_index(drop=True, inplace=True)
	removed=''
	if removal:
		for a in removal:
			removed=removed+str(a)+','
	else:
		removed='None'
	print('\nZero only rows removed: '+removed)
		
	#File output		
	outTitle=args.out_dir+args.out_file+'.csv'
	df.to_csv(outTitle, index=False)
	print('\n\nFile saved: '+outTitle+'\n')
	
	
###### Drop OTUs/rows from a df and save as a new file #####

def rm_rows(df,OTUs,samples,args):
	
	#Return OTU names to dataframe
	df.insert(0, "OTU names", OTUs)
		
	#Remove OTUs named in a list
	if args.basis=='names':
		row_names=df.iloc[:,0].tolist()
		removal=[]
		not_listed=[]
		for a in args.rm_names:
			if a in row_names:
				i=row_names.index(a)
				removal.append(i)
			else:
				not_listed.append(a)
		df=df.drop(index=removal)
		df.reset_index(drop=True, inplace=True)
		removed=''
		for a in removal:
			removed=removed+row_names[a]+','
		print('\nOTUs removed: \n')
		print(removed+'\n')
		if not_listed:
			nl=''
			for a in not_listed:
				nl=nl+a+','
			print('\nOTU names given, but not in table: \n')
			print(nl+'\n')

	#Remove OTUs below a POO threshold in the dataset
	if args.basis=='POO':
		row_names=df.iloc[:,0].tolist()
		POOs=POO(df,OTUs,samples)
		removal=[]
		for a in POOs.keys():
			if POOs[a]<args.POO_threshold:
				i=OTUs.index(a)
				removal.append(i)
		removed=''
		for a in removal:
			removed=removed+row_names[a]+','
		df=df.drop(index=removal)
		df.reset_index(drop=True, inplace=True)
		print('\nOTUs removed: \n'+removed+'\n')
		
	#Remove OTUs below an SAD-defined total proportion in the dataset
	if args.basis=='low_quant':
		row_names=df.iloc[:,0].tolist()
		
		#Get quants
		if args.transform!="untransf":
			df=dataTransforms(df,args.transform)
		rankedOTUs,scores=scoreReadAbundance(df,OTUs,samples,args.metric)
		pmf, parameters,llFit=modelFit(rankedOTUs,scores,args.model)
		
		#Find threshold of low quantity
		pmf.reverse()
		i=bisect.bisect(pmf,args.quant_threshold)
		lowNames=rankedOTUs[-i-1:]
		removal=[]
		for a in lowNames:
			i=OTUs.index(a)
			if i>-1:
				removal.append(i)
		removed=''
		for a in removal:
			removed=removed+OTUs[a]+','
		df=df.drop(index=removal)
		df.reset_index(drop=True, inplace=True)
		print('\n'+str(len(removal))+ ' OTUs removed: '+removed+'\n')
		print('\nBased on SAD model: '+args.model)
		print('Metric: '+args.metric)
		print('Transform: '+args.transform)
		print('With a threshold for inclusion of > '+str(args.quant_threshold)+' estimated total proportion in the OTU table')
		print('OTUs removed: '+removed)
		
	#Remove zero only columns
	removal=[]
	for col in df.columns:
		values=df[col].to_list()
		c=values.count(0)
		if len(values)==c:
			removal.append(col)
	df=df.drop(columns=removal)
	df.reset_index(drop=True, inplace=True)
	samples=list(df.columns.values[0:])
	removed=''
	if removal:
		for a in removal:
			removed=removed+str(a)+','
	else:
		removed='None'
	print('\nZero only columns removed: '+removed)
	
	#File output			
	outTitle=args.out_dir+args.out_file+'.csv'
	df.to_csv(outTitle, index=False)
	print('\n\nFile saved: '+outTitle+'\n')
	

###### Merge columns in a df, making one column and save df as a new file #####

def merge_columns(args):
	#Get file
	df = pd.read_csv(args.in_file)
	df=df.fillna('')
		
	#Merge samples by name
	cols=[]
	cts=[]
	for a in args.merge_titles:
		cts.append(a)
	for a in cts:
		cols.append(df.loc[:,a].to_list())
	replacement=[]
	for a in range(0,len(cols[0])):
		line=str(cols[0][a])
		for b in range(1,len(cols)):
			line=line+':'+str(cols[b][a])
		line=line.replace(' ','_')
		replacement.append(line)
	df=df.drop(cts,axis=1)
	df.insert(loc=0,column=args.new_name,value=replacement)
	df.reset_index(drop=True, inplace=True)
	
	#File output
	outTitle=args.out_dir+args.out_file+'.csv'
	df.to_csv(outTitle, index=False)
	print('\n\nFile saved: '+outTitle+'\n')
	
	
###### Filter an OTU table by items specified in one column, keeping all rows that have the item #####

def filter_keep(args):
	#Get file 
	df = pd.read_csv(args.in_file)
	df=df.fillna('')
	items=[]
	for a in args.filter_items:
		items.append(a)
	col=df.loc[:,args.filter_column]
	removal=[]
	
	for a in range(len(col)):
		if col[a] not in items:
				removal.append(a)
	df=df.drop(removal,axis=0)
	df.reset_index(drop=True, inplace=True)
	
	il=''
	for a in items:
		il=il+a+', '
	
	print('\nOTUs with items: '+il+' present in column: '+str(args.filter_column)+' retained, all other rows removed.')
	
	#File output
	outTitle=args.out_dir+args.out_file+'.csv'
	df.to_csv(outTitle, index=False)
	print('\n\nFile saved: '+outTitle+'\n')


###### Filter an OTU table by items specified in one column, losing all rows that have the item #####

def filter_lose(args):
	#Get file 
	df=pd.read_csv(args.in_file)
	df=df.fillna('')
	items=[]
	for a in args.filter_items:
		items.append(a)
	col=df.loc[:,args.filter_column]
	removal=[]
	for a in range(len(col)):
		if col[a] in items:
				removal.append(a)
	df=df.drop(removal,axis=0)
	df.reset_index(drop=True, inplace=True)
	il=''
	for a in items:
		il=il+a+', '
	
	print('\nOTUs with'+il+' present in column with index '+str(args.filter_column)+' removed.')

	#File output
	outTitle=args.out_dir+args.out_file+'.csv'
	df.to_csv(outTitle, index=False)
	print('\n\nFile saved: '+outTitle+'\n')
	
	
###### Merge OTUs specified by name, aggregating thier reads in a .csv file#####

def merge_otus(args):
	#Get file 
	df=pd.read_csv(args.in_file)
	df=df.fillna('')
	mergeOTUs=[]
	for a in args.merge_titles:
		mergeOTUs.append(a)
	col=df.iloc[:,0]
	tomerge=[]
	for a in range(len(col)):
		if col[a] in mergeOTUs:
				tomerge.append(a)
				
	#Sum values down columns and make new row of values
	mls=[]
	for a in tomerge:
		l=df.iloc[a,].tolist()
		mls.append(l[1:])
	m_rows=np.array(mls)
	m_row=np.sum(m_rows, axis = 0)
	m_row.tolist()
	if args.new_name:
		new_name=args.new_name
	else:
		new_name='+'.join(mergeOTUs)+'_merged'
	m_dict={df.columns[0]:new_name}
	for a in range(len(m_row)):
		m_dict[df.columns[a+1]]=[m_row[a]]
	
	#Remove old rows, then add the new row at the end
	df=df.drop(tomerge,axis=0)
	df.reset_index(drop=True, inplace=True)
	df=pd.concat([df,pd.DataFrame(m_dict)], ignore_index=True)
	df=df.fillna('')
	il=''
	for a in mergeOTUs:
		il=il+a+', '
	
	print('\nOTUs '+il+'\n\nCombined into new OTU '+new_name+' with reads summed among samples')
	
	#File output
	outTitle=args.out_dir+args.out_file+'.csv'
	df.to_csv(outTitle, index=False)
	print('\n\nFile saved: '+outTitle+'\n')

	

#####  Main  ####

print('\n\nStarting at: '+time.strftime("%a, %d %b %Y %H:%M:%S"))

#Get arguments from the command line	
parser = argparse.ArgumentParser()

parser.add_argument("base_function", choices=['fit_SAD','quantify','bdiv_metrics','dispersions','sim_samples','rm_columns','rm_rows','merge_columns','filter_keep','filter_lose','merge_otus'],default='fitting',help='Fits eDNA metabarcoding data to SADs')

parser.add_argument("-in",'--in_file', type=str, default='sqematest_1.csv')
parser.add_argument('-od','--out_dir', type=str, default='sqema_output/')
parser.add_argument('-of','--out_file', type=str, default='')

parser.add_argument('-ttr',"--test_transforms",choices=['untransf','arcsin_sqrt','expit_lim'],default=['untransf'],type=str,nargs='+',help='A list of test transforms for comparing their effect on model fit.')
parser.add_argument('-tme',"--test_metrics",choices=['RRA','RwRRA','POO','wPOO'],default=['RRA','POO'],type=str,nargs='+',help='A list of DNA abundance metric to compare for their effect on model fit.')
parser.add_argument('-tmo',"--test_models",choices=['nbinom','logser','zipf','genpareto','lognorm','geom'],default=['logser','lognorm','zipf','nbinom'],type=str,nargs='+',help='A list of SAD models to compare for their fit to the primary data.')

parser.add_argument('-tr','--transform', choices=['untransf','arcsin_sqrt','expit_lim'],default='untransf',help='Transforms are applied to the entire dataset before other calculations.')
parser.add_argument('-me',"--metric",choices=['RRA','RwRRA','POO','wPOO'],default='RRA',help='Metrics are assigned to each OTU in a sample based on calculations derived from read count abundance.' )
parser.add_argument('-mo',"--model",choices=['logser','zipf','genpareto','lognorm','geom','linear','nbinom'],default='logser',help='The SAD models relate the rank abundance of species to their real abundance.')

parser.add_argument("-pr",'--pseudoreplicates', type=int,default=500,help='The numnber of pseudoreplicate datasets generated for estimating confidence in rank differences.')
parser.add_argument("-mfp",'--max_fit_plot', type=int,default=12,help='The maximum number of the best fitted SADs to plot.')
parser.add_argument("-pv",'--p_value', type=float,default=0.05,help='The p value for Brunner-Munzel tests for rank differences assessed on pseudoreplicated data.')

parser.add_argument('-gf','--graph_format', choices=['.svg','.png','.jpg'],default='.png',help='The format for plotting the graphs - .svg for vector graphics, .png and .jpg for raster files.')
parser.add_argument('-py','--plot_yaxis', choices=['log','linear'],default='log',help='The y-axis can be set to either a log or linear scale.')

parser.add_argument("-sp",'--shape_par', type=float,default=0.9,help='A user-supplied shape metric for defining an SAD model of expected counts.')
parser.add_argument("-pch",'--patchiness', type=float,default=0.1,help='Proportion of OTUs in a simulated sample lost due to expected eDNA patchiness.')
parser.add_argument("-simR",'--sim_richness', type=int,default=25,help='Number of species in a simulated community')
parser.add_argument("-simC",'--sim_counts', type=int,default=10000,help='Counts / sequencing reads per sample in a simulated community.')
parser.add_argument("-simN",'--sim_samples', type=int,default=25,help='Number of samples for an OTU table derived from a simulated community.')

parser.add_argument('-b','--basis', choices=['names','low_reads','richness','POO','low_quant'],default='names',help='Basis for removing either samples/columns or rows/OTUs from an OTU table.')
parser.add_argument('-rn','--rm_names', type=str,nargs='+',default='',help='Names of columns (samples) or rows (OTUs) to remove from an OTU table.')
parser.add_argument('-minR',"--minimum_R",type=int, default=2,help='Minimum OTU richness for columns in an OTU table to be retained.')
parser.add_argument('-minReads',"--minimum_reads",type=int, default=5,help='Minimum number of reads for columns in an OTU table to be retained.')
parser.add_argument('-pt','--POO_threshold', type=float,default=0.005,help='Minimum POO for OTUs to be retained.')
parser.add_argument('-qt','--quant_threshold', type=float,default=0.001,help='Minimum estimated biomass proportion for an OTU to be retained.')

parser.add_argument('-mt','--merge_titles', type=str,nargs='+',default='',help='Name for column/samples to be combined when merging columns.')
parser.add_argument('-nn','--new_name', type=str,default='merged',help='Name for a new column/sample when merging columns/rows.')
parser.add_argument('-fi','--filter_items', type=str,nargs='+',default='',help='Names as a space-separated list to be used as a filter for keeping, losing, or merging rows in an OTU table.')
parser.add_argument('-fc','--filter_column', type=str,default='',help='Title of column containing filter for keeping/losing rows in an OTU table.')

args = parser.parse_args()

 ### Organise file i/o ###
clock=time.strftime("%a, %d %b %Y %H-%M-%S")
intitle=args.in_file.split('.')[0]
intitle=intitle.split('/')[-1]
if args.in_file=='sqematest_1.csv':
	if args.base_function == 'sim_samples':
		if not args.out_file:
			args.out_file=clock
if args.out_file == '':
	args.out_file=intitle+'_'+clock
print('\nFile loaded: '+args.in_file+'\n')

defaultDir=os.path.dirname(__file__)+'/'
title=args.in_file
if not os.path.isdir(args.out_dir):
	os.mkdir(args.out_dir)
	
# Apply base function
def main():
	if args.base_function=='fit_SAD':
		if args.in_file:
			df = pd.read_csv(args.in_file)
		else:
			print('\n.csv file unreadable')
		df,samples,OTUs=dataCuration(df)
		fit_SAD(df,OTUs,samples,args)
		
	if args.base_function=='quantify':
		if args.in_file:
			df = pd.read_csv(args.in_file)
		else:
			print('\n.csv file unreadable')
		df,samples,OTUs=dataCuration(df)
		quantify(df,OTUs,samples,args)
		
	if args.base_function=='bdiv_metrics':
		if args.in_file:
			df = pd.read_csv(args.in_file)
		else:
			print('\n.csv file unreadable')
		df,samples,OTUs=dataCuration(df)
		bdiv_metrics(df,samples,args)
		
	if args.base_function=='dispersions':
		if args.in_file:
			df = pd.read_csv(args.in_file)
		else:
			print('\n.csv file unreadable')
		df,samples,OTUs=dataCuration(df)
		dispersions(df,samples,args)
		
	if args.base_function=='sim_samples':
		sim_samples(args)
		
	if args.base_function=='rm_columns':
		if args.in_file:
			df = pd.read_csv(args.in_file)
		else:
			print('\n.csv file unreadable')
		rm_columns(df,args)
		
	if args.base_function=='rm_rows':
		if args.in_file:
			df = pd.read_csv(args.in_file)
		else:
			print('\n.csv file unreadable')
		df,samples,OTUs=dataCuration(df)
		rm_rows(df,OTUs,samples,args)
		
	if args.base_function=='merge_columns':
		if args.in_file:
			df = pd.read_csv(args.in_file)
		else:
			print('\n.csv file unreadable')
		merge_columns(args)
		
	if args.base_function=='filter_keep':
		if args.in_file:
			df = pd.read_csv(args.in_file)
		else:
			print('\n.csv file unreadable')
		filter_keep(args)
		
	if args.base_function=='filter_lose':
		if args.in_file:
			df = pd.read_csv(args.in_file)
		else:
			print('\n.csv file unreadable')
		filter_lose(args)

	if args.base_function=='merge_otus':
		if args.in_file:
			df = pd.read_csv(args.in_file)
		else:
			print('\n.csv file unreadable')
		merge_otus(args)


if __name__=='__main__':
	main()
