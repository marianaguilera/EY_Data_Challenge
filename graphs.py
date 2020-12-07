import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from toolbox import read_and_process_data
# Other charts will be displayed with plotly, for nice data visualization
import seaborn as sns
import orca
import matplotlib.pyplot as plt
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#Connect to my chart_studio account
import chart_studio.plotly as py
py.sign_in('svaldes.salas', 'owvxCCaHjEJC81iQ5p8B')

import os
if not os.path.exists("images"):
    os.mkdir("images")

#/////////////////////////////
#           Graph 1
#/////////////////////////////
def graph1(df4, df4_pub, df4_online, df4_pub_online):
    variables = ['Applications_First_Entry_Total', 'First_Entry_Total', 'Enrollment_Total', 'All_Graduate']
    df_a = df4.groupby(["State"]).sum()[variables].sum().to_frame(name="private")
    df_b = df4_pub.groupby(["State"]).sum()[variables].sum().to_frame(name="public")
    df_c = df4_online.groupby(["State"]).sum()[variables].sum().to_frame(name="private")
    df_d = df4_pub_online.groupby(["State"]).sum()[variables].sum().to_frame(name="public")
    # add onsite and online
    df_merged = pd.merge(df_a + df_c, df_b + df_d, on=df_a.index).set_index("key_0")
    df_merged.index = ['New applicants', 'New students', 'Enrolled', 'All Graduate']
    #Plot
    fig1 = go.Figure(data=[go.Bar(name='private', x=df_merged.index, y=df_merged['private'], marker_color='#6877dc'),
                           go.Bar(name='public', x=df_merged.index, y=df_merged['public'], marker_color='#444c7a')],
                     layout_title_text='Total students by type of institution in Mexico (2019-2020)')
    fig1.update_layout(barmode='group')
    fig1.update_yaxes(title_text='Total students')
    fig1.write_image("./images/fig1.png")
    py.iplot(fig1)
    return py.iplot(fig1)

#/////////////////////////////
#           Graph 2
#/////////////////////////////
def graph2(df1, df1_online, df2, df2_online, df3, df3_online, df4, df4_online):
    variables = ['Applications_First_Entry_Total', 'First_Entry_Total', 'Enrollment_Total', 'All_Graduate','Graduate_with_Diploma_Total']
    df_a = df1.groupby(["State"]).sum()[variables].sum().to_frame(name="2016-2017") + \
           df1_online.groupby(["State"]).sum()[variables].sum().to_frame(name="2016-2017")
    df_b = df2.groupby(["State"]).sum()[variables].sum().to_frame(name="2017-2018") + \
           df2_online.groupby(["State"]).sum()[variables].sum().to_frame(name="2017-2018")
    df_c = df3.groupby(["State"]).sum()[variables].sum().to_frame(name="2018-2019") + \
           df3_online.groupby(["State"]).sum()[variables].sum().to_frame(name="2018-2019")
    df_d = df4.groupby(["State"]).sum()[variables].sum().to_frame(name="2019-2020") + \
           df4_online.groupby(["State"]).sum()[variables].sum().to_frame(name="2019-2020")
    dfs = [df_a, df_b, df_c, df_d]
    dfs_ = pd.concat(dfs, axis=1).transpose()
    # plot
    fig2 = go.Figure()
    fig2 = fig2.add_trace(go.Scatter(x=dfs_.index, y=dfs_['Enrollment_Total'], mode='lines', line=dict(width=0.5, color='#96a4ff'),name='Enrolled', fill='tozeroy'))
    fig2 = fig2.add_trace(go.Scatter(x=dfs_.index, y=dfs_['Applications_First_Entry_Total'], mode='lines',
                                       line=dict(width=0.5, color='#6877dc'), name='Applications', fill='tozeroy'))
    fig2 = fig2.add_trace(go.Scatter(x=dfs_.index, y=dfs_['First_Entry_Total'], mode='lines', name='New students',
                                       line=dict(width=0.5, color='#636ead'), fill='tozeroy'))
    fig2 = fig2.add_trace(go.Scatter(x=dfs_.index, y=dfs_['All_Graduate'], mode='lines', name='All Graduate',
                                       line=dict(width=0.5, color='#444c7a'), fill='tozeroy'))
    fig2 = fig2.add_trace(go.Scatter(x=dfs_.index, y=dfs_['Graduate_with_Diploma_Total'], mode='lines', name='Graduate (w/ Diploma)',
                                     line=dict(width=0.5, color='#363a4d'), fill='tozeroy'))
    fig2.update_layout(title="Total students in private institutions by period (onsite and online modalities)",xaxis_title='Period',yaxis_title='Total')
    fig2.write_image("./images/fig2.png")
    return py.iplot(fig2)

#/////////////////////////////
#           Graph 3
#/////////////////////////////
def graph3(df1,df1_online,df2,df2_online,df3,df3_online,df4,df4_online,df1_pub,df1_pub_online,df2_pub,df2_pub_online,df3_pub,df3_pub_online,df4_pub,df4_pub_online):
    variables = ['Applications_First_Entry_Total', 'First_Entry_Total']
    # onsite dataframes
    df_a = df1.groupby(["State"]).sum()[variables].sum().to_frame(name="2016-2017") + \
           df1_online.groupby(["State"]).sum()[variables].sum().to_frame(name="2016-2017")
    df_b = df2.groupby(["State"]).sum()[variables].sum().to_frame(name="2017-2018") + \
           df2_online.groupby(["State"]).sum()[variables].sum().to_frame(name="2017-2018")
    df_c = df3.groupby(["State"]).sum()[variables].sum().to_frame(name="2018-2019") + \
           df3_online.groupby(["State"]).sum()[variables].sum().to_frame(name="2018-2019")
    df_d = df4.groupby(["State"]).sum()[variables].sum().to_frame(name="2019-2020") + \
           df4_online.groupby(["State"]).sum()[variables].sum().to_frame(name="2019-2020")
    dfs = [df_a, df_b, df_c, df_d]
    dfs_ = pd.concat(dfs, axis=1).transpose()
    dfs_change = dfs_.pct_change().fillna(0) * 100  # .iloc[1:]
    # online dataframes
    df_e = df1_pub.groupby(["State"]).sum()[variables].sum().to_frame(name="2016-2017") + \
           df1_pub_online.groupby(["State"]).sum()[variables].sum().to_frame(name="2016-2017")
    df_f = df2_pub.groupby(["State"]).sum()[variables].sum().to_frame(name="2017-2018") + \
           df2_pub_online.groupby(["State"]).sum()[variables].sum().to_frame(name="2017-2018")
    df_g = df3_pub.groupby(["State"]).sum()[variables].sum().to_frame(name="2018-2019") + \
           df3_pub_online.groupby(["State"]).sum()[variables].sum().to_frame(name="2018-2019")
    df_h = df4_pub.groupby(["State"]).sum()[variables].sum().to_frame(name="2019-2020") + \
           df4_pub_online.groupby(["State"]).sum()[variables].sum().to_frame(name="2019-2020")
    dfs_pub = [df_e, df_f, df_g, df_h]
    dfs_pub = pd.concat(dfs_pub, axis=1).transpose()
    dfs_pub_change = dfs_pub.pct_change().fillna(0) * 100
    dfs_pub_change['baseline'] = 0
    # Plot
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=dfs_change.index, y=dfs_change['Applications_First_Entry_Total'], mode='lines+markers',name='Private + New applications'))
    fig3.add_trace(go.Scatter(x=dfs_change.index, y=dfs_change['First_Entry_Total'], mode='lines+markers', name='Private + New students'))
    fig3.add_trace(go.Scatter(x=dfs_pub_change.index, y=dfs_pub_change['Applications_First_Entry_Total'], mode='lines+markers',name='Public + New applications'))
    fig3.add_trace(go.Scatter(x=dfs_pub_change.index, y=dfs_pub_change['First_Entry_Total'], mode='lines+markers', name='Public + New students'))
    fig3.add_trace(go.Scatter(x=dfs_pub_change.index, y=dfs_pub_change['baseline'], mode='lines', name='0', fill=None,line_color='black'))
    fig3.update_layout(title='Change of new applications and new students by type of institutions (all modalities)',xaxis_title='Period',yaxis_title='Percentage change')
    fig3.write_image("./images/fig3.png")
    #fig3.show()
    return py.iplot(fig3)

