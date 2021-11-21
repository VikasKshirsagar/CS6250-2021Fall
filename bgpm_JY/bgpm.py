#!/usr/bin/env python

from collections import defaultdict

import pybgpstream

import matplotlib.pyplot as plt

import os

import itertools

from statsmodels.distributions.empirical_distribution import ECDF

"""Code file for CS 6250 BGPM Project

Edit this file according to docstrings. 
Do not change the existing function name or arguments in any way.

"""

# Task 1 Part A.
def calculateUniqueIPAddresses(cache_files):
    """Retrieve the number of unique IP prefixes from input BGP data.

    Args:
        cache_files: A list of absolute file paths.
          File paths may not be in order but will end with a timestamp that can be used for sorting.
          For example: ["/rib_files_final/1357027200.120.cache", "/rib_files_final/1483257600.120.cache"]

    Returns:
        A list containing the number of unique IP prefixes for each input cache file.
          For example: [2, 5]
    """
    cache_files = sorted(cache_files, key = lambda x: x.split('.')[-3])	
    num_unique_ipfx = []
    for i in range(len(cache_files)):
        prefix = {}
        stream = pybgpstream.BGPStream(data_interface="singlefile")
        stream.set_data_interface_option("singlefile","rib-file",os.path.abspath(cache_files[i]))
        for rec in stream.records():
            for elem in rec:
                pfx = elem.fields["prefix"]
                if pfx in prefix.keys():
                    prefix[pfx] += 1
                else:
                    prefix[pfx] =1
        num_unique_ipfx.append(len(prefix.keys()))
        
    return num_unique_ipfx

def task1aGraph():
	cache_files = [os.path.join("rib_files/",x) for x in os.listdir("./rib_files")]
	#sorted_cache_files = sorted(cache_files, key = lambda x: x.split('.')[-3])
	num_unique_ipfx = calculateUniqueIPAddresses(cache_files)
	year = ["January 2013", "January 2014","January 2015", "January 2016", "January 2017", "January 2018", "January 2019", "January 2020", "January 2021"]
	fig, axs = plt.subplots(figsize=(6,4))
	axs.plot(year, num_unique_ipfx)
	axs.set_xticks(axs.get_xticks()[::2])
	plt.xlabel('Date')
	plt.title("Total Unique IP Address within the specific time period")
	plt.ylabel("Number of unique prefixes")
	plt.show()


# Task 1 Part B.
def calculateUniqueAses(cache_files):
    """Retrieve the number of unique ASes from input BGP data.

    Args:
        cache_files: A list of absolute file paths.
          File paths may not be in order but will end with a timestamp that can be used for sorting.
          For example: ["/rib_files_final/1357027200.120.cache", "/rib_files_final/1483257600.120.cache"]

    Returns:
        A list containing the number of the number of unique AS for each input file.
          For example: [2, 5]
    """
    cache_files = sorted(cache_files, key = lambda x: x.split('.')[-3])
    num_unique_ases = []
    for i in range(len(cache_files)):
        unique_ases = set()
        stream = pybgpstream.BGPStream(data_interface="singlefile")
        stream.set_data_interface_option("singlefile","rib-file",os.path.abspath(cache_files[i]))
        for rec in stream.records():
            for elem in rec:
                ases = elem.fields["as-path"].split(" ")
                if len(ases) > 0:
                	origin = ases[-1]
                	unique_ases.add(origin)
        num_unique_ases.append(len(unique_ases))
        
    return num_unique_ases

def task1bGraph():
  cache_files = [os.path.join("rib_files/",x) for x in os.listdir("./rib_files")]
  num_unique_ases = calculateUniqueAses(cache_files)
  year = ["January 2013", "January 2014","January 2015", "January 2016", "January 2017", "January 2018", "January 2019", "January 2020", "January 2021"]
  fig, axs = plt.subplots(figsize=(6,4))
  axs.plot(year, num_unique_ases)
  axs.set_xticks(axs.get_xticks()[::2])
  plt.xlabel('Date')
  plt.title("Total Unique Ases within the specific time period")
  plt.ylabel("Number of unique ases")
  plt.show()

# Task 1 Part C.
def examinePrefixes(cache_files):
    """
    Args:
        cache_files: A list of absolute file paths.
          File paths may not be in order but will end with a timestamp that can be used for sorting.
          For example: ["/rib_files_final/1357027200.120.cache", "/rib_files_final/1483257600.120.cache"]

    Returns:
        A list of the top 10 origin ASes according to percentage increase of the advertised prefixes.
        See assignment description for details.
    """
    cache_files = sorted(cache_files, key = lambda x: x.split('.')[-3])
    ases_pfx = defaultdict(list)
    for i in range(len(cache_files)):
        tem_dict = defaultdict(set)
        #tem_dict = defaultdict(list)
        stream = pybgpstream.BGPStream(data_interface="singlefile")
        stream.set_data_interface_option("singlefile","rib-file",os.path.abspath(cache_files[i]))
        
        for rec in stream.records():
            for elem in rec:
                pfx = elem.fields["prefix"]
                ases = elem.fields["as-path"].split(" ")
                if len(ases) > 0:
                    origin = ases[-1]
                    tem_dict[origin].add(pfx)

        for key, value in tem_dict.items():
            if key not in ases_pfx:
                ases_pfx[key] = [list(value)]
            else:
                ases_pfx[key] = ases_pfx[key]+ ([list(value)])    
    count = {key:(len(value[-1])/len(value[0])-1)*100 for key,value in ases_pfx.items()}
    sort_count = dict(sorted(count.items(), key =lambda kv:(kv[1], kv[0]), reverse=True))
    return (list(sort_count)[:10])

