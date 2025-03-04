import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# Streamlit page config
st.set_page_config(
    page_title="CharmCard 🌸✨",
    page_icon="🌸",
    layout="centered"
)

# Custom CSS for UI Enhancement
st.markdown(
    """
    <style>
    body { background-color: #D8BFD8 !important; }
    .stApp { background-color: #D8BFD8; color: #000000 !important; }
    .stTextInput input, .stSelectbox select { background-color: #FFFFFF !important; color: #000000 !important; }
    .stButton button, .stDownloadButton button {
        background-color: #9370DB !important; color: white !important;
        border-radius: 12px; font-size: 18px; transition: 0.3s;
    }
    .stButton button:hover, .stDownloadButton button:hover { background-color: #7A67EE !important; }
    .stTextInput label, .stSelectbox label { color: #000000 !important; font-weight: bold; }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to wrap text
def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + " " + word if current_line else word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        line_width = bbox[2] - bbox[0]

        if line_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines

# Function to draw wrapped text with center alignment
def draw_wrapped_text(draw, text, font, image_width, y, max_width, line_spacing=10, fill="black"):
    lines = wrap_text(draw, text, font, max_width)
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (image_width - text_width) // 2  # Center alignment
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + line_spacing

# Function to create the greeting card
def create_greeting_card(name, occasion):
    backgrounds = {
        "Eid": "eid_background.jpg",
        "Friendship": "friendship_background.jpg",
        "Birthday": "birthday_background.jpg",
        "New Year": "newyear_background.jpg",
        "Teacher's Day": "teachersday_background.jpg",
    }

    messages = {
        "Eid": {
            "greeting": "Eid Mubarak!",
            "quote": """May this Eid bring endless joy, peace, and countless blessings to you and your loved ones. 
            
Taqabbal Allahu minna wa minkum. May your prayers be accepted, your heart be filled with faith, and your home be filled with happiness. 

May this sacred occasion strengthen our bonds, purify our hearts, and bring light to our souls. Wishing you a joyous and spiritually uplifting Eid!"""
        },
        "Friendship": {
            "greeting": "Happy Friendship Day!",
            "quote": """A true friend is the greatest blessing of life. 

Thank you for being my source of strength, laughter, and endless memories. May our bond grow stronger with time, and may life always keep us close at heart. 

Here's to cherished moments and lifelong friendship!"""
        },
        "Birthday": {
            "greeting": "Happy Birthday!",
            "quote": """On this special day, I wish you boundless joy, endless success, and all the happiness your heart desires. 

May your journey ahead be filled with love, laughter, and unforgettable moments. May this year bring new adventures and dreams come true! 

Enjoy your day to the fullest!"""
        },
        "New Year": {
            "greeting": "Happy New Year!",
            "quote": """As we welcome a new year, may it bring you success, happiness, and peace. 

Let go of the past, embrace the present, and step into the future with hope and excitement. May each day be filled with new opportunities and beautiful moments. 

Wishing you a bright and prosperous year ahead!"""
        },
        "Teacher's Day": {
            "greeting": "Happy Teacher’s Day!",
            "quote": """A teacher is a guide, a mentor, and a source of inspiration. 

Your wisdom, patience, and dedication shape the future of many. Thank you for believing in your students and making a difference in their lives. 

Your impact lasts a lifetime. You are truly appreciated!"""
        }
    }

    if occasion not in backgrounds:
        st.error("Background image for this occasion is missing.")
        return None

    background_image = Image.open(backgrounds[occasion])
    width, height = background_image.size
    draw = ImageDraw.Draw(background_image)

    # Load fonts with fallback
    try:
        greeting_font = ImageFont.truetype("times.ttf", 80)  # Large font for greeting
        quote_font = ImageFont.truetype("times.ttf", 40)  # Smaller font for quote
    except:
        st.error("Font not available. Please check your font files.")
        return None

    greeting = messages[occasion]["greeting"]
    quote = messages[occasion]["quote"]
    signature = f"Regards, {name}"

    # Define margins
    max_text_width = width - 400  # Keeping margin

    # Draw greeting text
    y_greeting = height // 4
    draw_wrapped_text(draw, greeting, greeting_font, width, y_greeting, max_text_width)

    # Draw quote text and calculate its height
    y_quote = y_greeting + greeting_font.size + 50  # Add some spacing after greeting
    quote_lines = wrap_text(draw, quote, quote_font, max_text_width)
    for line in quote_lines:
        bbox = draw.textbbox((0, 0), line, font=quote_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2  # Center alignment
        draw.text((x, y_quote), line, font=quote_font, fill="black")
        y_quote += quote_font.size + 5  # Add line spacing

    # Draw signature text after the quote
    y_signature = y_quote + 50  # Add some spacing after the quote
    draw_wrapped_text(draw, signature, quote_font, width, y_signature, max_text_width, line_spacing=5, fill="darkblue")

    return background_image

# Streamlit app
def main():
    st.title("CharmCard 🌸")
    st.subheader("Make your greetings extra magical! 💖")
    st.write(
        "With **CharmCard**, you can personalize cute greeting cards by adding your **name** "
        "and downloading them instantly! 🏠💖 Perfect for birthdays, anniversaries, Eid, or "
        "just sending a little love! 💌💫\n\nSpread joy with a touch of **charm**! 🌸✨"
    )

    st.subheader("Pick a special occasion and create your own personalized greeting card! 🏠💌✨")

    occasion = st.selectbox(
        "Select an Occasion:",
        ["Eid", "Friendship", "Birthday", "New Year", "Teacher's Day"]
    )
    name = st.text_input("Enter your name:")

    if name:
        greeting_card = create_greeting_card(name, occasion)

        if greeting_card:
            st.image(greeting_card, caption=f"Your {occasion} Greeting Card 🎉", use_container_width=True)
            greeting_card.save("greeting_card.png")
            with open("greeting_card.png", "rb") as file:
                st.download_button(
                    label=f"💾 Download Your {occasion} Card",
                    data=file,
                    file_name=f"{occasion.lower()}_greeting_card.png",
                    mime="image/png"
                )

if __name__ == "__main__":
    main()