#/////////////////////////////
#           Graph 4
#/////////////////////////////
def graph4(df1,df2,df3,df4,df1_pub,df2_pub,df3_pub,df4_pub):
    variables = ['Applications_First_Entry_Total', 'First_Entry_Total']
    # onsite
    df_a = df1.groupby(["State"]).sum()[variables].sum().to_frame(name="2016-2017")
    df_b = df2.groupby(["State"]).sum()[variables].sum().to_frame(name="2017-2018")
    df_c = df3.groupby(["State"]).sum()[variables].sum().to_frame(name="2018-2019")
    df_d = df4.groupby(["State"]).sum()[variables].sum().to_frame(name="2019-2020")
    dfs = [df_a, df_b, df_c, df_d]
    dfs_ = pd.concat(dfs, axis=1).transpose()
    dfs_change = dfs_.pct_change().fillna(0) * 100
    # online
    df_e = df1_pub.groupby(["State"]).sum()[variables].sum().to_frame(name="2016-2017")
    df_f = df2_pub.groupby(["State"]).sum()[variables].sum().to_frame(name="2017-2018")
    df_g = df3_pub.groupby(["State"]).sum()[variables].sum().to_frame(name="2018-2019")
    df_h = df4_pub.groupby(["State"]).sum()[variables].sum().to_frame(name="2019-2020")
    dfs_pub = [df_e, df_f, df_g, df_h]
    dfs_pub = pd.concat(dfs_pub, axis=1).transpose()
    dfs_pub_change = dfs_pub.pct_change().fillna(0) * 100
    dfs_pub_change['baseline'] = 0
    # Plot
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(x=dfs_change.index, y=dfs_change['Applications_First_Entry_Total'], mode='lines+markers',name='Private + New applications'))
    fig4.add_trace(go.Scatter(x=dfs_change.index, y=dfs_change['First_Entry_Total'], mode='lines+markers',name='Private + New students'))
    fig4.add_trace(go.Scatter(x=dfs_pub_change.index, y=dfs_pub_change['Applications_First_Entry_Total'], mode='lines+markers',name='Public + New applications'))
    fig4.add_trace(go.Scatter(x=dfs_pub_change.index, y=dfs_pub_change['First_Entry_Total'], mode='lines+markers',name='Public + New students'))
    fig4.add_trace(go.Scatter(x=dfs_pub_change.index, y=dfs_pub_change['baseline'], mode='lines', name='0', fill=None,line_color='black'))
    fig4.update_layout(title='Change of new applications and new students by type of institutions (onsite modality)',xaxis_title='Period', yaxis_title='Percentage change')
    fig4.write_image("./images/fig4.png")
    #fig4.show()
    return py.iplot(fig4)

#/////////////////////////////
#           Graph 5
#/////////////////////////////
def graph5(df1_online,df2_online,df3_online,df4_online,df1_pub_online,df2_pub_online,df3_pub_online,df4_pub_online):
    variables = ['Applications_First_Entry_Total','First_Entry_Total']
    # onsite
    df_a = df1_online.groupby(["State"]).sum()[variables].sum().to_frame(name="2016-2017")
    df_b = df2_online.groupby(["State"]).sum()[variables].sum().to_frame(name="2017-2018")
    df_c = df3_online.groupby(["State"]).sum()[variables].sum().to_frame(name="2018-2019")
    df_d = df4_online.groupby(["State"]).sum()[variables].sum().to_frame(name="2019-2020")
    dfs = [df_a,df_b,df_c,df_d]
    dfs_ = pd.concat(dfs, axis=1).transpose()
    dfs_change = dfs_.pct_change().fillna(0)*100
    # online
    df_e = df1_pub_online.groupby(["State"]).sum()[variables].sum().to_frame(name="2016-2017")
    df_f = df2_pub_online.groupby(["State"]).sum()[variables].sum().to_frame(name="2017-2018")
    df_g = df3_pub_online.groupby(["State"]).sum()[variables].sum().to_frame(name="2018-2019")
    df_h = df4_pub_online.groupby(["State"]).sum()[variables].sum().to_frame(name="2019-2020")
    dfs_pub = [df_e,df_f,df_g,df_h]
    dfs_pub = pd.concat(dfs_pub, axis=1).transpose()
    dfs_pub_change = dfs_pub.pct_change().fillna(0)*100
    dfs_pub_change['baseline'] = 0 # define a baseline
    # Plot
    fig5 = go.Figure()
    fig5.add_trace(go.Scatter(x=dfs_change.index, y=dfs_change['Applications_First_Entry_Total'],mode='lines+markers',name='Private + New applications'))
    fig5.add_trace(go.Scatter(x=dfs_change.index, y=dfs_change['First_Entry_Total'],mode='lines+markers',name='Private + New students'))
    fig5.add_trace(go.Scatter(x=dfs_pub_change.index, y=dfs_pub_change['Applications_First_Entry_Total'],mode='lines+markers',name='Public + New applications'))
    fig5.add_trace(go.Scatter(x=dfs_pub_change.index, y=dfs_pub_change['First_Entry_Total'],mode='lines+markers',name='Public + New students'))
    fig5.add_trace(go.Scatter(x=dfs_pub_change.index, y=dfs_pub_change['baseline'],mode='lines', name='0', fill=None, line_color='black'))
    fig5.update_layout(title='Change of new applications and new students by type of institutions (online modality)',xaxis_title='Period',yaxis_title='Percentage change')
    fig5.write_image("./images/fig5.png")
    #fig5.show()
    return py.iplot(fig5)

