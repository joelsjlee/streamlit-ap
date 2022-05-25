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

st.set_page_config(layout="wide")



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

"Headline Variation in AP Wire Copy"

page = st.radio(
    "Select Date", ["Nazi Plan to Kill All Jews Confirmed: November 25th, 1942 A", 
    "Nazi Plan to Kill All Jews Confirmed: November 25th, 1942 B",
    "Allies Denounce Nazi Plan to 'Exterminate' the Jews: December 17th, 1942"], index=0
)

option = st.selectbox(
     'Page Number Filter',
     ('All', 'Only Front Page', 'Only Non Front Page'))

show_headline = st.checkbox('Always Display Headline', value=True)

class Entry:
    def __init__(self, l, h, p, n, c, s, u, pd, e):
        self.location = l
        self.headline = h
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
        entry = Entry([r["Latitude"], r["Longitude"]], r["Headline"], r["Page"], r["Newspaper"], r["City"], r["State"], r["Page URL"], r["Publication Date"], r["Event"])
        entries[(r["Latitude"], r["Longitude"])] = entry
        if r["Newspaper"] not in papers:
            new_paper = Newspaper(r["Newspaper"], [entry], r["City"], r["State"])
            papers[r["Newspaper"]] = new_paper
        else:
            papers[r["Newspaper"]].entries.append(entry)

populate("nov-25-a.csv", entries, papers)
populate("nov-25-b-offset.csv", entries, papers)
populate("dec-17-offset.csv", entries, papers)


# for i, r in pd.read_csv("nov-25-a.csv").iterrows():
#     entry = Entry([r["Latitude"], r["Longitude"]], r["Headline"], r["Page"], r["Newspaper"], r["City"], r["State"], r["Page URL"])
#     entries[(r["Latitude"], r["Longitude"])] = entry

def marker(m, filename):
    df = pd.read_csv(filename)
    for i, r in df.iterrows():
        tooltip = "<b>{}</b><br/>{}".format(r["Headline"], r['Sub Headline'])
        popup = "<a href='{}' target='_blank'>{}</a>".format(r['Page URL'], r['Page URL'])
        location = [r["Latitude"], r["Longitude"]]
        if show_headline:
            if option == "Only Front Page":
                if r["Page"] == "1":
                    m.add_marker(location, popup, folium.Tooltip(tooltip, permanent=True))
            if option == "Only Non Front Page":
                if r["Page"] != "1":
                    m.add_marker(location, popup, folium.Tooltip(tooltip, permanent=True))
            if option == "All":
                m.add_marker(location, popup, folium.Tooltip(tooltip, permanent=True))
        else:
            if option == "Only Front Page":
                if r["Page"] == "1":
                    m.add_marker(location, popup)
            if option == "Only Non Front Page":
                if r["Page"] != "1":
                    m.add_marker(location, popup)
            if option == "All":
                m.add_marker(location, popup)

m = leafmap.Map(location=[39, -95], zoom_start=5)
m.add_basemap("Esri.NatGeoWorldMap")
m.add_heatmap(
    "heats.csv",
    latitude="Latitude",
    longitude="Longitude",
    value="Jewish Population",
    name="Heat map",
    radius=20,
)

if page == "Nazi Plan to Kill All Jews Confirmed: November 25th, 1942 A":
    marker(m, "nov-25-a.csv")

if page == "Nazi Plan to Kill All Jews Confirmed: November 25th, 1942 B":
    marker(m, "nov-25-b-offset.csv")

if page == "Allies Denounce Nazi Plan to 'Exterminate' the Jews: December 17th, 1942":
    marker(m, "dec-17-offset.csv")

dct = st_folium(m, width=1300, height=600)


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
            st.write("Page Number: " + known_entry.pagenum)
            known_entry.url
            st.markdown("""---""") 
        
    else:
        st.write(" ")