# Task 2 Part A.
def calculateShortestPath(cache_files):
    """Compute the shortest AS path length for every origin AS from input BGP data.

    Retrieves the shortest AS path length for every origin AS for every input cache file.
    Your code should return a dictionary where every key is the AS string and every value associated with the key is
    a list of shortest path lengths for that AS. See project description for details on how to do this.

    Note: For any AS that is not present in every input file, fill the corresponding entry in its list with a zero.
    Every value in the dictionary should have the same length.

    Args:
        cache_files: A list of absolute file paths.
          File paths may not be in order but will end with a timestamp that can be used for sorting.
          For example: ["/rib_files/ris.rrc06.ribs.1357027200.120.cache", "/rib_files/ris.rrc06.ribs.1483257600.120.cache]

    Returns:
        A dictionary where every key is the AS and every value associated with the key is
          a list of shortest path lengths for that AS, for every input file, sorted by date (earliest first).
          For example: {"455": [4, 0, 3], "533": [0, 1, 2]}
          corresponds to the AS "455" with shortest path lengths 4, 0 and 3 and the AS "533" with shortest paths 0, 1 and 2.
    """

    unique_ases = set()
    cache_files = sorted(cache_files, key = lambda x: x.split('.')[-3])
    num_of_files = len(cache_files)
    for i in range(num_of_files):
        stream = pybgpstream.BGPStream(data_interface="singlefile")
        stream.set_data_interface_option("singlefile","rib-file",os.path.abspath(cache_files[i]))
        for rec in stream.records():
            for elem in rec:
                ases = elem.fields["as-path"].split(" ")
                if len(ases) > 0:
                  origin = ases[-1]
                  unique_ases.add(origin)
	
    dct = dict(zip(unique_ases, [None]*len(unique_ases)))
    for k, v in dct.items():
        dct[k] = [0]*num_of_files

    for i in range(num_of_files):
        stream = pybgpstream.BGPStream(data_interface="singlefile")
        stream.set_data_interface_option("singlefile","rib-file",os.path.abspath(cache_files[i]))
        for rec in stream.records():
            for elem in rec:
                ases = elem.fields["as-path"].split(" ")
                if len(ases) > 0:
                    length = len(set(ases))
                    for item in list(set(ases)):
                    	if item in unique_ases and (dct[item][i] == 0 or length<dct[item][i]):
                    		dct[item][i]=length
    return dct


# Task 2 Part B
def task2bGraph():
	cache_files = [os.path.join("rib_files/",x) for x in os.listdir("./rib_files")]
	dct = calculateShortestPath(cache_files)
	ecdf1 = ECDF([val[0] for val in list(dct.values()) if val[0]!=0] )
	ecdf2 = ECDF([val[1] for val in list(dct.values()) if val[1]!=0])
	ecdf3 = ECDF([val[2] for val in list(dct.values()) if val[2]!=0])
	ecdf4 = ECDF([val[3] for val in list(dct.values()) if val[3]!=0])
	ecdf5 = ECDF([val[4] for val in list(dct.values()) if val[4]!=0])
	ecdf6 = ECDF([val[5] for val in list(dct.values()) if val[5]!=0])
	ecdf7 = ECDF([val[6] for val in list(dct.values()) if val[6]!=0])
	ecdf8 = ECDF([val[7] for val in list(dct.values()) if val[7]!=0])
	ecdf9 = ECDF([val[8] for val in list(dct.values()) if val[8]!=0])
	
	# plot the cdf
	plt.plot(ecdf1.x, ecdf1.y, label = "January 2013")
	plt.plot(ecdf2.x, ecdf2.y, label = "January 2014")
	plt.plot(ecdf3.x, ecdf3.y, label = "January 2015")
	plt.plot(ecdf4.x, ecdf4.y, label = "January 2016")
	plt.plot(ecdf5.x, ecdf5.y, label = "January 2017")
	plt.plot(ecdf6.x, ecdf6.y, label = "January 2018")
	plt.plot(ecdf7.x, ecdf7.y, label = "January 2019")
	plt.plot(ecdf8.x, ecdf8.y, label = "January 2020")
	plt.plot(ecdf9.x, ecdf9.y, label = "January 2021")
	plt.legend()
	plt.xlabel('Path Length')
	plt.ylabel('% of Ases')
	plt.title('ECDF of the Shortest Path Lengths')
	plt.show()