#/////////////////////////////
#           Graph 6
#/////////////////////////////
def graph6(df1,df1_online,df4,df4_online):
    variables = ['Applications_First_Entry_Total', 'First_Entry_Total', 'Enrollment_Total', 'All_Graduate']
    df_a = df1.groupby(["State"]).sum()[variables].sum().to_frame(name="onsite 2016-2017")
    df_b = df1_online.groupby(["State"]).sum()[variables].sum().to_frame(name="online 2016-2017")
    df_c = df4.groupby(["State"]).sum()[variables].sum().to_frame(name="onsite 2019-2020")
    df_d = df4_online.groupby(["State"]).sum()[variables].sum().to_frame(name="online 2019-2020")
    dfs = [df_a, df_c, df_b, df_d]
    dfs_onsite = pd.concat(dfs[:2], axis=1).transpose()
    dfs_online = pd.concat(dfs[2:], axis=1).transpose()
    # plot
    fig6 = make_subplots(rows=1, cols=2)
    # plot onsite trends
    fig6.add_trace(go.Bar(name="New applications", x=dfs_onsite.index, y=dfs_onsite['Applications_First_Entry_Total'],marker_color='#96a4ff'), 1, 1)
    fig6.add_trace(go.Bar(name='New students', x=dfs_onsite.index, y=dfs_onsite['First_Entry_Total'], marker_color='#6877dc'), 1,1)
    fig6.add_trace(go.Bar(name='Enrolled', x=dfs_onsite.index, y=dfs_onsite['Enrollment_Total'], marker_color='#636ead'),1, 1)
    fig6.add_trace(go.Bar(name='All Graduate', x=dfs_onsite.index, y=dfs_onsite['All_Graduate'], marker_color='#444c7a'),1, 1)
    # plot online trends
    fig6.add_trace(go.Bar(name="New applications", x=dfs_online.index, y=dfs_online['Applications_First_Entry_Total'],marker_color='#96a4ff', showlegend=False), 1, 2)
    fig6.add_trace(go.Bar(name='New students', x=dfs_online.index, y=dfs_online['First_Entry_Total'], marker_color='#6877dc',showlegend=False), 1, 2)
    fig6.add_trace(go.Bar(name='Enrolled', x=dfs_online.index, y=dfs_online['Enrollment_Total'], marker_color='#636ead', showlegend=False), 1, 2)
    fig6.add_trace(go.Bar(name='All Graduate', x=dfs_online.index, y=dfs_online['All_Graduate'], marker_color='#444c7a',showlegend=False), 1, 2)
    fig6.update_layout(title_text="Total students in private institutions, by onsite or online modality in Mexico (2016-2017 vs 2019-2020)")
    fig6.update_xaxes(title_text='Period')
    fig6.update_yaxes(title_text='Total')
    fig6.write_image("./images/fig6.png")
    #fig6.show()
    x=(1219735-987661)/987661 *100
    y=(563555-304293)/304293*100
    print("Enrolled students in private-onsite education grew = {}%".format(round(x, 2)))
    print("Enrolled students in private-online education grew = {}%".format(round(y, 2)))
    return py.iplot(fig6)

#/////////////////////////////
#           Graph 7
#/////////////////////////////
def graph7(dfs_UVM_final):
    variables = ['Applications_First_Entry_Total','First_Entry_Total','Enrollment_Total','All_Graduate']
    UVM_by_modality = dfs_UVM_final.groupby(['period','modality']).sum()[variables].reset_index()
    last_period = UVM_by_modality[UVM_by_modality['period']=='2019-2020']
    df_a = last_period[last_period['modality']=='private-online'].set_index(['modality']).drop('period',axis=1).transpose()
    df_b = last_period[last_period['modality']=='private-onsite'].set_index(['modality']).drop('period',axis=1).transpose()
    merged = pd.concat([df_a,df_b],axis=1)
    merged = merged.rename(columns={'private-online':'online','private-onsite':'onsite'},index={'Applications_First_Entry_Total':'Applications','First_Entry_Total':'First year','Enrollment_Total':'Enrolled','All_Graduate':'Graduate'})
    # Plot
    fig7 = go.Figure(data=[go.Bar(name='onsite', x=merged.index, y=merged['onsite'], marker_color='#444c7a'),
                           go.Bar(name='online', x=merged.index, y=merged['online'], marker_color='#6877dc')],
                     layout_title_text='Total students in UVM by category, modality onsite and online (2019-2020)')
    fig7.update_layout(barmode='stack')
    fig7.update_xaxes(title_text='Category')
    fig7.update_yaxes(title_text='Total students')
    fig7.write_image("./images/fig7.png")
    return py.iplot(fig7)

#/////////////////////////////
#           Graph 8
#/////////////////////////////
def graph8(dfs_UVM_final):
    variables = ['Applications_First_Entry_Total','First_Entry_Total','Enrollment_Total','All_Graduate']
    UVM_by_modality = dfs_UVM_final.groupby(['period','modality']).sum()[variables].reset_index()
    last_period = UVM_by_modality[UVM_by_modality['period']=='2019-2020']
    online_values = last_period[last_period['modality']=='private-online'].set_index(['modality']).drop('period',axis=1)
    onsite_values = last_period[last_period['modality']=='private-onsite'].set_index(['modality']).drop('period',axis=1)
    df_a = onsite_values.transpose()
    df_b = online_values.transpose()
    merged = pd.concat([df_a,df_b],axis=1)
    merged = merged.rename(columns={'private-online':'online','private-onsite':'onsite'},index={'Applications_First_Entry_Total':'Applications','First_Entry_Total':'First year','Enrollment_Total':'Enrolled','All_Graduate':'Graduate'})
    perc = merged.sum(axis = 1)
    #merged['perc']= merged['score']/p['score'].sum() # we cannot sum the categories because they might not be mutually exclusively
    merged['online'] = merged['online']/perc*100
    merged['onsite'] = merged['onsite']/perc*100
    # plot
    sns.set_style('white')
    merged.plot(kind='barh', figsize=(13,5), stacked=True, color=['#464d77','#6a78d6']).invert_yaxis()
    plt.title('Distribution of students by category and by modality at UVM (2019-2020)', fontsize=18)
    plt.xlabel('Percentage', fontsize=15)
    plt.ylabel('')
    plt.legend(bbox_to_anchor=(1, 1), loc='best', fontsize=15)
    plt.savefig('./images/fig8.png')
    plt.yticks(fontsize=16)
    plt.xticks(fontsize=12)
    plt.show()
    return merged

#/////////////////////////////
#           Graph 9
#/////////////////////////////
def graph9(dfs_UVM_final):
    variables = ['Applications_First_Entry_Total','First_Entry_Total','Enrollment_Total','All_Graduate']
    UVM_by_modality = dfs_UVM_final.groupby(['period','modality']).sum()[variables].reset_index()
    last_period = UVM_by_modality[UVM_by_modality['period']=='2016-2017']
    online_values = last_period[last_period['modality']=='private-online'].set_index(['modality']).drop('period',axis=1)
    onsite_values = last_period[last_period['modality']=='private-onsite'].set_index(['modality']).drop('period',axis=1)
    df_a = onsite_values.transpose()
    df_b = online_values.transpose()
    merged = pd.concat([df_a,df_b],axis=1)
    merged = merged.rename(columns={'private-online':'online','private-onsite':'onsite'},index={'Applications_First_Entry_Total':'Applications','First_Entry_Total':'First year','Enrollment_Total':'Enrolled','All_Graduate':'Graduate'})
    perc = merged.sum(axis = 1)
    merged['online'] = merged['online']/perc*100
    merged['onsite'] = merged['onsite']/perc*100
    # plot
    sns.set_style('white')
    merged.plot(kind='barh', figsize=(13,5), stacked=True, color=['#464d77','#6a78d6']).invert_yaxis()
    plt.title('Distribution of students by category and by modality at UVM (2016-2017)', fontsize=18)
    plt.xlabel('Percentage', fontsize=15)
    plt.ylabel('')
    plt.legend(bbox_to_anchor=(1, 1), loc='best', fontsize=13)
    plt.savefig('./images/fig9.png')
    plt.yticks(fontsize=16)
    plt.xticks(fontsize=12)
    plt.show()
    return merged

