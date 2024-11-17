import streamlit as st
from PIL import Image
import pandas as pd
import glob

# Define functions for each page
def home_page():
    st.title("Home Page")
    st.write("Welcome!")

def image_processing_page():
    st.title("Tag selection")

    # Upload an image
    uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    
    if uploaded_image is not None:
        # Open the image with PIL
        image = Image.open(uploaded_image)

        # Display the uploaded image
        
        st.image(image, caption="Uploaded Image", use_container_width=True)

        # Process the image
        result = process_image(image)
        st.write("Result:")
        st.write(result)

def select_tags_page():
    st.title("Tag selection")
    # Sample CSV loading
    # Replace 'your_file.csv' with your actual file path
    # Example CSV structure:
    # Name,Tag
    # Alice,Python
    # Bob,Data Science
    # Charlie,Machine Learning

    # Load the CSV file

    #uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    #uploaded_file = pd.read_csv("attribute_data.csv")
    uploaded_file = "attribute_data.csv"

    if uploaded_file is not None:
        # Read the CSV into a DataFrame
        df = pd.read_csv(uploaded_file)

        #st.write("### Uploaded Data")
        #st.dataframe(df)

        # Extract unique tags
        unique_tags = df['attribute_name'].unique()

        # Tag selection
        selected_tags = st.multiselect("Select tags to filter by", unique_tags)
        if selected_tags:
            filtered_df = df[df['attribute_name'].isin(selected_tags)]
            unique_tags_filt = filtered_df['des_value'].unique()
            selected_tags_filt = st.multiselect("Filter by secondary tags", unique_tags_filt)

            if selected_tags_filt:
                col1, col2 = st.columns(2)
                filtered_df_filt = filtered_df[filtered_df['des_value'].isin(selected_tags_filt)]
                first_column_vector = filtered_df_filt.iloc[:, 0].tolist()

                # Initialize display range
                if "display_range" not in st.session_state:
                    st.session_state.display_range = 10

                # Display images
                for i in range(min(st.session_state.display_range, len(first_column_vector))):
                    if i%2==0:
                        with col1:
                            imatges = glob.glob(f'images/{first_column_vector[i]}*')
                            if len(imatges) > 0:
                                st.image(imatges[0], use_container_width=True)
                            #else:
                                #st.warning(f"No image found for: {first_column_vector[i]}")
                    else:
                        with col2:
                            imatges = glob.glob(f'images/{first_column_vector[i]}*')
                            if len(imatges) > 0:
                                st.image(imatges[0], use_container_width=True)
                            #else:
                                #st.warning(f"No image found for: {first_column_vector[i]}")

                # Load more button
                if st.session_state.display_range<len(first_column_vector):
                    if st.button("Load more"):
                        st.session_state.display_range += 10
            else:
                st.write("Select secondary tags to see filtered results.")
        else:
            st.write("Select primary tags to see filtered results.")

def about_page():
    st.title("about page")
    st.title("Multiple Buttons Example")

    #if st.button("Say Hello"):
    #    st.write("Hello there!")

    #if st.button("Say Goodbye"):
    #    st.write("Goodbye!")
# Example image processing function
def process_image(image):
    # Example logic: Count the number of pixels (placeholder)
    width, height = image.size
    return f"The image has dimensions: {width}x{height} pixels."

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Image Processing", "About","Tag selection"])


# Display the selected page
if page == "Home":
    home_page()
elif page == "Image Processing":
    image_processing_page()
elif page == "About":
    about_page()
elif page == "Tag selection":
    select_tags_page()
