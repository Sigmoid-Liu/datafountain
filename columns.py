base_columns = {'id':'企业唯一标识', 
                'oplocdistrict':'行政区划代码', 
                'industryphy':'行业类别代码', 
                'industryco':'行业细类代码', 
                'dom':'经营地址', #拆成省、市、区县
                'opscope':'经营范围', #LDA处理
                'enttype':'企业类型', 
                'enttypeitem':'企业类型小类', #0.33
                'opfrom':'经营期限起', 
                'opto':'经营期限止', #0.65缺失之填充“9999-12-31”
                'state':'状态', 
                'orgid':'机构标识', 
                'jobid':'职位标识', 
                'adbusign':'是否广告经营', 
                'townsign':'是否城镇', 
                'regtype':'主题登记类型',
                'empnum':'从业人数', #0.21
                'compform':'组织形式', #0.57
                'parnum':'合伙人数', #删除0.91
                'exenum':'执行人数', #删除
                'opform':'经营方式', #0.64
                'ptbusscope':'兼营范围', #1删除
                'venind':'风险行业', #0.66
                'enttypeminu':'企业类型细类', #0.71
                'midpreindcode':'中西部优势产业代码', #1删除
                'protype':'项目类型', #删除
                'oploc':'经营场所', #删除
                'regcap':'注册资本（金）', #0.01
                'reccap':'实缴资本', #0.72,转化成是否为空
                'forreccap':'实缴资本（外方）', #删除
                'forregcap':'注册资本（外方）', #删除
                'congro':'投资总额', #删除
                'enttypegb':'企业（机构）类型'
}

annual_report_columns = {'id':'企业唯一标识', 
                          'ANCHEYEAR':'年度', 
                          'STATE':'状态', 
                          'FUNDAM':'资金数额', 
                          'MEMNUM':'成员人数', 
                          'FARNUM':'农民人数', 
                          'ANNNEWMEMNUM':'本年度新增成员人数', 
                          'ANNREDMEMNUM':'本年度退出成员人数', 
                          'EMPNUM':'从业人数', 
                          'EMPNUMSIGN':'从业人数是否公示', 
                          'BUSSTNAME':'经营状态名称', 
                          'COLGRANUM':'其中高校毕业生人数经营者', 
                          'RETSOLNUM':'其中退役士兵人数经营者', 
                          'DISPERNUM':'其中残疾人人数经营者', 
                          'UNENUM':'其中下岗失业人数经营者', 
                          'COLEMPLNUM':'其中高校毕业生人数雇员', 
                          'RETEMPLNUM':'其中退役士兵人数雇员', 
                          'DISEMPLNUM':'其中残疾人人数雇员', 
                          'UNEEMPLNUM':'其中下岗失业人数雇员', 
                          'WEBSITSIGN':'是否有网站标志', 
                          'FORINVESTSIGN':'是否有对外投资企业标志', 
                          'STOCKTRANSIGN':'有限责任公司本年度是否发生股东股权转让标志', 
                          'PUBSTATE':'公示状态：1 全部公示，2部分公示,3全部不公示'
 }
tax_columns = {'id':'企业唯一标识', 
               'START_DATE':'起始时间', 
               'END_DATE':'终止时间', 
               'TAX_CATEGORIES':'税种', 
               'TAX_ITEMS':'税目', 
               'TAXATION_BASIS':'计税依据', 
               'TAX_RATE':'税率', 
               'DEDUCTION':'扣除数', 
               'TAX_AMOUNT':'税额'
}
change_columns = {'id':'企业唯一标识', 
                  'bgxmdm':'变更信息代码', 
                  'bgq':'变更前', 
                  'bgh':'变更后', 
                  'bgrq':'变更日期'
}

news_columns = {'id':'企业唯一标识', 
                'positive_negtive':'新闻正负面性', 
                'public_date':'发布日期'
}

other_columns = {'id':'企业唯一标识', 
                 'legal_judgment_num':'裁判文书数量', 
                 'brand_num':'注册商标数量', 
                 'patent_num':'专利数量'
}