#/////////////////////////////
#           Graph 10
#/////////////////////////////
def graph10(dfs_UVM_final):
    # applications as a percentage of offered places
    dfs_UVM_grouped_period_modality = dfs_UVM_final.groupby(['period', 'modality']).sum().reset_index()
    dfs_UVM_grouped_period_modality["applications_places_ratio"] = dfs_UVM_grouped_period_modality["Applications_First_Entry_Total"] / dfs_UVM_grouped_period_modality["Offered_places"]
    dfs_UVM_grouped_period_modality = dfs_UVM_grouped_period_modality[['period', 'modality', 'applications_places_ratio']]
    df_a = dfs_UVM_grouped_period_modality[dfs_UVM_grouped_period_modality['modality'] == 'private-onsite']
    df_b = dfs_UVM_grouped_period_modality[dfs_UVM_grouped_period_modality['modality'] == 'private-online']
    baseline = df_a.copy(deep=True) # define a baseline of 100%
    baseline['applications_places_ratio'] = 1
    # plot
    fig10 = go.Figure()
    fig10 = fig10.add_trace(go.Scatter(x=df_a['period'], y=df_a['applications_places_ratio'] * 100, mode='lines', name='onsite-UVM',fill='tozeroy'))
    fig10 = fig10.add_trace(go.Scatter(x=df_b['period'], y=df_b['applications_places_ratio'] * 100, mode='lines', name='online-UVM',fill='tozeroy'))
    fig10 = fig10.add_trace(go.Scatter(x=baseline['period'], y=baseline['applications_places_ratio'] * 100, mode='lines',name='100% of offered places', fill=None, line_color='black'))
    fig10.update_layout(title="Applications at UVM as a percentage of offered places by modalities (onsite and online)",xaxis_title='Period',yaxis_title='Percentage')
    fig10.write_image("./images/fig10.png")
    return py.iplot(fig10)

#/////////////////////////////
#   Graph 10 - offered places
#/////////////////////////////
def chart10a(dfs_UVM_final):
    # number of places
    offered_places = dfs_UVM_final.groupby(['period', 'modality']).sum()  # .reset_index()
    offered_unstack = offered_places[['Offered_places']].unstack(
        level=1)  # .reset_index().rename_axis((None,None), axis=1)
    # plot
    sns.set_style('white')
    offered_unstack.plot(kind='bar', figsize=(10, 7), color=['#6a78d6', '#464d77'])
    plt.title('Total places offered by period and by modality at UVM', fontsize=18)
    plt.xlabel('')
    plt.ylabel('Places offered', fontsize=14)
    plt.legend(['online', 'onsite'], loc='best', fontsize=13)
    plt.savefig('./images/fig10-a.png')
    plt.yticks(fontsize=13)
    plt.xticks(fontsize=12, rotation=0)
    plt.show()
    return offered_unstack

#/////////////////////////////
#  Graph 10-b enrollment geographic change
#/////////////////////////////
def graph10b(dfs_UVM_final):
    onsite = dfs_UVM_final  # [dfs_UVM_final['modality']=='private-onsite']
    onsite = onsite.groupby(['State', 'period']).sum().reset_index()
    df_a = onsite[onsite['period'] == '2016-2017'][['State', 'Enrollment_Total']].set_index('State').rename(
        columns={'Enrollment_Total': '2016-2017'})
    df_b = onsite[onsite['period'] == '2019-2020'][['State', 'Enrollment_Total']].set_index('State').rename(
        columns={'Enrollment_Total': '2019-2020'})
    dfs = pd.concat([df_a, df_b], axis=1)
    dfs = dfs.rename(index={'AGUASCALIENTES': 'AGU', 'BAJA CALIFORNIA': 'BCN', 'CHIAPAS': 'CHP', 'CHIHUAHUA': 'CHH',
                            'CIUDAD DE MÉXICO': 'CMX',
                            'COAHUILA': 'COA', 'JALISCO': 'JAL', 'MORELOS': 'MOR', 'MÉXICO': 'MEX', 'NUEVO LEÓN': 'NLE',
                            'PUEBLA': 'PUE',
                            'QUERÉTARO': 'QUE', 'SAN LUIS POTOSÍ': 'SLP', 'TABASCO': 'TAB', 'TAMAULIPAS': 'TAM',
                            'VERACRUZ': 'VER', 'YUCATÁN': 'YUC', 'SONORA': 'SON'})

    dfs['perc_change'] = (dfs['2019-2020'] - dfs['2016-2017']) / dfs['2016-2017'] * 100
    dfs_perc = dfs.drop(['2019-2020', '2016-2017'], axis=1).sort_values('perc_change', ascending=False)

    my_colors = sns.diverging_palette(258, 12, s=95, l=55, sep=1, n=18, center='dark')
    plt.figure(figsize=(14, 6))
    plt.xticks(fontsize=10, rotation=0)
    ax = sns.barplot(x=dfs_perc.index, y=dfs_perc['perc_change'], palette=my_colors)
    ax.set_xlabel("States", fontsize=15)
    ax.set_ylabel("Percentage change", fontsize=15)
    ax.axes.set_title('Change of enrollment at UVM  by state (2016-2017 vs 2019-2020)', fontsize=18)
    plt.axhline(linewidth=1, color='black')
    plt.savefig("./images/fig10-b.png")
    plt.show()
    return dfs

#/////////////////////////////
#  Graph 10-c app/offered geographic
#/////////////////////////////
def graph10c(dfs_UVM_final):
    onsite = dfs_UVM_final  # [(dfs_UVM_final['modality']=='private-onsite')|(dfs_UVM_final['modality']=='private-online')]
    onsite = onsite.groupby(['State', 'period']).sum().reset_index()
    # df_a = onsite[onsite['period']=='2016-2017'][['State','First_Entry_Total']].set_index('State').rename(columns={'First_Entry_Total':'2016-2017'})
    df_b = onsite[onsite['period'] == '2019-2020'][
        ['State', 'Offered_places', 'Applications_First_Entry_Total']].set_index(
        'State')  # .rename(columns={'First_Entry_Total':'2019-2020'})
    df_b = df_b.rename(index={'AGUASCALIENTES': 'AGU', 'BAJA CALIFORNIA': 'BCN', 'CHIAPAS': 'CHP', 'CHIHUAHUA': 'CHH',
                              'CIUDAD DE MÉXICO': 'CMX',
                              'COAHUILA': 'COA', 'JALISCO': 'JAL', 'MORELOS': 'MOR', 'MÉXICO': 'MEX',
                              'NUEVO LEÓN': 'NLE', 'PUEBLA': 'PUE',
                              'QUERÉTARO': 'QUE', 'SAN LUIS POTOSÍ': 'SLP', 'TABASCO': 'TAB', 'TAMAULIPAS': 'TAM',
                              'VERACRUZ': 'VER', 'YUCATÁN': 'YUC', 'SONORA': 'SON'})

    ratio = df_b['Applications_First_Entry_Total'] / df_b['Offered_places'] * 100
    ratio = ratio.sort_values(ascending=False)
    baseline = ratio.copy(deep=True)
    baseline = pd.Series([100] * len(ratio))

    # plot
    sns.set_style('white')
    ratio.plot(kind='bar', figsize=(14, 6), color=['#464d77'])
    baseline.plot(kind='line', figsize=(14, 6), color=['red'])
    plt.title('Applications as a percentage of offered places by state at UVM (2019-2020)', fontsize=18)
    plt.xlabel('State', fontsize=14)
    plt.ylabel('Percentage', fontsize=14)
    plt.legend(['100% of offered places'], loc='best', fontsize=13)
    plt.yticks(fontsize=13)
    plt.xticks(fontsize=10, rotation=45)
    plt.axhline(linewidth=1, color='black')
    plt.savefig('./images/fig10-c.png')
    plt.show()


