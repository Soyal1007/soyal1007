"""
Centralized configuration for GitHub Profile README & SVG Generators.
User can edit information here to automatically update generated profile assets.
"""

# GitHub Account Info
USERNAME = "Soyal1007"
FULL_NAME = "Soyal"
CURRENT_ROLE = "Full-Stack Developer & Software Engineer"
LOCATION = "India"
BIO = "Passionate developer crafting modern web applications, mobile platforms, and high-performance developer tools."
AVATAR_URL = f"https://avatars.githubusercontent.com/u/150875873?v=4"

# Tech Stack Categorized
TECH_STACK = {
    "Languages": ["Python", "JavaScript", "TypeScript", "Dart", "C++", "HTML5/CSS3"],
    "Frameworks": ["Flutter", "React", "Next.js", "Node.js", "Express"],
    "Tools & Platforms": ["Git", "GitHub Actions", "Docker", "VS Code", "Android Studio"],
    "Databases": ["SQLite", "PostgreSQL", "MongoDB", "Firebase"]
}

# Social / Contact Links
SOCIAL_LINKS = {
    "GitHub": f"https://github.com/{USERNAME}",
    "Email": "mailto:soyal@example.com",
}

# Featured Projects
FEATURED_PROJECTS = [
    {
        "name": "RAKSHAK / SafeHer",
        "desc": "Intelligent personal emergency safety platform featuring voice-triggered SOS activation, live audio/video evidence capture, and emergency dispatch.",
        "tech": ["Flutter", "Android", "Firebase"],
        "url": f"https://github.com/{USERNAME}/SafeHer-"
    },
    {
        "name": "smart-print",
        "desc": "Automated smart printing & document transformation utility for CLI and automated workflows.",
        "tech": ["Python", "CLI", "Automation"],
        "url": f"https://github.com/{USERNAME}/smart-print"
    },
    {
        "name": "Personal Command Center",
        "desc": "Feature-rich browser extension dashboard featuring rapid note capture, page saving, timeline search, and local persistence.",
        "tech": ["JavaScript", "WebExtensions", "CSS3"],
        "url": f"https://github.com/{USERNAME}"
    }
]
