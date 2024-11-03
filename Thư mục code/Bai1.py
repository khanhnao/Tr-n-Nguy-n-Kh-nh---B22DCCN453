from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

def xuly(s):
    if s == "N/A":
        return 0
    elif len(s) > 3 and s[1] == ',':
        return int(s[0]) * 1000 + int(s[2:])
    else:
        return int(s)

driver = webdriver.Chrome()
driver.get('https://fbref.com/en/comps/9/2023-2024/playingtime/2023-2024-Premier-League-Stats')



driver.implicitly_wait(10)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

players = []

table = soup.find('table', {'id': 'stats_playing_time'})
rows = table.find('tbody').find_all('tr')

for row in rows:
    cols = row.find_all('td')
    if len(cols) > 0:
        minutes = cols[7].text.strip() if cols[7].text.strip() else 'N/A'
        if xuly(minutes) > 90:
            name = cols[0].text.strip()
            nation = cols[1].text.strip().split()[1] if cols[1].text.strip() else 'N/A'
            team = cols[3].text.strip() if cols[3].text.strip() else 'N/A'
            pos = cols[2].text.strip() if cols[2].text.strip() else 'N/A'
            age = int(cols[4].text.strip()) if cols[4].text.strip() else 'N/A'
            matches_played = int(cols[6].text.strip()) if cols[6].text.strip() else 'N/A'
            starts = int(cols[11].text.strip()) if cols[11].text.strip() else 'N/A'
            minutes = cols[7].text.strip() if cols[7].text.strip() else 'N/A'

            player_data = {
                'Name': name,
                'Nation': nation,
                'Team': team,
                'Position': pos,
                'Age': age,
                'Matches Played': matches_played,
                'Starts': starts,
                'Minutes': xuly(minutes)
            }

            player_link = cols[0].find('a')['href']
            full_link = 'https://fbref.com' + player_link

            driver.get(full_link)

            driver.implicitly_wait(10)
            player_html = driver.page_source
            player_soup = BeautifulSoup(player_html, 'html.parser')

            table_standard_stat = player_soup.find('table', {'id': 'stats_standard_dom_lg'})
            rows_ss = table_standard_stat.find('tbody').find_all('tr')

            for row_ss in rows_ss:
                season = row_ss.find('th').text.strip()
                comp = row_ss.find('td', {'data-stat': 'comp_level'}).text.strip()
                min = row_ss.find('td', {'data-stat': 'minutes'}).text.strip()
                if season == '2023-2024' and comp == '1. Premier League' and min != '' and xuly(min) > 90:
                    cols_ss = row_ss.find_all('td')
                    non_Pen_goals = int(cols_ss[12].text.strip()) if cols_ss[12].text.strip() else 'N/A'
                    Pen_goals = int(cols_ss[11].text.strip()) - int(cols_ss[12].text.strip()) if cols_ss[11].text.strip() and cols_ss[12].text.strip() else 'N/A'
                    assists = int(cols_ss[10].text.strip()) if cols_ss[10].text.strip() else 'N/A'
                    yellow_cards = int(cols_ss[15].text.strip()) if cols_ss[15].text.strip() else 'N/A'
                    red_cards = int(cols_ss[16].text.strip()) if cols_ss[16].text.strip() else 'N/A'
                    xG = float(cols_ss[17].text.strip()) if cols_ss[17].text.strip() else 'N/A'
                    npxG = float(cols_ss[18].text.strip()) if cols_ss[18].text.strip() else 'N/A'
                    xAG = float(cols_ss[19].text.strip()) if cols_ss[19].text.strip() else 'N/A'
                    PrgC = int(cols_ss[21].text.strip()) if cols_ss[21].text.strip() else 'N/A'
                    PrgP = int(cols_ss[22].text.strip()) if cols_ss[22].text.strip() else 'N/A'
                    PrgR = int(cols_ss[23].text.strip()) if cols_ss[23].text.strip() else 'N/A'
                    GLs_p90m = float(cols_ss[24].text.strip()) if cols_ss[24].text.strip() else 'N/A'
                    Ast_p90m = float(cols_ss[25].text.strip()) if cols_ss[25].text.strip() else 'N/A'
                    G_plus_A_p90m = float(cols_ss[26].text.strip()) if cols_ss[26].text.strip() else 'N/A'
                    G_min_PK_p90m = float(cols_ss[27].text.strip()) if cols_ss[27].text.strip() else 'N/A'
                    G_plus_A_min_PK_p90m = float(cols_ss[28].text.strip()) if cols_ss[28].text.strip() else 'N/A'
                    xG_p90m = float(cols_ss[29].text.strip()) if cols_ss[29].text.strip() else 'N/A'
                    xAG_p90m = float(cols_ss[30].text.strip()) if cols_ss[30].text.strip() else 'N/A'
                    xG_plus_xAG_p90m = float(cols_ss[31].text.strip()) if cols_ss[31].text.strip() else 'N/A'
                    npxG_p90m = float(cols_ss[32].text.strip()) if cols_ss[32].text.strip() else 'N/A'
                    npxG_plus_xAG_p90m = float(cols_ss[33].text.strip()) if cols_ss[33].text.strip() else 'N/A'

                    player_data.update({
                        'Non-Penalty Goals': non_Pen_goals,
                        'Penalty Goals': Pen_goals,
                        'Assists': assists,
                        'Yellow Cards': yellow_cards,
                        'Red Cards': red_cards,
                        'xG': xG,
                        'npxG': npxG,
                        'xAG': xAG,
                        'PrgC': PrgC,
                        'PrgP': PrgP,
                        'PrgR': PrgR,
                        'Gls/90': GLs_p90m,
                        'Ast/90': Ast_p90m,
                        'G+A/90': G_plus_A_p90m,
                        'G-PK/90': G_min_PK_p90m,
                        'G+A-PK/90': G_plus_A_min_PK_p90m,
                        'xG/90': xG_p90m,
                        'xAG/90': xAG_p90m,
                        'xG+xAG/90': xG_plus_xAG_p90m,
                        'NpxG/90': npxG_p90m,
                        'NpxG+xAG/90': npxG_plus_xAG_p90m
                    })

            table_goalkeeping = player_soup.find('table', {'id': 'stats_keeper_dom_lg'})
            if table_goalkeeping:
                rows_gk = table_goalkeeping.find('tbody').find_all('tr')
                for row_gk in rows_gk:
                    season = row_gk.find('th').text.strip()
                    comp = row_gk.find('td', {'data-stat': 'comp_level'}).text.strip()
                    if season == '2023-2024' and comp == '1. Premier League':
                        cols_gk = row_gk.find_all('td')
                        GA = int(cols_gk[9].text.strip()) if cols_gk[9].text.strip() else 'N/A'
                        GA90 = float(cols_gk[10].text.strip()) if cols_gk[10].text.strip() else 'N/A'
                        SoTA = int(cols_gk[11].text.strip()) if cols_gk[11].text.strip() else 'N/A'
                        Saves = int(cols_gk[12].text.strip()) if cols_gk[12].text.strip() else 'N/A'
                        Save_percentage = float(cols_gk[13].text.strip()) if cols_gk[13].text.strip() else 'N/A'
                        W = int(cols_gk[14].text.strip()) if cols_gk[14].text.strip() else 'N/A'
                        D = int(cols_gk[15].text.strip()) if cols_gk[15].text.strip() else 'N/A'
                        L = int(cols_gk[16].text.strip()) if cols_gk[16].text.strip() else 'N/A'
                        CS = int(cols_gk[17].text.strip()) if cols_gk[17].text.strip() else 'N/A'
                        CS_percentage = float(cols_gk[18].text.strip()) if cols_gk[18].text.strip() else 'N/A'
                        PKat = int(cols_gk[19].text.strip()) if cols_gk[19].text.strip() else 'N/A'
                        PKA = int(cols_gk[20].text.strip()) if cols_gk[20].text.strip() else 'N/A'
                        PKsv = int(cols_gk[21].text.strip()) if cols_gk[21].text.strip() else 'N/A'
                        PKm = int(cols_gk[22].text.strip()) if cols_gk[22].text.strip() else 'N/A'
                        PK_save_percentage = float(cols_gk[23].text.strip()) if cols_gk[23].text.strip() else 'N/A'

                        player_data.update({
                            'GA': GA,
                            'GA90': GA90,
                            'SoTA': SoTA,
                            'Saves': Saves,
                            'Save%': Save_percentage,
                            'W': W,
                            'D': D,
                            'L': L,
                            'CS': CS,
                            'CS%': CS_percentage,
                            'PKat': PKat,
                            'PKA': PKA,
                            'PKsv': PKsv,
                            'PKm': PKm,
                            'PK_save%': PK_save_percentage
                        })
            else:
                player_data.update({
                    'GA': 'N/A',
                    'GA90': 'N/A',
                    'SoTA': 'N/A',
                    'Saves': 'N/A',
                    'Save%': 'N/A',
                    'W': 'N/A',
                    'D': 'N/A',
                    'L': 'N/A',
                    'CS': 'N/A',
                    'CS%': 'N/A',
                    'PKat': 'N/A',
                    'PKA': 'N/A',
                    'PKsv': 'N/A',
                    'PKm': 'N/A',
                    'PK_save%': 'N/A'
                })

            table_shooting = player_soup.find('table', {'id': 'stats_shooting_dom_lg'})

            if table_shooting:
                rows_st = table_shooting.find('tbody').find_all('tr')
                for row_st in rows_st:
                    season = row_st.find('th').text.strip()
                    comp = row_st.find('td', {'data-stat': 'comp_level'}).text.strip()
                    if season == '2023-2024' and comp == '1. Premier League':
                        cols_st = row_st.find_all('td')
                        # Gls, Sh, SoT, SoT%, Sh/90, SoT/90, G/Sh, G/SoT, Dist, FK, PK, PKat
                        Gls_st = int(cols_st[6].text.strip()) if cols_st[6].text.strip() else 'N/A'
                        Sh_st = int(cols_st[7].text.strip()) if cols_st[7].text.strip() else 'N/A'
                        SoT_st = int(cols_st[8].text.strip()) if cols_st[8].text.strip() else 'N/A'
                        SoT_percentage_st = float(cols_st[9].text.strip()) if cols_st[9].text.strip() else 'N/A'
                        Sh_p90m_st = float(cols_st[10].text.strip()) if cols_st[10].text.strip() else 'N/A'
                        SoT_p90m_st = float(cols_st[11].text.strip()) if cols_st[11].text.strip() else 'N/A'
                        G_per_Sh_st = float(cols_st[12].text.strip()) if cols_st[12].text.strip() else 'N/A'
                        G_per_SoT_st = float(cols_st[13].text.strip()) if cols_st[13].text.strip() else 'N/A'
                        Dist_st = float(cols_st[14].text.strip()) if cols_st[14].text.strip() else 'N/A'
                        FK_st = int(cols_st[15].text.strip()) if cols_st[15].text.strip() else 'N/A'
                        PK_st = int(cols_st[16].text.strip()) if cols_st[16].text.strip() else 'N/A'
                        PKat_st = int(cols_st[17].text.strip()) if cols_st[17].text.strip() else 'N/A'
                        # xG, npxG, npxG/Sh, G-xG, np:G-xG
                        xG_st = float(cols_st[18].text.strip()) if cols_st[18].text.strip() else 'N/A'
                        npxG_st = float(cols_st[19].text.strip()) if cols_st[19].text.strip() else 'N/A'
                        npxG_per_Sh_st = float(cols_st[20].text.strip()) if cols_st[20].text.strip() else 'N/A'
                        G_min_xG_st = float(cols_st[21].text.strip()) if cols_st[21].text.strip() else 'N/A'
                        np_G_min_xG = float(cols_st[22].text.strip()) if cols_st[22].text.strip() else 'N/A'

                        player_data.update({
                            'Gls_st': Gls_st,
                            'Sh_st': Sh_st,
                            'SoT_st': SoT_st,
                            'SoT%_st': SoT_percentage_st,
                            'Sh/90_st': Sh_p90m_st,
                            'SoT/90_st': SoT_p90m_st,
                            'G/Sh_st': G_per_Sh_st,
                            'G/SoT_st': G_per_SoT_st,
                            'Dist_st': Dist_st,
                            'FK_st': FK_st,
                            'PK_st': PK_st,
                            'PKat_st': PKat_st,
                            'xG_st': xG_st,
                            'npxG_st': npxG_st,
                            'npxG/Sh_st': npxG_per_Sh_st,
                            'G-xG_st': G_min_xG_st,
                            'np:G-xG': np_G_min_xG
                        })
            else:
                player_data.update({
                    'Gls_st': 'N/A',
                    'Sh_st': 'N/A',
                    'SoT_st': 'N/A',
                    'SoT%_st': 'N/A',
                    'Sh/90_st': 'N/A',
                    'SoT/90_st': 'N/A',
                    'G/Sh_st': 'N/A',
                    'G/SoT_st': 'N/A',
                    'Dist_st': 'N/A',
                    'FK_st': 'N/A',
                    'PK_st': 'N/A',
                    'PKat_st': 'N/A',
                    'xG_st': 'N/A',
                    'npxG_st': 'N/A',
                    'npxG/Sh_st': 'N/A',
                    'G-xG_st': 'N/A',
                    'np:G-xG': 'N/A'
                })

            table_passing = player_soup.find('table', {'id': 'stats_passing_dom_lg'})
            rows_ps = table_passing.find('tbody').find_all('tr')
            for row_ps in rows_ps:
                season = row_ps.find('th').text.strip()
                comp = row_ps.find('td', {'data-stat': 'comp_level'}).text.strip()
                if season == '2023-2024' and comp == '1. Premier League':
                    cols_ps = row_ps.find_all('td')
                    total_cmp_ps = int(cols_ps[6].text.strip()) if cols_ps[6].text.strip() else 'N/A'
                    total_att_ps = int(cols_ps[7].text.strip()) if cols_ps[7].text.strip() else 'N/A'
                    total_cmp_percentage_ps = float(cols_ps[8].text.strip()) if cols_ps[8].text.strip() else 'N/A'
                    total_totDist_ps = int(cols_ps[9].text.strip()) if cols_ps[9].text.strip() else 'N/A'
                    total_prgDist_ps = int(cols_ps[10].text.strip()) if cols_ps[10].text.strip() else 'N/A'
                    short_cmp_ps = int(cols_ps[11].text.strip()) if cols_ps[11].text.strip() else 'N/A'
                    short_att_ps = int(cols_ps[12].text.strip()) if cols_ps[12].text.strip() else 'N/A'
                    short_cmp_percentage_ps = float(cols_ps[13].text.strip()) if cols_ps[13].text.strip() else 'N/A'
                    med_cmp_ps = int(cols_ps[14].text.strip()) if cols_ps[14].text.strip() else 'N/A'
                    med_att_ps = int(cols_ps[15].text.strip()) if cols_ps[15].text.strip() else 'N/A'
                    med_cmp_percentage_ps = float(cols_ps[16].text.strip()) if cols_ps[16].text.strip() else 'N/A'
                    long_cmp_ps = int(cols_ps[17].text.strip()) if cols_ps[17].text.strip() else 'N/A'
                    long_att_ps = int(cols_ps[18].text.strip()) if cols_ps[18].text.strip() else 'N/A'
                    long_cmp_percentage_ps = float(cols_ps[19].text.strip()) if cols_ps[19].text.strip() else 'N/A'
                    ex_ast_ps = int(cols_ps[20].text.strip()) if cols_ps[20].text.strip() else 'N/A'
                    ex_xAG_ps = float(cols_ps[21].text.strip()) if cols_ps[21].text.strip() else 'N/A'
                    ex_xA_ps = float(cols_ps[22].text.strip()) if cols_ps[22].text.strip() else 'N/A'
                    ex_A_min_xAG = float(cols_ps[23].text.strip()[1:]) if cols_ps[23].text.strip() else 'N/A'
                    ex_KP_ps = int(cols_ps[24].text.strip()) if cols_ps[24].text.strip() else 'N/A'
                    ex_final_third_ps = int(cols_ps[25].text.strip()) if cols_ps[25].text.strip() else 'N/A'
                    ex_PPA_ps = int(cols_ps[26].text.strip()) if cols_ps[26].text.strip() else 'N/A'
                    ex_CrsPA_ps = int(cols_ps[27].text.strip()) if cols_ps[27].text.strip() else 'N/A'
                    ex_PrgP_ps = int(cols_ps[28].text.strip()) if cols_ps[28].text.strip() else 'N/A'

                    player_data.update({
                        'Total_cmp_ps': total_cmp_ps,
                        'Total_att_ps': total_att_ps,
                        'Total_cmp%_ps': total_cmp_percentage_ps,
                        'Total_TotDist_ps': total_totDist_ps,
                        'Total_PrgDist_ps': total_prgDist_ps,
                        'Short_cmp_ps': short_cmp_ps,
                        'Short_att_ps': short_att_ps,
                        'Short_cmp%_ps': short_cmp_percentage_ps,
                        'Medium_cmp_ps': med_cmp_ps,
                        'Medium_att_ps': med_att_ps,
                        'Medium_cmp%_ps': med_cmp_percentage_ps,
                        'Long_cmp_ps': long_cmp_ps,
                        'Long_att_ps': long_att_ps,
                        'Long_cmp%_ps': long_cmp_percentage_ps,
                        'Expected_ast_ps': ex_ast_ps,
                        'Expected_xAG_ps': ex_xAG_ps,
                        'Expected_xA_ps': ex_xA_ps,
                        'Expected_A-xAG_ps': ex_A_min_xAG,
                        'Expected_KP_ps': ex_KP_ps,
                        'Expected_1/3_ps': ex_final_third_ps,
                        'Expected_PPA_ps': ex_PPA_ps,
                        'Expected_CrsPA_ps': ex_CrsPA_ps,
                        'Expected_PrgP': ex_PrgP_ps
                    })

            table_pass_types = player_soup.find('table', {'id': 'stats_passing_types_dom_lg'})
            rows_pt = table_pass_types.find('tbody').find_all('tr')
            for row_pt in rows_pt:
                season = row_pt.find('th').text.strip()
                comp = row_pt.find('td', {'data-stat': 'comp_level'}).text.strip()
                if season == '2023-2024' and comp == '1. Premier League':
                    cols_pt = row_pt.find_all('td')
                    live_pt = int(cols_pt[7].text.strip()) if cols_pt[7].text.strip() else 'N/A'
                    dead_pt = int(cols_pt[8].text.strip()) if cols_pt[8].text.strip() else 'N/A'
                    fk_pt = int(cols_pt[9].text.strip()) if cols_pt[9].text.strip() else 'N/A'
                    tb_pt = int(cols_pt[10].text.strip()) if cols_pt[10].text.strip() else 'N/A'
                    sw_pt = int(cols_pt[11].text.strip()) if cols_pt[11].text.strip() else 'N/A'
                    crs_pt = int(cols_pt[12].text.strip()) if cols_pt[12].text.strip() else 'N/A'
                    ti_pt = int(cols_pt[13].text.strip()) if cols_pt[13].text.strip() else 'N/A'
                    ck_pt = int(cols_pt[14].text.strip()) if cols_pt[14].text.strip() else 'N/A'
                    in_pt = int(cols_pt[15].text.strip()) if cols_pt[15].text.strip() else 'N/A'
                    out_pt = int(cols_pt[16].text.strip()) if cols_pt[16].text.strip() else 'N/A'
                    str_pt = int(cols_pt[17].text.strip()) if cols_pt[17].text.strip() else 'N/A'
                    cmp_pt = int(cols_pt[18].text.strip()) if cols_pt[18].text.strip() else 'N/A'
                    off_pt = int(cols_pt[19].text.strip()) if cols_pt[19].text.strip() else 'N/A'
                    blocks_pt = int(cols_pt[20].text.strip()) if cols_pt[20].text.strip() else 'N/A'

                    player_data.update({
                        'Live_pt': live_pt,
                        'Dead_pt': dead_pt,
                        'FK_pt': fk_pt,
                        'TB_pt': tb_pt,
                        'Sw_pt': sw_pt,
                        'Crs_pt': crs_pt,
                        'TI_pt': ti_pt,
                        'CK_pt': ck_pt,
                        'In_pt': in_pt,
                        'Out_pt': out_pt,
                        'Str_pt': str_pt,
                        'Cmp_pt': cmp_pt,
                        'Off_pt': off_pt,
                        'Blocks_pt': blocks_pt
                    })

            table_goal_and_shot_creation = player_soup.find('table', {'id': 'stats_gca_dom_lg'})
            rows_gsc = table_goal_and_shot_creation.find('tbody').find_all('tr')
            for row_gsc in rows_gsc:
                season = row_gsc.find('th').text.strip()
                comp = row_gsc.find('td', {'data-stat': 'comp_level'}).text.strip()
                if season == '2023-2024' and comp == '1. Premier League':
                    cols_gsc = row_gsc.find_all('td')
                    sca_gsc = int(cols_gsc[6].text.strip()) if cols_gsc[6].text.strip() else 'N/A'
                    sca90_gsc = float(cols_gsc[7].text.strip()) if cols_gsc[7].text.strip() else 'N/A'
                    passlive_sca = int(cols_gsc[8].text.strip()) if cols_gsc[8].text.strip() else 'N/A'
                    passdead_sca = int(cols_gsc[9].text.strip()) if cols_gsc[9].text.strip() else 'N/A'
                    to_sca = int(cols_gsc[10].text.strip()) if cols_gsc[10].text.strip() else 'N/A'
                    sh_sca = int(cols_gsc[11].text.strip()) if cols_gsc[11].text.strip() else 'N/A'
                    fld_sca = int(cols_gsc[12].text.strip()) if cols_gsc[12].text.strip() else 'N/A'
                    def_sca = int(cols_gsc[13].text.strip()) if cols_gsc[13].text.strip() else 'N/A'
                    gca_gsc = int(cols_gsc[14].text.strip()) if cols_gsc[14].text.strip() else 'N/A'
                    gca90_gsc = float(cols_gsc[15].text.strip()) if cols_gsc[15].text.strip() else 'N/A'
                    passlive_gca = int(cols_gsc[16].text.strip()) if cols_gsc[16].text.strip() else 'N/A'
                    passdead_gca = int(cols_gsc[17].text.strip()) if cols_gsc[17].text.strip() else 'N/A'
                    to_gca = int(cols_gsc[18].text.strip()) if cols_gsc[18].text.strip() else 'N/A'
                    sh_gca = int(cols_gsc[19].text.strip()) if cols_gsc[19].text.strip() else 'N/A'
                    fld_gca = int(cols_gsc[20].text.strip()) if cols_gsc[20].text.strip() else 'N/A'
                    def_gca = int(cols_gsc[21].text.strip()) if cols_gsc[21].text.strip() else 'N/A'

                    player_data.update({
                        'SCA': sca_gsc,
                        'SCA90': sca90_gsc,
                        'PassLive_SCA': passlive_sca,
                        'PassDead_SCA': passdead_sca,
                        'TO_SCA': to_sca,
                        'Sh_SCA': sh_sca,
                        'Fld_SCA': fld_sca,
                        'Def_SCA': def_sca,
                        'GCA': gca_gsc,
                        'GCA90': gca90_gsc,
                        'PassLive_GCA': passlive_gca,
                        'PassDead_GCA': passdead_gca,
                        'TO_GCA': to_gca,
                        'Sh_GCA': sh_gca,
                        'Fld_GCA': fld_gca,
                        'Def_GCA': def_gca
                    })

            table_defensive_action = player_soup.find('table', {'id': 'stats_defense_dom_lg'})
            rows_da = table_defensive_action.find('tbody').find_all('tr')
            for row_da in rows_da:
                season = row_da.find('th').text.strip()
                comp = row_da.find('td', {'data-stat': 'comp_level'}).text.strip()
                if season == '2023-2024' and comp == '1. Premier League':
                    cols_da = row_da.find_all('td')
                    tkl_da = int(cols_da[6].text.strip()) if cols_da[6].text.strip() else 'N/A'
                    tklw_da = int(cols_da[7].text.strip()) if cols_da[7].text.strip() else 'N/A'
                    def_3rd_da = int(cols_da[8].text.strip()) if cols_da[8].text.strip() else 'N/A'
                    mid_3rd_da = int(cols_da[9].text.strip()) if cols_da[9].text.strip() else 'N/A'
                    att_3rd_da = int(cols_da[10].text.strip()) if cols_da[10].text.strip() else 'N/A'
                    tkl_challenges_da = int(cols_da[11].text.strip()) if cols_da[11].text.strip() else 'N/A'
                    att_da = int(cols_da[12].text.strip()) if cols_da[12].text.strip() else 'N/A'
                    tkl_percentage_da = float(cols_da[13].text.strip()) if cols_da[13].text.strip() else 'N/A'
                    lost_da = int(cols_da[14].text.strip()) if cols_da[14].text.strip() else 'N/A'
                    blocks_da = int(cols_da[15].text.strip()) if cols_da[15].text.strip() else 'N/A'
                    sh_da = int(cols_da[16].text.strip()) if cols_da[16].text.strip() else 'N/A'
                    pass_da = int(cols_da[17].text.strip()) if cols_da[17].text.strip() else 'N/A'
                    int_da = int(cols_da[18].text.strip()) if cols_da[18].text.strip() else 'N/A'
                    tkl_plus_int = int(cols_da[19].text.strip()) if cols_da[19].text.strip() else 'N/A'
                    clr_da = int(cols_da[20].text.strip()) if cols_da[20].text.strip() else 'N/A'
                    err_da = int(cols_da[21].text.strip()) if cols_da[21].text.strip() else 'N/A'

                    player_data.update({
                        'Tkl_tackles': tkl_da,
                        'TklW_da': tklw_da,
                        'Def 3rd': def_3rd_da,
                        'Mid 3rd': mid_3rd_da,
                        'Att 3rd': att_3rd_da,
                        'Tkl_Challenges': tkl_challenges_da,
                        'Att_da': att_da,
                        'Tkl%_da': tkl_percentage_da,
                        'Lost_da': lost_da,
                        'Blocks_da': blocks_da,
                        'Sh_da': sh_da,
                        'Pass_da': pass_da,
                        'Int_da': int_da,
                        'Tkl+Int': tkl_plus_int,
                        'Clr_da': clr_da,
                        'Err_da': err_da
                    })

            table_possession = player_soup.find('table', {'id': 'stats_possession_dom_lg'})
            rows_p = table_possession.find('tbody').find_all('tr')
            for row_p in rows_p:
                season = row_p.find('th').text.strip()
                comp = row_p.find('td', {'data-stat': 'comp_level'}).text.strip()
                if season == '2023-2024' and comp == '1. Premier League':
                    cols_p = row_p.find_all('td')
                    touches = int(cols_p[6].text.strip()) if cols_p[6].text.strip() else 'N/A'
                    def_pen_p = int(cols_p[7].text.strip()) if cols_p[7].text.strip() else 'N/A'
                    def_3rd_p = int(cols_p[8].text.strip()) if cols_p[8].text.strip() else 'N/A'
                    mid_3rd_p = int(cols_p[9].text.strip()) if cols_p[9].text.strip() else 'N/A'
                    att_3rd_p = int(cols_p[10].text.strip()) if cols_p[10].text.strip() else 'N/A'
                    att_pen_p = int(cols_p[11].text.strip()) if cols_p[11].text.strip() else 'N/A'
                    live_p = int(cols_p[12].text.strip()) if cols_p[12].text.strip() else 'N/A'
                    att_p = int(cols_p[13].text.strip()) if cols_p[13].text.strip() else 'N/A'
                    succ_p = int(cols_p[14].text.strip()) if cols_p[14].text.strip() else 'N/A'
                    succ_percentage_p = float(cols_p[15].text.strip()) if cols_p[15].text.strip() else 'N/A'
                    tkld_p = int(cols_p[16].text.strip()) if cols_p[16].text.strip() else 'N/A'
                    tkld_percentage_p = float(cols_p[17].text.strip()) if cols_p[17].text.strip() else 'N/A'
                    carries = int(cols_p[18].text.strip()) if cols_p[18].text.strip() else 'N/A'
                    totDist_p = int(cols_p[19].text.strip()) if cols_p[19].text.strip() else 'N/A'
                    proDist_p = int(cols_p[20].text.strip()) if cols_p[20].text.strip() else 'N/A'
                    progC_p = int(cols_p[21].text.strip()) if cols_p[21].text.strip() else 'N/A'
                    one_third_p = int(cols_p[22].text.strip()) if cols_p[22].text.strip() else 'N/A'
                    cpa_p = int(cols_p[23].text.strip()) if cols_p[23].text.strip() else 'N/A'
                    mis_p = int(cols_p[24].text.strip()) if cols_p[24].text.strip() else 'N/A'
                    dis_p = int(cols_p[25].text.strip()) if cols_p[25].text.strip() else 'N/A'
                    rec_p = int(cols_p[26].text.strip()) if cols_p[26].text.strip() else 'N/A'
                    prgR_p = int(cols_p[27].text.strip()) if cols_p[27].text.strip() else 'N/A'

                    player_data.update({
                        'touches': touches,
                        'Def Pen': def_pen_p,
                        'def_3rd_p': def_3rd_p,
                        'mid_3rd_p': mid_3rd_p,
                        'att_3rd_p': att_3rd_p,
                        'att_pen_p': att_pen_p,
                        'live_p': live_p,
                        'att_p': att_p,
                        'succ_p': succ_p,
                        'succ%_p': succ_percentage_p,
                        'tkld_p': tkld_p,
                        'tkld%_p': tkld_percentage_p,
                        'carries': carries,
                        'totDist_p': totDist_p,
                        'proDist_p': proDist_p,
                        'progC_p': progC_p,
                        '1/3_p': one_third_p,
                        'cpa_p': cpa_p,
                        'mis_p': mis_p,
                        'dis_p': dis_p,
                        'rec_p': rec_p,
                        'prgR_p': prgR_p
                    })

            table_playing_time = player_soup.find('table', {'id': 'stats_playing_time_dom_lg'})
            rows_plt = table_playing_time.find('tbody').find_all('tr')
            for row_plt in rows_plt:
                season = row_plt.find('th').text.strip()
                comp = row_plt.find('td', {'data-stat': 'comp_level'}).text.strip()
                min = row_plt.find('td', {'data-stat': 'minutes'}).text.strip()
                if season == '2023-2024' and comp == '1. Premier League' and min and xuly(min) > 90:
                    cols_plt = row_plt.find_all('td')
                    starts_plt = int(cols_plt[10].text.strip()) if cols_plt[10].text.strip() else 'N/A'
                    mn_dv_start_plt = int(cols_plt[11].text.strip()) if cols_plt[11].text.strip() else 'N/A'
                    compl_plt = int(cols_plt[12].text.strip()) if cols_plt[12].text.strip() else 'N/A'
                    subs_plt = int(cols_plt[13].text.strip()) if cols_plt[13].text.strip() else 'N/A'
                    mn_dv_sub_plt = int(cols_plt[14].text.strip()) if cols_plt[14].text.strip() else 'N/A'
                    unSub_plt = int(cols_plt[15].text.strip()) if cols_plt[15].text.strip() else 'N/A'
                    PPM_plt = float(cols_plt[16].text.strip()) if cols_plt[16].text.strip() else 'N/A'
                    onG_plt = int(cols_plt[17].text.strip()) if cols_plt[17].text.strip() else 'N/A'
                    onGA_plt = int(cols_plt[18].text.strip()) if cols_plt[18].text.strip() else 'N/A'
                    onxG_plt = float(cols_plt[22].text.strip()) if cols_plt[22].text.strip() else 'N/A'
                    onxGA_plt = float(cols_plt[23].text.strip()) if cols_plt[23].text.strip() else 'N/A'

                    player_data.update({
                        'starts_plt': starts_plt,
                        'mn/start_plt': mn_dv_start_plt,
                        'compl_plt': compl_plt,
                        'subs_plt': subs_plt,
                        'mn/sub_plt': mn_dv_sub_plt,
                        'unSub_plt': unSub_plt,
                        'PPM_plt': PPM_plt,
                        'onG_plt': onG_plt,
                        'onGA_plt': onGA_plt,
                        'onxG_plt': onxG_plt,
                        'onxGA_plt': onxGA_plt
                    })

            table_miscellaneous_stats = player_soup.find('table', {'id': 'stats_misc_dom_lg'})
            rows_ms = table_miscellaneous_stats.find('tbody').find_all('tr')
            for row_ms in rows_ms:
                season = row_ms.find('th').text.strip()
                comp = row_ms.find('td', {'data-stat': 'comp_level'}).text.strip()
                if season == '2023-2024' and comp == '1. Premier League':
                    cols_ms = row_ms.find_all('td')
                    fls = int(cols_ms[9].text.strip()) if cols_ms[9].text.strip() else 'N/A'
                    fld_ms = int(cols_ms[10].text.strip()) if cols_ms[10].text.strip() else 'N/A'
                    off_ms = int(cols_ms[11].text.strip()) if cols_ms[11].text.strip() else 'N/A'
                    Crs_ms = int(cols_ms[12].text.strip()) if cols_ms[12].text.strip() else 'N/A'
                    OG = int(cols_ms[17].text.strip()) if cols_ms[17].text.strip() else 'N/A'
                    recov = int(cols_ms[18].text.strip()) if cols_ms[18].text.strip() else 'N/A'
                    Won = int(cols_ms[19].text.strip()) if cols_ms[19].text.strip() else 'N/A'
                    Lost = int(cols_ms[20].text.strip()) if cols_ms[20].text.strip() else 'N/A'
                    Won_percentage = float(cols_ms[21].text.strip()) if cols_ms[21].text.strip() else 'N/A'

                    player_data.update({
                        'fls': fls,
                        'fld_ms': fld_ms,
                        'off_ms': off_ms,
                        'Crs_ms': Crs_ms,
                        'OG': OG,
                        'recov': recov,
                        'Won': Won,
                        'Lost': Lost,
                        'Won%': Won_percentage
                    })
            # Thêm cầu thủ vào danh sách player
            players.append(player_data)
            print(player_data)


            time.sleep(5)

#print(players)
df = pd.DataFrame(players)
df.to_csv('result.csv', index=False)

driver.quit()
