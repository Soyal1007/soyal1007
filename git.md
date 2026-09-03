# Build a Premium Animated GitHub Profile README

You are an expert full-stack developer, GitHub profile designer, SVG animator, Python developer, and GitHub Actions engineer.

I want you to build a **professional, premium, technically impressive animated GitHub profile README** for my personal GitHub account.

This is not a temporary demo. The final result will be publicly visible on my GitHub profile, so prioritize:

* Professionalism
* Clean visual hierarchy
* Strong first impression
* Readability
* Reliability
* Maintainability
* Fast loading
* GitHub compatibility
* Originality
* Subtle, high-quality animation
* Correct repository structure
* No broken images
* No unnecessary complexity

Use this article as a technical reference for the animated SVG/contribution concept:

https://www.avivashishta.com/blog/build-animated-github-profile-readme.html

Do NOT blindly copy the author's personal information, branding, wording, or design. Build an original implementation inspired by the underlying technical approach.

---

# 1. FIRST: INSPECT THE ENVIRONMENT

Before writing code:

1. Inspect the current repository.
2. Determine the GitHub username from the repository name or git remote.
3. Inspect whether any files already exist.
4. Do not overwrite existing work unnecessarily.
5. Determine whether the default branch is `main` or another branch.
6. Check whether Python is installed.
7. Check whether Git is configured.
8. Check whether GitHub Actions configuration already exists.

If something important is missing, make a sensible decision rather than stopping unnecessarily.

Do NOT ask me unnecessary questions.

---

# 2. TARGET RESULT

The final GitHub profile should feel like a polished developer portfolio rather than a generic README.

The visual concept should be:

**Premium terminal / modern developer aesthetic**

The profile should communicate:

* Who I am
* What I build
* What technologies I use
* What I am interested in
* My major projects
* My GitHub activity
* Ways to connect with me

The profile should not look childish, overloaded, or like a collection of random GitHub badges.

Avoid:

* Excessive emojis
* Huge walls of text
* 20+ technology badges
* Random GIFs
* Low-quality animations
* Generic motivational quotes
* Fake statistics
* Fake achievements
* Excessive neon effects
* Visual clutter

Use animation as a design enhancement, not as a gimmick.

---

# 3. PROJECT ARCHITECTURE

Create a clean structure similar to:

YOUR_USERNAME/
│
├── README.md
│
├── source-photo.jpg
│
├── avi-ascii.svg
├── info-card.svg
├── contrib-heatmap.svg
│
├── data/
│   └── contributions.json
│
├── scripts/
│   ├── requirements.txt
│   ├── prep_photo.py
│   ├── make_ascii_svg.py
│   ├── make_info_card.py
│   ├── fetch_contributions.py
│   └── render_heatmap_svg.py
│
└── .github/
└── workflows/
└── update-profile-art.yml

You may improve the architecture if there is a technically superior approach, but keep it simple and understandable.

Do not create unnecessary files.

---

# 4. README DESIGN

The README is the most important part because it is displayed directly on my GitHub profile.

Design it with a strong visual hierarchy.

Suggested structure:

1. Animated hero / identity section
2. Short introduction
3. Animated contribution visualization
4. About / current focus
5. Tech stack
6. Featured projects
7. GitHub statistics
8. Contact / social links
9. Small closing statement

However, don't blindly follow this structure if a better composition exists.

The top portion must immediately communicate my identity.

Use centered layouts where appropriate.

Keep the README relatively compact.

---

# 5. HERO SECTION

Create a premium hero section.

Use a terminal-inspired heading such as:

`username@github ~ $ whoami`

or another sophisticated variation.

Do not make it look like a cheap hacker template.

The hero should include:

* My name
* Developer/student identity
* Short professional description
* Key interests
* Links where appropriate

Keep the wording concise.

Do not invent professional experience, awards, companies, certifications, or achievements.

Only use information that I provide or that can safely be derived from my existing repository/profile.

---

# 6. ANIMATED ASCII PORTRAIT

Implement an animated ASCII portrait inspired by the article.

Pipeline:

source-photo.jpg
↓
prep_photo.py
↓
source-prepped.png
↓
make_ascii_svg.py
↓
avi-ascii.svg

Requirements:

* Remove background where practical.
* Normalize the image.
* Convert appropriately to grayscale.
* Maintain facial proportions.
* Use a carefully selected ASCII character density ramp.
* Generate SVG rather than a raster GIF.
* Animate subtly using SVG animation.
* Avoid excessive flashing or distracting movement.
* Make the portrait look intentional and premium.

Use SVG/SMIL or another GitHub-compatible mechanism.

Do not depend on JavaScript inside the SVG.

Make sure the generated SVG works when referenced from README.md using:

`<img src="./avi-ascii.svg">`

---

# 7. INFORMATION CARD

Create a terminal-style animated information card.

Generate:

`info-card.svg`

It should visually complement the ASCII portrait.

The card should support information such as:

* Current role
* Education/status
* Primary stack
* Current focus
* Interests
* Projects
* Areas of exploration