# Task 3 Part A.
def calculateRTBHDurations(cache_files):
    """Identify blackholing events and compute the duration of all RTBH events from input BGP data.

    Identify events where the IPV4 prefixes are tagged with at least one Remote Triggered Blackholing (RTBH) community.
    See project description for details on how to do this.

    Args:
        cache_files: A list of absolute file paths.
          File paths may not be in order but will end with a timestamp that can be used for sorting.
          For example: ["/update_files_blackholing/ris.rrc06.ribs.1357027200.120.cache", "/update_files_blackholing/ris.rrc06.ribs.1483257600.120.cache]

    Returns:
        A dictionary where each key is a peerIP and each value is another dictionary with key equal to a
            prefix and each value equal to a list of explicit RTBH event durations.
            For example: {"455": {"123": [4, 1, 3]}}
            The above example corresponds to the peerIP "455", the prefix "123" and event durations of 4, 1 and 3.
    """
    cache_files = sorted(cache_files, key = lambda x: x.split('.')[-3])
    dct = defaultdict(lambda:defaultdict(list))
    last_anm = defaultdict(lambda:defaultdict(lambda:[0,0]))
    for i in range(len(cache_files)):
    	stream = pybgpstream.BGPStream(data_interface="singlefile",filter = 'ipversion 4')
    	stream.set_data_interface_option("singlefile","rib-file",os.path.abspath(cache_files[i]))
    	for rec in stream.records():
    		for elem in rec:
    			time = elem.time
    			peer_ip = elem.peer_address
    			pfx = elem.fields['prefix']
    			t = elem.type
    			if t == 'A':
    				comm = elem.fields['communities']
    				if str(comm).find(':666') !=-1:
    					last_anm[peer_ip][pfx][0]='A'
    					last_anm[peer_ip][pfx][1]=time
    				elif last_anm[peer_ip][pfx]:
    					del last_anm[peer_ip][pfx]
    			if t == 'W':
    				if last_anm[peer_ip][pfx]:
    					if last_anm[peer_ip][pfx][0] == 'A':
    						duration = time - last_anm[peer_ip][pfx][1]
    						if duration>0:
    							dct[peer_ip][pfx].append(duration)
    						last_anm[peer_ip][pfx][0] = 'W'						
    return dct


def task3bGraph():
	cache_files = [os.path.join("update_files_blackholing/",x) for x in os.listdir("./update_files_blackholing")]
	dct = calculateRTBHDurations(cache_files)
	nested_list = list()
	for k1, v1 in dct.items():
		for k2, v2 in v1.items():
			nested_list.extend(v2)
	ecdf = ECDF(nested_list)
	plt.plot(ecdf.x, ecdf.y)
	plt.xlabel('Durations')
	plt.ylabel('% of Events')
	plt.title('Event Durations')
	plt.show()
	
				
# Task 4.
def calculateAWDurations(cache_files):
    """Identify Announcement and Withdrawal events and compute the duration of all explicit AW events in the input data.

    Identify explicit AW events.
    See project description for details on how to do this.

    Args:
        cache_files: A list of absolute file paths.
          File paths may not be in order but will end with a timestamp that can be used for sorting.
          For example: ["/update_files/ris.rrc06.ribs.1357027200.120.cache", "/update_files/ris.rrc06.ribs.1483257600.120.cache]

    Returns:
        A dictionary where each key is a peerIP and each value is another dictionary with key equal to a
            prefix and each value equal to a list of explicit AW event durations.
            For example: {"455": {"123": [4, 1, 3]}}
            The above example corresponds to the peerIP "455", the prefix "123" and event durations of 4, 1 and 3.
    """
    cache_files = sorted(cache_files, key = lambda x: x.split('.')[-3])
    dct = defaultdict(lambda:defaultdict(list))
    last_anm = defaultdict(lambda:defaultdict(lambda:[0,0]))
    for i in range(len(cache_files)):
      stream = pybgpstream.BGPStream(data_interface="singlefile")
      stream.set_data_interface_option("singlefile","rib-file",os.path.abspath(cache_files[i]))
      for rec in stream.records():
        for elem in rec:
          time = elem.time
          peer_ip = elem.peer_address
          t = elem.type
          if t == 'A':
          	pfx = elem.fields['prefix']
          	last_anm[peer_ip][pfx][0]='A'
          	last_anm[peer_ip][pfx][1]=time
          if t == 'W':
          	pfx = elem.fields['prefix']
          	if last_anm[peer_ip][pfx]:
          		if last_anm[peer_ip][pfx][0] == 'A':
          			duration = time - last_anm[peer_ip][pfx][1]
          			if duration>0:
          				dct[peer_ip][pfx].append(duration)
          			last_anm[peer_ip][pfx][0] = 'W'  
    return dct


if __name__ == '__main__':

	task1aGraph()
	task1bGraph()
	task2bGraph()
	task3bGraph()
