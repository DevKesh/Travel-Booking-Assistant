import random
from datetime import datetime, timedelta

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


class MultilingualTravelAssistant:
    def __init__(self):
        self.responses = {
            "greet": {
                "english": "Hello! I am your travel assistant. I can help you book trips. Where would you like to go?",
                "tamil": "வணக்கம்! நான் உங்கள் பயண உதவியாளர். நான் பயணங்களை பதிவு செய்ய உதவ முடியும். நீங்கள் எங்கு செல்ல விரும்புகிறீர்கள்?",
                "kannada": "ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ ಪ್ರಯಾಣ ಸಹಾಯಕ. ನಾನು ಪ್ರಯಾಣಗಳನ್ನು ಬುಕ್ ಮಾಡಲು ಸಹಾಯ ಮಾಡಬಲ್ಲೆ. ನೀವು ಎಲ್ಲಿಗೆ ಹೋಗಲು ಬಯಸುತ್ತೀರಿ?"
            },
            "ask_destination": {
                "english": "Which destination would you like to visit?",
                "tamil": "எந்த இடத்தை பார்க்க விரும்புகிறீர்கள்?",
                "kannada": "ಎಲ್ಲಿಗೆ ಭೇಟಿ ನೀಡಲು ಬಯಸುತ್ತೀರಿ?"
            },
            "ask_people": {
                "english": "How many people will be traveling?",
                "tamil": "எத்தனை பேர் பயணம் செய்கிறார்கள்?",
                "kannada": "ಎಷ್ಟು ಜನ ಪ್ರಯಾಣಿಸುತ್ತಾರೆ?"
            },
            "ask_date": {
                "english": "When would you like to travel?",
                "tamil": "நீங்கள் எப்போது பயணிக்க விரும்புகிறீர்கள்?",
                "kannada": "ನೀವು ಯಾವಾಗ ಪ್ರಯಾಣಿಸಲು ಬಯಸುತ್ತೀರಿ?"
            },
            "ask_duration": {
                "english": "How many days would you like to stay?",
                "tamil": "எத்தனை நாட்கள் தங்க விரும்புகிறீர்கள்?",
                "kannada": "ಎಷ್ಟು ದಿನಗಳು ಉಳಿಯಲು ಬಯಸುತ್ತೀರಿ?"
            },
            "confirm_booking": {
                "english": "Let me confirm your booking. Destination: {destination}. People: {people}. Date: {date}. Duration: {duration} days. Is this correct?",
                "tamil": "உங்கள் முன்பதிவை உறுதிப்படுத்துகிறேன். இலக்கு: {destination}. நபர்கள்: {people}. தேதி: {date}. காலம்: {duration} நாட்கள். இது சரியானதா?",
                "kannada": "ನಿಮ್ಮ ಬುಕಿಂಗ್ ಅನ್ನು ದೃಢಪಡಿಸುತ್ತೇನೆ. ಗಮ್ಯಸ್ಥಾನ: {destination}. ಜನರು: {people}. ದಿನಾಂಕ: {date}. ಅವಧಿ: {duration} ದಿನಗಳು. ಇದು ಸರಿಯಾಗಿದೆಯೇ?"
            },
            "booking_confirmed": {
                "english": "Booking confirmed. Your trip to {destination} is booked. Booking ID: {booking_id}. Travelers: {people}. Check in: {date}. Duration: {duration} days. Total: {price}. Thank you for booking.",
                "tamil": "முன்பதிவு உறுதிப்படுத்தப்பட்டது. உங்கள் {destination} பயணம் பதிவு செய்யப்பட்டது. முன்பதிவு ஐடி: {booking_id}. பயணிகள்: {people}. சேக இன்: {date}. காலம்: {duration} நாட்கள். மொத்தம்: {price}. முன்பதிவு செய்ததற்கு நன்றி.",
                "kannada": "ಬುಕಿಂಗ್ ದೃಢಪಡಿಸಲಾಗಿದೆ. ನಿಮ್ಮ {destination} ಪ್ರಯಾಣ ಬುಕ್ ಆಗಿದೆ. ಬುಕಿಂಗ್ ಐಡಿ: {booking_id}. ಪ್ರಯಾಣಿಕರು: {people}. ಚೆಕ್ ಇನ್: {date}. ಅವಧಿ: {duration} ದಿನಗಳು. ಒಟ್ಟು: {price}. ಬುಕ್ ಮಾಡಿದ್ದಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು."
            },
            "booking_cancelled": {
                "english": "Let's start over. Where would you like to go?",
                "tamil": "மீண்டும் தொடங்குவோம். நீங்கள் எங்கு செல்ல விரும்புகிறீர்கள்?",
                "kannada": "ಮತ್ತೆ ಪ್ರಾರಂಭಿಸೋಣ. ನೀವು ಎಲ್ಲಿಗೆ ಹೋಗಲು ಬಯಸುತ್ತೀರಿ?"
            },
            "help_booking": {
                "english": "I can help you book a trip. Tell me where you want to go, how many people, when, and for how many days.",
                "tamil": "நான் ஒரு பயணத்தை பதிவு செய்ய உதவ முடியும். நீங்கள் எங்கு செல்ல விரும்புகிறீர்கள், எத்தனை பேர், எப்போது, எத்தனை நாட்கள் என்று சொல்லுங்கள்.",
                "kannada": "ನಾನು ಪ್ರಯಾಣವನ್ನು ಬುಕ್ ಮಾಡಲು ಸಹಾಯ ಮಾಡಬಲ್ಲೆ. ನೀವು ಎಲ್ಲಿಗೆ ಹೋಗಲು ಬಯಸುತ್ತೀರಿ, ಎಷ್ಟು ಜನ, ಯಾವಾಗ, ಎಷ್ಟು ದಿನಗಳು ಎಂದು ಹೇಳಿ."
            }
        }

        self.destinations = ["goa", "kerala", "mysore", "ooty", "coorg"]
        self.booking_states = {}
        self.prices = {
            "goa": 2000,
            "kerala": 2500,
            "mysore": 1500,
            "ooty": 1800,
            "coorg": 1700
        }

    def detect_language(self, text):
        text_lower = text.lower()

        # Strict Tamil detection - only respond in Tamil if clear Tamil input
        tamil_keywords = ['vanakkam', 'por', 'pannanum', 'yathrai', 'enga', 'evvalavu',
                          'edhu', 'nandri', 'romba', 'nalla', 'poganum', 'varalaam',
                          'seri', 'aamaam', 'illai', 'naal', 'vaaram', 'per', 'hotel',
                          'யாத்திரை', 'எங்க', 'எவ்வளவு', 'நன்றி', 'ரொம்ப', 'நல்ல', 'போகணும்']

        # Strict Kannada detection - only respond in Kannada if clear Kannada input
        kannada_keywords = ['namaskara', 'ge', 'madu', 'yelli', 'estu', 'yava',
                            'dhanyavada', 'tumba', 'chennagide', 'hogalu', 'banni',
                            'hogi', 'olliya', 'houdu', 'illa', 'dina', 'vara', 'jana',
                            'ಹೋಗಿ', 'ಮಾಡು', 'ಯಲ್ಲಿ', 'ಎಷ್ಟು', 'ಯಾವ', 'ಧನ್ಯವಾದ', 'ತುಂಬ', 'ಚೆನ್ನಾಗಿದೆ']

        # Count matches for each language
        tamil_matches = sum(1 for keyword in tamil_keywords if keyword in text_lower)
        kannada_matches = sum(1 for keyword in kannada_keywords if keyword in text_lower)

        # Only switch if there are multiple clear indicators
        if tamil_matches >= 2:  # Need at least 2 Tamil words
            return "tamil"
        elif kannada_matches >= 2:  # Need at least 2 Kannada words
            return "kannada"
        else:
            return "english"

    def generate_booking_id(self):
        return f"TRVL{random.randint(10000, 99999)}"

    def parse_date(self, date_text):
        date_text = date_text.lower()
        today = datetime.now()

        if 'tomorrow' in date_text or 'naalai' in date_text or 'naale' in date_text:
            return (today + timedelta(days=1)).strftime("%Y-%m-%d")
        elif 'next week' in date_text or 'adutha vaaram' in date_text:
            return (today + timedelta(days=7)).strftime("%Y-%m-%d")
        elif 'weekend' in date_text:
            # Next Saturday
            days_ahead = 5 - today.weekday()  # 5 is Saturday
            if days_ahead <= 0:
                days_ahead += 7
            return (today + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
        else:
            # Default to 3 days from now
            return (today + timedelta(days=3)).strftime("%Y-%m-%d")

    def parse_people(self, text):
        numbers = {
            'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6,
            'oru': 1, 'rendu': 2, 'moonu': 3, 'naalu': 4, 'ainthu': 5,
            'ondu': 1, 'eradu': 2, 'mooru': 3, 'nalku': 4, 'aidu': 5
        }

        text_lower = text.lower()

        # Check for numeric words
        for word, number in numbers.items():
            if word in text_lower:
                return number

        # Check for digits
        words = text_lower.split()
        for word in words:
            if word.isdigit():
                return int(word)

        # Default to 2 people
        return 2

    def parse_duration(self, text):
        text_lower = text.lower()

        if 'weekend' in text_lower or '2 days' in text_lower or 'rendu naal' in text_lower or 'eradu dinagalu' in text_lower:
            return 2
        elif '3 days' in text_lower or 'moonu naal' in text_lower or 'mooru dinagalu' in text_lower:
            return 3
        elif 'week' in text_lower or '7 days' in text_lower or 'vaaram' in text_lower or 'varusha' in text_lower:
            return 7
        else:
            # Default to 3 days
            return 3

    def process_message(self, user_input, user_id="default"):
        language = self.detect_language(user_input)
        user_input_lower = user_input.lower()

        # Initialize or get user booking state
        if user_id not in self.booking_states:
            self.booking_states[user_id] = {
                'step': 'greet',
                'destination': None,
                'people': None,
                'date': None,
                'duration': None
            }

        state = self.booking_states[user_id]

        # Handle booking flow based on current step
        if state['step'] == 'greet':
            if any(word in user_input_lower for word in ['book', 'trip', 'travel', 'plan', 'yathrai', 'prayana']):
                state['step'] = 'ask_destination'
                return self.responses["ask_destination"][language]
            else:
                state['step'] = 'ask_destination'
                return self.responses["greet"][language]

        elif state['step'] == 'ask_destination':
            # Extract destination
            destination = None
            for dest in self.destinations:
                if dest in user_input_lower:
                    destination = dest
                    break

            if destination:
                state['destination'] = destination
                state['step'] = 'ask_people'
                return self.responses["ask_people"][language]
            else:
                return self.responses["ask_destination"][language]

        elif state['step'] == 'ask_people':
            people = self.parse_people(user_input)
            state['people'] = people
            state['step'] = 'ask_date'
            return self.responses["ask_date"][language]

        elif state['step'] == 'ask_date':
            date = self.parse_date(user_input)
            state['date'] = date
            state['step'] = 'ask_duration'
            return self.responses["ask_duration"][language]

        elif state['step'] == 'ask_duration':
            duration = self.parse_duration(user_input)
            state['duration'] = duration
            state['step'] = 'confirm'

            # Format confirmation message
            confirmation = self.responses["confirm_booking"][language].format(
                destination=state['destination'].title(),
                people=state['people'],
                date=state['date'],
                duration=state['duration']
            )
            return confirmation

        elif state['step'] == 'confirm':
            if any(word in user_input_lower for word in ['yes', 'confirm', 'correct', 'aamaam', 'houdu', 'seri']):
                # Generate booking confirmation
                booking_id = self.generate_booking_id()
                total_price = state['people'] * state['duration'] * self.prices[state['destination']]

                confirmation = self.responses["booking_confirmed"][language].format(
                    destination=state['destination'].title(),
                    booking_id=booking_id,
                    people=state['people'],
                    date=state['date'],
                    duration=state['duration'],
                    price=f"₹{total_price:,}"
                )

                # Reset state for new booking
                self.booking_states[user_id] = {
                    'step': 'greet',
                    'destination': None,
                    'people': None,
                    'date': None,
                    'duration': None
                }

                return confirmation

            elif any(word in user_input_lower for word in ['no', 'change', 'wrong', 'illai', 'illa']):
                state['step'] = 'ask_destination'
                return self.responses["booking_cancelled"][language]
            else:
                return self.responses["confirm_booking"][language].format(
                    destination=state['destination'].title(),
                    people=state['people'],
                    date=state['date'],
                    duration=state['duration']
                )

        # Help command
        if any(word in user_input_lower for word in ['help', 'sahaya', 'upakarama']):
            return self.responses["help_booking"][language]

        # Fallback
        fallback = {
            "english": "I can help you book a trip! Just tell me where you want to go, how many people, when, and for how many days.",
            "tamil": "Naan trip book panna help pannuven! Enga poganum, evvalavu per, eppo, evvalavu naal nu solunga.",
            "kannada": "Nānu trip book māḍi help māḍutēne! Yellige hōgalu bēku, estu jana, yāvāga, estu dina anta heli."
        }
        return fallback[language]


# Initialize the assistant
assistant = MultilingualTravelAssistant()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    user_input = data.get('message', '')
    user_id = data.get('user_id', 'default')

    response = assistant.process_message(user_input, user_id)
    language = assistant.detect_language(user_input)

    return jsonify({
        'response': response,
        'language': language
    })


@app.route('/process_voice', methods=['POST'])
def process_voice():
    data = request.json
    text = data.get('text', '')
    user_id = data.get('user_id', 'voice_user')

    response = assistant.process_message(text, user_id)
    language = assistant.detect_language(text)

    return jsonify({
        'response': response,
        'language': language
    })


@app.route('/speak', methods=['POST'])
def speak():
    # Voice is handled by browser - just return success
    return jsonify({'status': 'voice_handled_by_browser'})

@app.route('/start_listening')
def start_listening():
    return jsonify({"text": "Voice recognition is handled by your browser. Please use the browser's voice feature."})

@app.route('/reset_booking', methods=['POST'])
def reset_booking():
    data = request.json
    user_id = data.get('user_id', 'default')

    if user_id in assistant.booking_states:
        assistant.booking_states[user_id] = {
            'step': 'greet',
            'destination': None,
            'people': None,
            'date': None,
            'duration': None
        }

    return jsonify({'status': 'reset'})


if __name__ == '__main__':
    print("🚀 Starting Multilingual Travel Booking Assistant...")
    print("🌐 Access at: http://localhost:3000")
    print("🗣️  Complete booking flow supported!")
    print("🎯 Try: 'I want to book a trip to Goa'")
    app.run(host='0.0.0.0', port=3000, debug=True)