Use a clean terminal-inspired design.

Animation should be subtle:

* line-by-line reveal
* cursor effect
* small typing/reveal transitions
* restrained looping

Do NOT create a noisy animation.

Make the card readable on both desktop and smaller screens.

---

# 8. GITHUB CONTRIBUTION HEATMAP

Implement the animated contribution heatmap concept from the reference article.

Pipeline:

GitHub contribution page
↓
fetch_contributions.py
↓
data/contributions.json
↓
render_heatmap_svg.py
↓
contrib-heatmap.svg

Requirements:

* Fetch publicly available contribution data.
* Do not hard-code contribution counts.
* Do not fabricate GitHub activity.
* Handle GitHub HTML structure carefully.
* Fail gracefully if GitHub changes its HTML.
* Store structured data in JSON.
* Generate the SVG from the JSON.
* Animate the heatmap subtly.
* Use contribution intensity levels.
* Keep dimensions appropriate for a GitHub README.
* Ensure SVG is valid XML.

Do not require a GitHub Personal Access Token unless absolutely necessary.

Prefer the public contribution data approach from the reference implementation.

---

# 9. GITHUB ACTIONS

Create:

`.github/workflows/update-profile-art.yml`

The workflow should:

1. Run on a daily schedule.
2. Allow manual execution using `workflow_dispatch`.
3. Check out the repository.
4. Install the required Python version.
5. Install dependencies.
6. Fetch current contribution data.
7. Generate the contribution SVG.
8. Commit changes only when files actually changed.
9. Push changes back to the repository.

Use the minimum required GitHub permissions.

For example, use appropriate repository contents write permissions only where required.

Do not expose secrets.

Do not create unnecessary GitHub tokens.

The workflow should be reliable and easy to debug.

---

# 10. PYTHON QUALITY

Write production-quality Python.

Requirements:

* Python 3.11+
* Clear function separation
* Meaningful variable names
* Helpful comments only where needed
* Error handling
* Useful command-line errors
* No unnecessary dependencies
* Cross-platform compatibility where practical
* Avoid hard-coded absolute paths
* Use `pathlib`
* Use deterministic output where possible

Scripts should work when executed from the repository root.

For example:

`python scripts/prep_photo.py source-photo.jpg`

and:

`python scripts/fetch_contributions.py`

and:

`python scripts/render_heatmap_svg.py`

---

# 11. DEPENDENCIES

Create:

`scripts/requirements.txt`

Only include dependencies that are actually required.

Pin versions where appropriate for GitHub Actions reliability.

Do not install enormous frameworks for simple functionality.

If `rembg`, OpenCV, Pillow, NumPy, BeautifulSoup, or Requests are required, use them appropriately.

Do not introduce unnecessary ML models or huge assets simply for visual effects.

---

# 12. PERSONALIZATION

Use my actual GitHub username.

Do not invent personal information.

If information is not available, use a clearly marked placeholder in the source code rather than inventing facts.

Create a clearly identifiable configuration section, for example:

```python
PROFILE_NAME = "YOUR NAME"
CURRENT_ROLE = "..."
FOCUS = "..."
STACK = "..."
INTERESTS = "..."
```

Make it extremely easy for me to edit later.

If possible, centralize personal information so I don't have to modify multiple files.

---

# 13. TECH STACK SECTION

Create a clean technology section.

Prioritize technologies I actually use.

Do not list every technology imaginable.

Prefer categories such as:

* Languages
* Frameworks
* Tools
* Databases
* Platforms

Use clean icons or simple text where appropriate.

Avoid turning the profile into a badge wall.

---

# 14. FEATURED PROJECTS

Create a professional featured-project section.

Only include projects that actually exist or that I explicitly provide.

For each project, show:

* Project name
* One-line description
* Main technologies
* GitHub link

Keep each description short.

If the repository contains known projects, inspect them and use their actual information instead of inventing descriptions.

Do not claim a project is production-ready unless that is demonstrably true.

---

# 15. STATISTICS

If GitHub statistics are used, make sure they are legitimate and stable.

Avoid unreliable third-party statistic services if a native or simpler solution exists.

Do not display fake:

* Stars
* Followers
* Contributions
* Ranking
* Commit counts

If a statistic service is used, isolate it so the profile still looks acceptable if the service becomes unavailable.

---

# 16. SOCIAL / CONTACT SECTION

Include only links that actually exist.

Potential examples:

* GitHub
* LinkedIn
* Portfolio
* Email
* Other professional profiles

Do not invent URLs.

Use clean icons or text links.

---

# 17. RESPONSIVE / GITHUB COMPATIBILITY

GitHub README rendering has limitations.

Do not use:

* JavaScript
* React
* CSS files that GitHub won't render
* external scripts
* unsupported HTML
* complex browser-dependent behavior

Prefer:

* Markdown
* safe HTML
* SVG
* `<img>`
* tables only where useful

Make sure the README renders correctly on GitHub.

---

# 18. SVG QUALITY

Every generated SVG must:

