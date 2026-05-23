import os
import json
import urllib.request
from datetime import datetime

def main():
    print("Fetching Catalog API...")
    url = 'https://learn.microsoft.com/api/catalog/'
    req = urllib.request.urlopen(url)
    catalog = json.loads(req.read())
    print("Catalog fetched successfully.")
    
    # Map target paths/modules
    courses = [
        {
            "id": 1,
            "uid": "learn.wwl.get-started-microsoft-365-copilot-business-chat",
            "type": "module",
            "category": "Copilot",
            "short_name": "1_get_started_copilot_chat",
            "url": "https://learn.microsoft.com/en-us/plans/k72rs2tq8o2w17?learnerGroupId=5bc70771-fa00-4bb0-9c1d-b71e639e0bc3"
        },
        {
            "id": 2,
            "uid": "learn.explore-microsoft-copilot-business-users",
            "type": "module",
            "category": "Copilot",
            "short_name": "2_work_smarter_copilot",
            "url": "https://learn.microsoft.com/en-us/plans/gxqrt3txxrqqe7?learnerGroupId=6a70099d-150e-4d53-8cd4-7a95c5852ebc"
        },
        {
            "id": 3,
            "uid": "learn.wwl.implement-no-code-copilot-agents-microsoft-365-sharepoint",
            "type": "path",
            "category": "Copilot",
            "short_name": "3_transform_everyday_work_agents",
            "url": "https://learn.microsoft.com/en-us/plans/d8qzu1tw5n88nr?learnerGroupId=bd4d84b8-5fb0-4fa1-b703-b2f1553f6a4e"
        },
        {
            "id": 4,
            "uids": ["learn.philanthropies.explore-generative-ai", "learn.philanthropies.explore-ai-basics"],
            "type": "combo",
            "category": "AI",
            "title": "Explore AI basics and Generative AI",
            "short_name": "4_explore_ai_basics_generative_ai",
            "url": "https://learn.microsoft.com/en-us/plans/r3wnt2tp27mwmp?learnerGroupId=f4a8bfe0-65d4-42e8-8f06-459eee7a5dcc"
        },
        {
            "id": 5,
            "uid": "learn.wwl.get-started-ai-fundamentals",
            "type": "module",
            "category": "AI",
            "short_name": "5_learn_more_ai_concepts",
            "url": "https://learn.microsoft.com/en-us/plans/1ejxsot6dkmjge?learnerGroupId=1c40f7ab-24ba-4f1b-b23c-ab5d0b9886e5"
        },
        {
            "id": 6,
            "uid": "learn.wwl.develop-computer-vision-with-foundry",
            "type": "path",
            "category": "AI",
            "short_name": "6_develop_computer_vision_solutions",
            "url": "https://learn.microsoft.com/en-us/plans/1ejxsotx50wj2z?learnerGroupId=113e84c2-bee0-414c-906e-ffc477a74738"
        },
        {
            "id": 7,
            "uid": "learn.wwl.describe-basic-concepts-of-cybersecurity",
            "type": "path",
            "category": "Security",
            "short_name": "7_describe_concepts_cybersecurity",
            "url": "https://learn.microsoft.com/en-us/plans/okwrbgt8p22qy8?learnerGroupId=7bd5ecc7-27d4-44b1-a6b5-4ddc887d394a"
        },
        {
            "id": 8,
            "uid": "learn.wwl.describe-concepts-of-security-compliance-identity",
            "type": "path",
            "category": "Security",
            "short_name": "8_intro_security_compliance_identity",
            "url": "https://learn.microsoft.com/en-us/plans/p3wntztymyeymw?learnerGroupId=30f7ba8b-3274-42ae-bfdd-ed0a75ab1f93"
        },
        {
            "id": 9,
            "uid": "learn.wwl.describe-capabilities-of-microsoft-security-solutions",
            "type": "path",
            "category": "Security",
            "short_name": "9_intro_microsoft_security_solutions",
            "url": "https://learn.microsoft.com/en-us/plans/3op7a6tm28dkdz?learnerGroupId=98f0867f-9b78-484a-b379-3d07b797a181"
        }
    ]
    
    modules_map = {m['uid']: m for m in catalog.get('modules', [])}
    paths_map = {p['uid']: p for p in catalog.get('learningPaths', [])}
    units_map = {u['uid']: u for u in catalog.get('units', [])}
    
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_dir = os.path.join(workspace_root, 'study', 'AI_Skills_Yatra')
    os.makedirs(base_dir, exist_ok=True)
    
    # Subfolders
    for cat in ['Copilot', 'AI', 'Security']:
        os.makedirs(os.path.join(base_dir, cat), exist_ok=True)
        
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    for c in courses:
        title = ""
        tasks = []
        resources = [f"[Official Microsoft Learn Link]({c['url']})"]
        concepts = []
        
        if c['type'] == 'module':
            m = modules_map.get(c['uid'])
            if m:
                title = m['title']
                for u_uid in m.get('units', []):
                    if u_uid in units_map:
                        tasks.append(f"Complete Unit: {units_map[u_uid]['title']}")
                concepts = [
                    f"Explain the main objective of {title} in your own words.",
                    "Complete the Module Assessment with a passing score."
                ]
        elif c['type'] == 'path':
            p = paths_map.get(c['uid'])
            if p:
                title = p['title']
                for m_uid in p.get('modules', []):
                    if m_uid in modules_map:
                        tasks.append(f"Complete Module: {modules_map[m_uid]['title']}")
                        # also add units as nested tasks
                        for u_uid in modules_map[m_uid].get('units', []):
                            if u_uid in units_map:
                                tasks.append(f"  - Complete Unit: {units_map[u_uid]['title']}")
                concepts = [
                    f"Explain the primary architecture and capability definitions of {title}.",
                    "Pass all knowledge checks for all modules in this path."
                ]
        elif c['type'] == 'combo':
            title = c['title']
            for m_uid in c['uids']:
                m = modules_map.get(m_uid)
                if m:
                    tasks.append(f"Complete Module: {m['title']}")
                    for u_uid in m.get('units', []):
                        if u_uid in units_map:
                            tasks.append(f"  - Complete Unit: {units_map[u_uid]['title']}")
            concepts = [
                "Differentiate between traditional AI and Generative AI systems.",
                "Describe the mechanical role of deep neural networks in computer vision."
            ]
            
        # Format the checklist content
        checklist_content = f"""# {title} — Assignment Checklist
> Course: **AI Skills Yatra by Microsoft** | Generated: {date_str}

---

## ✅ Practice Tasks

"""
        for t in tasks:
            checklist_content += f"- [ ] {t}\n"
            
        checklist_content += """
---

## 🔍 Concept Checks

"""
        for cp in concepts:
            checklist_content += f"- [ ] {cp}\n"
            
        checklist_content += """
---

## 🔗 Resources Reviewed

"""
        for r in resources:
            checklist_content += f"- [ ] {r}\n"
            
        checklist_content += """
---

## 📝 Notes

> Add your observations here after completing each task.
"""
        
        # Write to file
        file_path = os.path.join(base_dir, c['category'], f"{c['short_name']}.md")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(checklist_content)
        print(f"Created checklist: {file_path}")

if __name__ == '__main__':
    main()
