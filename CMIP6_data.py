import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import xarray as xr
import numpy as np
import hvplot.xarray
import hvplot
import holoviews as hv
# In[2]:

st.set_page_config(
     #page_title="CMIP6 climate variables",
     #layout="wide",
     initial_sidebar_state="expanded",
)

st.sidebar.title('CMIP6 climate variables')

st.sidebar.markdown('**Welcome to the CMIP6 climate variables interactive guide! Below, you can select whether you want to see all the available variables, filter them or see a NetCDF file example:**')
tabletype = st.sidebar.radio('', ['All CMIP6 variables', 'Filter variables', 'Interactive map'])


dict1 = pd.read_excel('CMIP6_MIP_tables.xlsx', sheet_name = None)

@st.cache
def load_data():
    df = pd.concat(dict1.values(), ignore_index=True)
    return df[['Long name', 'units', 'description', 'comment', 'Variable Name', 'CF Standard Name', 'dimensions', 'modeling_realm', 'frequency']]
    
data = load_data()


if tabletype == 'All CMIP6 variables':
	st.title('All CMIP6 variables')
	st.dataframe(data)
	col1, col2 = st.beta_columns(2)	
	with col1:
		fig1= plt.figure(figsize=(5, 4))
		sns.countplot(y=data['modeling_realm'])
		st.pyplot(fig1)
	
	with col2:
		fig2= plt.figure(figsize=(5, 4))
		sns.countplot(y=data['frequency'])
		st.pyplot(fig2)

elif tabletype == 'Filter variables':
	st.title('Filter variables')	
	st.sidebar.markdown('Please use the 3 available filters to confine your search. Barplots will 	  start appearing and at the end you will see the filtered table.')
	
	realm = st.multiselect('Realm', data['modeling_realm'].unique())
	f_data = data[(data['modeling_realm'].isin(realm))]
	
	freq = st.multiselect('Frequency', f_data['frequency'].unique())
	f_data2 = f_data[(f_data['frequency'].isin(freq))]
	
	dim = st.multiselect('Dimensions', f_data2['dimensions'].unique())
	f_data3 = f_data2[(f_data2['dimensions'].isin(dim))]
	
	col3, col4 = st.beta_columns(2)
	with col3:
		fig3= plt.figure(figsize = (6, len(f_data['dimensions'].unique())*0.2))
		sns.countplot(y=f_data['frequency'])
		st.pyplot(fig3)
	
	with col4:
		fig4= plt.figure(figsize = (5, len(f_data2['dimensions'].unique())*0.5))
		sns.countplot(y=f_data2['dimensions'])
		st.pyplot(fig4)
	
	st.subheader('Filtered data')
	st.write('You have ') 	
	st.write(len(f_data3))
	st.write('variables!')
	st.table(f_data3)
	
else:
	st.title('Interactive map')
	st.sidebar.markdown('Feel free to play around with the interactive plots (move the slider, zoom in / zoom out, select an area) in order to get a feeling of the time scales and spatio-temporal resolution of the CMIP6 variables. In this specific example, only the monthly averages of 1 variable were used, with a spatial resolution of 1x1 degree')
	@st.cache(hash_funcs={xr.core.dataset.Dataset: id},  allow_output_mutation=True)
	def load_data2():
		dset = xr.open_dataset('decade_thetao2000_regridded_short.nc')
		return dset
    
	data2 = load_data2()

	f_time = st.slider('Month', 1, 60, 1)
	st.subheader(data2.time.values[f_time-1])
	
	fig5 = plt.figure(figsize=(8, 0.1))
	plot5 = data2.thetaot2000.isel(time=f_time-1).hvplot(clim=(-2, 35), cmap='viridis')
	st.bokeh_chart(hv.render(plot5, backend='bokeh'))
	st.pyplot(fig5)
	st.markdown('**Fig.1: Global map of Depth Average Potential Temperature of Upper 2000m  monthly averages, according to the EC-Earth3 model for the years 1852 to 1856**')
	
	st.markdown("---")
	
	fig6 = plt.figure(figsize=(8, 0.1))
	plot6 = data2.thetaot2000.mean(dim='lon').T.hvplot()
	st.bokeh_chart(hv.render(plot6, backend='bokeh'))
	st.pyplot(fig6)
	st.markdown('**Fig.2: Zonal means of Depth Average Potential Temperature of Upper 2000m  monthly averages, according to the EC-Earth3 model for the years 1852 to 1856**')
	
	st.markdown("---")
	
	col5, col6 = st.beta_columns(2)
	with col5:
		f_lon = st.slider('Longitude', -180, 180, 1) 
	with col6:
		f_lat = st.slider('Latitude', -90, 90, 1)
	fig7 = plt.figure(figsize=(8, 0.1))
	plot7 = data2.thetaot2000.sel(lon=f_lon, lat=f_lat).T.hvplot()
	st.bokeh_chart(hv.render(plot7, backend='bokeh'))
	st.pyplot(fig7)
	st.markdown('**Fig.3: Depth Average Potential Temperature of Upper 2000m  monthly averages, according to the EC-Earth3 model for the years 1852 to 1856 for gricell with coordinates (lon, lat):**')
	st.write(data2.lon.values[f_lon+180]); st.write(data2.lat.values[f_lat+90])

	st.markdown('---')
	
	with st.beta_expander("NetCDF file structure"):
		st.write(data2)
		
	with st.beta_expander("NetCDF file contents"):
		st.write(data2.variables)


