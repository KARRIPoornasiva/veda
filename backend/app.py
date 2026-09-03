from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="")
CORS(app)

problem_statements = [
    {
        "id": "PS-01",
        "round": "round-1",
        "domain": "healthcare",
        "domainLabel": "🏥 Healthcare & Clinical AI",
        "title": "AI Health Assistance Agent",
        "difficulty": "Medium",
        "diffClass": "medium",
        "summary": "Develop an AI Health Assistance Agent that provides reliable health information, helps users understand common symptoms, recommends appropriate next steps, provides medicine/appointment reminders, and connects users with nearby healthcare facilities.",
        "fullDescription": "People, especially in rural and underserved areas, often face difficulty accessing basic health information, understanding symptoms, finding nearby healthcare services, and following preventive health practices. The system should clearly indicate that it is NOT a replacement for a qualified medical professional.",
        "capabilities": [
            "Symptom Understanding & Analysis",
            "Health Information Retrieval",
            "Healthcare Service Locator",
            "Appointment & Medication Reminders",
            "Preventive Health Recommendations",
            "Multilingual Support",
        ],
        "techStack": ["LangChain / CrewAI", "FastAPI / Python", "Vector RAG (ChromaDB)", "Google Maps API", "Twilio / SMS"],
        "sampleFlow": "User: 'I have a persistent cough for 3 days' -> Agent asks clarifying questions -> Provides possible causes -> Recommends when to see doctor -> Locates nearby clinics -> Sets medication reminder.",
        "rubricFocus": "Medical safety, clarity on limitations, accurate symptom analysis, reliable healthcare location data, and multilingual support.",
    },
    {
        "id": "PS-02",
        "round": "round-1",
        "domain": "agriculture",
        "domainLabel": "🌾 Agriculture & Farming Advisory",
        "title": "AI Agriculture Advisory Agent",
        "difficulty": "Hard",
        "diffClass": "hard",
        "summary": "Develop an AI Agriculture Agent that provides personalized farming recommendations using information such as crop type, soil conditions, weather, season, and location. Farmers can interact with the agent through text, voice, or images of crops.",
        "fullDescription": "Farmers often face difficulties in identifying crop diseases, selecting suitable crops, managing irrigation, and obtaining timely information about weather, soil, fertilizers, and market conditions. This autonomous agent leverages computer vision, weather APIs, and agricultural databases to deliver real-time, location-aware farming insights.",
        "capabilities": [
            "Crop Disease Detection from Images",
            "Crop Selection Recommendation",
            "Weather-Based Farming Alerts",
            "Irrigation & Fertilizer Guidance",
            "Pest Management Strategies",
            "Market Price Information",
            "Voice & Local Language Support",
        ],
        "techStack": ["LangChain / AutoGen", "Computer Vision (OpenCV/YOLO)", "Weather APIs", "Google Lens / Custom Models", "Vector RAG"],
        "sampleFlow": "Farmer uploads leaf image -> Agent identifies fungal disease -> Recommends fungicide treatment -> Checks weather forecast -> Suggests optimal spray timing -> Provides market rates for harvest.",
        "rubricFocus": "Image recognition accuracy, location-aware recommendations, real-time weather integration, market data reliability, and voice interaction support.",
    },
    {
        "id": "PS-03",
        "round": "round-1",
        "domain": "sustainability",
        "domainLabel": "♻️ Waste Management & Sustainability",
        "title": "AI Waste Management Agent",
        "difficulty": "Medium",
        "diffClass": "medium",
        "summary": "Develop an AI Waste Management Agent that helps citizens identify different types of waste and provides guidance on proper disposal. The system can also allow users to report overflowing garbage bins or waste-dumping locations.",
        "fullDescription": "Improper segregation and disposal of waste creates environmental and public-health problems in cities, towns, and villages. This autonomous agent educates users on waste classification, connects them with local recycling centers, enables crowdsourced waste-site reporting, and helps local authorities identify waste hotspots for prioritized collection.",
        "capabilities": [
            "Waste Classification & Categorization",
            "Waste Segregation Guidance",
            "Recycling & Disposal Information",
            "Waste Hotspot Reporting",
            "Location-Based Facility Finder",
            "Community Crowdsourcing",
            "Local Authority Integration",
        ],
        "techStack": ["LangChain", "Computer Vision (for waste images)", "Google Maps API", "PostgreSQL (hotspot database)", "Geospatial Tools"],
        "sampleFlow": "User: 'I have electronics to dispose' -> Agent identifies e-waste category -> Suggests nearby e-waste collection center -> User reports overflowing bin location -> System updates heat map for authorities.",
        "rubricFocus": "Accurate waste classification, user-friendly segregation guidance, reliable recycling center locator, and effective hotspot mapping for authorities.",
    },
    {
        "id": "PS-04",
        "round": "round-1",
        "domain": "emergency",
        "domainLabel": "🚨 Emergency & Disaster Response",
        "title": "AI Emergency & Disaster Assistance Agent",
        "difficulty": "Hard",
        "diffClass": "hard",
        "summary": "Develop an AI Emergency Assistance Agent that provides location-aware emergency information, safety instructions, emergency contacts, shelter information, and alerts based on verified sources.",
        "fullDescription": "During floods, cyclones, earthquakes, fires, and other emergencies, people may not receive timely information about evacuation routes, emergency contacts, shelters, and safety procedures. This autonomous agent delivers real-time, verified disaster alerts, location-specific safety guidance, and connects citizens with emergency services and shelters using geospatial awareness and multi-modal communication.",
        "capabilities": [
            "Emergency Safety Instructions",
            "Verified Disaster Alerts",
            "Evacuation Route Guidance",
            "Shelter & Safe Area Locator",
            "Emergency Contact Directory",
            "Disaster Preparedness Planning",
            "Multilingual & Voice Support",
            "Real-Time Geospatial Awareness",
        ],
        "techStack": ["CrewAI / LangGraph", "Weather APIs (tornado/flood forecasting)", "Google Maps / Geospatial APIs", "Twilio (SMS/Voice)", "Real-time data feeds"],
        "sampleFlow": "Earthquake detected -> Agent pushes verified alert -> Queries user location -> Recommends nearest shelter -> Provides evacuation map -> Contacts emergency services -> Sends safety tips.",
        "rubricFocus": "Alert verification accuracy, real-time geospatial precision, reliable shelter/service locator, multilingual emergency instructions, and seamless emergency service integration.",
    },
]


