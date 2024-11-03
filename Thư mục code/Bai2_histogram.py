import pandas as pd
import matplotlib.pyplot as plt

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

# Vẽ histogram cho toàn giải
for col in stats_columns:
    plt.figure(figsize=(8, 6))
    plt.hist(df[col].dropna(), bins=10, edgecolor='black', alpha=0.7)
    plt.title(f'Distribution of {col} for all players')
    plt.xlabel(col)
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

# Vẽ histogram cho từng đội
teams = df['Team'].unique()
for team in teams:
    team_df = df[df['Team'] == team]
    for col in stats_columns:
        plt.figure(figsize=(8, 6))
        plt.hist(team_df[col].dropna(), bins=10, edgecolor='black', alpha=0.7)
        plt.title(f'Distribution of {col} for {team}')
        plt.xlabel(col)
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.show()

# Tìm đội bóng có chỉ số cao nhất ở mỗi chỉ số
top_teams = {}
for col in stats_columns:
    team_mean = df.groupby('Team')[col].mean()
    top_team = team_mean.idxmax()  # Đội có trung bình cao nhất ở chỉ số đó
    top_value = team_mean.max()    # Giá trị cao nhất của chỉ số đó
    top_teams[col] = (top_team, top_value)

# Đội có nhiều chỉ số cao nhất là đội có phong độ tốt nhất
team_counts = pd.Series([team for team, value in top_teams.values()]).value_counts()
best_team = team_counts.idxmax()

print(f"\nTeam with best performance: {best_team}")
