# study/Youtube/build_sell_claude_code_operating_systems.py
# 
# Runnable python script illustrating a simplified AIOS framework skeleton.
# Demonstrates the 4Cs (Context, Connections, Capabilities, Cadence) in action.

import os
import sys
import json
import time

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


class MockAIOS:
    def __init__(self, workspace_path):
        self.workspace = workspace_path
        self.context = {}
        self.connections = {}
        self.skills = []
        
    # --- 1. CONTEXT LAYER ---
    def load_context(self):
        print("[1/4] Loading Context Layer...")
        # Check for operating manual
        manual_path = os.path.join(self.workspace, "GEMINI.md")
        if os.path.exists(manual_path):
            print("  ✓ Operating Manual found (GEMINI.md)")
            self.context["manual_active"] = True
        else:
            print("  ✗ Operating Manual missing")
            self.context["manual_active"] = False
            
        # Check for priorities file
        priorities_path = os.path.join(self.workspace, "context", "priorities.md")
        if os.path.exists(priorities_path):
            print("  ✓ Priorities file found (context/priorities.md)")
            self.context["priorities_active"] = True
        else:
            print("  ✗ Priorities file missing")
            self.context["priorities_active"] = False

    # --- 2. CONNECTIONS LAYER ---
    def load_connections(self):
        print("\n[2/4] Initializing Connections...")
        # Check if environment file is present
        env_path = os.path.join(self.workspace, ".env")
        if os.path.exists(env_path):
            print("  ✓ Environment variables loaded (.env)")
            self.connections["env_configured"] = True
        else:
            print("  ✗ Environment variables file (.env) missing")
            self.connections["env_configured"] = False
            
        # Check for Notion configuration token
        notion_token = os.environ.get("NOTION_INTEGRATION_TOKEN") or "ntn_mock_token_12345"
        print(f"  ✓ Notion API connection established (Token: {notion_token[:8]}...)")
        
        # Check for Google Drive token
        token_path = os.path.join(self.workspace, "token.json")
        if os.path.exists(token_path):
            print("  ✓ Google Drive OAuth connection: ACTIVE (token.json present)")
            self.connections["gdrive_connected"] = True
        else:
            print("  ✗ Google Drive OAuth connection: PENDING (token.json missing)")
            self.connections["gdrive_connected"] = False

    # --- 3. CAPABILITIES LAYER ---
    def load_capabilities(self):
        print("\n[3/4] Scanning installed Agent Skills...")
        skills_dir = os.path.join(self.workspace, ".antigravity", "skills")
        if os.path.exists(skills_dir):
            for skill_folder in os.listdir(skills_dir):
                skill_path = os.path.join(skills_dir, skill_folder, "SKILL.md")
                if os.path.exists(skill_path):
                    print(f"  ✓ Loaded capability: /{skill_folder}")
                    self.skills.append(skill_folder)
        else:
            print("  ✗ No local skills directory found")

    # --- 4. CADENCE LAYER ---
    def execute_cadence(self):
        print("\n[4/4] Executing Cadence Hooks...")
        print("  ✓ Checking for scheduled tasks...")
        # Mock daily briefing trigger
        print("  ⚡ Daily Briefing Hook fired: 'Good morning Parth! Here is your study queue for today.'")

    # --- RUN THE OS ---
    def run_diagnostic(self):
        print("=========================================")
        print("     PARTH'S AIOS DIAGNOSTIC RUN         ")
        print("=========================================")
        self.load_context()
        self.load_connections()
        self.load_capabilities()
        self.execute_cadence()
        print("=========================================")
        print("Diagnostics completed. AIOS status: STABLE")
        print("=========================================")

if __name__ == "__main__":
    # Get workspace root relative to this file
    workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Initialize and run
    aios = MockAIOS(workspace_root)
    aios.run_diagnostic()
