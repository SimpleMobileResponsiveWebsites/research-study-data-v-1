import streamlit as st
import pandas as pd
import plotly.express as px

# App title and introduction
st.title("Research Study Data Explorer")
st.write("Upload your dataset to explore, analyze, and visualize.")

# Step 1: Data Upload
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file is not None:
    # Load data into a DataFrame
    df = pd.read_csv(uploaded_file)
    st.write("Data successfully loaded!")
    
    # Display basic information about the dataset
    st.subheader("Data Overview")
    st.write("**Shape of the dataset:**", df.shape)
    st.write("**Column names:**", list(df.columns))
    
    if st.checkbox("Show raw data"):
        st.write(df)
    
    # Step 2: Data Exploration
    st.subheader("Column Analysis")
    
    column = st.selectbox("Select a column to view unique values and summary statistics", df.columns)
    if column:
        st.write("Unique values:", df[column].unique())
        if pd.api.types.is_numeric_dtype(df[column]):
            st.write("Summary statistics:")
            st.write(df[column].describe())
    
    # Step 3: Filtering and Sorting
    st.subheader("Filter and Sort Data")
    
    # Filtering by numerical column
    numeric_columns = df.select_dtypes(include=["float64", "int64"]).columns
    if len(numeric_columns) > 0:
        selected_column = st.selectbox("Select a column to filter by", numeric_columns)
        min_value, max_value = df[selected_column].min(), df[selected_column].max()
        filter_values = st.slider(f"Select range of values for {selected_column}", min_value, max_value, (min_value, max_value))
        filtered_df = df[(df[selected_column] >= filter_values[0]) & (df[selected_column] <= filter_values[1])]
    else:
        filtered_df = df.copy()
    
    # Sorting
    sort_column = st.selectbox("Select a column to sort by", df.columns)
    sort_order = st.radio("Order", ["Ascending", "Descending"])
    filtered_df = filtered_df.sort_values(by=sort_column, ascending=(sort_order == "Ascending"))
    
    st.write("Filtered and Sorted Data:")
    st.write(filtered_df)
    
    # Step 4: Visualization
    st.subheader("Data Visualization")
    chart_type = st.selectbox("Select Chart Type", ["Scatter Plot", "Histogram", "Box Plot"])
    
    if chart_type == "Scatter Plot":
        x_axis = st.selectbox("Select X-axis", df.columns)
        y_axis = st.selectbox("Select Y-axis", df.columns)
        scatter_plot = px.scatter(filtered_df, x=x_axis, y=y_axis)
        st.plotly_chart(scatter_plot)
    
    elif chart_type == "Histogram":
        hist_column = st.selectbox("Select column for Histogram", df.columns)
        histogram = px.histogram(filtered_df, x=hist_column)
        st.plotly_chart(histogram)
    
    elif chart_type == "Box Plot":
        box_column = st.selectbox("Select column for Box Plot", df.columns)
        box_plot = px.box(filtered_df, y=box_column)
        st.plotly_chart(box_plot)
    
    # Step 5: Download Filtered Data
    st.subheader("Download Filtered Data")
    @st.cache_data
    def convert_df(df):
        return df.to_csv(index=False).encode("utf-8")
    
    csv = convert_df(filtered_df)
    st.download_button("Download Filtered Data as CSV", csv, "filtered_data.csv", "text/csv", key="download-csv")
else:
    st.write("Please upload a CSV file to start.")

