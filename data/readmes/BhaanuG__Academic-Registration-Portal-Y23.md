<div align="center">

<a href="https://github.com/BhaanuG/Academic-Registration-Portal-Y23">
  <img src="public/assets/klef-logo.png" alt="KLEF University Logo" width="340" style="object-fit: contain;" />
</a>

# Academic Registration Portal (Y23 Batch)

### Course Registration and Faculty Preference Platform
**KLEF Deemed to be University (KL University)**  
*Department of Computer Science & Engineering*

<p align="center">
  <b>Built by <a href="mailto:Bhaanugali@gmail.com">Bhaanu G (Bhaanu Gali)</a></b><br/>
  <code>Student ID / Reg No: 2400030952</code> &bull; 
  <a href="mailto:Bhaanugali@gmail.com">Bhaanugali@gmail.com</a> &bull; 
  <a href="mailto:2400030952@kluniversity.in">2400030952@kluniversity.in</a> &bull; 
  <a href="https://github.com/BhaanuG/Academic-Registration-Portal-Y23">GitHub Repository</a>
</p>

---

<p align="center">
  <img src="https://img.shields.io/badge/Active%20Students-1%2C159-blue?style=flat-square" alt="Students" />
  <img src="https://img.shields.io/badge/Faculty%20Members-426-indigo?style=flat-square" alt="Faculty" />
  <img src="https://img.shields.io/badge/Available%20Courses-102-orange?style=flat-square" alt="Courses" />
  <img src="https://img.shields.io/badge/Next.js-16.4.6-black?style=flat-square&logo=next.js" alt="Next.js" />
  <img src="https://img.shields.io/badge/React-19.3.1-61DAFB?style=flat-square&logo=react&logoColor=black" alt="React 19" />
  <img src="https://img.shields.io/badge/Tailwind-v4.0-38BDF8?style=flat-square&logo=tailwindcss&logoColor=white" alt="Tailwind CSS" />
  <img src="https://img.shields.io/badge/Database-SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white" alt="SQLite" />
</p>

</div>

---

## What is this project?

At KL University, every semester over a thousand engineering students need to register for their upcoming courses, pick their subjects, and choose which teachers they want to take classes with.

If you have ever been through university course registration, you know how messy it usually is:
- Registration opens at 9:00 AM, and hundreds of students hit the website at once. The server freezes or crashes.
- A student spends 20 minutes carefully picking subjects. Suddenly their internet drops or the session times out, and every single selection gets wiped clean.
- A student accidentally signs up for a section meant for a completely different department or ends up with two classes scheduled at the exact same hour.
- Nobody knows for sure if their choices went through, and students have to take phone photos of their screens as proof.

I designed and built this portal to completely replace that messy process with a clean, dependable web app that works smoothly on phones, tablets, and laptops. It guides each student step-by-step through choosing their subjects, automatically keeps them in their correct section group, lets them vote for their preferred professors, and saves every single click in the background so nobody ever loses their work.

---

## How does it work for a student?

Here is the exact journey a student goes through when using the portal:

```
[ Step 1: Login ] ──▶ [ Step 2: Overview ] ──▶ [ Step 3: Cluster Cohort ]
Enter ID & Birthday      See progress & counselor    Assigned to S1-S50 or S51-S100
                                                               │
                                                               ▼
[ Step 6: Get Receipts ] ◀── [ Step 5: Faculty Rank ] ◀── [ Step 4: Pick Courses ]
Download PDF & PNG proof     Rank 1st, 2nd, 3rd choices     Pick subjects across 7 buckets
```

### 1. Simple Sign-In (`/KLEF/8-2/GBS.php`)
Students do not need to create a new password or worry about forgotten password links. They simply enter their 10-digit University Registration Number (like `2400030952`) and pick their registered Date of Birth from a clean calendar picker.

### 2. Academic Overview (`Academic-Overview.php`)
Right after signing in, students see their personalized dashboard:
- How many credits they have selected so far vs. how many they need this semester (typically 20 to 24 credits).
- Their assigned academic counselor’s name, employee ID, and contact email.
- Important university guidelines and registration rules.