#/////////////////////////////
#           Graph 11
#/////////////////////////////
def graph11(dfs_UVM_final):
    offered_places = dfs_UVM_final.groupby(['period', 'modality']).sum()
    offered_unstack = offered_places[['Offered_places']].unstack(level=1)
    # plot
    sns.set_style('white')
    offered_unstack.plot(kind='bar', figsize=(10, 7), color=['#6a78d6', '#464d77'])
    plt.title('Total places offered by period and by modality at UVM', fontsize=18)
    plt.xlabel('')
    plt.ylabel('Places offered', fontsize=15)
    plt.legend(['online', 'onsite'], loc='best', fontsize=13)
    plt.yticks(fontsize=13)
    plt.xticks(fontsize=12, rotation='horizontal')
    plt.savefig('./images/fig11.png')
    plt.show()

#/////////////////////////////
#           Graph 12
#/////////////////////////////
def graph12(dfs_all, competitors_onsite, competitors_online):
    #competitors_onsite = []
    #competitors_online = []
    # onsite learning
    variables = ['Enrollment_Total']
    total_enrolled = dfs_all.groupby(["Institute", "modality", "period"]).sum()[variables].reset_index()
    total_enrolled_onsite = total_enrolled[(total_enrolled['period'] == '2019-2020') & (total_enrolled['modality'] == 'private-onsite')]
    # This is the total number of players in online education
    print("Total players in onsite learning in 2019-2020 = ",total_enrolled_onsite['Institute'].nunique())
    # total enrolled students
    total_onsite = total_enrolled_onsite['Enrollment_Total'].sum()
    # sort and clean dataframe
    enrolled_sorted = total_enrolled_onsite.sort_values(by='Enrollment_Total', ascending=False).drop(['modality', 'period'], axis=1).set_index('Institute')
    # get percentage
    perc_onsite = enrolled_sorted[['Enrollment_Total']] / total_onsite * 100
    # get top players
    top_players_onsite = perc_onsite[perc_onsite['Enrollment_Total'] > 2]
    top_players_onsite_renamed = top_players_onsite.rename(index={'UNIVERSIDAD TECNOLÓGICA DE MÉXICO': 'UNITEC', 'UNIVERSIDAD DEL VALLE DE MÉXICO': 'UVM','INSTITUTO TECNOLÓGICO Y DE ESTUDIOS SUPERIORES DE MONTERREY': 'ITESM'}).reset_index()
    # Add rest
    rest_onsite = 100 - top_players_onsite_renamed['Enrollment_Total'].sum()
    top_players_onsite_renamed = top_players_onsite_renamed.append({'Institute': 'REST OF INSTITUTIONS', 'Enrollment_Total': rest_onsite}, ignore_index=True).set_index('Institute')
    # extend competitors list
    competitors_onsite.extend(top_players_onsite.index.tolist()[:-1])

    # online learning
    variables = ['Enrollment_Total']
    total_enrolled = dfs_all.groupby(["Institute", "modality", "period"]).sum()[variables].reset_index()
    total_enrolled_online = total_enrolled[(total_enrolled['period'] == '2019-2020') & (total_enrolled['modality'] == 'private-online')]
    # This is the total number of players in online education
    print("Total players in online learning in 2019-2020 = ",total_enrolled_online['Institute'].nunique())
    total_online = total_enrolled_online['Enrollment_Total'].sum()  # total enrolled students
    # sort and clean dataframe
    enrolled_sorted = total_enrolled_online.sort_values(by='Enrollment_Total', ascending=False).drop(['modality', 'period'], axis=1).set_index('Institute')
    # get percentage
    perc_online = enrolled_sorted[['Enrollment_Total']] / total_online * 100
    # get top players
    top_players_online = perc_online[perc_online['Enrollment_Total'] > 2]
    top_players_online_renamed = top_players_online.rename(index={'UNIVERSIDAD TECNOLÓGICA DE MÉXICO': 'UNITEC', 'UNIVERSIDAD DEL VALLE DE MÉXICO': 'UVM','INSTITUTO TECNOLÓGICO Y DE ESTUDIOS SUPERIORES DE MONTERREY': 'ITESM',
                                                                  'UNIVERSIDAD INTERAMERICANA PARA EL DESARROLLO': 'UNID','ENSEÑANZA E INVESTIGACIÓN SUPERIOR, A.C.': 'EISAC',
                                                                  'UNIVERSIDAD TECNOLÓGICA LATINOAMERICANA EN LÍNEA': 'UTEL','UNIVERSIDAD LATINOAMERICANA, S.C.': 'ULA', 'INSTITUTO DE ESTUDIOS UNIVERSITARIOS, A.C.': 'IEU',
                                                                  'UNIVERSIDAD INSURGENTES': 'UNIV. INSURGENTES'}).reset_index()
    # Add rest
    rest_online = 100 - top_players_online_renamed['Enrollment_Total'].sum()
    top_players_online_renamed = top_players_online_renamed.append({'Institute': 'REST OF INSTITUTIONS', 'Enrollment_Total': rest_online}, ignore_index=True).set_index('Institute')
    # extend competitors list
    competitors_online.extend(top_players_online.index.tolist()[:-1])

    # get labels and values
    def ValuesLabels(df, column='%'):
        t = 0
        values = []
        labels = []
        for index, row in df.iterrows():
            v = row[column]
            t += v
            values.append(v)
            labels.append(index)
        values.append(100 - t)
        labels.append('Others')
        return values, labels

    values_prev = ValuesLabels(top_players_onsite_renamed, column='Enrollment_Total')[0][:-1]
    labels_prev = ValuesLabels(top_players_onsite_renamed, column='Enrollment_Total')[1][:-1]
    values_last = ValuesLabels(top_players_online_renamed, column='Enrollment_Total')[0][:-1]
    labels_last = ValuesLabels(top_players_online_renamed, column='Enrollment_Total')[1][:-1]

    # Create subplots: use 'domain' type for Pie subplot
    fig12 = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
    fig12.add_trace(go.Pie(labels=labels_prev, values=values_prev, name="2016-2017"), 1, 1)
    fig12.add_trace(go.Pie(labels=labels_last, values=values_last, name="2019-2020"), 1, 2)
    fig12.update_traces(hole=0.3, hoverinfo='label+percent')
    fig12.update_layout(title_text="Distribution of enrolled students by private institutes by modality (2019-2020)",annotations=[dict(text='ONSITE', x=0.20, y=0.5, font_size=14, showarrow=False),
                                                                                                                              dict(text='ONLINE', x=0.80, y=0.5, font_size=14, showarrow=False)])
    fig12.write_image("./images/fig12.png")
    return py.iplot(fig12), competitors_onsite, competitors_online

