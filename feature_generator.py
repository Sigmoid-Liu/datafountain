

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()
from sklearn import preprocessing
le = preprocessing.LabelEncoder()
enc = preprocessing.OneHotEncoder()


def get_category_feature(data,id_,col):
    '''
    针对序列的类别变量，进行特征衍生
    参数：
        data：数据
        id_：主键
        col：类别变量名
    '''
    data[col] = data[col].fillna('nan').astype(str)
    temp = list(set(data[col]))#类别种类
    temp = dict(zip(temp,[col +'_'+ v + 'CNT' for v in temp]))
    data[col] = data[col].replace(temp)
    temp = data.groupby([id_])[col].agg(lambda x:' '.join(x)).reset_index()
    id_list = temp[id_].tolist()
    corpus = temp[col].tolist()
    feature = pd.DataFrame(vectorizer.fit_transform(corpus).toarray())
    feature.columns = vectorizer.get_feature_names()
    feature[id_] = id_list
    return feature

def get_continue_feature(data,id_,col):
    '''
    针对序列的数值型变量，进行特征衍生
    参数：
        data：数据
        id_：主键
        col：数值型变量名
    '''
    feature = data.groupby([id_])[col].agg({col+'_SUM':'sum',
                                        col+'_MEAN':'mean',
                                        col+'_MAX':'max',
                                        col+'_MIN':'min',
                                        col+'_VAR':'var'
                                        }).reset_index()
    return feature


def category_transform(data,category_col):
    '''
    针对类别较多的变量，按出现的次数对其进行编码
    '''
    category_dict = dict(data[category_col].value_counts().rank(method='dense'))
    return data[category_col].replace(category_dict)

def get_base_feature(base_info):

    base_feature = base_info
    base_feature['opfrom_now'] = 2020 - base_feature['opfrom'].str[:4].astype(int)
    
    oplocdistrict_cnt = base_info.groupby(['oplocdistrict'])['id'].count().reset_index().rename({'id':'oplocdistrict_cnt'},axis=1)
    industryphy_cnt = base_info.groupby(['industryphy'])['id'].count().reset_index().rename({'id':'industryphy_cnt'},axis=1)
    enttype_cnt = base_info.groupby(['enttype'])['id'].count().reset_index().rename({'id':'enttype_cnt'},axis=1)
    enttypeitem_cnt = base_info.groupby(['enttypeitem'])['id'].count().reset_index().rename({'id':'enttypeitem_cnt'},axis=1)
    enttypegb_cnt = base_info.groupby(['enttypegb'])['id'].count().reset_index().rename({'id':'enttypegb_cnt'},axis=1)
    base_feature = base_feature.merge(oplocdistrict_cnt,on=['oplocdistrict'],how='left')
    base_feature = base_feature.merge(industryphy_cnt,on=['industryphy'],how='left')
    base_feature = base_feature.merge(industryco_cnt,on=['industryco'],how='left')
    base_feature = base_feature.merge(enttype_cnt,on=['enttype'],how='left')
    base_feature = base_feature.merge(enttypeitem_cnt,on=['enttypeitem'],how='left')
    base_feature = base_feature.merge(opform_cnt,on=['opform'],how='left')
    base_feature = base_feature.merge(enttypeminu_cnt,on=['enttypeminu'],how='left')
    base_feature = base_feature.merge(enttypegb_cnt,on=['enttypegb'],how='left')
    
    
    return base_feature
    
    

def get_annual_report_feature(annual_report_info):

    annual_report_info['rank'] = annual_report_info.groupby(['id'])['ANCHEYEAR'].rank(ascending=False)
    cols = annual_report_info.columns.difference(['rank'])
    #最近年报的信息
    annual_report_feature = annual_report_info[annual_report_info['rank']==1][cols]
    annual_report_feature.columns = [col + '_LAST' if col!='id' else col for col in cols]
    #年报数量
    temp = annual_report_info.groupby(['id'])['rank'].agg({'annual_report_count':'max'}).reset_index().rename({'rank':'REPORT_CNT'},axis=1)
    annual_report_feature = annual_report_feature.merge(temp,on=['id'],how='left')
    cols = ['FUNDAM','EMPNUM','COLGRANUM','RETSOLNUM','DISPERNUM',
        'UNENUM','COLEMPLNUM','RETEMPLNUM','DISEMPLNUM','UNEEMPLNUM']
    #连续变量序列特征
    for col in ['FUNDAM','EMPNUM','COLGRANUM','RETSOLNUM','DISPERNUM','UNENUM','COLEMPLNUM','RETEMPLNUM','DISEMPLNUM','UNEEMPLNUM']:
        temp = get_continue_feature(annual_report_info,'id',col)
        annual_report_feature = annual_report_feature.merge(temp,on=['id'],how='left')
    #类编变量序列特征
    for col in ['STATE','EMPNUMSIGN','BUSSTNAME','WEBSITSIGN','FORINVESTSIGN','STOCKTRANSIGN','PUBSTATE']:
        temp = get_category_feature(annual_report_info,'id',col)
        annual_report_feature = annual_report_feature.merge(temp,on=['id'],how='left')
    
    return annual_report_feature

