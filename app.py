# import streamlit as st
# import leafmap

# m = leafmap.Map(locate_control=True, plugin_LatLngPopup=False)
# m.add_basemap("Esri.NatGeoWorldMap")
# m.to_streamlit(10000,1000)


import streamlit as st
from streamlit_folium import folium_static, st_folium
import folium
import pandas as pd
from datetime import datetime
import leafmap.foliumap as leafmap
import math

st.set_page_config(layout="wide")

a_text = """
Details of a campaign which Dr. Stephen Wise said was planned to exterminate all Jews in Nazi-occupied Europe by the end of the year are to be laid before a committee of leading Jewish organizations today in New York.

The story which Dr. Wise says was reportedly confirmed by the state department and a personal representative of President Roosevelt–deals with how more than 2,000,000 Jews already have been slaughtered in accordance with a race extinction order by Adolf Hitler.

Before leaving for New York to address the committee this afternoon, Dr. Stephen S. Wise, chairman of he World Jewish congress and president of the American Jewish congress, said he caried official documentary proof that "Hitler has ordered the extermination of all Jews in Nazi-ruled Europe in 1942." After a consultation with state department officials, he announced they had termed authentic certain sources which revealed that approximately half of the estimated 4,000,000 Jews in Nazi-occupied Europe already have been killed and that Hitler was wrathful at "failure to complete the extermination immediately."

To speed the slaughter of the other half during the remaining month before the edict's deadline, Dr. Wise said the Nazis were moving some four-fifths of the Jews in Hitler-ruled European countries to Poland. There, he said Nazi doctors were killing them at the rate of "more than 100 men an hour, per doctor," by injecting air bubbles into their veins "the simplest and cheapest method" they could find.

Dr. Wise, who heads the committee, asserted that already the Jewish population of Warsaw had been reduced from 500,000 to about 100,000.

(The Polish government in exile reported in London yesterday that Heinrich Himmler, Nazi Gestapo chief, had ordered the extermination of one-half of the Jewish population of Poland by the end of this year and that 250,000 had been killed through September under the program. Only 40,000 Jews skilled workers in the German war industry are to remain in the Warsaw Ghetto, the government said)

In addition to the state department which he said had provided the documentary proof of previous rumors and reports, the chairman said a "representative of President Roosevelt, recently returned from Europe," had confirmed other stories and told him that "the worst you thought is true."

Whether details of the gruesome campaign will be revealed publicly will be decided by the committee, Dr. Wise, said, adding that any contemplated action will be announced after today's meeting.
"""

b_text = """

Dr. Stephen S. Wise, chairman of the World Jewish Congress, said tonight that he had learned through sources confirmed by the State Department that approximately half the estimated 4,000,000 Jews in Nazi-occupied Europe had been slain in an "extermination campaign."

Dr. Wise, who also is president of the American Jewish Congress, said these sources also disclosed:

1. That Adolf Hitler has ordered the extermination of all Jews in Nazi ruled Europe in 1942.

2. That the Jewish population of Warsaw, Poland, already has been reduced from 500,000 to about 100,000.

3. That when chief Nazis speak of "exterminating" Jews in Poland, they speak of "four-fifths of the Jewish population in Hitler-ruled Europe," since that percentage either now is in Poland or enroute there under a Nazi grouping plan.

4. That Nazis have established a price of 50 Reichsmarks for each corpse mostly Jewish, Dr. Wise indicated and are reclaiming bodies of slain civilians to be "processed into such war vital commodities as soap fats and fertilizer."

“He (Hitler) is even exhuming the dead for the value of the corpses” Dr. Wise said during a press conference shortly after he had conferred with state department officials.

He stressed the fact that most of his information came from various sources other than the State Department, but said those sources had been confirmed as authentic by the department. Dr. Wise attributed the Hitler-ian campaign to "a last desperate effort one of his last mad acts before he is destroyed, or called to his judgment."

In addition, he quoted a “representative of President Roosevelt recently returned from Europe” as saying that the “worst you (Dr. Wise) have thought is true”

Dr. Wise attributed the Hitlerian campaign toward elimination of all European Jewry this year to "a last desperate effort one of his last mad acts before he is destroyed, or called to this judgment."
"""