#/////////////////////////////
#           Graph 13
#/////////////////////////////
def graph13(dfs_all, competitors_onsite):
    variables = ['Applications_First_Entry_Total']
    total_applications = dfs_all.groupby(["Institute", "modality", "period"]).sum()[variables].reset_index()
    total_applications_onsite = total_applications[(total_applications['period'] == '2019-2020') & (total_applications['modality'] == 'private-onsite')]
    #total_onsite = total_applications_onsite['Applications_First_Entry_Total'].sum()
    # get top 15
    applications_onsite_top15 = total_applications_onsite.sort_values(by='Applications_First_Entry_Total',
                                                                      ascending=False).drop(['modality', 'period'],axis=1).set_index('Institute')[:15].reset_index().sort_values('Applications_First_Entry_Total')
    # add to onsite competitors list
    for i in applications_onsite_top15['Institute'].values.tolist():
        if i not in competitors_onsite:
            competitors_onsite.append(i)

    # plot incidence
    colors = ["#464d77"] * 15
    colors[13] = 'crimson'
    fig13 = go.Figure(go.Bar(
        y=applications_onsite_top15['Institute'], x=applications_onsite_top15['Applications_First_Entry_Total'],
        marker_color=colors,
        orientation='h'),
        layout_title_text='Private institutions with the highest number of applications in 2019-2020 (onsite modality)')
    fig13.update_layout(barmode='group')
    fig13.write_image("./images/fig13.png")
    return py.iplot(fig13), competitors_onsite

#/////////////////////////////
#           Graph 14
#/////////////////////////////
def graph14(dfs_all, competitors_online):
    variables = ['Applications_First_Entry_Total']
    total_applications = dfs_all.groupby(["Institute", "modality", "period"]).sum()[variables].reset_index()
    total_applications_online = total_applications[(total_applications['period']=='2019-2020') & (total_applications['modality']=='private-online')]
    #total_onsite = total_applications_online['Applications_First_Entry_Total'].sum()
    # get top 15
    applications_online_top15 = total_applications_online.sort_values(by='Applications_First_Entry_Total',
                                                                      ascending=False).drop(['modality', 'period'],axis=1).set_index('Institute')[:15].reset_index().sort_values('Applications_First_Entry_Total')

    # add to onsite competitors list
    for i in applications_online_top15['Institute'].values.tolist():
        if i not in competitors_online:
            competitors_online.append(i)

    # plot incidence
    colors = ["#464d77"] * 15
    colors[14] = 'crimson'
    fig14 = go.Figure(go.Bar(
        y=applications_online_top15['Institute'], x=applications_online_top15['Applications_First_Entry_Total'],
        marker_color=colors,
        orientation='h'),
        layout_title_text='Private institutions with the highest number of applications in 2019-2020 (online modality)')
    fig14.update_layout(barmode='group')
    fig14.write_image("./images/fig14.png")
    return py.iplot(fig14), competitors_online

#/////////////////////////////
#           Graph 15
#/////////////////////////////
# First entry onsite
def graph15(dfs_all, final_onsite_competitors):
    variables = ['First_Entry_Total']
    df_a = dfs_all[(dfs_all['period'] == '2019-2020') & (dfs_all['modality'] == 'private-onsite') & (
        dfs_all['Institute'].isin(final_onsite_competitors))]
    df_b = dfs_all[(dfs_all['period'] == '2016-2017') & (dfs_all['modality'] == 'private-onsite') & (
        dfs_all['Institute'].isin(final_onsite_competitors))]
    df_a = df_a.groupby(['Institute']).sum()[variables].rename(columns={variables[0]: '2019-2020'})
    df_b = df_b.groupby(['Institute']).sum()[variables].rename(columns={variables[0]: '2016-2017'})
    merged = pd.concat([df_b, df_a], axis=1)
    merged['perc_change'] = (merged['2019-2020'] - merged['2016-2017']) / merged['2016-2017'] * 100
    merged = merged.rename(index={'FUNDACIÓN UNIVERSIDAD DE LAS AMÉRICAS, PUEBLA': 'UDLAP',
                                  'INSTITUTO TECNOLÓGICO Y DE ESTUDIOS SUPERIORES DE MONTERREY': 'ITESM',
                                  'UNIVERSIDAD ANÁHUAC': 'Anahuac', 'UNIVERSIDAD AUTÓNOMA DE DURANGO A.C.': 'UAD',
                                  'UNIVERSIDAD AUTÓNOMA DE GUADALAJARA': 'UAG',
                                  'UNIVERSIDAD DEL VALLE DE MÉXICO': 'UVM',
                                  'UNIVERSIDAD IBEROAMERICANA - CIUDAD DE MÉXICO': 'UIA',
                                  'UNIVERSIDAD PANAMERICANA': 'UP',
                                  'UNIVERSIDAD POPULAR AUTÓNOMA DEL ESTADO DE PUEBLA': 'UPAEP',
                                  'UNIVERSIDAD TECNOLÓGICA DE MÉXICO': 'UNITEC',
                                  'UNIVERSIDAD VIZCAYA DE LAS AMÉRICAS': 'UVA',
                                  'UNIVERSIDAD TECNOLÓGICA DE MÉXICO': 'UNITEC',
                                  'UNIVERSIDAD DEL VALLE DE MÉXICO': 'UVM',
                                  'INSTITUTO TECNOLÓGICO Y DE ESTUDIOS SUPERIORES DE MONTERREY': 'ITESM',
                                  'UNIVERSIDAD INTERAMERICANA PARA EL DESARROLLO': 'UNID',
                                  'ENSEÑANZA E INVESTIGACIÓN SUPERIOR, A.C.': 'EISAC',
                                  'UNIVERSIDAD TECNOLÓGICA LATINOAMERICANA EN LÍNEA': 'UTEL',
                                  'UNIVERSIDAD LATINOAMERICANA, S.C.': 'ULA',
                                  'INSTITUTO DE ESTUDIOS UNIVERSITARIOS, A.C.': 'IEU',
                                  'UNIVERSIDAD INSURGENTES': 'UNIV. INSURGENTES'})

    merged1 = merged.sort_values(by="2019-2020", ascending=False)
    merged2 = merged.sort_values(by="perc_change", ascending=False)

    from matplotlib.pyplot import figure
    figure(num=None, figsize=(16, 6))
    x1 = merged1.index
    y1 = merged1['2019-2020']
    x2 = merged2.index
    y2 = merged2['perc_change']
    # Draw first subplot using plt.subplot
    plt.subplot(1, 2, 1)
    plt.bar(x1, y1, color=['#464d77', '#464d77', '#ca3143', '#464d77', '#464d77'])
    plt.xlabel('Onsite institutions', fontsize=14)
    plt.ylabel('Total', fontsize=14)
    plt.title("Total first entry (2019-2020)", fontsize=17)
    plt.axhline(linewidth=1, color='black')
    # Draw second subplot using plt.subplot
    plt.subplot(1, 2, 2)
    plt.bar(x2, y2, color=['#464d77','#464d77','#464d77','#464d77','#464d77','#ca3143'])
    plt.xlabel('Onsite institutions', fontsize=14)
    plt.ylabel('Percentage', fontsize=14)
    plt.title("Change of first entry (2016-2017 vs 2019-2020)", fontsize=17)
    plt.axhline(linewidth=1, color='black')
    plt.savefig('./images/fig15.png')
    plt.show()