### 3. Cluster Confirmation (`Cluster-Selection.php`)
To make sure sections don't get overcrowded, the department splits students into two balanced groups based on what technology they are specializing in:
- **Cluster 1 (Sections S1 to S50):** For students specializing in Cloud Architecture, Data Science, Software Engineering, DevOps, Cybersecurity, etc.
- **Cluster 2 (Sections S51 to S100):** For students specializing in Artificial Intelligence, Machine Learning, Robotics, Embedded Systems, etc.

The portal checks the student's degree and automatically locks them into their correct group. Students cannot accidentally pick the wrong group, which eliminates classroom timetable clashes before they can even happen.

### 4. Course Selection (`Subject-Selection.php`)
The university curriculum is arranged into 7 straightforward categories (called "Buckets"):
- **Bucket C0:** Capstone Major Project
- **Bucket C1 & C2:** Open Electives (subjects taken outside computer science, such as Green Technology or Bio-informatics)
- **Bucket C3 & C4:** Professional Electives (advanced technical subjects in their specific field)
- **Bucket C5 & C6:** Practical Skills and Audit Courses (Campus Recruitment Training, Ethics, and Constitution of India)

As the student clicks their subjects, a live counter on screen updates their credits in real time, so they never submit under or over the required credit limit.

### 5. Ranking Preferred Teachers (`Faculty-Preferences.php`)
This is one of the most important parts of the platform:
- For every subject they picked, students get to submit their **1st, 2nd, and 3rd choice professors** for lectures.
- The system is smart: when a student picks a lecture professor who teaches in section `S-58`, the portal automatically pulls up the specific laboratory instructors and tutorial mentors tied to that exact section. The student can then rank their sub-preferences for labs (`A`, `B`, `C`) as well.

### 6. Saving and Getting Proof (`My-Preference.php`)
When finished, the student sees a clean summary table of all their chosen subjects, section numbers, and faculty rankings.
- **Download PDF Directory:** Downloads a complete, official PDF list of all professors available in their cohort.
- **Download PNG Receipt:** Generates an official image card summarizing their submitted preferences with their name, registration number, and timestamp.

---

## Why this portal is different

### 1. Zero data loss (Instant auto-save)
Traditional forms only save when you reach the very end and press a big "Submit" button. If anything goes wrong before that click, everything is lost.

In this portal, **every single selection is saved the moment you make it**. If you pick a subject, it saves in 2 milliseconds. If you change a professor preference, it saves immediately. You can close your browser tab, turn off your computer, or log in from a friend’s laptop tomorrow, and every single choice you made is still there exactly as you left it. There are no distracting popup boxes or "Saving..." spinners interrupting you.

### 2. Automatic branch-to-section matching
In huge batches with over 1,000 students, sorting who belongs in which classroom is usually a massive headache for college staff. Here, the system handles it automatically. The moment a student logs in, the portal identifies their branch and locks them to their proper cohort (`Cluster 1` or `Cluster 2`). Students don't have to guess or ask their classmates which section number they are supposed to take.

### 3. Fair and structured teacher selection
Instead of a chaotic "first-come, first-served" free-for-all where students scramble for popular teachers, this portal collects 1st, 2nd, and 3rd preferences from everyone in a clean, orderly way. The department can then use these rankings to distribute classroom seats fairly.

### 4. An admin dashboard for university staff
College coordinators have their own separate administrative dashboard (`/KLEF/8-2/Admin/G-Bhaanu-Sai/Dashboard.php`). From here, administrators can:
- Search and filter all 1,159 student profiles by branch, section, or name.
- View all 426 faculty members and see which sections they are assigned to teach.
- Add, update, or correct student and course records on the fly.
- See live counts of how many students have registered and how classroom seats are filling up.

---

## Real numbers behind this portal

I built and tested this project using the actual academic data for our Y23 batch:

| What it tracks | Total Count | What this means |
| :--- | :--- | :--- |
| **Total Enrolled Students** | **1,159 Students** | Every student in the batch has a record in the database. |
| **Total Teaching Faculty** | **426 Teachers** | Full roster of professors, associate professors, and lab mentors. |
| **Classroom Allocations** | **682 Allocations** | Real-world teaching assignments across lectures, practicals, and tutorials. |
| **Total Courses Offered** | **102 Courses** | Complete list of core subjects and electives available to choose from. |
| **Curricular Buckets** | **9 Buckets (C0 to C8)** | Structured course groups required for degree completion. |
| **Specialization Tracks** | **17 Disciplines** | Including Artificial Intelligence, Cloud Computing, Cybersecurity, Robotics, and DevOps. |
| **Section Groups** | **2 Clusters** | `Cluster 1` (Sections S1–S50: 646 students) and `Cluster 2` (Sections S51–S100: 512 students). |

