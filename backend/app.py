from datetime import datetime
import os
from pathlib import Path
import secrets
import sqlite3

from flask import Flask, jsonify, request, send_from_directory, session
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
DATABASE_PATH = BASE_DIR / "backend" / "veda.db"

app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="")
app.config.update(
    SECRET_KEY=os.getenv("VEDA_SECRET_KEY", secrets.token_hex(32)),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.getenv("VEDA_SECURE_COOKIES", "0") == "1",
)
CORS(app)

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD_HASH = os.getenv(
    "ADMIN_PASSWORD_HASH",
    generate_password_hash(os.getenv("ADMIN_PASSWORD", "veda-admin-2026")),
)


def get_db_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    with get_db_connection() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS registrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id TEXT NOT NULL UNIQUE,
                team_name TEXT NOT NULL,
                team_size TEXT NOT NULL DEFAULT '2',
                lead_name TEXT NOT NULL,
                lead_roll TEXT NOT NULL,
                lead_email TEXT NOT NULL,
                lead_phone TEXT NOT NULL DEFAULT '',
                member2_name TEXT NOT NULL DEFAULT '',
                member2_roll TEXT NOT NULL DEFAULT '',
                track TEXT NOT NULL DEFAULT 'GENERAL',
                registered_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id TEXT NOT NULL,
                round TEXT NOT NULL DEFAULT 'round-1',
                repo_url TEXT NOT NULL,
                demo_url TEXT NOT NULL DEFAULT '',
                notes TEXT NOT NULL DEFAULT '',
                submitted_at TEXT NOT NULL
            );
            """
        )


init_database()

problem_statements = [
    {
        "id": "PS-01",
        "round": "round-1",
        "domain": "healthcare",
        "domainLabel": "🏥 Healthcare & Clinical AI",
        "title": "AI Health Support and Guidance Agent",
        "difficulty": "Medium",
        "diffClass": "medium",
        "summary": "Develop an AI Health Support and Guidance Agent that provides reliable health information, helps users understand common symptoms, recommends appropriate next steps, provides medicine/appointment reminders, and connects users with nearby healthcare facilities.",
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
    {
        "id": "PS-05",
        "round": "round-1",
        "domain": "fintech",
        "domainLabel": "💳 FinTech & Fraud Intelligence",
        "title": "AI Fraud Investigation Agent",
        "difficulty": "Hard",
        "diffClass": "hard",
        "summary": "Build an autonomous fraud investigation agent that analyzes suspicious transactions, identifies risk patterns, gathers supporting evidence, and produces an explainable investigation report.",
        "fullDescription": "Financial teams receive large volumes of alerts but often lack the time to investigate each case thoroughly. The agent should combine transaction analysis, customer history, policy retrieval, and external intelligence to prioritize alerts and explain why a transaction is suspicious without making unsupported accusations.",
        "capabilities": [
            "Transaction Anomaly Detection",
            "Customer History Retrieval",
            "Risk Score Calculation",
            "Evidence Collection from APIs",
            "Explainable Investigation Reports",
            "Human Review Escalation",
        ],
        "techStack": ["LangGraph / AutoGen", "Python / FastAPI", "SQLite or PostgreSQL", "Fraud Rules API", "Vector RAG"],
        "sampleFlow": "Analyst submits transaction ID -> Agent retrieves account history -> Detects unusual location and amount -> Queries fraud policy -> Produces evidence-backed risk report -> Escalates high-risk case.",
        "rubricFocus": "Detection accuracy, evidence traceability, explainable reasoning, safe escalation, and useful investigator workflow.",
    },
    {
        "id": "PS-06",
        "round": "round-1",
        "domain": "devtools",
        "domainLabel": "🧰 DevTools & Code Intelligence",
        "title": "Self-Reflective Code Review Agent",
        "difficulty": "Hard",
        "diffClass": "hard",
        "summary": "Create a code review agent that understands a repository, runs targeted checks, identifies defects, proposes fixes, and verifies its recommendations with an execution loop.",
        "fullDescription": "Developers need fast feedback that goes beyond surface-level style comments. The agent should inspect repository context, select suitable tests or linters, reason about failures, and return prioritized findings with concrete evidence while avoiding changes that it cannot validate.",
        "capabilities": [
            "Repository Structure Discovery",
            "Static Analysis Tool Calling",
            "Test Selection and Execution",
            "Bug Severity Prioritization",
            "Patch Recommendation",
            "Self-Verification Loop",
        ],
        "techStack": ["Python or Node.js", "Tree-sitter / AST Tools", "GitHub API", "Jest or Pytest", "Sandboxed Code Runner"],
        "sampleFlow": "User submits repository URL -> Agent maps modules -> Runs focused tests and linter -> Correlates failures with source lines -> Suggests patch -> Re-runs the failing check and reports confidence.",
        "rubricFocus": "Repository understanding, actionable findings, tool selection, reproducibility, and reliable self-correction.",
    },
    {
        "id": "PS-07",
        "round": "round-1",
        "domain": "edtech",
        "domainLabel": "🎓 EdTech & Campus Services",
        "title": "Campus Academic Navigator",
        "difficulty": "Medium",
        "diffClass": "medium",
        "summary": "Develop a campus assistant that answers academic questions using verified university documents, checks schedules, recommends resources, and creates personalized study plans.",
        "fullDescription": "Students often search across disconnected notices, timetables, syllabi, and campus portals for simple answers. The agent should retrieve the correct institutional source, distinguish official facts from suggestions, and take useful actions such as building reminders or study schedules.",
        "capabilities": [
            "University Document RAG",
            "Timetable and Notice Search",
            "Source Citation",
            "Personalized Study Planning",
            "Calendar Reminder Creation",
            "Student Preference Memory",
        ],
        "techStack": ["LlamaIndex / LangChain", "PDF and OCR Parsers", "ChromaDB", "Calendar API", "SQLite"],
        "sampleFlow": "Student asks for exam schedule -> Agent retrieves the latest official notice -> Cites the source -> Checks free study hours -> Creates a revision plan and optional calendar reminders.",
        "rubricFocus": "Grounded answers, current-source selection, personalization, citations, and practical campus workflows.",
    },
    {
        "id": "PS-08",
        "round": "round-1",
        "domain": "research",
        "domainLabel": "🔎 Research & Fact-Checking",
        "title": "Investigative Fact-Checking Agent",
        "difficulty": "Hard",
        "diffClass": "hard",
        "summary": "Build a research agent that decomposes claims, searches reliable sources, compares conflicting evidence, and produces a cited fact-check with uncertainty clearly identified.",
        "fullDescription": "Online claims frequently combine true, outdated, and misleading information. The agent should break a claim into verifiable subclaims, retrieve evidence from multiple sources, detect contradictions, and provide a transparent conclusion rather than presenting speculation as fact.",
        "capabilities": [
            "Claim Decomposition",
            "Multi-Source Web Search",
            "Evidence Quality Ranking",
            "Contradiction Detection",
            "Citation Generation",
            "Uncertainty and Bias Reporting",
        ],
        "techStack": ["CrewAI / LangGraph", "Search API", "News and Research APIs", "Vector Database", "Citation Parser"],
        "sampleFlow": "User submits a viral claim -> Agent splits it into subclaims -> Searches primary and independent sources -> Compares publication dates and evidence -> Returns a cited verdict with confidence and open questions.",
        "rubricFocus": "Source quality, citation accuracy, balanced reasoning, contradiction handling, and transparent uncertainty.",
    },
    {
        "id": "PS-09",
        "round": "round-2",
        "domain": "cybersecurity",
        "domainLabel": "🛡️ Cybersecurity & Threat Response",
        "title": "Autonomous Security Incident Triage Agent",
        "difficulty": "Expert",
        "diffClass": "hard",
        "summary": "Create a security triage agent that correlates alerts, enriches indicators, recommends containment actions, and maintains an auditable incident timeline for a human analyst.",
        "fullDescription": "Security analysts must quickly distinguish real incidents from noisy alerts. The agent should safely combine log analysis, threat-intelligence lookups, and response playbooks, while requiring human approval before disruptive actions such as blocking accounts or isolating systems.",
        "capabilities": [
            "Alert Correlation",
            "Threat Intelligence Lookup",
            "Log and Indicator Analysis",
            "Incident Timeline Construction",
            "Playbook Recommendation",
            "Human-Approved Containment",
        ],
        "techStack": ["LangGraph / Semantic Kernel", "SIEM Log Parser", "Threat Intel APIs", "Elasticsearch", "Approval Workflow"],
        "sampleFlow": "Multiple login alerts arrive -> Agent correlates IP, device, and user data -> Enriches the IP with threat intelligence -> Builds incident timeline -> Recommends containment -> Waits for analyst approval.",
        "rubricFocus": "Safe action boundaries, alert correlation, evidence quality, auditability, and analyst-in-the-loop design.",
    },
    {
        "id": "PS-10",
        "round": "round-2",
        "domain": "smartcity",
        "domainLabel": "🏙️ Smart City & Public Services",
        "title": "Multi-Agent Civic Operations Coordinator",
        "difficulty": "Expert",
        "diffClass": "hard",
        "summary": "Build a multi-agent civic operations system that coordinates complaints, verifies reports, assigns departments, tracks service progress, and adapts plans when conditions change.",
        "fullDescription": "Public-service requests often cross department boundaries and lose context during handoffs. The system should use specialized agents for intake, verification, routing, and follow-up, sharing structured state while keeping every decision traceable to a report or policy.",
        "capabilities": [
            "Natural-Language Complaint Intake",
            "Image and Location Verification",
            "Multi-Agent Department Routing",
            "Priority and SLA Tracking",
            "Status Update Notifications",
            "Conflict Resolution and Replanning",
        ],
        "techStack": ["AutoGen / CrewAI", "Maps and Geocoding API", "Computer Vision", "PostgreSQL", "SMS or Email Notifications"],
        "sampleFlow": "Resident reports a damaged streetlight with a photo -> Intake agent extracts location -> Verification agent checks duplicate reports -> Routing agent assigns the electrical department -> Follow-up agent tracks SLA and notifies the resident.",
        "rubricFocus": "Agent coordination, reliable routing, state consistency, measurable service outcomes, and graceful replanning.",
    },
]

from new_problem_statements import problem_statements


@app.route("/", methods=["GET"])
def index():
    return send_from_directory(str(FRONTEND_DIR), "main.html")


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "VEDA backend is running"})


@app.route("/api/problems", methods=["GET"])
def get_problems():
    return jsonify(problem_statements)


@app.route("/admin", methods=["GET"])
def admin_page():
    return send_from_directory(str(FRONTEND_DIR), "admin.html")


@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    payload = request.get_json(silent=True) or {}
    username = str(payload.get("username", "")).strip()
    password = str(payload.get("password", ""))

    if username != ADMIN_USERNAME or not check_password_hash(ADMIN_PASSWORD_HASH, password):
        return jsonify({"error": "Invalid admin credentials"}), 401

    session["admin_authenticated"] = True
    return jsonify({"message": "Admin login successful"})


@app.route("/api/admin/logout", methods=["POST"])
def admin_logout():
    session.pop("admin_authenticated", None)
    return jsonify({"message": "Admin logged out"})


def admin_required():
    if not session.get("admin_authenticated"):
        return jsonify({"error": "Admin authentication required"}), 401
    return None


@app.route("/api/admin/dashboard", methods=["GET"])
def admin_dashboard():
    unauthorized = admin_required()
    if unauthorized:
        return unauthorized

    with get_db_connection() as connection:
        submissions = [dict(row) for row in connection.execute(
            "SELECT * FROM submissions ORDER BY id DESC"
        )]

    return jsonify({
        "submissions": submissions,
        "stats": {
            "submissionCount": len(submissions),
        },
    })


@app.route("/api/admin/submissions", methods=["DELETE"])
def delete_submissions():
    unauthorized = admin_required()
    if unauthorized:
        return unauthorized

    payload = request.get_json(silent=True) or {}
    submission_id = payload.get("id")
    delete_all = payload.get("all") is True or payload.get("all") == "true"

    if submission_id is None and not delete_all:
        return jsonify({"error": "Provide an id or set all=true to delete submissions."}), 400

    with get_db_connection() as connection:
        if delete_all:
            cursor = connection.execute("DELETE FROM submissions")
            deleted_count = cursor.rowcount
            message = "All submissions deleted successfully"
        else:
            try:
                target_id = int(submission_id)
            except (TypeError, ValueError):
                return jsonify({"error": "Submission id must be a number."}), 400
            cursor = connection.execute("DELETE FROM submissions WHERE id = ?", (target_id,))
            deleted_count = cursor.rowcount
            message = f"Submission {target_id} deleted successfully" if deleted_count else "Submission not found"

    return jsonify({
        "message": message,
        "deletedCount": deleted_count,
    })


@app.route("/api/register", methods=["POST"])
def register_team():
    payload = request.get_json(silent=True) or {}
    required = ["teamName", "leadName", "leadRoll", "leadEmail"]
    missing = [field for field in required if not payload.get(field)]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    team_id = payload.get("teamId") or f"VEDA-AGENT-{secrets.randbelow(9000) + 1000}"
    registered_at = datetime.utcnow().isoformat() + "Z"
    entry = {
        "teamId": team_id,
        "teamName": payload.get("teamName"),
        "teamSize": payload.get("teamSize", "2"),
        "leadName": payload.get("leadName"),
        "leadRoll": payload.get("leadRoll"),
        "leadEmail": payload.get("leadEmail"),
        "leadPhone": payload.get("leadPhone", ""),
        "member2Name": payload.get("member2Name", ""),
        "member2Roll": payload.get("member2Roll", ""),
        "track": payload.get("track", "GENERAL"),
        "registeredAt": registered_at,
    }

    try:
        with get_db_connection() as connection:
            connection.execute(
                """
                INSERT INTO registrations
                (team_id, team_name, team_size, lead_name, lead_roll, lead_email,
                 lead_phone, member2_name, member2_roll, track, registered_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    entry["teamId"], entry["teamName"], entry["teamSize"],
                    entry["leadName"], entry["leadRoll"], entry["leadEmail"],
                    entry["leadPhone"], entry["member2Name"], entry["member2Roll"],
                    entry["track"], entry["registeredAt"],
                ),
            )
    except sqlite3.IntegrityError:
        return jsonify({"error": "Could not create a unique team ID. Please try again."}), 409

    return jsonify({"message": "Registration confirmed", "team": entry}), 201


@app.route("/api/submit", methods=["POST"])
def submit_project():
    payload = request.get_json(silent=True) or {}
    if not payload.get("teamId") or not payload.get("repoUrl"):
        return jsonify({"error": "teamId and repoUrl are required"}), 400

    submission = {
        "teamId": payload.get("teamId"),
        "round": payload.get("round", "round-1"),
        "repoUrl": payload.get("repoUrl"),
        "demoUrl": payload.get("demoUrl", ""),
        "notes": payload.get("notes", ""),
        "submittedAt": datetime.utcnow().isoformat() + "Z",
    }
    with get_db_connection() as connection:
        connection.execute(
            """
            INSERT INTO submissions (team_id, round, repo_url, demo_url, notes, submitted_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                submission["teamId"], submission["round"], submission["repoUrl"],
                submission["demoUrl"], submission["notes"], submission["submittedAt"],
            ),
        )

    return jsonify({
        "message": "Solution submitted successfully for evaluation",
        "submission": submission,
    }), 201


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