#/////////////////////////////
#           Graph 16
#/////////////////////////////
# Enrolled onsite
def graph16(dfs_all, final_onsite_competitors):
    variables = ['Enrollment_Total']
    df_a = dfs_all[(dfs_all['period'] == '2019-2020') & (dfs_all['modality'] == 'private-onsite') & (
        dfs_all['Institute'].isin(final_onsite_competitors))]
    df_b = dfs_all[(dfs_all['period'] == '2016-2017') & (dfs_all['modality'] == 'private-onsite') & (
        dfs_all['Institute'].isin(final_onsite_competitors))]
    df_a = df_a.groupby(['Institute']).sum()[variables].rename(columns={variables[0]: '2019-2020'})
    df_b = df_b.groupby(['Institute']).sum()[variables].rename(columns={variables[0]: '2016-2017'})
    merged = pd.concat([df_b, df_a], axis=1)
    merged['perc_change'] = (merged['2019-2020'] - merged['2016-2017']) / merged['2016-2017'] * 100
    merged = merged.rename(index={'FUNDACIÓN UNIVERSIDAD DE LAS AMÉRICAS, PUEBLA': 'UDLAP',
                                  'INSTITUTO TECNOLÓGICO Y DE ESTUDIOS SUPERIORES DE MONTERREY': 'ITESM',
                                  'UNIVERSIDAD ANÁHUAC': 'Anahuac', 'UNIVERSIDAD AUTÓNOMA DE DURANGO A.C.': 'UAD',
                                  'UNIVERSIDAD AUTÓNOMA DE GUADALAJARA': 'UAG',
                                  'UNIVERSIDAD DEL VALLE DE MÉXICO': 'UVM',
                                  'UNIVERSIDAD IBEROAMERICANA - CIUDAD DE MÉXICO': 'UIA',
                                  'UNIVERSIDAD PANAMERICANA': 'UP',
                                  'UNIVERSIDAD POPULAR AUTÓNOMA DEL ESTADO DE PUEBLA': 'UPAEP',
                                  'UNIVERSIDAD TECNOLÓGICA DE MÉXICO': 'UNITEC',
                                  'UNIVERSIDAD VIZCAYA DE LAS AMÉRICAS': 'UVA',
                                  'UNIVERSIDAD TECNOLÓGICA DE MÉXICO': 'UNITEC',
                                  'UNIVERSIDAD DEL VALLE DE MÉXICO': 'UVM',
                                  'INSTITUTO TECNOLÓGICO Y DE ESTUDIOS SUPERIORES DE MONTERREY': 'ITESM',
                                  'UNIVERSIDAD INTERAMERICANA PARA EL DESARROLLO': 'UNID',
                                  'ENSEÑANZA E INVESTIGACIÓN SUPERIOR, A.C.': 'EISAC',
                                  'UNIVERSIDAD TECNOLÓGICA LATINOAMERICANA EN LÍNEA': 'UTEL',
                                  'UNIVERSIDAD LATINOAMERICANA, S.C.': 'ULA',
                                  'INSTITUTO DE ESTUDIOS UNIVERSITARIOS, A.C.': 'IEU',
                                  'UNIVERSIDAD INSURGENTES': 'UNIV. INSURGENTES'})

    merged1 = merged.sort_values(by="2019-2020", ascending=False)
    merged2 = merged.sort_values(by="perc_change", ascending=False)

    from matplotlib.pyplot import figure
    figure(num=None, figsize=(16, 6))
    x1 = merged1.index
    y1 = merged1['2019-2020']
    x2 = merged2.index
    y2 = merged2['perc_change']
    # Draw first subplot using plt.subplot
    plt.subplot(1, 2, 1)
    plt.bar(x1, y1, color=['#464d77', '#ca3143', '#464d77', '#464d77', '#464d77'])
    plt.xlabel('Onsite institutions', fontsize=14)
    plt.ylabel('Total', fontsize=14)
    plt.title("Enrollment (2019-2020)", fontsize=17)
    plt.axhline(linewidth=1, color='black')
    # Draw second subplot using plt.subplot
    plt.subplot(1, 2, 2)
    plt.bar(x2, y2, color=['#464d77','#464d77','#464d77','#464d77','#464d77','#ca3143'])
    plt.xlabel('Onsite institutions', fontsize=14)
    plt.ylabel('Percentage', fontsize=14)
    plt.title("Change of enrollment (2016-2017 vs 2019-2020)", fontsize=17)
    plt.axhline(linewidth=1, color='black')
    plt.savefig('./images/fig16.png')
    plt.show()