---

## Breakdown of the 17 Specializations

Here is how the university’s degree specializations are distributed between the two cohorts in the portal:

### Cluster 1 (Sections S1 through S50 — 646 Students)
- Data Science and Big Data Analytics (87 students)
- Cyber Security and Blockchain Technology (128 students)
- Data Engineering for AI (95 students)
- Software Modelling and DevOps (87 students)
- Cloud Native Software Engineering (62 students)
- Cloud Infrastructure Design and Engineering (57 students)
- Distributed Ledger Analytics (36 students)
- Cloud and Edge Computing (30 students)
- Social and Digital Media Analytics (26 students)
- Blockchain Engineering for Web3 (23 students)
- Game Development and UX Design (15 students)

### Cluster 2 (Sections S51 through S100 — 512 Students)
- AI for Computational Intelligence (191 students)
- AI Systems for Visual Intelligence (171 students)
- AI-Driven Language Technologies (124 students)
- AI-Driven Edge Architectures and Applications (13 students)
- AI and Autonomous Systems (9 students)
- Robotics and Automation (4 students)

---

## Complete page address map

All pages in the portal use clean `.php` addresses matching university enterprise conventions:

| View | Web Address | Who uses it | Purpose |
| :--- | :--- | :--- | :--- |
| **Sign-In** | `/KLEF/8-2/GBS.php` | Students & Staff | Simple login with student ID and Date of Birth |
| **Dashboard** | `/KLEF/8-2/{id}/{name}/Academic-Overview.php` | Students | Progress, credit summary, and counselor info |
| **Cluster** | `/KLEF/8-2/{id}/{name}/Cluster-Selection.php` | Students | View your specialization cohort (Cluster 1 or 2) |
| **Courses** | `/KLEF/8-2/{id}/{name}/Subject-Selection.php` | Students | Pick your 7 bucket subjects |
| **Faculty** | `/KLEF/8-2/{id}/{name}/Faculty-Preferences.php` | Students | Rank 1st, 2nd, and 3rd choice professors |
| **Directory** | `/KLEF/8-2/{id}/{name}/Faculty-Directory.php` | Students | Searchable staff directory with PDF download |
| **Summary** | `/KLEF/8-2/{id}/{name}/My-Preference.php` | Students | Final review grid with PNG proof download |
| **Profile** | `/KLEF/8-2/{id}/{name}/My-Profile.php` | Students | Personal info, Aadhaar, and password management |
| **Admin** | `/KLEF/8-2/Admin/G-Bhaanu-Sai/Dashboard.php` | Staff / Admin | Overall registration stats and quick actions |
| **Students** | `/KLEF/8-2/Admin/G-Bhaanu-Sai/Students.php` | Staff / Admin | Search and edit all 1,159 student records |
| **Teachers** | `/KLEF/8-2/Admin/G-Bhaanu-Sai/Faculty.php` | Staff / Admin | Search and inspect 426 faculty assignments |
| **Buckets** | `/KLEF/8-2/Admin/G-Bhaanu-Sai/Buckets.php` | Staff / Admin | Configure academic bucket rules |
| **Catalog** | `/KLEF/8-2/Admin/G-Bhaanu-Sai/Courses.php` | Staff / Admin | View all 102 curriculum courses |
| **About Me** | `/KLEF/8-2/Developer/G-Bhaanu-Sai.php` | Everyone | Developer portfolio and bio |

---

## What technologies are used and why?

I picked tools that make the portal as fast, lightweight, and reliable as possible:

- **React 19 & Next.js 16 (App Router):** The website loads once and runs like a native phone app. Clicking between tabs is instantaneous because the browser never has to reload the entire screen from scratch.
- **Tailwind CSS v4:** Allowed me to build clean, custom styles matching the university’s official Navy Blue (`#1b2d42`) and warm gold brand colors. The layout adjusts automatically for phone, tablet, and desktop screens.
- **Built-in Node SQLite Database (`node:sqlite`):** Instead of connecting to a slow remote database across the internet, the app reads student and teacher data directly using Node’s native SQLite engine. This makes searches and queries instantaneous.
- **jsPDF & html2canvas:** Lets students download their official PDF directories and PNG receipt cards directly in their browser without having to wait for a server email.
- **Lucide Icons:** Clean, modern outline icons for navigation tabs, buttons, and alert badges.

