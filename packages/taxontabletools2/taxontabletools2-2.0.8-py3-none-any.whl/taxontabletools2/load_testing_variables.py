from taxontabletools2.utilities import load_df, collect_traits, strip_traits
from pathlib import Path

path_to_outdirs = Path('/Users/tillmacher/Desktop/TTT_projects/AA_test')
taxon_table_xlsx = Path('/Users/tillmacher/Desktop/TTT_projects/AA_test/TaXon_tables/Ruwer_eDNA_fish_2024_d4_taxon_table_RuMo_merged_NCsub_fish_norm.xlsx')
taxon_table_df = load_df(taxon_table_xlsx)
selected_metadata = 'River type'
traits_df = collect_traits(taxon_table_df)
taxon_table_df = strip_traits(taxon_table_df)
samples = list(taxon_table_df.columns[9:])
metadata_df = pd.read_excel(taxon_table_xlsx, sheet_name='Metadata Table').fillna('')
user_settings = {'project_name': 'AA_test', 'path_to_outdirs': Path('/Users/tillmacher/Desktop/TTT_projects'),
                 'plot_height': 1000, 'plot_width': 1000, 'show_legend': True, 'template': 'simple_white',
                 'font_size': 20, 'clustering_unit': 'ESVs', 'scatter_size': 15, 'color_1': 'navy', 'color_2': 'teal',
                 'colorsequence': 'Plotly', 'colorscale': 'blues'}
tool_settings = {'selected_metadata': 'Sort', 'presence_absence': True}
perlodes_TTT_conversion_xlsx = Path('/Users/tillmacher/Documents/GitHub/TaxonTableTools2.0/taxontabletools2/WFD_conversion/perlodes_TTT_conversion.xlsx')




path_to_outdirs = Path('/Users/tillmacher/Desktop/TTT_projects/AA_test')
taxon_table_xlsx = Path('/Users/tillmacher/Desktop/TTT_projects/AA_test/TaXon_tables/GeDNA_MZB_20_21_taxon_table_cons_NCsub_MZB_merged_shared.xlsx')
taxon_table_df = load_df(taxon_table_xlsx)
selected_metadata = 'River'
traits_df = collect_traits(taxon_table_df)
taxon_table_df = strip_traits(taxon_table_df)
samples = list(taxon_table_df.columns[9:])
metadata_df = pd.read_excel(taxon_table_xlsx, sheet_name='Metadata Table').fillna('')
user_settings = {'project_name': 'AA_test', 'path_to_outdirs': Path('/Users/tillmacher/Desktop/TTT_projects'),
                 'plot_height': 1000, 'plot_width': 1000, 'show_legend': True, 'template': 'simple_white',
                 'font_size': 20, 'clustering_unit': 'ESVs', 'scatter_size': 15, 'color_1': 'navy', 'color_2': 'teal',
                 'colorsequence': 'Plotly', 'colorscale': 'blues'}
tool_settings = {'selected_metadata': 'River', 'presence_absence': True}
perlodes_TTT_conversion_xlsx = Path('/Users/tillmacher/Documents/GitHub/TaxonTableTools2.0/taxontabletools2/WFD_conversion/perlodes_TTT_conversion.xlsx')