d_text = """
The United States has joined other United Nations governments in condemning Germany's “bestial policy of cold-blooded extermination" of the Jews and in pledging those responsible "shall not escape retribution." 

In announcing the move the state department said reports from Europe indicate German authorities, passing beyond the stage of ordinary persecution "are carrying into effect Hitler’s oft repeated intention to exterminate the Jewish people in Europe." 

The announcement described Poland is “the principal Nazi slaughter house” where ghettos established by the Germans are being systematically emptied of all Jews except a few skilled workers valuable to the war industries. 

“None of those taken away are ever heard of again. The able-bodied are slowly worked to death in labor camps. The infirm are left to die of exposure and starvation or are deliberately massacred in mass executions. The number of victims of these bloody cruelties is reckoned in the many hundreds of thousands of entirely innocent men, women and children," the announcement said. 

Associated with the United States in the joint action are the Belgian Czechoslovak Greek, Luxembourg, Netherlands, Norwegian, Polish, Soviet, United Kingdom and Yugoslav governments and the French National (Fighting French) Committee. 

Attention recently was called to the German extermination campaign by Rabbi Stephen M. Wise who charged the Germans not only systematically slaughtered Jews but utilized the corpses in the manufacture of soaps, fats and other products.

"""


# def _max_width_(prcnt_width:int = 75):
#     max_width_str = "padding-left: 0rem; padding-right: 0rem;"
#     st.markdown(f""" 
#                 <style> 
#                 .leaflet-container.leaflet-touch.leaflet-fade-anim.leaflet-grab.leaflet-touch-drag.leaflet-touch-zoom{{{max_width_str}}}
#                 </style>    
#                 """, 
#                 unsafe_allow_html=True,
#     )

# _max_width_()

st.title("Headline Variation in AP Wire Copy")

page = st.radio(
    "Select Date", ["Nazi Plan to Kill All Jews Confirmed: November 25th, 1942 A", 
    "Nazi Plan to Kill All Jews Confirmed: November 25th, 1942 B",
    "Allies Denounce Nazi Plan to 'Exterminate' the Jews: December 17th, 1942"], index=0
)

# option = st.selectbox(
#      'Page Number Filter',
#      ('All', 'Only Front Page', 'Only Non Front Page'))

show_headline = st.checkbox('Always Display Headline', value=True)

class Entry:
    def __init__(self, l, h, sh, p, n, c, s, u, pd, e):
        self.location = l
        self.headline = h
        self.subheading = sh
        self.pagenum = p
        self.newspaper = n
        self.city = c
        self.state = s
        self.url = u
        self.pubdate = pd
        self.event = e

class Newspaper:
    def __init__(self, n, e, c, s):
        self.name = n
        self.entries = e
        self.city = c
        self.state = s




# listofEntries = [Entry([r["Latitude"], r["Longitude"]], r["Headline"]) for i, r in pd.read_csv("nov-25-a.csv")]

entries = {}
papers = {}

def populate(filename, entries, papers):
    for i, r in pd.read_csv(filename).iterrows():
        entry = Entry([r["Latitude"], r["Longitude"]], r["Headline"], r["Sub Headline"], r["Page"], r["Newspaper"], r["City"], r["State"], r["Page URL"], r["Publication Date"], r["Event"])
        entries[(r["Latitude"], r["Longitude"])] = entry
        if r["Newspaper"] not in papers:
            new_paper = Newspaper(r["Newspaper"], [entry], r["City"], r["State"])
            papers[r["Newspaper"]] = new_paper
        else:
            papers[r["Newspaper"]].entries.append(entry)

populate("nov-25-a.csv", entries, papers)
populate("nov-25-b-offset.csv", entries, papers)
populate("dec-17-final-offset.csv", entries, papers)


# for i, r in pd.read_csv("nov-25-a.csv").iterrows():
#     entry = Entry([r["Latitude"], r["Longitude"]], r["Headline"], r["Page"], r["Newspaper"], r["City"], r["State"], r["Page URL"])
#     entries[(r["Latitude"], r["Longitude"])] = entry