#/////////////////////////////
#           Graph 17
#/////////////////////////////
# first entry online
def graph17(dfs_all, final_online_competitors):
    variables = ['First_Entry_Total']
    df_a = dfs_all[(dfs_all['period'] == '2019-2020') & (dfs_all['modality'] == 'private-online') & (
        dfs_all['Institute'].isin(final_online_competitors))]
    df_b = dfs_all[(dfs_all['period'] == '2016-2017') & (dfs_all['modality'] == 'private-online') & (
        dfs_all['Institute'].isin(final_online_competitors))]
    df_a = df_a.groupby(['Institute']).sum()[variables].rename(columns={variables[0]: '2019-2020'})
    df_b = df_b.groupby(['Institute']).sum()[variables].rename(columns={variables[0]: '2016-2017'})
    merged = pd.concat([df_b, df_a], axis=1)
    merged['perc_change'] = (merged['2019-2020'] - merged['2016-2017']) / merged['2016-2017'] * 100
    merged = merged.rename(index={'FUNDACIÓN UNIVERSIDAD DE LAS AMÉRICAS, PUEBLA': 'UDLAP',
                                  'INSTITUTO TECNOLÓGICO Y DE ESTUDIOS SUPERIORES DE MONTERREY': 'ITESM',
                                  'UNIVERSIDAD ANÁHUAC': 'Anahuac', 'UNIVERSIDAD AUTÓNOMA DE DURANGO A.C.': 'UAD',
                                  'UNIVERSIDAD AUTÓNOMA DE GUADALAJARA': 'UAG',
                                  'UNIVERSIDAD DEL VALLE DE MÉXICO': 'UVM',
                                  'UNIVERSIDAD IBEROAMERICANA - CIUDAD DE MÉXICO': 'UIA',
                                  'UNIVERSIDAD PANAMERICANA': 'UP',
                                  'UNIVERSIDAD POPULAR AUTÓNOMA DEL ESTADO DE PUEBLA': 'UPAEP',
                                  'UNIVERSIDAD TECNOLÓGICA DE MÉXICO': 'UNITEC',
                                  'UNIVERSIDAD VIZCAYA DE LAS AMÉRICAS': 'UVA',
                                  'UNIVERSIDAD TECNOLÓGICA DE MÉXICO': 'UNITEC',
                                  'UNIVERSIDAD DEL VALLE DE MÉXICO': 'UVM',
                                  'INSTITUTO TECNOLÓGICO Y DE ESTUDIOS SUPERIORES DE MONTERREY': 'ITESM',
                                  'UNIVERSIDAD INTERAMERICANA PARA EL DESARROLLO': 'UNID',
                                  'ENSEÑANZA E INVESTIGACIÓN SUPERIOR, A.C.': 'EISAC',
                                  'UNIVERSIDAD TECNOLÓGICA LATINOAMERICANA EN LÍNEA': 'UTEL',
                                  'UNIVERSIDAD LATINOAMERICANA, S.C.': 'ULA',
                                  'INSTITUTO DE ESTUDIOS UNIVERSITARIOS, A.C.': 'IEU',
                                  'UNIVERSIDAD INSURGENTES': 'UNIV. INSURGENTES'})

    merged1 = merged.sort_values(by="2019-2020", ascending=False)
    merged2 = merged.sort_values(by="perc_change", ascending=False)

    from matplotlib.pyplot import figure
    figure(num=None, figsize=(16, 6))
    x1 = merged1.index
    y1 = merged1['2019-2020']
    x2 = merged2.index
    y2 = merged2['perc_change']
    # Draw first subplot using plt.subplot
    plt.subplot(1, 2, 1)
    plt.bar(x1, y1, color=['#ca3143', '#464d77', '#464d77', '#464d77', '#464d77', '#464d77'])
    plt.xlabel('Online institutions', fontsize=14)
    plt.ylabel('Total', fontsize=14)
    plt.title("Total first entry (2019-2020)", fontsize=17)
    plt.axhline(linewidth=1, color='black')
    # Draw second subplot using plt.subplot
    plt.subplot(1, 2, 2)
    plt.bar(x2, y2, color=['#464d77', '#464d77', '#ca3143', '#464d77', '#464d77', '#464d77'])
    plt.xlabel('Online institutions', fontsize=14)
    plt.ylabel('Percentage', fontsize=14)
    plt.title("Change of first entry (2016-2017 vs 2019-2020)", fontsize=17)
    plt.axhline(linewidth=1, color='black')
    plt.savefig('./images/fig17.png')

#/////////////////////////////
#           Graph 18
#/////////////////////////////
# enrolled online
def graph18(dfs_all, final_online_competitors):
    variables = ['Enrollment_Total']
    df_a = dfs_all[(dfs_all['period'] == '2019-2020') & (dfs_all['modality'] == 'private-online') & (
        dfs_all['Institute'].isin(final_online_competitors))]
    df_b = dfs_all[(dfs_all['period'] == '2016-2017') & (dfs_all['modality'] == 'private-online') & (
        dfs_all['Institute'].isin(final_online_competitors))]
    df_a = df_a.groupby(['Institute']).sum()[variables].rename(columns={variables[0]: '2019-2020'})
    df_b = df_b.groupby(['Institute']).sum()[variables].rename(columns={variables[0]: '2016-2017'})
    merged = pd.concat([df_b, df_a], axis=1)
    merged['perc_change'] = (merged['2019-2020'] - merged['2016-2017']) / merged['2016-2017'] * 100
    merged = merged.rename(index={'FUNDACIÓN UNIVERSIDAD DE LAS AMÉRICAS, PUEBLA': 'UDLAP',
                                  'INSTITUTO TECNOLÓGICO Y DE ESTUDIOS SUPERIORES DE MONTERREY': 'ITESM',
                                  'UNIVERSIDAD ANÁHUAC': 'Anahuac', 'UNIVERSIDAD AUTÓNOMA DE DURANGO A.C.': 'UAD',
                                  'UNIVERSIDAD AUTÓNOMA DE GUADALAJARA': 'UAG',
                                  'UNIVERSIDAD DEL VALLE DE MÉXICO': 'UVM',
                                  'UNIVERSIDAD IBEROAMERICANA - CIUDAD DE MÉXICO': 'UIA',
                                  'UNIVERSIDAD PANAMERICANA': 'UP',
                                  'UNIVERSIDAD POPULAR AUTÓNOMA DEL ESTADO DE PUEBLA': 'UPAEP',
                                  'UNIVERSIDAD TECNOLÓGICA DE MÉXICO': 'UNITEC',
                                  'UNIVERSIDAD VIZCAYA DE LAS AMÉRICAS': 'UVA',
                                  'UNIVERSIDAD TECNOLÓGICA DE MÉXICO': 'UNITEC',
                                  'UNIVERSIDAD DEL VALLE DE MÉXICO': 'UVM',
                                  'INSTITUTO TECNOLÓGICO Y DE ESTUDIOS SUPERIORES DE MONTERREY': 'ITESM',
                                  'UNIVERSIDAD INTERAMERICANA PARA EL DESARROLLO': 'UNID',
                                  'ENSEÑANZA E INVESTIGACIÓN SUPERIOR, A.C.': 'EISAC',
                                  'UNIVERSIDAD TECNOLÓGICA LATINOAMERICANA EN LÍNEA': 'UTEL',
                                  'UNIVERSIDAD LATINOAMERICANA, S.C.': 'ULA',
                                  'INSTITUTO DE ESTUDIOS UNIVERSITARIOS, A.C.': 'IEU',
                                  'UNIVERSIDAD INSURGENTES': 'UNIV. INSURGENTES'})

    merged1 = merged.sort_values(by="2019-2020", ascending=False)
    merged2 = merged.sort_values(by="perc_change", ascending=False)

    from matplotlib.pyplot import figure
    figure(num=None, figsize=(16, 6))
    x1 = merged1.index
    y1 = merged1['2019-2020']
    x2 = merged2.index
    y2 = merged2['perc_change']
    # Draw first subplot using plt.subplot
    plt.subplot(1, 2, 1)
    plt.bar(x1, y1, color=['#464d77', '#464d77', '#ca3143', '#464d77', '#464d77', '#464d77'])
    plt.xlabel('Online institutions', fontsize=14)
    plt.ylabel('Total', fontsize=14)
    plt.title("Enrollment (2019-2020)", fontsize=17)
    plt.axhline(linewidth=1, color='black')
    # Draw second subplot using plt.subplot
    plt.subplot(1, 2, 2)
    plt.bar(x2, y2, color=['#464d77', '#464d77', '#464d77', '#ca3143', '#464d77', '#464d77'])
    plt.xlabel('Online institutions', fontsize=14)
    plt.ylabel('Percentage', fontsize=14)
    plt.title("Change of enrollment (2016-2017 vs 2019-2020)", fontsize=17)
    plt.axhline(linewidth=1, color='black')
    plt.savefig('./images/fig18.png')

