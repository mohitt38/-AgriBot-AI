# 🌾 AgriBot AI - Grow Smarter , Farm Better.
##  Autonomous Agentic AI for Agriculture.

<div align="center">



*Your Personal Farm Assistant with 24/7 Autonomous Intelligence*

### Streamlit UI
[🚀 Live Demo](https://your-deployed-app.streamlit.app) | [📖 Documentation](docs/) 

</div>

---

## 📋 *Table of Contents*
- [🌟 Overview](#-overview)
- [🎯 Features](#-features)
- [🏗 Architecture](#-architecture)
- [📸 Screenshots](#-screenshots)
- [🚀 Getting Started](#-getting-started)
- [💻 Installation](#-installation)
- [🎮 Usage](#-usage)
- [🤖 Autonomous Features](#-autonomous-features)
- [🛣 Roadmap](#-roadmap)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🌟 *Overview*

AgriBot AI is the *A autonomous agentic AI system* designed specifically for agriculture. It combines 4 specialized AI agents with autonomous learning capabilities to provide farmers with intelligent, proactive agricultural assistance.

### *🎯 Key Highlights:*
- 🤖 *Autonomous Intelligence*: AI that learns and operates 24/7
- 🌱 *4 Specialized Agents*: Crop advice, Disease detection, Market Intelligence, Alerts
- 📱 *Beautiful Interface*: Dark/light theme, mobile-responsive
- 🌍 *Indian Context*: Deep understanding of local farming practices
- 🔄 *Proactive Tasks*: Generates autonomous farming tasks and alerts

### *💡 Problem We Solve:*
- *70%* of farmers lack access to timely agricultural advice
- *$40B* annual crop losses due to late disease detection  
- *30%* below-market selling prices due to information gaps
- *20-40%* yield reduction from poor timing of farming activities

---

## 🎯 *Features*

### *🤖 AI Agents*
| Agent | Function | Capabilities |
|-------|----------|--------------|
| 🌱 *Crop Advisor* | Crop recommendations | Soil analysis, climate matching, yield optimization |
| 🔬 *Disease Detector* | Plant health analysis | Image-based diagnosis, treatment recommendations |
| 🤝 *Market Broker* | Market intelligence | Price tracking, buyer connections, selling strategies |
| ⚠️ *Alert System* | Proactive monitoring | Reports disease outbreaks |


### *🎨 User Interface*
- 🌓 *Theme Support*: Auto dark/light theme switching
- 📱 *Mobile Responsive*: Works perfectly on all devices
- 🗂 *Chat Interface*: Natural conversation with AI agents
- 📊 *Dashboard*: Real-time agent status and user insights
- 🖼 *Image Upload*: Drag-and-drop disease detection
- 🔔 *Real-time Alerts*: Alerts notifications and suggestions

---

### *Technology Stack*
- *Frontend*: Streamlit (Python web framework)
- *AI Engine*: Google Gemini 1.5 Flash
- *Scheduling*: Python Schedule for autonomous tasks
- *Image Processing*: PIL/Pillow for crop analysis
- *Architecture*: Multi-agent autonomous system

---

## 📸 *Screenshots*

### *🏠 Home Interface*
<div align="center">
<img src="smart_crop_ai\Screenshots\Screenshot 2025-08-05 103047.png" alt="Home Interface" width="80%">
<p><i>Beautiful home interface with feature overview and chat</i></p>
</div>

### *💬 Chat Interface*
<div align="center">
<img src="smart_crop_ai\Screenshots\Screenshot 2025-08-05 205826.pngg" alt="Chat Interface" width="80%">
<p><i>Natural conversation with AI agents</i></p>


</div>


---

## 🚀 *Getting Started*

### *⚡ Quick Start*
bash
# Clone the repository
git clone https://github.com/yourusername/AgriBot_AI-git
cd smart-crop-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your Google Gemini API key to .env

# Run the application
streamlit run app.py


### *🌐 Access the App*
- *Local*: http://localhost:8502
- *Network*: Your app will be accessible on your network
- *Cloud*: Deploy to Streamlit Cloud for public access

---

## 💻 *Installation*

### *📋 Prerequisites*
- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://ai.google.dev))
- Git (for cloning)

### *🔧 Environment Setup*

#### *1. Clone Repository*
bash
git clone https://github.com/yourusername/smart-crop-ai.git
cd smart-crop-ai


#### *2. Create Virtual Environment*
bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate


#### *3. Install Dependencies*
bash
pip install -r requirements.txt


#### *4. Environment Configuration*
Create .env file in project root:
env
GOOGLE_API_KEY=your_gemini_api_key_here
DATABASE_URL=sqlite:///autonomous_ai.db
DEBUG=True


#### *5. Initialize Database*
bash
python -c "from autonomous_layers import AutonomousMemorySystem; AutonomousMemorySystem()"


### *📦 Dependencies*
txt
streamlit>=1.28.0
google-generativeai>=0.3.0
python-dotenv>=1.0.0
Pillow>=10.0.0
pandas>=2.0.0
numpy>=1.24.0
schedule>=1.2.0
sqlite3
asyncio


---

## 🎮 *Usage*

### *🚀 Basic Usage*

#### *1. Start the Application*
bash
streamlit run app.py


#### *2. Interact with AI Agents*
- *Text Queries*: Type questions about farming
- *Image Upload*: Upload crop images for disease detection
- *Voice Input*: Use browser's voice input feature

#### *3. Example Interactions*

👨‍🌾 "What crops should I grow in red soil in Rajasthan?"
🤖 Crop Advisor provides personalized recommendations...

👨‍🌾 [Upload image of diseased leaves]
🤖 Disease Detector analyzes and provides treatment...

👨‍🌾 "Where can I sell wheat at best price?"
🤖 Market Broker suggests optimal selling strategies...


---

### *💾 Memory System*
The system maintains:
- *User Profiles*: Location, crops, soil type, preferences
- *Learning Records*: Interaction history with feedback analysis
- *Knowledge Base*: Continuously updated agricultural insights
- *Task History*: Record of all autonomous operations

### *🔄 Real-time Operations*
- *Background Monitoring*: 24/7 weather and market surveillance
- *Proactive Alerts*: Automatic notifications for important events
- *Smart Suggestions*: Context-aware recommendations
- *Adaptive Learning*: Continuous improvement without manual intervention

---

## 🛣 *Roadmap*

### *Current Status (v1.0)*
- ✅ Multi-agent AI system
- ✅ Autonomous learning capabilities
- ✅ Streamlit web interface
- ✅ Basic disease detection
- ✅ Market intelligence

### *Future Scope*
### *Phase 2*
- 🔄 Advanced image recognition
- 🔄 Voice interface integration
- 🔄 Mobile app development
- 🔄 API for third-party integrations
- 🔄 Multi-language support (Hindi, regional languages)

### *Phase 4* 
- 🔄 International expansion
- 🔄 Advanced predictive analytics
- 🔄 Climate change adaptation
- 🔄 Carbon footprint tracking
- 🔄 Sustainable farming recommendations

---

## 📄 *License*

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 *Acknowledgments*

### *🎯 Special Thanks*
- *Google AI* for Gemini API access
- *Streamlit* for the amazing web framework
- *Farming Community* for valuable feedback and testing

---

## 📞 *Contact & Support*

### *👥 Team*
- *Lead Developer*: [Mohit_Nagda] - [nagdamohit19@gmail.com]
- *AI Research*: [Vandita_Soni] - [vanditasoni726@gmail.com]
- *Developer*: [Deepesh_Suthar] - [deepeshsuthar5@gmail.com]

### *🌐 Links*
- *Website*: https://smartcropai.com
- *Documentation*: https://docs.smartcropai.com
- *Live Demo*: https://demo.smartcropai.com
---

<div align="center">

### *🌾 Making Agriculture Intelligent, One Farm at a Time 🚀*

[![GitHub stars](https://img.shields.io/github/stars/yourusername/smart-crop-ai.svg?style=social)](https://github.com/yourusername/smart-crop-ai/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/smart-crop-ai.svg?style=social)](https://github.com/yourusername/smart-crop-ai/network)
[![GitHub watchers](https://img.shields.io/github/watchers/yourusername/smart-crop-ai.svg?style=social)](https://github.com/yourusername/smart-crop-ai/watchers)

*⭐ Star this repository if you find it helpful! ⭐*

---

## 🤝 *Contributing*

We welcome contributions from the community! Here's how you can help:

### *🔧 Development Setup*
bash
# Fork the repository
git clone https://github.com/yourusername/AgriBot-AI-.git

# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and test
python -m pytest tests/

# Submit pull request
git push origin feature/your-feature-name


### *📝 Contribution Guidelines*
- Follow PEP 8 coding standards
- Add tests for new features
- Update documentation
- Use descriptive commit messages
- Ensure all tests pass

### *🐛 Bug Reports*
Please use GitHub Issues to report bugs:
- Use clear, descriptive titles
- Provide reproduction steps
- Include error messages and screenshots
- Specify your environment (OS, Python version)

### *💡 Feature Requests*
We love new ideas! Submit feature requests via GitHub Issues:
- Explain the use case
- Describe the expected behavior
- Consider implementation complexity
- Discuss potential alternatives

---

## 📄 *License*

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


MIT License

Copyright (c) 2024 Smart Crop AI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...


---

[![GitHub stars](https://img.shields.io/github/stars/yourusername/smart-crop-ai.svg?style=social)](https://github.com/yourusername/smart-crop-ai/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/smart-crop-ai.svg?style=social)](https://github.com/yourusername/smart-crop-ai/network)
[![GitHub watchers](https://img.shields.io/github/watchers/yourusername/smart-crop-ai.svg?style=social)](https://github.com/yourusername/smart-crop-ai/watchers)

*⭐ Star this repository if you find it helpful! ⭐*

</div>