import pandas as pd
import numpy as np
from pathlib import Path
from taxontabletools2.utilities import add_traits, filter_taxontable, export_taxon_table
import plotly.graph_objects as go
import plotly.express as px
from scipy.spatial.distance import pdist, squareform
from scipy.spatial import ConvexHull
import streamlit as st
import plotly.colors
from taxontabletools2.utilities import load_df, collect_traits, strip_traits

def convert_to_perlodes(path_to_outdirs, taxon_table_xlsx, taxon_table_df, samples, metadata_df, selected_metadata, traits_df, selected_traits, user_settings, tool_settings):

    # Make copies of input dataframes to prevent altering the originals
    taxon_table_df = taxon_table_df.copy()
    metadata_df = metadata_df.copy()
    traits_df = traits_df.copy()

    # Extract relevant settings from the tool settings
    selected_metadata = tool_settings['selected_metadata']
    presence_absence = tool_settings['presence_absence']

    # Load the operational taxon list for conversion
    perlodes_TTT_conversion_xlsx = st.session_state['perlodes_TTT_conversion_xlsx']
    operational_taxon_list_df = pd.read_excel(Path(perlodes_TTT_conversion_xlsx), sheet_name="TTT import").fillna('')

    # Create a dictionary for freshwater types from metadata
    types_dict = {i[0]: i[1] for i in metadata_df[['Sample', selected_metadata]].values.tolist() if i[1] != ''}
    taxon_table_taxonomy = taxon_table_df.columns.tolist()[0:7]  # Extract taxonomy columns

    # Lists to store hits and dropped OTUs
    hit_list, dropped_list = [], []

    # Loop through the taxon table to match taxonomy with operational taxon list
    for taxonomy in taxon_table_df[taxon_table_taxonomy].values.tolist():
        # Initialize result as empty
        res = taxonomy + ['', '']

        # Check against species, genus, family, order, class, and phylum
        if taxonomy[6] != '' and taxonomy[6] in operational_taxon_list_df['Species'].values.tolist():
            res = taxonomy + operational_taxon_list_df[operational_taxon_list_df['Species'].str.contains(taxonomy[6])][
                ['ID_ART', 'Perlodes']].values.tolist()[0]
        elif taxonomy[5] != '' and taxonomy[5] in operational_taxon_list_df['Genus'].values.tolist():
            res = taxonomy + operational_taxon_list_df[operational_taxon_list_df['Genus'].str.contains(taxonomy[5])][
                ['ID_ART', 'Perlodes']].values.tolist()[0]
        elif taxonomy[4] != '' and taxonomy[4] in operational_taxon_list_df['Family'].values.tolist():
            res = taxonomy + operational_taxon_list_df[operational_taxon_list_df['Family'].str.contains(taxonomy[4])][
                ['ID_ART', 'Perlodes']].values.tolist()[0]
        elif taxonomy[3] != '' and taxonomy[3] in operational_taxon_list_df['Order'].values.tolist():
            res = taxonomy + operational_taxon_list_df[operational_taxon_list_df['Order'].str.contains(taxonomy[3])][
                ['ID_ART', 'Perlodes']].values.tolist()[0]
        elif taxonomy[2] != '' and taxonomy[2] in operational_taxon_list_df['Class'].values.tolist():
            res = taxonomy + operational_taxon_list_df[operational_taxon_list_df['Class'].str.contains(taxonomy[2])][
                ['ID_ART', 'Perlodes']].values.tolist()[0]
        elif taxonomy[1] != '' and taxonomy[1] in operational_taxon_list_df['Phylum'].values.tolist():
            res = taxonomy + operational_taxon_list_df[operational_taxon_list_df['Phylum'].str.contains(taxonomy[1])][
                ['ID_ART', 'Perlodes']].values.tolist()[0]
        else:
            dropped_list.append(taxonomy)  # Append to dropped list if no match is found

        hit_list.append(res)  # Append results for matched taxonomy

    # Create a new DataFrame from the hit list
    hit_df = pd.DataFrame(hit_list, columns=taxon_table_df.columns[0:7].values.tolist() + ['ID_ART', 'TAXON_NAME'])

    if len(hit_df) == 0:
        st.warning('No species was assigned. Please check your data.')
    else:

        # Extract the sample read counts from the taxon table
        samples_reads_df = taxon_table_df[['ID'] + samples]

        # Merge the two DataFrames based on the 'ID' column
        merged_df = pd.merge(hit_df, samples_reads_df, on='ID', how='inner')

        # Extract unique taxa with 'ID_ART' and 'TAXON_NAME'
        unique_taxa_df = merged_df[['ID_ART', 'TAXON_NAME']].drop_duplicates()

        # Initialize the list for storing presence/absence or read sum data
        perlodes_results = []

        # Loop over the unique taxa to calculate read sums or presence/absence
        for taxon_entry in unique_taxa_df.values.tolist():
            taxon_id = taxon_entry[0]
            taxon_name = taxon_entry[1]
            if taxon_name:
                # Calculate the sum of reads for the current taxon across all samples
                read_sums = merged_df[merged_df['TAXON_NAME'].str.contains(taxon_name, regex=False)][samples].sum(
                    axis=0).values.tolist()
                # Convert read counts to presence/absence if required
                if presence_absence:
                    read_sums = [0 if count == 0 else 1 for count in read_sums]
                # Append the results to the list
                perlodes_results.append([taxon_id, taxon_name] + read_sums)

        # Create header rows for the input file
        # Create a DataFrame for Perlodes output
        perlodes_df = pd.DataFrame(perlodes_results, dtype=object)  # Set dtype to object to avoid type mismatch
        perlodes_df.columns = ["ID_ART", "TAXON_NAME"] + samples

        # Insert header rows for the Perlodes output
        perlodes_df.loc[0] = ["Gewässertyp", ""] + [types_dict[i] for i in samples]  # Water type header
        perlodes_df.loc[1] = ["Taxaliste", ""] + ["original"] * len(samples)  # Taxon list header
        perlodes_df.loc[2] = ["Nutzung", ""] + ["keine"] * len(samples)  # Usage header (none)

        # Update taxon table
        taxon_table_df_perlodes = taxon_table_df.copy()
        traits_df_perlodes = traits_df.copy()
        traits_df_perlodes = pd.merge(hit_df[['ID', 'ID_ART', 'TAXON_NAME']], traits_df_perlodes, on='ID', how='inner')
        export_taxon_table(taxon_table_xlsx, taxon_table_df_perlodes, traits_df_perlodes, metadata_df, 'perlodes')

        # Export Perlodes table
        perlodes_input_xlsx = path_to_outdirs.joinpath('Perlodes', taxon_table_xlsx.stem + '_perlodes.xlsx')
        perlodes_df.to_excel(perlodes_input_xlsx, index=False)
        st.success(f'Wrote Perlodes upload file to: {perlodes_input_xlsx}')

