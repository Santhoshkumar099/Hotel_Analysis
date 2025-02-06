import pandas as pd
import streamlit as st
import plotly.express as px
from matplotlib import pyplot as plt
from streamlit_option_menu import option_menu

# Load the CSV file
df = pd.read_csv("airbnbproject.csv")

def main():
    # Sidebar Menu
    with st.sidebar:
        selected = option_menu("Menu", ["🗺 Search","📊Insights"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#FF5A5F"},
                        "nav-link-selected": {"background-color": "#FF5A5F"}})

    # Search Section
    if selected == "🗺 Search":
        # Filters
        st.sidebar.header("Please Filter")
        region = st.sidebar.multiselect(
            "Select Country",
            options=df["Country"].unique().tolist()
        )
        Location = st.sidebar.multiselect(
            "Select Location",
            options=df["Market"].unique().tolist()
        )

        # Filter DataFrame
        df_selection = df.query(
            "Country == @region & Market == @Location"
        )

        # Average Rating Calculation
        try:
            a = df_selection["Rating"]/10
            average_rating = round(a.mean(), 1)
            star_rating = ":star:" * int(round(average_rating, 0))

            c1, c2 = st.columns(2)
            with c1:
                st.subheader("Average Rating")
                st.subheader(f"{average_rating} {star_rating}")
        except:
            st.write("Select the correct Location")

        # Top 10 Hotels Pie Chart
        a = df_selection[['Name', 'Rating', 'Prize']]
        sorted_value = a.sort_values(by=['Rating', 'Name'], ascending=[False, True])
        filtered_value = sorted_value.head(10)

        fig = px.pie(filtered_value, values='Rating',
                     names='Name',
                     title='Top 10 Hotels',
                     color_discrete_sequence=px.colors.sequential.Agsunset,
                     hover_data=['Prize'],
                     labels={'Prize':'Prize'})

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

        # Hotel Details Selection
        try:
            selected_hotel = st.selectbox("Select the Hotel", options=df_selection['Name'].tolist(), index=None)
            
            filtered_df = df[df['Name'] == selected_hotel]
            c1, c2 = st.columns(2)

            with c1:
                st.subheader(f"Details of {selected_hotel}")
                st.image(filtered_df['Images'].values[0], caption=filtered_df['Name'].values[0], width=300)
                st.write(f"**Price:** ${filtered_df['Prize'].values[0]}")
                st.write(f"**:green[Listing URL]:** {filtered_df['Url'].values[0]}")
                st.write(f"**:green[Description]:** {filtered_df['Description'].values[0]}")
                st.write(f"**:green[Room Type]:** {filtered_df['Room_type'].values[0]}")
                st.write(f"**:green[Bed Type]:** {filtered_df['Room_type'].values[0]}")
                st.write(f"**:green[Bedrooms]:** {filtered_df['Bedrooms'].values[0]}")
                st.write(f"**:green[Beds]:** {filtered_df['Beds'].values[0]}")
                
            with c2:
                st.write("")
                st.write("")
                st.write(f"**:green[Neighborhood overview]:** {filtered_df['Neighborhood_overview'].values[0]}")
                st.write(f"**:green[House Rules]:** {filtered_df['House_rules'].values[0]}")
                st.write(f"**:green[Property Type]:** {filtered_df['Property_type'].values[0]}")   
                st.write(f"**:green[Amenities]:** {filtered_df['Amenities'].values[0]}")               
                st.write(f"**:green[Minimum Nights]:** {filtered_df['Min_nights'].values[0]}") 
                st.write(f"**:green[Maximum Nights]:** {filtered_df['Max_nights'].values[0]}") 
                
            # Host Details
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("Host Details")
                st.write(f"**Host Name:** {filtered_df['Host_name'].values[0]}")
                st.image(filtered_df['Host_pic_url'].values[0], caption=filtered_df['Host_name'].values[0])
                st.write(f"**Host ID:** {filtered_df['Host_id'].values[0]}")
                st.write(f"**Host URL:** {filtered_df['Host_url'].values[0]}")
                st.write(f"**Host Location:** {filtered_df['Host_location'].values[0]}")
                st.write(f"**About Host:** {filtered_df['Host_about'].values[0]}")
                st.write(f"**Host Response:** {filtered_df['Host_response'].values[0]}")

        except:
            st.write(f"<span style='color:#FF0000'>Please select the hotel name</span>", unsafe_allow_html=True)

    # Insights Section
    if selected == "📊Insights":
        opt = [
            'Top 10 Hotels with Highest Price',
            'Top 10 Hotels with Lowest Price',
            'Price Based on Host Neighbourhood',
            'Average price on Host Neighbourhood',
            'Top 10 Countries with the Most Listings'
        ]
        
        question = st.selectbox(':red[Select the question]', options=opt, index=None)

        # Top 10 Highest Price Hotels
        if question == opt[0]:
            sorted_df = df.sort_values(by='Prize', ascending=False)
            aa = sorted_df.head(10)
            aa = aa[['Name', 'Country', 'Prize']]

            # Sunburst Chart
            fig = px.sunburst(aa, 
                            path=['Country', 'Name'], 
                            values='Prize', 
                            title='Top 10 Most Expensive Accommodations',
                            color_continuous_scale='RdBu',
                            hover_data=['Prize'],
                            labels={'Country': 'Country', 'Name': 'Name', 'Prize': 'Prize'})
            st.plotly_chart(fig)

            # Pie Chart
            fig = px.pie(aa, 
                        values='Prize', 
                        names='Name', 
                        title='Top 10 Most Expensive Accommodations',
                        hover_data=['Country', 'Prize'],
                        labels={'Name': 'Hotel', 'Country': 'Country', 'Prize': 'Prize'})
            st.plotly_chart(fig)

        # Top 10 Lowest Price Hotels
        elif question == opt[1]:
            sorted_df = df.sort_values(by='Prize', ascending=True)
            aa = sorted_df.head(10)
            aa = aa[['Name', 'Country', 'Prize']]

            # Sunburst Chart
            fig = px.sunburst(aa, 
                            path=['Country', 'Name'], 
                            values='Prize', 
                            title='Top 10 Least Expensive Accommodations',
                            color_continuous_scale='RdBu',
                            hover_data=['Prize'],
                            labels={'Country': 'Country', 'Name': 'Name', 'Prize': 'Prize'})
            st.plotly_chart(fig)

            # Pie Chart
            fig = px.pie(aa, 
                        values='Prize', 
                        names='Name', 
                        title='Top 10 Least Expensive Accommodations',
                        hover_data=['Country', 'Prize'],
                        labels={'Name': 'Hotel', 'Country': 'Country', 'Prize': 'Prize'})
            st.plotly_chart(fig)

        # Price Based on Host Neighbourhood
        elif question == opt[2]:
            c_t = df["Country"].unique()[0]
            df_c_t = df[df["Country"] == c_t]
            df_c_t_sorted = df_c_t.sort_values(by="Prize")
            df_p_n = pd.DataFrame(df_c_t_sorted.groupby("Host_neighbour")["Prize"].agg(["sum", "mean"])).reset_index()
            df_p_n.columns = ["Host_neighbourhood", "Total_price", "Average_price"]
            
            fig = px.bar(df_p_n, 
                         x="Total_price", 
                         y="Host_neighbourhood", 
                         orientation='h',
                         title="PRICE BASED ON HOST_NEIGHBOURHOOD", 
                         width=600, height=800)
            st.plotly_chart(fig)

        # Average Price on Host Neighbourhood
        elif question == opt[3]:
            c_t = df["Country"].unique()[0]
            df_c_t = df[df["Country"] == c_t]
            df_c_t_sorted = df_c_t.sort_values(by="Prize")
            df_p_n = pd.DataFrame(df_c_t_sorted.groupby("Host_neighbour")["Prize"].agg(["sum", "mean"])).reset_index()
            df_p_n.columns = ["Host_neighbourhood", "Total_price", "Average_price"]

            fig = px.bar(df_p_n, 
                         x="Average_price", 
                         y="Host_neighbourhood", 
                         orientation='h',
                         title="AVERAGE PRICE BASED ON HOST_NEIGHBOURHOOD", 
                         width=600, height=800)
            st.plotly_chart(fig)
        
        # Top 10 Countries with Most Listings
        elif question == opt[4]:
            country_listings_count = df['Country'].value_counts()
            top_10_countries = country_listings_count.head(10)

            st.title('Top 10 Countries with the Most Listings')

            fig, ax = plt.subplots(figsize=(10,6))
            top_10_countries.plot(kind='bar', ax=ax)
            plt.xlabel('Country')
            plt.ylabel('Number of Listings')
            plt.title('Top 10 Countries by Airbnb Listings')
            plt.xticks(rotation=45)
            plt.tight_layout()

            st.pyplot(fig)

if __name__ == "__main__":
    main()
