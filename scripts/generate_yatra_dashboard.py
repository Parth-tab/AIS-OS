import os
import json
import urllib.request

def main():
    print("Fetching Catalog API...")
    url = 'https://learn.microsoft.com/api/catalog/'
    req = urllib.request.urlopen(url)
    catalog = json.loads(req.read())
    print("Catalog fetched successfully.")
    
    modules_map = {m['uid']: m for m in catalog.get('modules', [])}
    paths_map = {p['uid']: p for p in catalog.get('learningPaths', [])}
    units_map = {u['uid']: u for u in catalog.get('units', [])}
    
    # Define our yatra structure
    yatra = [
        {
            "category": "AI-Powered Work",
            "badge": "Copilot",
            "color": "#f59e0b",
            "courses": [
                {
                    "level": "Day 1 Target",
                    "title": "Get started with Microsoft 365 Copilot Chat",
                    "uid": "learn.wwl.get-started-microsoft-365-copilot-business-chat",
                    "type": "module",
                    "link": "Copilot/1_get_started_copilot_chat.md"
                },
                {
                    "level": "Day 1 Target",
                    "title": "Work smarter with AI using Microsoft Copilot",
                    "uid": "learn.explore-microsoft-copilot-business-users",
                    "type": "module",
                    "link": "Copilot/2_work_smarter_copilot.md"
                },
                {
                    "level": "Day 2 Target",
                    "title": "Transform your everyday work with agents",
                    "uid": "learn.wwl.implement-no-code-copilot-agents-microsoft-365-sharepoint",
                    "type": "path",
                    "link": "Copilot/3_transform_everyday_work_agents.md"
                }
            ]
        },
        {
            "category": "Building with AI",
            "badge": "AI",
            "color": "#10b981",
            "courses": [
                {
                    "level": "Day 3 Target",
                    "title": "Explore AI basics and Generative AI",
                    "uids": ["learn.philanthropies.explore-generative-ai", "learn.philanthropies.explore-ai-basics"],
                    "type": "combo",
                    "link": "AI/4_explore_ai_basics_generative_ai.md"
                },
                {
                    "level": "Day 3 Target",
                    "title": "Learn more on the AI concepts",
                    "uid": "learn.wwl.get-started-ai-fundamentals",
                    "type": "module",
                    "link": "AI/5_learn_more_ai_concepts.md"
                },
                {
                    "level": "Day 4 Target",
                    "title": "Develop computer vision solutions in Azure",
                    "uid": "learn.wwl.develop-computer-vision-with-foundry",
                    "type": "path",
                    "link": "AI/6_develop_computer_vision_solutions.md"
                }
            ]
        },
        {
            "category": "Security in the AI Era",
            "badge": "Security",
            "color": "#3b82f6",
            "courses": [
                {
                    "level": "Day 5 Target",
                    "title": "Describe the concepts of cybersecurity",
                    "uid": "learn.wwl.describe-basic-concepts-of-cybersecurity",
                    "type": "path",
                    "link": "Security/7_describe_concepts_cybersecurity.md"
                },
                {
                    "level": "Day 5 Target",
                    "title": "Introduction to security, compliance, and identity concepts",
                    "uid": "learn.wwl.describe-concepts-of-security-compliance-identity",
                    "type": "path",
                    "link": "Security/8_intro_security_compliance_identity.md"
                },
                {
                    "level": "Day 6 Target",
                    "title": "Introduction to Microsoft security solutions",
                    "uid": "learn.wwl.describe-capabilities-of-microsoft-security-solutions",
                    "type": "path",
                    "link": "Security/9_intro_microsoft_security_solutions.md"
                }
            ]
        }
    ]
    
    # Populate subunits for each course
    for cat in yatra:
        for course in cat['courses']:
            course['subitems'] = []
            if course['type'] == 'module':
                m = modules_map.get(course['uid'])
                if m:
                    course['duration'] = m.get('duration_in_minutes', 0)
                    for u_uid in m.get('units', []):
                        if u_uid in units_map:
                            course['subitems'].append({
                                "title": units_map[u_uid]['title'],
                                "uid": u_uid,
                                "type": "unit"
                            })
            elif course['type'] == 'path':
                p = paths_map.get(course['uid'])
                if p:
                    course['duration'] = p.get('duration_in_minutes', 0)
                    for m_uid in p.get('modules', []):
                        if m_uid in modules_map:
                            m_title = modules_map[m_uid]['title']
                            course['subitems'].append({
                                "title": m_title,
                                "uid": m_uid,
                                "type": "module_header"
                            })
                            for u_uid in modules_map[m_uid].get('units', []):
                                if u_uid in units_map:
                                    course['subitems'].append({
                                        "title": units_map[u_uid]['title'],
                                        "uid": u_uid,
                                        "type": "unit"
                                    })
            elif course['type'] == 'combo':
                course['duration'] = 0
                for m_uid in course['uids']:
                    m = modules_map.get(m_uid)
                    if m:
                        course['duration'] += m.get('duration_in_minutes', 0)
                        course['subitems'].append({
                            "title": m['title'],
                            "uid": m_uid,
                            "type": "module_header"
                        })
                        for u_uid in m.get('units', []):
                            if u_uid in units_map:
                                course['subitems'].append({
                                    "title": units_map[u_uid]['title'],
                                    "uid": u_uid,
                                    "type": "unit"
                                })

    # Generate HTML code
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Paathshala — Microsoft AI Skills Yatra Planner</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.45);
            --card-border: rgba(255, 255, 255, 0.08);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent-yellow: #ffb900;
            --accent-cyan: #06b6d4;
            --font-display: 'Outfit', sans-serif;
            --font-body: 'Inter', sans-serif;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(at 10% 20%, rgba(30, 41, 59, 0.5) 0px, transparent 50%),
                radial-gradient(at 90% 80%, rgba(15, 23, 42, 0.8) 0px, transparent 50%);
            color: var(--text-main);
            font-family: var(--font-body);
            min-height: 100vh;
            padding: 2rem 1.5rem;
            line-height: 1.5;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            margin-bottom: 2.5rem;
        }

        h1 {
            font-family: var(--font-display);
            font-size: 3rem;
            font-weight: 700;
            letter-spacing: -0.025em;
            margin-bottom: 0.5rem;
            background: linear-gradient(to right, #ffb900, #ff8c00);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .subtitle-area {
            max-width: 800px;
            margin: 0 auto;
        }

        .subtitle-title {
            font-family: var(--font-display);
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: var(--text-main);
        }

        .subtitle-desc {
            color: var(--text-muted);
            font-size: 0.95rem;
            margin-bottom: 1.5rem;
        }

        /* Progress Dashboard */
        .progress-dashboard {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 2.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 1.5rem;
        }

        .overall-progress-container {
            flex: 1;
            min-width: 250px;
        }

        .progress-label {
            font-family: var(--font-display);
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            display: flex;
            justify-content: space-between;
        }

        .progress-bar-bg {
            background: rgba(255, 255, 255, 0.08);
            border-radius: 9999px;
            height: 12px;
            overflow: hidden;
            width: 100%;
        }

        .progress-bar-fill {
            background: linear-gradient(90deg, var(--accent-yellow), #ff8c00);
            height: 100%;
            width: 0%;
            transition: width 0.4s ease;
        }

        .stats-grid {
            display: flex;
            gap: 2rem;
        }

        .stat-box {
            text-align: center;
        }

        .stat-val {
            font-family: var(--font-display);
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--accent-yellow);
        }

        .stat-lbl {
            font-size: 0.8rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        /* 3-Column Grid */
        .columns-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
            gap: 1.5rem;
        }

        .column-card {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .column-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        }

        .column-header {
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }

        .badge {
            display: inline-block;
            font-family: var(--font-display);
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 0.25rem 0.6rem;
            border-radius: 4px;
            margin-bottom: 0.5rem;
            color: #000;
        }

        .column-title {
            font-family: var(--font-display);
            font-size: 1.4rem;
            font-weight: 600;
        }

        /* Course Item */
        .course-item {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-radius: 10px;
            margin-bottom: 1rem;
            overflow: hidden;
            transition: border-color 0.2s ease;
        }

        .course-item:hover {
            border-color: rgba(255, 255, 255, 0.1);
        }

        .course-summary {
            padding: 1rem;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .course-info {
            flex: 1;
            padding-right: 0.75rem;
        }

        .course-level {
            font-size: 0.75rem;
            color: var(--accent-yellow);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.15rem;
        }

        .course-name {
            font-size: 0.95rem;
            font-weight: 500;
            color: var(--text-main);
        }

        .course-meta {
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-top: 0.25rem;
            display: flex;
            gap: 0.75rem;
        }

        .course-link {
            color: var(--accent-cyan);
            text-decoration: none;
        }

        .course-link:hover {
            text-decoration: underline;
        }

        .progress-donut-container {
            width: 36px;
            height: 36px;
            position: relative;
        }

        /* Expanding Details */
        .course-details {
            display: none;
            padding: 0 1rem 1rem 1rem;
            border-top: 1px solid rgba(255, 255, 255, 0.03);
            background: rgba(0, 0, 0, 0.1);
        }

        .unit-list {
            list-style: none;
            margin-top: 0.5rem;
        }

        .unit-item {
            display: flex;
            align-items: flex-start;
            gap: 0.5rem;
            padding: 0.35rem 0;
            font-size: 0.85rem;
        }

        .unit-item.module-header {
            font-weight: 600;
            color: var(--accent-cyan);
            font-size: 0.9rem;
            margin-top: 0.5rem;
            padding-bottom: 0.15rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.03);
        }

        .unit-item input[type="checkbox"] {
            margin-top: 0.2rem;
            cursor: pointer;
            accent-color: var(--accent-yellow);
        }

        .unit-title {
            color: var(--text-muted);
            transition: color 0.2s ease;
        }

        .unit-item input[type="checkbox"]:checked + .unit-title {
            color: var(--text-main);
            text-decoration: line-through;
        }

        /* Donut SVG styling */
        svg.donut {
            transform: rotate(-90deg);
        }

        circle.donut-ring {
            stroke: rgba(255, 255, 255, 0.05);
        }

        circle.donut-segment {
            stroke: var(--accent-yellow);
            transition: stroke-dashoffset 0.3s ease;
        }

        .course-item.open .course-details {
            display: block;
        }
        
        .arrow-indicator {
            font-size: 0.75rem;
            color: var(--text-muted);
            transition: transform 0.2s ease;
        }
        
        .course-item.open .arrow-indicator {
            transform: rotate(180deg);
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>AI Paathshala</h1>
            <div class="subtitle-area">
                <div class="subtitle-title">1. Start Learning AI and Unlock Your Digital Badges</div>
                <div class="subtitle-desc">
                    <strong>Summer Sprint (6-Day Plan):</strong> Since you are on summer break, we have accelerated your learning schedule to 3-4 hours a day. Complete this 18-hour Microsoft AI Skills Yatra curriculum in just 6 days!
                </div>
            </div>
        </header>

        <!-- Progress Dashboard -->
        <div class="progress-dashboard">
            <div class="overall-progress-container">
                <div class="progress-label">
                    <span>Overall Yatra Progress</span>
                    <span id="overall-pct">0%</span>
                </div>
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill" id="overall-fill"></div>
                </div>
            </div>
            <div class="stats-grid">
                <div class="stat-box">
                    <div class="stat-val" id="units-completed">0/0</div>
                    <div class="stat-lbl">Units Completed</div>
                </div>
                <div class="stat-box">
                    <div class="stat-val" id="hours-left">18.0</div>
                    <div class="stat-lbl">Hours Left</div>
                </div>
            </div>
        </div>

        <!-- 3-Column Grid -->
        <div class="columns-grid">
    """
    
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_dir = os.path.join(workspace_root, 'study', 'AI_Skills_Yatra')
    
    for cat in yatra:
        html += f"""
            <!-- Column: {cat['category']} -->
            <div class="column-card">
                <div class="column-header">
                    <span class="badge" style="background-color: {cat['color']};">{cat['badge']}</span>
                    <div class="column-title">{cat['category']}</div>
                </div>
                <div class="courses-list">
        """
        for i, course in enumerate(cat['courses']):
            total_units = len([x for x in course['subitems'] if x['type'] == 'unit'])
            meta_str = f"<span>⏱️ {course['duration']} mins</span>"
            meta_str += f"""<span><a class="course-link" href="file:///{base_dir.replace('\\', '/')}/{course['link']}">📋 Checklist</a></span>"""
            
            html += f"""
                    <!-- Course Card -->
                    <div class="course-item" id="course-{course['uid'] if 'uid' in course else course['link'].replace('/', '-').replace('.md', '')}">
                        <div class="course-summary" onclick="toggleDetails(this)">
                            <div class="course-info">
                                <div class="course-level">{course['level']}</div>
                                <div class="course-name">{course['title']}</div>
                                <div class="course-meta">{meta_str}</div>
                            </div>
                            <div style="display: flex; align-items: center; gap: 0.5rem;">
                                <div class="progress-donut-container">
                                    <svg width="36" height="36" viewBox="0 0 36 36" class="donut">
                                        <circle class="donut-ring" cx="18" cy="18" r="15.915" fill="transparent" stroke-width="3"></circle>
                                        <circle class="donut-segment" cx="18" cy="18" r="15.915" fill="transparent" stroke-width="3" 
                                                stroke-dasharray="0 100" stroke-dashoffset="0" id="donut-fill-{course['uid'] if 'uid' in course else course['link'].replace('/', '-').replace('.md', '')}"></circle>
                                    </svg>
                                </div>
                                <span class="arrow-indicator">▼</span>
                            </div>
                        </div>
                        <div class="course-details">
                            <ul class="unit-list">
            """
            
            for item in course['subitems']:
                if item['type'] == 'module_header':
                    html += f"""                                <li class="unit-item module-header">{item['title']}</li>\n"""
                elif item['type'] == 'unit':
                    chk_id = f"chk-{item['uid']}"
                    html += f"""                                <li class="unit-item">
                                    <input type="checkbox" id="{chk_id}" onchange="updateProgress()" data-course="{'course-' + (course['uid'] if 'uid' in course else course['link'].replace('/', '-').replace('.md', ''))}" data-duration="{course['duration'] / total_units if total_units > 0 else 0}">
                                    <span class="unit-title">{item['title']}</span>
                                </li>\n"""
            
            html += """                            </ul>
                        </div>
                    </div>
            """
            
        html += """                </div>
            </div>
        """
        
    html += """
        </div>
    </div>

    <script>
        function toggleDetails(summaryEl) {
            const courseItem = summaryEl.parentElement;
            courseItem.classList.toggle('open');
        }

        function updateProgress() {
            const checkboxes = document.querySelectorAll('input[type="checkbox"]');
            const totalUnits = checkboxes.length;
            let completedUnits = 0;
            let completedMinutes = 0;
            
            // Group by course to update donut charts
            const courseStatus = {};
            
            checkboxes.forEach(cb => {
                const courseId = cb.getAttribute('data-course');
                const duration = parseFloat(cb.getAttribute('data-duration'));
                
                if (!courseStatus[courseId]) {
                    courseStatus[courseId] = { total: 0, completed: 0 };
                }
                
                courseStatus[courseId].total++;
                
                if (cb.checked) {
                    completedUnits++;
                    completedMinutes += duration;
                    courseStatus[courseId].completed++;
                    localStorage.setItem(cb.id, 'true');
                } else {
                    localStorage.removeItem(cb.id);
                }
            });
            
            // Update individual donut charts
            for (const courseId in courseStatus) {
                const status = courseStatus[courseId];
                const pct = status.total > 0 ? Math.round((status.completed / status.total) * 100) : 0;
                const fillEl = document.getElementById('donut-fill-' + courseId.replace('course-', ''));
                if (fillEl) {
                    fillEl.setAttribute('stroke-dasharray', `${pct} ${100 - pct}`);
                }
            }
            
            // Overall stats
            const overallPct = totalUnits > 0 ? Math.round((completedUnits / totalUnits) * 100) : 0;
            document.getElementById('overall-pct').innerText = overallPct + '%';
            document.getElementById('overall-fill').style.width = overallPct + '%';
            document.getElementById('units-completed').innerText = `${completedUnits}/${totalUnits}`;
            
            const totalMinutes = 1073;
            const minutesLeft = Math.max(0, totalMinutes - completedMinutes);
            const hoursLeft = (minutesLeft / 60).toFixed(1);
            document.getElementById('hours-left').innerText = hoursLeft;
        }

        // Restore state on load
        window.addEventListener('DOMContentLoaded', () => {
            const checkboxes = document.querySelectorAll('input[type="checkbox"]');
            checkboxes.forEach(cb => {
                if (localStorage.getItem(cb.id) === 'true') {
                    cb.checked = true;
                }
            });
            updateProgress();
        });
    </script>
</body>
</html>
"""
    
    out_file = os.path.join(base_dir, 'study_planner.html')
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated HTML study planner at: {out_file}")

if __name__ == '__main__':
    main()