def get_tax_feature(tax_info):
    #纳税数量（次数、天数、年数、月数）
    tax_feature = tax_info.groupby(['id'])['TAX_AMOUNT'].agg({'TAX_AMOUNT_CNT':'count'}).reset_index()
    for col in ['END_DATE','END_YEAR','END_MONTH']:
        temp = tax_info[['id',col]].drop_duplicates().groupby(['id'])[col].agg({'TAX_'+col[4:]+'_CNT':'count'}).reset_index()
        tax_feature = tax_feature.merge(temp,on=['id'],how='left')
    #连续变量序列特征
    for col in ['TAXATION_BASIS','TAX_RATE','DEDUCTION','TAX_AMOUNT']:
        temp = get_continue_feature(tax_info,'id',col)
        tax_feature = tax_feature.merge(temp,on=['id'],how='left')
    #类编变量序列特征
    for col in ['TAX_CATEGORIES']:
        temp = get_category_feature(tax_info,'id',col)
        tax_feature = tax_feature.merge(temp,on=['id'],how='left')
        temp = get_category_feature(tax_info[['id',col]].drop_duplicates(),'id',col)
        temp.columns = [c+'_DISTINCT' if c != 'id' else 'id' for c in temp.columns]
        tax_feature = tax_feature.merge(temp,on=['id'],how='left')

    return tax_feature

def get_change_feature(change_info):

    #变更次数
    change_feature = change_info.groupby(['id'])[['bgxmdm']].count().reset_index().rename({'bgxmdm':'BGXMDM_CNT'},axis=1)
    
    for col in ['bgxmdm','year','month','day','hour']:
        temp = get_category_feature(change_info,'id',col)
        change_feature = change_feature.merge(temp,on=['id'],how='left')
    
    return change_feature

def get_news_feature(news_info):
    #新闻数量
    news_feature = news_info.groupby(['id'])[['positive_negtive']].count().reset_index().rename({'positive_negtive':'POSITIVE_NEGTIVE_CNT'},axis=1)
    #类编变量序列特征
    for col in ['positive_negtive','year','month','day','year_status','month_status','day_status']:
        temp = get_category_feature(news_info,'id',col)
        news_feature = news_feature.merge(temp,on=['id'],how='left')

    news_feature['positive_negtive_中立_ratio'] = news_feature['positive_negtive_中立cnt']/news_feature['POSITIVE_NEGTIVE_CNT']
    news_feature['positive_negtive_消极_ratio'] = news_feature['positive_negtive_消极cnt']/news_feature['POSITIVE_NEGTIVE_CNT']
    news_feature['positive_negtive_积极_ratio'] = news_feature['positive_negtive_积极cnt']/news_feature['POSITIVE_NEGTIVE_CNT']

    return news_feature

def get_other_feature(other_info):
    other_feature = other_info.drop_duplicates()
    return other_feature


def gen_feature(data):
    base_info = data['base']
    annual_report_info = data['annual_report']
    tax_info = data['tax']
    change_info = data['change']
    news_info = data['news']
    other_info = data['other']
    
    feature = get_base_feature(base_info)
    feature = feature.merge(get_annual_report_feature(annual_report_info),on=['id'],how='left')
    feature = feature.merge(get_tax_feature(tax_info),on=['id'],how='left')
    feature = feature.merge(get_change_feature(change_info),on=['id'],how='left')
    feature = feature.merge(get_news_feature(news_info),on=['id'],how='left')
    feature = feature.merge(get_other_feature(other_info),on=['id'],how='left')
    
    return feature