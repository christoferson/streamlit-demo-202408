import streamlit as st
import pandas as pd
import numpy as np
import time
import random
from datetime import datetime, timedelta
import json

# Custom CSS for the creative playground
st.markdown("""
<style>
    .playground-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .creative-card {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border: 2px solid transparent;
        background-clip: padding-box;
        position: relative;
    }
    
    .creative-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: 15px;
        padding: 2px;
        background: linear-gradient(45deg, #667eea, #764ba2, #f093fb);
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: exclude;
        z-index: -1;
    }
    
    .game-score {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    
    .magic-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 25px;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .rainbow-text {
        background: linear-gradient(45deg, #ff0000, #ff7f00, #ffff00, #00ff00, #0000ff, #4b0082, #9400d3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: bold;
        font-size: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Page header
st.markdown("""
<div class="playground-header">
    <h1>🎨 Creative Playground</h1>
    <p>Interactive experiments, games, and creative tools!</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for playground controls
st.sidebar.markdown("# 🎮 Playground Controls")
playground_mode = st.sidebar.selectbox(
    "Choose your adventure:",
    ["🎯 Number Guessing Game", "🎨 Color Palette Generator", "📊 Data Art Creator", 
     "🎵 Mood Music Matcher", "🔮 Fortune Teller", "🧮 Calculator Playground"]
)

# Initialize session state
if 'game_score' not in st.session_state:
    st.session_state.game_score = 0
if 'secret_number' not in st.session_state:
    st.session_state.secret_number = random.randint(1, 100)
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'fortune_count' not in st.session_state:
    st.session_state.fortune_count = 0

# 🎯 Number Guessing Game
if playground_mode == "🎯 Number Guessing Game":
    st.markdown("### 🎯 Guess the Secret Number!")
    st.markdown("I'm thinking of a number between 1 and 100. Can you guess it?")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        guess = st.number_input("Your guess:", min_value=1, max_value=100, value=50)
        
        if st.button("🎲 Make Guess", type="primary"):
            st.session_state.attempts += 1
            
            if guess == st.session_state.secret_number:
                st.success(f"🎉 Congratulations! You guessed it in {st.session_state.attempts} attempts!")
                st.balloons()
                st.session_state.game_score += max(10 - st.session_state.attempts, 1)
                # Reset game
                st.session_state.secret_number = random.randint(1, 100)
                st.session_state.attempts = 0
            elif guess < st.session_state.secret_number:
                st.info("📈 Too low! Try a higher number.")
            else:
                st.info("📉 Too high! Try a lower number.")
    
    with col2:
        st.markdown(f"""
        <div class="game-score">
            🏆 Score: {st.session_state.game_score}<br>
            🎯 Attempts: {st.session_state.attempts}
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 New Game"):
            st.session_state.secret_number = random.randint(1, 100)
            st.session_state.attempts = 0

# 🎨 Color Palette Generator
elif playground_mode == "🎨 Color Palette Generator":
    st.markdown("### 🎨 Dynamic Color Palette Generator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        palette_style = st.selectbox("Palette Style:", 
                                   ["Warm", "Cool", "Vibrant", "Pastel", "Monochrome", "Random"])
        num_colors = st.slider("Number of colors:", 3, 10, 5)
    
    with col2:
        if st.button("🎨 Generate New Palette", type="primary"):
            st.session_state.current_palette = True
    
    # Generate colors based on style
    def generate_palette(style, count):
        colors = []
        if style == "Warm":
            base_hues = [0, 30, 60]  # Reds, oranges, yellows
        elif style == "Cool":
            base_hues = [180, 210, 240]  # Blues, cyans, purples
        elif style == "Vibrant":
            base_hues = [0, 60, 120, 180, 240, 300]
        elif style == "Pastel":
            base_hues = [0, 60, 120, 180, 240, 300]
        elif style == "Monochrome":
            base_hues = [220]  # Blue monochrome
        else:  # Random
            base_hues = list(range(0, 360, 30))
        
        for i in range(count):
            if style == "Pastel":
                hue = random.choice(base_hues)
                color = f"hsl({hue}, 60%, 80%)"
            elif style == "Monochrome":
                lightness = 20 + (i * 60 // count)
                color = f"hsl(220, 50%, {lightness}%)"
            else:
                hue = random.choice(base_hues) + random.randint(-20, 20)
                saturation = random.randint(60, 90)
                lightness = random.randint(40, 70)
                color = f"hsl({hue}, {saturation}%, {lightness}%)"
            colors.append(color)
        return colors
    
    # Display palette
    colors = generate_palette(palette_style, num_colors)
    
    cols = st.columns(num_colors)
    for i, color in enumerate(colors):
        with cols[i]:
            st.markdown(f"""
            <div style="background: {color}; height: 100px; border-radius: 10px; 
                        display: flex; align-items: center; justify-content: center;
                        color: white; font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">
                Color {i+1}
            </div>
            """, unsafe_allow_html=True)
            st.code(color, language="css")

# 📊 Data Art Creator
elif playground_mode == "📊 Data Art Creator":
    st.markdown("### 📊 Turn Data into Art!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        art_type = st.selectbox("Art Style:", ["Sine Wave Art", "Random Walk", "Spiral Pattern", "Fractal-like"])
        complexity = st.slider("Complexity:", 10, 200, 50)
        color_scheme = st.selectbox("Color Scheme:", ["Rainbow", "Ocean", "Sunset", "Forest"])
    
    with col2:
        if st.button("🎨 Create Art", type="primary"):
            # Generate artistic data
            if art_type == "Sine Wave Art":
                x = np.linspace(0, 4*np.pi, complexity)
                y1 = np.sin(x) * np.cos(x/2)
                y2 = np.cos(x) * np.sin(x/3)
                y3 = np.sin(x*2) * 0.5
                
                art_data = pd.DataFrame({
                    'x': x,
                    'Wave 1': y1,
                    'Wave 2': y2,
                    'Wave 3': y3
                })
                st.line_chart(art_data.set_index('x'))
                
            elif art_type == "Random Walk":
                steps = np.random.randn(complexity).cumsum()
                steps2 = np.random.randn(complexity).cumsum()
                
                walk_data = pd.DataFrame({
                    'Step': range(complexity),
                    'Walk 1': steps,
                    'Walk 2': steps2
                })
                st.line_chart(walk_data.set_index('Step'))
                
            elif art_type == "Spiral Pattern":
                t = np.linspace(0, 4*np.pi, complexity)
                r = t
                x = r * np.cos(t)
                y = r * np.sin(t)
                
                spiral_data = pd.DataFrame({'X': x, 'Y': y})
                st.scatter_chart(spiral_data, x='X', y='Y')
                
            else:  # Fractal-like
                x = np.random.randn(complexity)
                y = np.random.randn(complexity)
                
                # Apply some fractal-like transformations
                for _ in range(3):
                    x = x + 0.1 * np.sin(y)
                    y = y + 0.1 * np.cos(x)
                
                fractal_data = pd.DataFrame({'X': x, 'Y': y})
                st.scatter_chart(fractal_data, x='X', y='Y')

# 🎵 Mood Music Matcher
elif playground_mode == "🎵 Mood Music Matcher":
    st.markdown("### 🎵 What's Your Musical Mood?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        energy = st.slider("Energy Level:", 0, 100, 50)
        happiness = st.slider("Happiness Level:", 0, 100, 50)
        focus = st.slider("Need for Focus:", 0, 100, 50)
    
    with col2:
        time_of_day = st.selectbox("Time of Day:", ["Morning", "Afternoon", "Evening", "Night"])
        activity = st.selectbox("Current Activity:", ["Working", "Relaxing", "Exercising", "Studying", "Partying"])
    
    if st.button("🎵 Find My Music", type="primary"):
        # Music recommendation logic
        if energy > 70 and happiness > 60:
            mood = "Energetic & Happy"
            genres = ["Pop", "Dance", "Rock", "Hip-Hop"]
            emoji = "🎉"
        elif energy < 30 and focus > 60:
            mood = "Calm & Focused"
            genres = ["Classical", "Ambient", "Lo-fi", "Instrumental"]
            emoji = "🧘"
        elif happiness < 40:
            mood = "Melancholic"
            genres = ["Blues", "Indie", "Alternative", "Acoustic"]
            emoji = "🌧️"
        elif energy > 60 and activity == "Exercising":
            mood = "Workout Mode"
            genres = ["Electronic", "Rock", "Hip-Hop", "Pump-up"]
            emoji = "💪"
        else:
            mood = "Balanced"
            genres = ["Indie Pop", "Alternative", "Folk", "Jazz"]
            emoji = "😌"
        
        st.success(f"{emoji} Your mood: **{mood}**")
        st.info(f"🎶 Recommended genres: {', '.join(genres)}")
        
        # Create a mood visualization
        mood_data = pd.DataFrame({
            'Aspect': ['Energy', 'Happiness', 'Focus'],
            'Level': [energy, happiness, focus]
        })
        st.bar_chart(mood_data.set_index('Aspect'))

# 🔮 Fortune Teller
elif playground_mode == "🔮 Fortune Teller":
    st.markdown("### 🔮 Digital Crystal Ball")
    
    fortunes = [
        "🌟 A brilliant idea will come to you this week!",
        "💰 Financial opportunities are heading your way!",
        "❤️ Love and friendship will flourish around you!",
        "🚀 Your next project will exceed all expectations!",
        "🌈 A colorful adventure awaits you soon!",
        "📚 Knowledge gained today will prove invaluable tomorrow!",
        "🎯 Your focus and determination will pay off!",
        "🌸 Beauty and joy will surround you this month!",
        "⚡ Your energy and enthusiasm will inspire others!",
        "🎨 Your creativity will unlock new possibilities!"
    ]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("Ask the crystal ball a question and discover your fortune!")
        question = st.text_input("What would you like to know?", placeholder="Ask anything...")
        
        if st.button("🔮 Reveal My Fortune", type="primary") and question:
            st.session_state.fortune_count += 1
            fortune = random.choice(fortunes)
            
            # Add some mystical delay
            with st.spinner("🔮 Consulting the crystal ball..."):
                time.sleep(2)
            
            st.markdown(f"""
            <div class="rainbow-text">
                {fortune}
            </div>
            """, unsafe_allow_html=True)
            
            st.balloons()
    
    with col2:
        st.markdown(f"""
        <div class="game-score">
            🔮 Fortunes Revealed<br>
            {st.session_state.fortune_count}
        </div>
        """, unsafe_allow_html=True)

# 🧮 Calculator Playground
else:  # Calculator Playground
    st.markdown("### 🧮 Advanced Calculator Playground")
    
    calc_mode = st.selectbox("Calculator Mode:", 
                           ["Basic Math", "Scientific", "Unit Converter", "Tip Calculator"])
    
    if calc_mode == "Basic Math":
        col1, col2, col3 = st.columns(3)
        
        with col1:
            num1 = st.number_input("First number:", value=0.0)
        with col2:
            operation = st.selectbox("Operation:", ["+", "-", "×", "÷", "^"])
        with col3:
            num2 = st.number_input("Second number:", value=0.0)
        
        if st.button("Calculate", type="primary"):
            if operation == "+":
                result = num1 + num2
            elif operation == "-":
                result = num1 - num2
            elif operation == "×":
                result = num1 * num2
            elif operation == "÷":
                result = num1 / num2 if num2 != 0 else "Cannot divide by zero!"
            else:  # ^
                result = num1 ** num2
            
            st.success(f"Result: **{result}**")
    
    elif calc_mode == "Unit Converter":
        col1, col2 = st.columns(2)
        
        with col1:
            value = st.number_input("Value to convert:", value=1.0)
            from_unit = st.selectbox("From:", ["Celsius", "Fahrenheit", "Meters", "Feet", "Kilograms", "Pounds"])
        
        with col2:
            to_unit = st.selectbox("To:", ["Fahrenheit", "Celsius", "Feet", "Meters", "Pounds", "Kilograms"])
        
        if st.button("Convert", type="primary"):
            # Temperature conversions
            if from_unit == "Celsius" and to_unit == "Fahrenheit":
                result = (value * 9/5) + 32
            elif from_unit == "Fahrenheit" and to_unit == "Celsius":
                result = (value - 32) * 5/9
            # Length conversions
            elif from_unit == "Meters" and to_unit == "Feet":
                result = value * 3.28084
            elif from_unit == "Feet" and to_unit == "Meters":
                result = value / 3.28084
            # Weight conversions
            elif from_unit == "Kilograms" and to_unit == "Pounds":
                result = value * 2.20462
            elif from_unit == "Pounds" and to_unit == "Kilograms":
                result = value / 2.20462
            else:
                result = "Invalid conversion"
            
            st.success(f"{value} {from_unit} = **{result:.2f}** {to_unit}")
    
    else:  # Tip Calculator
        col1, col2 = st.columns(2)
        
        with col1:
            bill_amount = st.number_input("Bill amount ($):", value=50.0, min_value=0.0)
            tip_percent = st.slider("Tip percentage:", 0, 30, 18)
        
        with col2:
            people = st.number_input("Number of people:", value=1, min_value=1)
        
        if bill_amount > 0:
            tip_amount = bill_amount * (tip_percent / 100)
            total_amount = bill_amount + tip_amount
            per_person = total_amount / people
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Tip Amount", f"${tip_amount:.2f}")
            with col2:
                st.metric("Total Amount", f"${total_amount:.2f}")
            with col3:
                st.metric("Per Person", f"${per_person:.2f}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem;">
    <p>🎨 <strong>Creative Playground</strong> - Where data meets imagination!</p>
    <p>Try different modes and discover new interactive experiences!</p>
</div>
""", unsafe_allow_html=True)