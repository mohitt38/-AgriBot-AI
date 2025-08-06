# simple_orchestrator.py - Works with your current structure
import os
import sys
import json
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Simple import strategy - adjust paths as needed
def import_agents():
    """Dynamically import agents with error handling"""
    agents = {}
    
    try:
        # Try to import from current directory structure
        if os.path.exists("Agents"):
            sys.path.append("Agents")
            
        # Import individual agents
        try:
            from crop_advisor import get_crop_advice
            agents['crop_advisor'] = get_crop_advice
            print("✅ Crop Advisor loaded")
        except ImportError as e:
            print(f"⚠️ Could not load Crop Advisor: {e}")
            
        try:
            from market_broker import get_market_broker_response
            agents['market_broker'] = get_market_broker_response
            print("✅ Market Broker loaded")
        except ImportError as e:
            print(f"⚠️ Could not load Market Broker: {e}")
            
        try:
            from crop_disease_detector import analyze_crop_image
            agents['disease_detector'] = analyze_crop_image
            print("✅ Disease Detector loaded")
        except ImportError as e:
            print(f"⚠️ Could not load Disease Detector: {e}")
            
        try:
            from alert_agent import check_disease_alert
            agents['alert_system'] = check_disease_alert
            print("✅ Alert System loaded")
        except ImportError as e:
            print(f"⚠️ Could not load Alert System: {e}")
            
    except Exception as e:
        print(f"❌ Error loading agents: {e}")
    
    return agents

