import streamlit as st
import pandas as pd
import numpy as np
import subprocess
import glob, sys, time, statistics, os.path, random
from pathlib import Path
import psutil
import plotly.graph_objects as go
from taxontabletools2.start import TTT_variables
from taxontabletools2.utilities import load_df
from taxontabletools2.utilities import collect_replicates
from taxontabletools2.utilities import collect_sample_stats
from taxontabletools2.basic_stats import basic_stats_reads
from taxontabletools2.basic_stats import basic_stats_OTUs
from taxontabletools2.basic_stats import taxonomic_resolution
from taxontabletools2.basic_stats import taxonomic_richness
from taxontabletools2.utilities import collect_traits
from taxontabletools2.utilities import strip_traits
from taxontabletools2.utilities import check_replicates
from taxontabletools2.table_processing import replicate_merging
from taxontabletools2.table_processing import negative_control_subtraction
from taxontabletools2.table_processing import read_based_filter
from taxontabletools2.table_processing import read_based_normalisation
from taxontabletools2.table_processing import taxonomic_filtering
from taxontabletools2.table_processing import sample_filtering
from taxontabletools2.taxontable_conversion import taxon_table_converter_ttt
from taxontabletools2.taxontable_conversion import taxon_table_converter_qiime2
from taxontabletools2.WFD_tools import convert_to_perlodes
import streamlit as st
from taxontabletools2.start import start

# Call the sidebar function
settings = start()
users_settings = settings['new_user_preferences_dict']

## Page title
st.write(""" ## WFD conversion """)

# Ensure the session state variables are retained across subpages
if 'TaXon_table_df' not in st.session_state:
    error1, error2, error3 = st.columns(3)
    with error2:
        st.write('##### Please load a TaXon table to continue!')

elif 'TaXon_table_xlsx' not in st.session_state:
    error1, error2, error3 = st.columns(3)
    with error2:
        st.write('##### Please load a TaXon table to continue!')

elif st.session_state['TaXon_table_df'].empty == True:
    error1, error2, error3 = st.columns(3)
    with error2:
        st.write('##### Please check your TaXon table. It seems to be empty!')

elif st.session_state['TaXon_table_xlsx'].is_file() == False:
    error1, error2, error3 = st.columns(3)
    with error2:
        st.write('##### The TaXon table does not exist in the selected project folder!')

########################################################################################################################

else:
    st.write('### Perlodes')

    perlodes1, perlodes2 = st.columns(2)

    with perlodes1:
        available_metadata = st.session_state['metadata_df'].columns.tolist()[1:]
        selected_metadata = st.selectbox('Select river type column:', available_metadata)

    with perlodes2:
        presence_absence = st.selectbox('Convert to presence/absence data:', [True, False], index=0)

    if st.button(f'Create perlodes upload file from {selected_metadata} column.'):

        # Call the venn function and render it within Streamlit
        convert_to_perlodes(
            st.session_state['path_to_outdirs'],
            st.session_state['TaXon_table_xlsx'],
            st.session_state['TaXon_table_df'],
            st.session_state['samples'],
            st.session_state['metadata_df'],
            selected_metadata,
            st.session_state['traits_df'],
            '',
            users_settings,
            {'selected_metadata': selected_metadata,
             'presence_absence':presence_absence}
        )