---

## Project folder layout

Here is where everything lives in the project:

```
Academic-Registration-Portal-Y23/
├── public/
│   ├── assets/
│   │   └── klef-logo.png              # Official KL University emblem
│   └── favicon.png                    # Browser tab icon
├── src/
│   ├── app/(frontend)/
│   │   ├── [...slug]/page.jsx         # Catch-all page router
│   │   ├── portal-api/                # API routes for student & course data
│   │   ├── styles/                    # Individual CSS files for each page
│   │   ├── layout.jsx                 # Main website HTML layout
│   │   └── styles.css                 # Global colors and theme styles
│   ├── lib/
│   │   ├── db/
│   │   │   ├── client.js              # SQLite database connection
│   │   │   ├── eligibilityEngine.js   # Logic matching specializations to clusters
│   │   │   ├── optionSheetRules.json  # Department section boundaries
│   │   │   ├── queries.js             # Database search and get queries
│   │   │   └── schema.sql             # Full database structure (tables & indexes)
│   │   └── portal-auth.js             # Sign-in and session verification
│   └── portal/
│       ├── app/
│       │   ├── App.jsx                # Top-level React app component
│       │   └── routes.jsx             # All .php route definitions
│       ├── components/                # Reusable UI cards, headers, inputs
│       ├── pages/                     # The visual screens (Overview, Faculty, Admin, etc.)
│       └── services/                  # Auto-save handlers and local database records
├── docs/                              # Project governance & open-source documentation
│   ├── ACCESSIBILITY.md               # Accessibility practices (WCAG 2.1 AA)
│   ├── CODE_OF_CONDUCT.md             # Community standards & reporting guidelines
│   ├── CONTRIBUTING.md                # Guidelines for contributing & workflow
│   ├── LICENSE                        # MIT Open Source License
│   └── SECURITY.md                    # Security report instructions
├── next.config.mjs                    # Production web server configuration
├── package.json                       # Dependencies list
└── tsconfig.json                      # TypeScript settings
```

---

## How to run this project on your own computer

If you want to run this project locally to test or view it:

### Prerequisites
- Install **Node.js** (version 20, 22, or 24) on your computer.
- Install **Git**.

### 1. Clone this repository
```bash
git clone https://github.com/BhaanuG/Academic-Registration-Portal-Y23.git
cd "Academic-Registration-Portal-Y23"
```

### 2. Install project packages
```bash
npm install
```

### 3. Start the local server
```bash
npm run dev
```

### 4. Build for production
```bash
npm run build
```

---

## Author & Developer

<table align="center">
  <tr>
    <td align="center">
      <a href="https://github.com/BhaanuG">
        <img src="https://github.com/BhaanuG.png" width="115px;" alt="Bhaanu Gali" style="border-radius: 50%; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" /><br /><br />
        <b>Bhaanu G (Bhaanu Gali)</b>
      </a><br />
      Lead Developer & Systems Architect<br />
      Student ID: <code>2400030952</code><br />
      <a href="mailto:Bhaanugali@gmail.com">Bhaanugali@gmail.com</a> &bull; 
      <a href="mailto:2400030952@kluniversity.in">2400030952@kluniversity.in</a>
    </td>
  </tr>
</table>

<p align="center">
  Developed for and maintained under the academic governance of <b>Koneru Lakshmaiah Education Foundation (KLEF Deemed-to-be University)</b>.
</p>

---

## Project Documentation & Guidelines

- **[docs/LICENSE](docs/LICENSE)**: Legal terms under the MIT Open Source License.
- **[docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)**: Rules and workflow for contributing to this repository.
- **[docs/CODE_OF_CONDUCT.md](docs/CODE_OF_CONDUCT.md)**: Community standards and reporting guidelines.
- **[docs/SECURITY.md](docs/SECURITY.md)**: How to privately report security concerns.
- **[docs/ACCESSIBILITY.md](docs/ACCESSIBILITY.md)**: Our commitment to WCAG 2.1 AA accessibility standards for all users.
