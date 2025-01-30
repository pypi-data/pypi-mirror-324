import os
import sys
import argparse

import pybedtools

import tempfile
import uuid

import numpy as np
import pandas as pd

from .util import atoi, natural_keys, bed_file

def get_df(path, category_field_num):
	
	if os.path.isdir(path):
	
		filenames = os.listdir(path)
		filenames = list(filter(bed_file, filenames))
		filenames.sort(key=natural_keys)
		
		filepaths = [os.path.join(path, filename) for filename in filenames]
		
		dfs = []
		
		for i, filepath in enumerate(filepaths):
			
			df = pd.read_csv(filepath, sep='\t', header=None, usecols=[0,1,2])
			df[3] = filenames[i].replace('.bed', '')
			
			# ensure consistent naming convention
			df[0] = [f'chr{i}' if 'chr' not in f'{i}' else i for i in list(df[0])]
			
			dfs.append(df)
			
		df_merged = pd.concat(dfs)
		
		return df_merged, 3
		
	else:
		
		if category_field_num is not None:
		
			df = pd.read_csv(path, sep='\t', header=None, usecols=[0, 1, 2, int(category_field_num)])
			
			# ensure consistent naming convention
			df[0] = [f'chr{i}' if 'chr' not in f'{i}' else i for i in list(df[0])]
			
			return df, int(category_field_num)
			
		else:
			
			print(f'Please provide a field number for identifying categories in {path}')
			sys.exit()

def odds_ratio_intersection(path_1, path_2, category_field_num_1, category_field_num_2):
	
	temp_dir = tempfile.gettempdir()
	
	df_1, category_field_num_1 = get_df(path_1, category_field_num_1)
	df_2, category_field_num_2 = get_df(path_2, category_field_num_2)
	
	categories_1 = sorted(list(set(df_1[category_field_num_1].tolist())), key=natural_keys)
	categories_2 = sorted(list(set(df_2[category_field_num_2].tolist())), key=natural_keys)
	
	path_tmp_1 = os.path.join(temp_dir, f'{str(uuid.uuid4())}.bed')
	path_tmp_2 = os.path.join(temp_dir, f'{str(uuid.uuid4())}.bed')
	
	df_1.to_csv(path_tmp_1, sep='\t', header=False, index=False)
	df_2.to_csv(path_tmp_2, sep='\t', header=False, index=False)
	
	bedtool_1 = pybedtools.BedTool(path_tmp_1)
	bedtool_2 = pybedtools.BedTool(path_tmp_2)
	
	bedtool_1.sort()
	bedtool_2.sort()
	
	num_fields_1 = bedtool_1.field_count()
	num_fields_2 = bedtool_2.field_count()
	
	intersection = bedtool_1.intersect(bedtool_2, wo=True)
	
	# the inverse intersections also need to be accounted for
	# everything in bedtool 1 that doesn't overlap with anything is a "false positive" along with other categorizations
	# everything in bedtool 2 that doesn't overlap with a feature is a "true negative" along with other categorizations
	intersection_v_1 = bedtool_1.intersect(bedtool_2, v=True)
	intersection_v_2 = bedtool_2.intersect(bedtool_1, v=True)
	
	path_tmp_3 = os.path.join(temp_dir, f'{str(uuid.uuid4())}.bed')
	intersection.saveas(path_tmp_3)
	
	path_tmp_4 = os.path.join(temp_dir, f'{str(uuid.uuid4())}.bed')
	intersection_v_1.saveas(path_tmp_4)
	
	path_tmp_5 = os.path.join(temp_dir, f'{str(uuid.uuid4())}.bed')
	intersection_v_2.saveas(path_tmp_5)
	
	df = pd.read_csv(path_tmp_3, sep='\t', header=None)
	
	odds_records = []
	
	for category_1 in categories_1:
		
		for category_2 in categories_2:
		
			df_filtered = df.loc[(df[category_field_num_1] == category_1) & (df[num_fields_1 + category_field_num_2] == category_2)]
			
			# Number of overlaps and lengths
			num_overlaps = len(df_filtered.index)
			total_overlap_length = np.sum(df_filtered[len(df_filtered.columns) - 1])
			
			odds_records.append({'category_1': category_1, 'category_2': category_2, 'num_overlaps': num_overlaps, 'bp_overlap': total_overlap_length})
			
			
	df_v_1 = pd.read_csv(path_tmp_4, sep='\t', header=None)
	df_v_1['length'] = df_v_1[2] - df_v_1[1]
	
	for category_1 in categories_1:
		
		df_filtered = df_v_1.loc[(df_v_1[category_field_num_1] == category_1)]
		
		# Number of overlaps and lengths
		num_overlaps = len(df_filtered.index)
		total_overlap_length = np.sum(df_filtered['length'])
		
		odds_records.append({'category_1': category_1, 'category_2': 'NULL', 'num_overlaps': num_overlaps, 'bp_overlap': total_overlap_length})
	
	df_v_2 = pd.read_csv(path_tmp_5, sep='\t', header=None)
	df_v_2['length'] = df_v_2[2] - df_v_2[1]
	
	for category_2 in categories_2:
	
		df_filtered = df_v_2.loc[(df_v_2[category_field_num_2] == category_2)]
		
		# Number of overlaps and lengths
		num_overlaps = len(df_filtered.index)
		total_overlap_length = np.sum(df_filtered['length'])
		
		odds_records.append({'category_1': 'NULL', 'category_2': category_2, 'num_overlaps': num_overlaps, 'bp_overlap': total_overlap_length})
	
	df_odds = pd.DataFrame.from_records(odds_records)
	
	os.remove(path_tmp_1)
	os.remove(path_tmp_2)
	os.remove(path_tmp_3)
	os.remove(path_tmp_4)
	os.remove(path_tmp_5)
	
	return df_odds