class SimpleAgenticOrchestrator:
    def __init__(self):
        print("🤖 Initializing Agentic AI System...")
        self.agents = import_agents()
        self.conversation_history = []
        self.user_context = {}
        print(f"✅ Loaded {len(self.agents)} agents successfully")
    
    def analyze_user_intent(self, user_input, has_image=False):
        """Enhanced intent analysis with better agent classification"""
        prompt = f"""
        You are an expert agricultural AI classifier. Analyze this query and classify it precisely:
        
        Query: "{user_input}"
        Has Image Attached: {has_image}
        
        CLASSIFICATION RULES:
        - disease_detector: ONLY if mentions disease, pest, leaf problems, image analysis, crop health issues, or has_image=True
        - crop_advisor: ONLY if asking what crops to grow, crop suggestions, planting advice
        - market_broker: ONLY if asking where to sell, market prices, buyers, selling platforms
        - alert_system: ONLY if asking about disease alerts, area warnings, recent outbreaks
        
        KEYWORDS TO WATCH:
        - Disease/Health: "disease", "pest", "sick", "spots", "dying", "problem", "leaf", "analyze image", "check photo"
        - Crop Selection: "what to grow", "which crop", "suggest crops", "best crops", "planting"
        - Market: "sell", "buyer", "market", "price", "where to sell"
        - Alerts: "alert", "warning", "outbreak", "recent disease"
        
        Return JSON:
        {{
            "intent": "specific intent description",
            "agents_needed": ["ONLY the most relevant agent(s)"],
            "primary_task": "disease_detection|crop_selection|market_info|alert_check|general",
            "parameters": {{
                "crop": "extracted crop name or null",
                "location": "extracted location or null", 
                "soil_type": "extracted soil type or null",
                "has_image": {has_image}
            }},
            "confidence": 0.9,
            "reasoning": "why you chose these agents"
        }}
        
        BE STRICT: Choose only ONE primary agent unless clearly multiple tasks are requested.
        """
        
        try:
            response = model.generate_content(prompt)
            # Clean the response text
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:-3]
            elif response_text.startswith('```'):
                response_text = response_text[3:-3]
                
            return json.loads(response_text)
        except Exception as e:
            print(f"Intent analysis error: {e}")
            # Fallback simple intent detection
            return {
                "intent": "general agricultural query",
                "agents_needed": ["crop_advisor"] if any(word in user_input.lower() for word in ['crop', 'grow', 'plant']) else [],
                "parameters": {"crop": None, "location": None, "soil_type": None, "has_image": False},
                "confidence": 0.5
            }
    
    def extract_parameters(self, user_input):
        """Extract parameters from user input"""
        prompt = f"""
        Extract agricultural parameters from: "{user_input}"
        
        Return JSON:
        {{
            "crop": "crop name or null",
            "location": "city/region or null",
            "soil_type": "soil type or null", 
            "quantity": "quantity mentioned or null"
        }}
        """
        
        try:
            response = model.generate_content(prompt)
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:-3]
            elif response_text.startswith('```'):
                response_text = response_text[3:-3]
            return json.loads(response_text)
        except:
            return {"crop": None, "location": None, "soil_type": None, "quantity": None}
    
    def call_agent(self, agent_name, parameters):
        """Call specific agent with parameters"""
        if agent_name not in self.agents:
            return f"Agent {agent_name} not available"
        
        try:
            if agent_name == 'crop_advisor':
                soil = parameters.get('soil_type') or 'mixed'
                location = parameters.get('location') or 'India'
                return self.agents[agent_name](soil, location)
                
            elif agent_name == 'market_broker':
                crop = parameters.get('crop') or 'wheat'
                location = parameters.get('location') or 'India'
                quantity = parameters.get('quantity')
                return self.agents[agent_name](crop, location, quantity)
                
            elif agent_name == 'disease_detector':
                # For now, return placeholder - implement image handling separately
                return "Disease detection requires image upload. Please use the web interface."
                
            elif agent_name == 'alert_system':
                crop = parameters.get('crop') or 'wheat'
                location = parameters.get('location') or 'India'
                return self.agents[agent_name](crop, location)
                
        except Exception as e:
            return f"Error calling {agent_name}: {str(e)}"
    
    def synthesize_response(self, user_input, agent_results, intent):
        """Create comprehensive response from agent outputs"""
        prompt = f"""
        User asked: "{user_input}"
        Intent: {intent}
        
        Agent Results:
        {json.dumps(agent_results, indent=2)}
        
        Create a helpful, comprehensive response that:
        1. Directly answers the user's question
        2. Integrates all agent outputs naturally
        3. Uses friendly, professional tone
        4. Provides actionable advice
        5. Includes both English and Hindi where appropriate
        
        Make it conversational and helpful.
        """
        
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            # Fallback response
            result_text = ""
            for agent, result in agent_results.items():
                result_text += f"\n**{agent.replace('_', ' ').title()}:**\n{result}\n"
            return f"Here's what I found for your query:\n{result_text}"
    
    def process_request(self, user_input, image_file=None):
        """Enhanced processing method with better agent routing"""
        print(f"\n🧠 Processing: {user_input}")
        has_image = image_file is not None
        
        # Step 1: Enhanced intent analysis
        intent_analysis = self.analyze_user_intent(user_input, has_image)
        print(f"📋 Intent: {intent_analysis['intent']}")
        print(f"🎯 Primary Task: {intent_analysis.get('primary_task', 'general')}")
        print(f"🤖 Agents needed: {intent_analysis['agents_needed']}")
        print(f"💭 Reasoning: {intent_analysis.get('reasoning', 'N/A')}")
        
        # Step 2: Validate agent selection based on task type
        validated_agents = self.validate_agent_selection(
            intent_analysis['agents_needed'], 
            intent_analysis.get('primary_task'),
            has_image,
            user_input
        )
        
        if validated_agents != intent_analysis['agents_needed']:
            print(f"🔄 Corrected agents: {validated_agents}")
        
        # Step 3: Extract parameters
        parameters = self.extract_parameters(user_input)
        if has_image:
            parameters['image_file'] = image_file
        print(f"🔧 Parameters: {parameters}")
        
        # Step 4: Call agents with enhanced logic
        agent_results = {}
        for agent_name in validated_agents:
            if agent_name in self.agents:
                print(f"🤖 Calling {agent_name}...")
                result = self.call_agent(agent_name, parameters)
                agent_results[agent_name] = result
            else:
                print(f"⚠️ Agent {agent_name} not available")
        
        # Step 5: Synthesize response
        if agent_results:
            final_response = self.synthesize_response(
                user_input, 
                agent_results, 
                intent_analysis['intent']
            )
        else:
            final_response = self.generate_fallback_response(user_input, intent_analysis)
        
        # Step 6: Update context
        self.update_context(parameters, intent_analysis)
        
        # Save to history
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "intent": intent_analysis['intent'],
            "primary_task": intent_analysis.get('primary_task'),
            "agents_called": validated_agents,
            "response": final_response,
            "had_image": has_image
        })
        
        return final_response
    
    def validate_agent_selection(self, suggested_agents, primary_task, has_image, user_input):
        """Validate and correct agent selection based on rules"""
        
        # Define strict keywords for each agent
        disease_keywords = ['disease', 'pest', 'sick', 'dying', 'spots', 'leaf', 'problem', 'analyze', 'check', 'diagnose', 'health']
        crop_keywords = ['grow', 'plant', 'suggest crops', 'which crop', 'best crop', 'suitable crop', 'recommend']
        market_keywords = ['sell', 'buyer', 'market', 'price', 'selling', 'purchase', 'buy']
        alert_keywords = ['alert', 'warning', 'outbreak', 'recent', 'area', 'nearby']
        
        user_lower = user_input.lower()
        
        # Force disease detector if image is present or disease keywords found
        if has_image or any(keyword in user_lower for keyword in disease_keywords):
            return ['disease_detector']
        
        # Force crop advisor only for crop selection queries
        elif any(keyword in user_lower for keyword in crop_keywords) and 'soil' in user_lower:
            return ['crop_advisor']
        
        # Force market broker for selling queries
        elif any(keyword in user_lower for keyword in market_keywords):
            return ['market_broker']
        
        # Force alert system for alert queries
        elif any(keyword in user_lower for keyword in alert_keywords):
            return ['alert_system']
        
        # If no clear match, return suggested agents but limit to 1
        elif suggested_agents:
            return [suggested_agents[0]]  # Take only the first suggestion
        
        else:
            # Default fallback based on common patterns
            if 'what' in user_lower and ('crop' in user_lower or 'grow' in user_lower):
                return ['crop_advisor']
            else:
                return ['crop_advisor']  # Safe default
    
    def update_context(self, parameters, intent_analysis):
        """Update user context intelligently"""
        if parameters.get('location'):
            self.user_context['location'] = parameters['location']
        if parameters.get('crop'):
            self.user_context['current_crop'] = parameters['crop']
        if parameters.get('soil_type'):
            self.user_context['soil_type'] = parameters['soil_type']
        
        # Track user's primary interests
        primary_task = intent_analysis.get('primary_task')
        if primary_task:
            if 'interests' not in self.user_context:
                self.user_context['interests'] = {}
            
            if primary_task not in self.user_context['interests']:
                self.user_context['interests'][primary_task] = 0
            self.user_context['interests'][primary_task] += 1
    
    def generate_fallback_response(self, user_input, intent_analysis):
        """Generate helpful fallback when no agents are available"""
        primary_task = intent_analysis.get('primary_task', 'general')
        
        fallback_responses = {
            'disease_detection': "🔬 I understand you want disease analysis. To help you better, please upload an image of your crop leaves, and I'll analyze them for diseases and provide treatment suggestions.",
            'crop_selection': "🌱 I can help suggest the best crops for your area! Please provide your soil type and location for personalized recommendations.",
            'market_info': "🤝 I can help you find the best places to sell your crops! Please tell me what crop you have and your location.",
            'alert_check': "⚠️ I can check for disease alerts in your area. Please specify your location and the crop you're concerned about."
        }
        
        return fallback_responses.get(primary_task, 
            "I understand your agricultural question. Could you please be more specific about what you need help with? I can assist with:\n"
            "🌱 Crop selection and growing advice\n"
            "🔬 Disease detection (with images)\n" 
            "🤝 Market information and selling platforms\n"
            "⚠️ Disease alerts and warnings"
        )

def main():
    """Enhanced main function with testing option"""
    print("🌾 SMART CROP AI - AGENTIC SYSTEM")
    print("="*50)  
    orchestrator = SimpleAgenticOrchestrator()
    
    print("\nAsk me anything about farming! Type 'exit' to quit.")
    print("💡 Try these examples:")
    print("  • 'My tomato leaves have spots' (Disease Detection)")
    print("  • 'What crops for red soil in Udaipur?' (Crop Advisor)")  
    print("  • 'Where to sell wheat in Punjab?' (Market Broker)")
    print("  • 'Disease alerts in my area?' (Alert System)")
    
    # Show context if available
    if orchestrator.user_context:
        print(f"\n📋 Your context: {orchestrator.user_context}")
    
    while True:
        try:
            user_input = input("\n👨‍🌾 You: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("👋 Happy farming!")
                break
            
            if not user_input:
                print("💡 Try asking about crops, diseases, markets, or alerts!")
                continue
            
            # Ask if they have an image (for testing)
            has_image = input("Do you have an image to upload? (y/n): ").lower() == 'y'
            image_file = "test_image.jpg" if has_image else None
            
            response = orchestrator.process_request(user_input, image_file)
            print(f"\n🤖 AI Assistant:\n{response}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()