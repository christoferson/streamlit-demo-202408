import streamlit as st
import time

# Custom CSS for enhanced styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .feature-card {
        background: linear-gradient(145deg, #f0f2f6, #ffffff);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .stats-container {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .cta-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 25px;
        text-decoration: none;
        display: inline-block;
        margin: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .hero-section {
        text-align: center;
        padding: 3rem 0;
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border-radius: 20px;
        margin-bottom: 3rem;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <h1 style="font-size: 3.5rem; margin-bottom: 1rem; color: #2c3e50;">
        🚀 Welcome to StreamLit Demo
    </h1>
    <p style="font-size: 1.3rem; color: #34495e; margin-bottom: 2rem;">
        Discover the power of interactive data applications with beautiful visualizations
    </p>
</div>
""", unsafe_allow_html=True)

# Main features showcase
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>📊 Interactive Charts</h3>
        <p>Beautiful data visualizations that respond to your input in real-time.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>🎨 Rich Components</h3>
        <p>Explore a wide variety of Streamlit components and styling options.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>⚡ Fast & Responsive</h3>
        <p>Lightning-fast performance with smooth user interactions.</p>
    </div>
    """, unsafe_allow_html=True)

# Stats section
st.markdown("---")
st.markdown("### 📈 App Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🎯 Components",
        value="25+",
        delta="5 new this month"
    )

with col2:
    st.metric(
        label="📊 Charts",
        value="10+",
        delta="Interactive"
    )

with col3:
    st.metric(
        label="🎨 Themes",
        value="Custom",
        delta="Beautiful"
    )

with col4:
    st.metric(
        label="⚡ Performance",
        value="Fast",
        delta="Optimized"
    )

# Interactive demo section
st.markdown("---")
st.markdown("### 🎮 Quick Demo")

# Add some interactive elements for the landing page
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Try it out!")
    name = st.text_input("What's your name?", placeholder="Enter your name...")
    if name:
        st.success(f"Hello {name}! 👋 Welcome to our demo app!")
        st.balloons()

with col2:
    st.markdown("#### Choose your experience")
    experience = st.selectbox(
        "What interests you most?",
        ["Data Visualization", "Interactive Components", "Custom Styling", "All of the above!"]
    )
    
    if experience:
        if experience == "Data Visualization":
            st.info("📊 Check out Page 2 for amazing charts!")
        elif experience == "Interactive Components":
            st.info("🎛️ Page 1 has tons of interactive widgets!")
        elif experience == "Custom Styling":
            st.info("🎨 This landing page shows custom CSS styling!")
        else:
            st.info("🌟 Explore all pages to see everything!")

# Call to action
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem;">
    <h3>Ready to explore?</h3>
    <p>Navigate through the pages using the sidebar to discover all features!</p>
</div>
""", unsafe_allow_html=True)

# Footer with animated elements
if st.button("🎉 Show Celebration", type="primary"):
    st.balloons()
    st.success("Thanks for visiting our demo app! 🚀")
    time.sleep(1)
    st.snow()