# DESCRIPTION
# --------
# Script will intersect path_1 with path_2
# --------

# TF Binding BASiCS Mean
#odds_ratio_intersection -path_1 /home/data/Shared/shared_datasets/chip_seq/data/GSE61475/data/ecto/bed/input -path_2 /home/data/Shared/shared_datasets/sc_rna_seq/nlaszik/dko_mean_basics_promoter_type -path_out_csv /home/data/Shared/shared_datasets/sc_rna_seq/nlaszik/tko_mean_basics_promoter_type/tf_binding_ecto/tf.test.lod_odds.csv

#odds_ratio_intersection -path_1 /home/data/Shared/shared_datasets/sc_rna_seq/nlaszik/dko_mean_basics -path_2 /home/data/Shared/shared_datasets/chip_seq/nlaszik/bivalent_chromatin_hesc_10.18632-oncotarget.13746.bed -category_field_num_2 3 -path_out_csv /home/data/Shared/shared_datasets/sc_rna_seq/nlaszik/dko_mean_basics/ChromatinClassificationAlt.log_odds.csv

#odds_ratio_intersection -path_1 /home/data/Shared/shared_datasets/sc_rna_seq/nlaszik/dko_noise_basics -path_2 /home/data/Shared/shared_datasets/chip_seq/nlaszik/bivalent_chromatin_hesc_10.18632-oncotarget.13746.bed -category_field_num_2 3 -path_out_csv /home/data/Shared/shared_datasets/sc_rna_seq/nlaszik/dko_noise_basics/ChromatinClassificationAlt.log_odds.csv

# Chromatin
#odds_ratio_intersection -path_1 /home/data/Shared/shared_datasets/sc_rna_seq/nlaszik/tko_zero_ratio/tko_zero_ratio_0.2.bed -path_2 /home/data/Shared/shared_datasets/chip_seq/nlaszik/bivalent_chromatin_hesc_10.18632-oncotarget.13746.bed -category_field_num_1 7 -category_field_num_2 3 -path_out_csv /home/data/Shared/shared_datasets/sc_rna_seq/nlaszik/tko_zero_ratio/chromatin_class_0.2.log_odds.csv

# DMR
#odds_ratio_intersection -path_1 /home/data/Shared/shared_datasets/sc_rna_seq/nlaszik/tko_zero_ratio/tko_zero_ratio_downstream_0.15.bed -category_field_num_1 8 -path_2 /home/data/Shared/shared_datasets/wgbs/nlaszik/wt_tko_wgbs_intersect/dmr_0.7 -path_out_csv /home/data/Shared/shared_datasets/sc_rna_seq/nlaszik/tko_zero_ratio/dmr0.7_0.15.log_odds.csv

