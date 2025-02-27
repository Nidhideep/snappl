import streamlit as st
from utils.image_processor import analyze_card_image
from utils.data_generator import generate_card_data

def display_card_analysis(uploaded_file):
    """
    Display the analysis results for an uploaded card image.
    """
    if uploaded_file is None:
        return
    
    with st.spinner('Analyzing card image...'):
        # Process the uploaded image
        analysis_result = analyze_card_image(uploaded_file)
        
        if not analysis_result['success']:
            st.error(f"Error analyzing image: {analysis_result['error']}")
            return
            
        analysis_data = analysis_result['data']
        
        # Display analysis results
        st.subheader("Card Analysis Results")
        
        # Create columns for layout
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Display the uploaded image
            st.image(uploaded_file, caption="Uploaded Card", use_column_width=True)
        
        with col2:
            # Display extracted information
            st.markdown("### Detected Information")
            st.write(f"Card Name: {analysis_data['card_name']}")
            
            with st.expander("Raw Text Content"):
                for line in analysis_data['text_content']:
                    st.write(line)
        
        # Market Analysis Section
        st.markdown("### Market Analysis")
        
        # Generate sample market data for the detected card
        similar_cards = generate_card_data(5)  # Get 5 similar cards
        
        # Display similar cards in the market
        st.markdown("#### Similar Cards in Market")
        for _, card in similar_cards.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.write(f"**{card['name']}** ({card['condition']})")
                with col2:
                    st.write(f"${card['price']:,.2f}")
                with col3:
                    st.write(f"Trend: {card['market_trend']}")
