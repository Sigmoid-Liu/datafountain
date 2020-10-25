

import pandas as pd

def base_data_process(base_info):
    drop_columns = ['dom','parnum','exenum','ptbusscope','midpreindcode','protype','forreccap','forregcap','congro','oploc','opform','opto']
    category_columns = ['oplocdistrict','industryphy','enttype','state','regtype','compform','opform','venind','enttypegb']
    mutile_type_columns = ['industryco','opscope','enttypeitem','orgid','jobid','enttypeminu']

    base_info['oplocdistrict'] = base_info['oplocdistrict'].astype(str)
    base_info['industryco'] = base_info['industryco'].astype(str)
    base_info['enttype'] = base_info['enttype'].astype(str)
    base_info['enttypeitem'] = base_info['enttypeitem'].astype(str).fillna('nan')
    base_info['opfrom'] = base_info['enttypeitem'].str[:10]
    base_info['state'] = base_info['state'].astype(str)
    base_info['adbusign'] = base_info['adbusign'].astype(str)
    base_info['townsign'] = base_info['townsign'].astype(str)
    base_info['regtype'] = base_info['regtype'].astype(str)
    base_info['compform'] = base_info['compform'].astype(str).fillna('nan')
    base_info['venind'] = base_info['venind'].astype(str).fillna('nan')
    base_info['enttypeminu'] = base_info['enttypeminu'].astype(str).fillna('nan')
    base_info['reccap'] = base_info['reccap'].apply(lambda x: False if pd.isna(x) else True)
    base_info['enttypegb'] = base_info['enttypegb'].astype(str)

    for col in base_info.columns:
        if col in category_columns:
            base_info[col] = base_info[col].astype('category')
    return base_info

def data_process(data_path):
    data = {}

    base_info = pd.read_csv(data_path+'base_info.csv')
    base_info = base_data_process(base_info)


    annual_report_info = pd.read_csv(data_path+'annual_report_info.csv')

    tax_info = pd.read_csv(data_path+'tax_info.csv')
    tax_info['END_YEAR'] = tax_info['END_DATE'].str[:4]
    tax_info['END_MONTH'] = tax_info['END_DATE'].str[5:7]

    change_info = pd.read_csv(data_path+'change_info.csv')
    change_info['bgrq'] = change_info['bgrq'].astype(str).str[:14]
    change_info['bgxmdm'] = change_info['bgxmdm'].astype(str).str[:-2]
    change_info['date'] = change_info['bgrq'].str[:8]
    change_info['year'] = change_info['bgrq'].str[:4]
    change_info['month'] = change_info['bgrq'].str[4:6]
    change_info['day'] = change_info['bgrq'].str[6:8]
    change_info['hour'] = change_info['bgrq'].str[8:10]

    news_info = pd.read_csv(data_path+'news_info.csv')
    news_info['year'] = news_info['public_date'].str[:4]
    news_info['month'] = news_info['public_date'].str[5:7]
    news_info['day'] = news_info['public_date'].str[8:10]
    news_info['year_status'] = news_info['year']+'_'+news_info['positive_negtive']
    news_info['month_status'] = news_info['month']+'_'+news_info['positive_negtive']
    news_info['day_status'] = news_info['day']+'_'+news_info['positive_negtive']

    other_info = pd.read_csv('./train/other_info.csv')

    data['base'] = base_info
    data['annual_report'] = annual_report_info
    data['tax'] = tax_info
    data['change'] = change_info
    data['news'] = news_info
    data['other'] = other_info
    
    return data