# TF
#odds_ratio_intersection -path_1 /home/data/Shared/shared_datasets/sc_rna_seq/nlaszik/tko_zero_ratio/tko_zero_ratio_0.15.bed -category_field_num_1 8 -path_2 /home/data/Shared/shared_datasets/chip_seq/data/GSE61475/data/h64/bed/input -path_out_csv /home/data/Shared/shared_datasets/sc_rna_seq/nlaszik/tko_zero_ratio/tf_0.15.log_odds.csv


# Aging DMRs and TKO DMRs
#odds_ratio_intersection -path_1 /home/data/Shared/shared_datasets/wgbs/nlaszik/wt_tko_wgbs_intersect/dmr_0.3 -path_2 /home/data/Shared/shared_datasets/wgbs/data/GSE31263/dmr_0.3 -path_out_csv /home/data/Shared/shared_datasets/wgbs/nlaszik/wt_tko_wgbs_intersect/aging_dmr_0.3_tko_dmr_0.3.log_odds.csv

# Aging DMRs and DKO DMRs
#odds_ratio_intersection -path_1 /home/data/Shared/shared_datasets/wgbs/nlaszik/wt_wgbs/stratified_wgbs_0.05 -path_2 /home/data/Shared/shared_datasets/wgbs/data/GSE31263/dmr_0.2 -path_out_csv /home/data/Shared/shared_datasets/wgbs/nlaszik/wt_wgbs/aging_dmr_0.2.log_odds.csv

# Aging DMRs and TKO/DKO/LowWT
#odds_ratio_intersection -path_1 /home/data/Shared/shared_datasets/sc_rna_seq/nlaszik/tko_zero_ratio/tko_h3k4me3_downstream_upstream.bed -category_field_num_1 6 -path_2 /home/data/Shared/shared_datasets/wgbs/nlaszik/wt_tko_wgbs_intersect/dmr_0.3 -path_out_csv /home/data/Shared/shared_datasets/sc_rna_seq/nlaszik/tko_zero_ratio/h3k4me3_updown_dmr_0.3.log_odds.csv


# TKO DMRs and Bivalent Upstream/Downstream
#odds_ratio_intersection -path_1 /home/data/Shared/shared_datasets/sc_rna_seq/nlaszik/tko_zero_ratio/tko_bivalent_downstream_upstream.bed -category_field_num_1 6 -path_2 /home/data/Shared/shared_datasets/wgbs/nlaszik/wt_tko_wgbs_intersect/dmr_0.3 -path_out_csv /home/data/Shared/shared_datasets/sc_rna_seq/nlaszik/tko_zero_ratio/bivalent_updown_dmr_0.3.log_odds.csv

# TKO DMRs and H3K4me3 Upstream/Downstream
#odds_ratio_intersection -path_1 /home/data/Shared/shared_datasets/sc_rna_seq/nlaszik/tko_zero_ratio/tko_h3k4me3_downstream_upstream.bed -category_field_num_1 6 -path_2 /home/data/Shared/shared_datasets/wgbs/nlaszik/wt_tko_wgbs_intersect/dmr_0.3 -path_out_csv /home/data/Shared/shared_datasets/sc_rna_seq/nlaszik/tko_zero_ratio/h3k4me3_updown_dmr_0.3.log_odds.csv



def parse_arguments():
	"""
	Parses command-line arguments.
	"""
	parser = argparse.ArgumentParser()
	
	parser.add_argument("-path_1", required = True)
	parser.add_argument("-path_2", required = True)
	parser.add_argument("-path_out_csv", required = True)
	parser.add_argument("-category_field_num_1", required = False)
	parser.add_argument("-category_field_num_2", required = False)
	
	# get arguments
	return parser.parse_args()

def main():
	
	"""
	Main function for command-line usage.
	"""
	args = parse_arguments()
	
	path_1 = args.path_1
	path_2 = args.path_2
	path_out_csv = args.path_out_csv
	category_field_num_1 = args.category_field_num_1
	category_field_num_2 = args.category_field_num_2
	
	df = odds_ratio_intersection(path_1, path_2, category_field_num_1, category_field_num_2)
	
	df.to_csv(path_out_csv)
	
	pybedtools.helpers.cleanup()

if __name__ == "__main__":
	main()