* Be valid XML
* Have explicit dimensions/viewBox
* Render without external dependencies
* Avoid broken references
* Avoid JavaScript
* Use readable typography
* Have sensible file size

Do not create unnecessarily enormous SVG files.

Optimize generated SVGs where practical.

---

# 19. ANIMATION PRINCIPLES

The profile should feel alive, but professional.

Use animation for:

* reveal
* subtle movement
* contribution progression
* terminal cursor
* typing effect
* gentle transitions

Do NOT use:

* flashing backgrounds
* rapidly changing colors
* excessive blinking
* seizure-triggering effects
* chaotic movement

The animation should still look good if the user ignores it.

---

# 20. ACCESSIBILITY

Where practical:

* Add useful `alt` text to images.
* Maintain readable contrast.
* Don't communicate essential information only through color.
* Keep text readable.
* Avoid excessive animation.

The profile should remain understandable even if SVG animation is not supported.

---

# 21. PERFORMANCE

Optimize for GitHub.

The final profile should load quickly.

Avoid:

* huge images
* unnecessary external assets
* enormous SVGs
* dozens of remote services
* unnecessary API calls

The profile should still look premium without being technically bloated.

---

# 22. LOCAL TESTING

After creating the project:

1. Install dependencies.
2. Run every Python script.
3. Generate every SVG.
4. Validate the SVG files.
5. Inspect generated files.
6. Check that all README image paths are correct.
7. Check that the workflow YAML is valid.
8. Run the contribution fetching process.
9. Confirm JSON is valid.
10. Confirm the repository contains all required files.

If possible, render or inspect the SVGs locally.

Do not declare success just because the scripts execute without an exception.

Actually verify that the generated assets are usable.

---

# 23. GIT WORKFLOW

Do not push anything automatically unless I explicitly ask you to.

You may prepare the repository for commit.

Before finishing, show me:

* files created
* files modified
* commands executed
* tests performed
* any remaining manual steps

Do not delete unrelated existing files.

---

# 24. README SAFETY CHECK

Before finishing, verify that:

Every image path in README.md exists.

For example:

`./avi-ascii.svg`

must actually exist.

`./info-card.svg`

must actually exist.

`./contrib-heatmap.svg`

must actually exist.

Do not use broken external image URLs.

---

# 25. GITHUB ACTION SAFETY CHECK

Verify that:

* YAML syntax is valid.
* Workflow has `workflow_dispatch`.
* Workflow has a daily schedule.
* Python version is valid.
* Dependencies install correctly.
* Scripts execute from repository root.
* Generated files are committed only when changed.
* GitHub Actions has the required permission.
* No secret/token is accidentally hard-coded.

---

# 26. DESIGN DIRECTION

Use this overall visual direction:

**Premium + Minimal + Terminal + Modern Developer**

Think:

* sophisticated developer portfolio
* clean terminal UI
* restrained monochrome base
* carefully used accent color
* crisp typography
* generous spacing
* subtle animation
* strong hierarchy

Do not make it look like:

* a gaming profile
* an anime profile
* a hacker cliché
* a cyberpunk template
* a badge collection
* a generic AI-generated README

The result should look like someone intentionally designed their developer identity.

---

# 27. IMPORTANT: DO NOT COPY THE REFERENCE AUTHOR

The linked article is only a technical reference.

Do not use:

* the author's name
* the author's photo
* the author's biography
* the author's projects
* the author's links
* the author's personal statistics
* the author's exact wording
* the author's personal branding

Build an original profile for me.

---

# 28. ERROR HANDLING

If something fails:

1. Diagnose the actual cause.
2. Fix the implementation.
3. Re-run the failing step.
4. Do not simply suppress the error.
5. Do not replace functionality with fake placeholder output.
6. Do not tell me something works unless you actually tested it.

If a dependency is problematic on Windows, find a practical alternative or explain exactly what needs to be installed.

---

# 29. FINAL DELIVERABLE

At the end, I want a complete working repository containing:

* README.md
* animated ASCII portrait
* animated information card
* animated GitHub contribution heatmap
* contribution JSON data
* Python generation scripts
* dependency file
* GitHub Actions workflow
* clean folder structure
* professional design
* no fake information
* no broken paths

The final result should be ready for me to commit and push to my GitHub profile repository.

---

# 30. FINAL RESPONSE TO ME

After implementation, do NOT give me a huge explanation.

Give me:

### 1. What you built

Short summary.

### 2. Files created

List them.

### 3. Tests completed

List what you actually tested.

### 4. Manual steps I need to do

For example:

```text
1. Add source-photo.jpg
2. Edit personal information
3. Review README.md
4. git add .
5. git commit -m "Create premium profile"
6. git push origin main
7. Open GitHub → Actions
8. Run "Update Profile Art"
```

### 5. Any issues

Be honest about anything that remains unresolved.

Do not claim the project is complete if it is not.

---

# START NOW

Begin by inspecting the repository and environment.

Then implement the complete system.

Do not stop after creating a plan.

Actually create the files, write the code, run the scripts, test the output, and fix problems you encounter.

Prioritize correctness and professional visual quality over speed.