def marker(m, filename, article):
    df = pd.read_csv(filename)
    for i, r in df.iterrows():
        if type(r['Sub Headline']) == str:
            tooltip = "<b>{}</b><br/>{}".format(r["Headline"], r['Sub Headline'])
        elif math.isnan(r['Sub Headline']):
            tooltip = "<b>{}</b>".format(r["Headline"])
        if show_headline:
            popup = "<a href='{}' target='_blank'>{}</a>".format(r['Page URL'], r['Page URL'])
        else:
            if type(r['Sub Headline']) == str:
                popup = "<b>{}</b><br/>{}<br/><a href='{}' target='_blank'>{}</a>".format(r["Headline"], r["Sub Headline"], r['Page URL'], r['Page URL'])
            elif math.isnan(r['Sub Headline']):
                popup = "<b>{}</b><br/><a href='{}' target='_blank'>{}</a>".format(r["Headline"], r['Page URL'], r['Page URL'])
        location = [r["Latitude"], r["Longitude"]]
        # if show_headline:
        #     if option == "Only Front Page":
        #         if r["Page"] == "1":
        #             m.add_marker(location, popup, folium.Tooltip(tooltip, permanent=True))
        #     if option == "Only Non Front Page":
        #         if r["Page"] != "1":
        #             m.add_marker(location, popup, folium.Tooltip(tooltip, permanent=True))
        #     if option == "All":
        #         m.add_marker(location, popup, folium.Tooltip(tooltip, permanent=True))
        # else:
        #     if option == "Only Front Page":
        #         if r["Page"] == "1":
        #             m.add_marker(location, popup)
        #     if option == "Only Non Front Page":
        #         if r["Page"] != "1":
        #             m.add_marker(location, popup)
        #     if option == "All":
        #         m.add_marker(location, popup)
        if article == "A":
            if option == "Wise":
                if show_headline:
                    if r["Wise"] == 1:
                        m.add_marker(location, popup, folium.Tooltip(tooltip, permanent=True))
                    else:
                        m.add_marker(location, popup, folium.Tooltip(tooltip, permanent=True), icon=folium.Icon(color="red", icon="info-sign"))
                else:
                    if r["Wise"] == 1:
                        m.add_marker(location, popup)
                    else:
                        m.add_marker(location, popup, icon=folium.Icon(color="red", icon="info-sign"))
            elif option == "Policy/Discussion":
                if show_headline:
                    if r["Discussion"] == 1:
                        m.add_marker(location, popup, folium.Tooltip(tooltip, permanent=True))
                    else:
                        m.add_marker(location, popup, folium.Tooltip(tooltip, permanent=True), icon=folium.Icon(color="red", icon="info-sign"))
                else:
                    if r["Discussion"] == 1:
                        m.add_marker(location, popup)
                    else:
                        m.add_marker(location, popup, icon=folium.Icon(color="red", icon="info-sign"))
            else:
                if show_headline:
                    m.add_marker(location, popup, folium.Tooltip(tooltip, permanent=True))
                else:
                    m.add_marker(location, popup)
        elif article == "B":
            if option == "Wise":
                if show_headline:
                    if r["Wise"] == 1:
                        m.add_marker(location, popup, folium.Tooltip(tooltip, permanent=True))
                    else:
                        m.add_marker(location, popup, folium.Tooltip(tooltip, permanent=True), icon=folium.Icon(color="red", icon="info-sign"))
                else:
                    if r["Wise"] == 1:
                        m.add_marker(location, popup)
                    else:
                        m.add_marker(location, popup, icon=folium.Icon(color="red", icon="info-sign"))
            elif option == "Shocking the Reader":
                if show_headline:
                    if r["Soap_Corpse"] == 1:
                        m.add_marker(location, popup, folium.Tooltip(tooltip, permanent=True))
                    else:
                        m.add_marker(location, popup, folium.Tooltip(tooltip, permanent=True), icon=folium.Icon(color="red", icon="info-sign"))
                else:
                    if r["Soap_Corpse"] == 1:
                        m.add_marker(location, popup)
                    else:
                        m.add_marker(location, popup, icon=folium.Icon(color="red", icon="info-sign"))
            elif option == "Perpetrators":
                if show_headline:
                    if r["Mention Perpatrator"] == 1:
                        m.add_marker(location, popup, folium.Tooltip(tooltip, permanent=True))
                    else:
                        m.add_marker(location, popup, folium.Tooltip(tooltip, permanent=True), icon=folium.Icon(color="red", icon="info-sign"))
                else:
                    if r["Mention Perpatrator"] == 1:
                        m.add_marker(location, popup)
                    else:
                        m.add_marker(location, popup, icon=folium.Icon(color="red", icon="info-sign"))
            else:
                if show_headline:
                    m.add_marker(location, popup, folium.Tooltip(tooltip, permanent=True))
                else:
                    m.add_marker(location, popup)
        elif article == "D":
            if option == "Perpetrators":
                if show_headline:
                    if r["Perpetrator"] == "y":
                        m.add_marker(location, popup, folium.Tooltip(tooltip, permanent=True))
                    else:
                        m.add_marker(location, popup, folium.Tooltip(tooltip, permanent=True), icon=folium.Icon(color="red", icon="info-sign"))
                else:
                    if r["Perpetrator"] == "y":
                        m.add_marker(location, popup)
                    else:
                        m.add_marker(location, popup, icon=folium.Icon(color="red", icon="info-sign"))
            elif option == "Policy":
                if show_headline:
                    if r["Policy"] == "y":
                        m.add_marker(location, popup, folium.Tooltip(tooltip, permanent=True))
                    else:
                        m.add_marker(location, popup, folium.Tooltip(tooltip, permanent=True), icon=folium.Icon(color="red", icon="info-sign"))
                else:
                    if r["Policy"] == "y":
                        m.add_marker(location, popup)
                    else:
                        m.add_marker(location, popup, icon=folium.Icon(color="red", icon="info-sign"))
            else:
                if show_headline:
                    m.add_marker(location, popup, folium.Tooltip(tooltip, permanent=True))
                else:
                    m.add_marker(location, popup)



        # if show_headline:
        #     m.add_marker(location, popup, folium.Tooltip(tooltip, permanent=True))
        # else:
        #     m.add_marker(location, popup, icon=folium.Icon(color="red", icon="info-sign"))