@app.route("/", methods=["GET"])
def index():
    return send_from_directory(str(FRONTEND_DIR), "index.html")


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "VEDA backend is running"})


@app.route("/api/problems", methods=["GET"])
def get_problems():
    return jsonify(problem_statements)


@app.route("/api/register", methods=["POST"])
def register_team():
    payload = request.get_json(silent=True) or {}
    required = ["teamName", "leadName", "leadRoll", "leadEmail"]
    missing = [field for field in required if not payload.get(field)]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    team_id = payload.get("teamId") or f"VEDA-AGENT-{__import__('random').randint(1000, 9999)}"
    entry = {
        "teamId": team_id,
        "teamName": payload.get("teamName"),
        "leadName": payload.get("leadName"),
        "leadRoll": payload.get("leadRoll"),
        "leadEmail": payload.get("leadEmail"),
        "track": payload.get("track", "GENERAL"),
        "registeredAt": datetime.utcnow().isoformat() + "Z",
    }
    return jsonify({"message": "Registration confirmed", "team": entry}), 201


@app.route("/api/submit", methods=["POST"])
def submit_project():
    payload = request.get_json(silent=True) or {}
    if not payload.get("teamId") or not payload.get("repoUrl"):
        return jsonify({"error": "teamId and repoUrl are required"}), 400

    return jsonify({
        "message": "Solution submitted successfully for evaluation",
        "submission": {
            "teamId": payload.get("teamId"),
            "repoUrl": payload.get("repoUrl"),
            "notes": payload.get("notes", ""),
        },
    }), 201


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
