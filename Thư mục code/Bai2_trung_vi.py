import pandas as pd

df = pd.read_csv('result.csv')

stats_columns = ['Matches Played', 'Starts', 'Minutes', 'Non-Penalty Goals', 'Penalty Goals',
                 'Assists', 'Yellow Cards', 'Red Cards', 'xG', 'npxG', 'xAG', 'PrgC', 'PrgP', 'PrgR',
                 'Gls/90', 'Ast/90', 'G+A/90', 'G-PK/90', 'G+A-PK/90', 'xG/90', 'xAG/90', 'xG+xAG/90',
                 'NpxG/90', 'NpxG+xAG/90', 'GA', 'GA90', 'SoTA', 'Saves', 'Save%', 'W', 'D', 'L', 'CS',
                 'CS%', 'PKat', 'PKA', 'PKsv', 'PKm', 'PK_save%', 'Gls_st', 'Sh_st', 'SoT_st', 'SoT%_st',
                 'Sh/90_st', 'SoT/90_st', 'G/Sh_st', 'G/SoT_st', 'Dist_st', 'FK_st', 'PK_st', 'PKat_st',
                 'xG_st', 'npxG_st', 'npxG/Sh_st', 'G-xG_st', 'np:G-xG', 'Total_cmp_ps', 'Total_att_ps',
                 'Total_cmp%_ps', 'Total_TotDist_ps', 'Total_PrgDist_ps', 'Short_cmp_ps', 'Short_att_ps',
                 'Short_cmp%_ps', 'Medium_cmp_ps', 'Medium_att_ps', 'Medium_cmp%_ps', 'Long_cmp_ps', 'Long_att_ps',
                 'Long_cmp%_ps', 'Expected_ast_ps', 'Expected_xAG_ps', 'Expected_xA_ps', 'Expected_A-xAG_ps',
                 'Expected_KP_ps', 'Expected_1/3_ps', 'Expected_PPA_ps', 'Expected_CrsPA_ps', 'Expected_PrgP',
                 'Live_pt', 'Dead_pt', 'FK_pt', 'TB_pt', 'Sw_pt', 'Crs_pt', 'TI_pt', 'CK_pt', 'In_pt', 'Out_pt',
                 'Str_pt', 'Cmp_pt', 'Off_pt', 'Blocks_pt', 'SCA', 'SCA90', 'PassLive_SCA', 'PassDead_SCA', 'TO_SCA',
                 'Sh_SCA', 'Fld_SCA', 'Def_SCA', 'GCA', 'GCA90', 'PassLive_GCA', 'PassDead_GCA', 'TO_GCA', 'Sh_GCA',
                 'Fld_GCA', 'Def_GCA', 'Tkl_tackles', 'TklW_da', 'Def 3rd', 'Mid 3rd', 'Att 3rd', 'Tkl_Challenges',
                 'Att_da', 'Tkl%_da', 'Lost_da', 'Blocks_da', 'Sh_da', 'Pass_da', 'Int_da', 'Tkl+Int', 'Clr_da', 'Err_da',
                 'touches', 'Def Pen', 'def_3rd_p', 'mid_3rd_p', 'att_3rd_p', 'att_pen_p', 'live_p', 'att_p', 'succ_p',
                 'succ%_p', 'tkld_p', 'tkld%_p', 'carries', 'totDist_p', 'proDist_p', 'progC_p', '1/3_p', 'cpa_p', 'mis_p',
                 'dis_p', 'rec_p', 'prgR_p', 'starts_plt', 'mn/start_plt', 'compl_plt', 'subs_plt', 'mn/sub_plt', 'unSub_plt',
                 'PPM_plt', 'onG_plt', 'onGA_plt', 'onxG_plt', 'onxGA_plt', 'fls', 'fld_ms', 'off_ms', 'Crs_ms', 'OG', 'recov',
                 'Won', 'Lost', 'Won%']

results = pd.DataFrame(columns=['Team'] +
                               [f'Median of {col}' for col in stats_columns] +
                               [f'Mean of {col}' for col in stats_columns] +
                               [f'Std of {col}' for col in stats_columns])

# Tính toán cho toàn giải
all_stats = ['all']
for col in stats_columns:
    all_stats.append(df[col].median())
    all_stats.append(round(df[col].mean(), 2))
    all_stats.append(round(df[col].std(), 2))

results.loc[0] = all_stats

# Tính toán cho từng đội
teams = df['Team'].unique()
for idx, team in enumerate(teams, start=1):
    team_df = df[df['Team'] == team]
    team_stats = [team]

    for col in stats_columns:
        team_stats.append(team_df[col].median())
        team_stats.append(round(team_df[col].mean(), 2))
        team_stats.append(round(team_df[col].std(), 2))

    results.loc[idx] = team_stats

results.to_csv('results2.csv', index=False)