heat_option = st.selectbox(
        'Heatmap',
        ('Jewish Population', 'Percentage of Total Population that is Jewish'))

if heat_option == "Jewish Population":
    val = "Jewish Population"
elif heat_option == "Percentage of Total Population that is Jewish":
    val = "Percentage"

m = leafmap.Map(location=[39, -95], zoom_start=5)
m.add_basemap("Esri.NatGeoWorldMap")
m.add_heatmap(
    "heats.csv",
    latitude="Latitude",
    longitude="Longitude",
    value=val,
    name="Heat map",
    radius=20,
)

if page == "Nazi Plan to Kill All Jews Confirmed: November 25th, 1942 A":
    option = st.selectbox(
        'Clusters',
        ('None', 'Wise', 'Policy/Discussion'))
    if option == "Wise":
        st.write("Blue denotes that Wise is mentioned in the heading or subheading. Red denotes that Wise is not mentioned")
    elif option == "Policy/Discussion":
        st.write("Blue denotes that terms like 'policy' or 'discussion' are used, or that the focus is primarily on Jews as the audience receiving the news. Red denotes that they are not used.")
    marker(m, "nov-25-a.csv", "A")
    

if page == "Nazi Plan to Kill All Jews Confirmed: November 25th, 1942 B":
    option = st.selectbox(
        'Clusters',
        ('None', 'Wise', 'Shocking the Reader', 'Perpetrators'))
    if option == "Wise":
        st.write("Blue denotes that Wise is mentioned in the heading or subheading. Red denotes that Wise is not mentioned")
    elif option == "Shocking the Reader":
        st.write("Blue denotes it's use, Red denotes that it is not mentioned.")
    elif option == "Perpetrators":
        st.write("Blue denotes that the perpetrators are included in the headline. Red denotes that they are not.")
    marker(m, "nov-25-b-offset.csv", "B")

if page == "Allies Denounce Nazi Plan to 'Exterminate' the Jews: December 17th, 1942":
    option = st.selectbox(
        'Clusters',
        ('None', 'Perpetrators', 'Policy'))
    if option == "Perpetrators":
        st.write("Blue denotes that the perpetrators are included in the headline. Red denotes that they are not.")
    elif option == "Policy":
        st.write("Blue denotes that 'policy' is used. Red denotes that it is not")
    marker(m, "dec-17-final-offset.csv", "D")

dct = st_folium(m, width=1300, height=600)
st.subheader("Wire Story:")
if page == "Nazi Plan to Kill All Jews Confirmed: November 25th, 1942 A":
    st.write(a_text)
elif page == "Nazi Plan to Kill All Jews Confirmed: November 25th, 1942 B":
    st.write(b_text)
elif page == "Allies Denounce Nazi Plan to 'Exterminate' the Jews: December 17th, 1942":
    st.write(d_text)

with st.sidebar:
    if dct["last_object_clicked"] is not None:
        entry = entries[(dct["last_object_clicked"]["lat"], dct["last_object_clicked"]["lng"])]
        sel_paper = papers[entry.newspaper]
        st.header("Newspaper: " + sel_paper.name)
        st.write("Location: " + sel_paper.city + ", " + sel_paper.state)
        st.subheader("Known Events:")
        for known_entry in sel_paper.entries:
            st.write("Event: " + known_entry.event)
            st.write("Publication Date: " + known_entry.pubdate)
            st.write("Headline: " + known_entry.headline)
            if type(known_entry.subheading) == str:
                st.write("Subheading: " + known_entry.subheading)
            elif not math.isnan(known_entry.subheading):
                st.write("Subheading: " + known_entry.subheading)
            st.write("Page Number: " + str(known_entry.pagenum))
            known_entry.url
            st.markdown("""---""") 
        
    else:
        st.write(" ")