'use client';

import React, { useEffect, useState } from 'react';

interface CareerDetails {
  title: string;
  track: string;
  image: string;
  description: string;
  salary: string;
  degree: string;
}

const CAREERS_DATABASE: Record<string, CareerDetails> = {
  "Product Management & UI/UX Design": {
    title: "Product Management & UI/UX Design",
    track: "Tech & Business Strategy",
    image: "/product-manager.jpg",
    description: "Lead product development cycles by bridging technology, human-centered UI/UX design, and business metrics. You will prioritize feature roadmaps, conduct user discovery, and direct sprint deliveries for digital platforms across startups and MNCs.",
    salary: "₹12 - ₹35+ LPA (Senior PMs & VPs: ₹50 LPA - ₹1.2 Cr)",
    degree: "B.Tech / B.Des / BBA + MBA (IIMs / Top Tier B-Schools)"
  },
  "Data Science & Artificial Intelligence": {
    title: "Data Science & Artificial Intelligence",
    track: "Applied Mathematics & ML Engineering",
    image: "/ai-engineer.jpg",
    description: "Design mathematical architectures, deep learning models, and NLP pipelines. Focus on building real-time predictive engines, big data analytics, and autonomous generative AI systems for enterprise deployment.",
    salary: "₹10 - ₹30+ LPA (Lead Data Scientists: ₹45 - ₹80+ LPA)",
    degree: "B.Tech in CSE/Data Science / M.Tech / MS (IITs / IIITs / Top Tier)"
  },
  "Full-Stack / Core Software Engineering": {
    title: "Full-Stack / Core Software Engineering",
    track: "Software Systems & Architecture",
    image: "/ai-engineer.jpg",
    description: "Develop enterprise-scale web applications, microservices, and distributed backend pipelines. Manage end-to-end software lifecycles across modern frontend frameworks, REST/GraphQL APIs, and database engines.",
    salary: "₹8 - ₹28+ LPA (Staff Engineers / Architects: ₹45 - ₹90+ LPA)",
    degree: "B.Tech in Computer Science / Information Technology"
  },
  "Cybersecurity & Ethical Hacking": {
    title: "Cybersecurity & Ethical Hacking",
    track: "Information Security & Threat Defense",
    image: "/ai-engineer.jpg",
    description: "Defend digital infrastructure, conduct penetration testing, and protect corporate systems against adversarial exploits, data breaches, and zero-day vulnerabilities across banking, defense, and SaaS sectors.",
    salary: "₹9 - ₹25+ LPA (Chief Information Security Officers: ₹50 LPA - ₹1 Cr)",
    degree: "B.Tech CSE / IT + CEH, CISSP, OSCP Certifications"
  },
  "Cloud Architecture & DevOps": {
    title: "Cloud Architecture & DevOps",
    track: "Infrastructure & Platform Engineering",
    image: "/aerospace-engineer.jpg",
    description: "Architect scalable multi-cloud infrastructure, implement container orchestration (Kubernetes), and build continuous integration/continuous deployment (CI/CD) pipelines to guarantee high availability and uptime.",
    salary: "₹10 - ₹28+ LPA (Principal DevOps Architects: ₹40 - ₹75+ LPA)",
    degree: "B.Tech in CSE/IT/ECE + AWS/GCP/Azure Solutions Architect Certifications"
  },
  "Game Development & Interactive Media": {
    title: "Game Development & Interactive Media",
    track: "Graphics Programming & Real-time Systems",
    image: "/architectural-designer.jpg",
    description: "Program 2D/3D interactive physics engines, custom shaders, and immersive environments using C++, Unity, and Unreal Engine for gaming studios, simulation software, and AR/VR ecosystems.",
    salary: "₹6 - ₹20+ LPA (Lead Technical Directors: ₹30 - ₹55+ LPA)",
    degree: "B.Tech in CSE / Game Development / B.Des Animation & Interactive Media"
  },
  "Advanced Academic Research & Higher Studies (MS / Ph.D.)": {
    title: "Advanced Academic Research & Higher Studies",
    track: "Fundamental Research & Academia",
    image: "/genomic-researcher.jpg",
    description: "Pursue deep fundamental research in theoretical computer science, computational mathematics, or engineering physics. Focus on research grants, authoring peer-reviewed conference publications, and faculty appointments.",
    salary: "₹12 - ₹35+ LPA (National Labs, R&D Wings, or Academic Professorships)",
    degree: "GATE Qualified -> M.Tech / MS -> Ph.D. (IISc / IITs / Global Universities)"
  },
  "Clinical Practice (Medicine/Surgery/Dentistry)": {
    title: "Clinical Practice (Medicine / Surgery)",
    track: "Clinical Healthcare & Diagnostics",
    image: "/neurological-surgeon.jpg",
    description: "Perform diagnosis, primary healthcare delivery, inpatient care, and surgical interventions in tertiary healthcare hospitals or private practice.",
    salary: "₹12 - ₹35+ LPA (Established Surgeons/Consultants: ₹50 LPA - ₹1.5 Cr)",
    degree: "NEET UG -> MBBS + NEET PG -> MD/MS/DM/MCh (AIIMS / Top Medical Colleges)"
  },
  "Biotechnology & Genomic Research": {
    title: "Biotechnology & Genomic Research",
    track: "Life Sciences & Molecular Biology",
    image: "/genomic-researcher.jpg",
    description: "Analyze molecular markers, genetic sequences, and biological vectors to formulate vaccines, therapeutic antibodies, and agritech innovations.",
    salary: "₹6 - ₹18+ LPA (Principal Scientists: ₹25 - ₹50+ LPA)",
    degree: "B.Tech/B.Sc Biotech + M.Tech/M.Sc + Ph.D. in Molecular Biology / Genomics"
  },
  "Pharmacology & Drug Development": {
    title: "Pharmacology & Drug Development",
    track: "Pharmaceutical Sciences",
    image: "/genomic-researcher.jpg",
    description: "Formulate active pharmaceutical ingredients (APIs), conduct controlled clinical trials, and supervise regulatory compliance across pharmaceutical manufacturing facilities.",
    salary: "₹6 - ₹16+ LPA (R&D Directors: ₹30 - ₹60+ LPA)",
    degree: "B.Pharm -> M.Pharm / Ph.D. in Pharmacology / Clinical Research"
  },
  "Public Health & Epidemiology": {
    title: "Public Health & Epidemiology",
    track: "Preventive Health & Public Policy",
    image: "/international-diplomat.jpg",
    description: "Track disease spread patterns, design national health interventions, and advise state/central healthcare ministries or international organizations like the WHO.",
    salary: "₹7 - ₹20+ LPA (Health Advisors / Directors: ₹25 - ₹45+ LPA)",
    degree: "MBBS / BDS / B.Sc -> Master of Public Health (MPH)"
  },
  "Allied Health & Rehabilitation": {
    title: "Allied Health & Physiotherapy",
    track: "Physical Medicine & Rehabilitation",
    image: "/clinical-psychologist.jpg",
    description: "Provide physical rehabilitation, musculoskeletal therapy, sports injury management, and occupational health recovery programs.",
    salary: "₹4.5 - ₹12+ LPA (Sports Consultants / Clinic Owners: ₹20 - ₹40+ LPA)",
    degree: "Bachelor of Physiotherapy (BPT) -> Master of Physiotherapy (MPT)"
  },
  "Mechanical & Aerospace Engineering": {
    title: "Mechanical & Aerospace Engineering",
    track: "Thermal, Mechanical & Flight Systems",
    image: "/aerospace-engineer.jpg",
    description: "Design and validate propulsion systems, robotics, aerodynamic surfaces, and industrial machines across automotive, aerospace (ISRO/DRDO/Private Space), and manufacturing sectors.",
    salary: "₹7 - ₹22+ LPA (Chief Engineers: ₹35 - ₹70+ LPA)",
    degree: "B.Tech in Mechanical / Aerospace Engineering (IITs / NITs)"
  },
  "Civil & Sustainable Infrastructure": {
    title: "Civil & Sustainable Infrastructure",
    track: "Structural Engineering & Urban Planning",
    image: "/architectural-designer.jpg",
    description: "Lead structural design calculations, mega-infrastructure project execution (expressways, metro rails, airports), and sustainable environmental engineering implementations.",
    salary: "₹6 - ₹18+ LPA (Project Directors: ₹30 - ₹60+ LPA)",
    degree: "B.Tech in Civil Engineering + M.Tech in Structural Engineering / NICMAR"
  },
  "Electronics, VLSI & IoT": {
    title: "Electronics, VLSI & IoT",
    track: "Semiconductors & Embedded Hardware",
    image: "/aerospace-engineer.jpg",
    description: "Design microchip architectures, ASIC circuits, FPGA configurations, and IoT devices at semiconductor design houses and hardware manufacturing units.",
    salary: "₹10 - ₹30+ LPA (VLSI Design Leads: ₹45 - ₹90+ LPA)",
    degree: "B.Tech in ECE / EEE -> M.Tech in VLSI / Embedded Systems (IITs / NITs)"
  },
  "Chemical & Materials Engineering": {
    title: "Chemical & Materials Engineering",
    track: "Process Chemistry & Material Science",
    image: "/genomic-researcher.jpg",
    description: "Optimize large-scale industrial chemical processes, battery cell chemistry, polymer manufacturing, and advanced metallurgy in refinery and energy sectors.",
    salary: "₹7 - ₹20+ LPA (Plant Operations Heads: ₹30 - ₹60+ LPA)",
    degree: "B.Tech in Chemical Engineering / Materials Science"
  },
  "Investment Banking & Corporate Finance": {
    title: "Investment Banking & Corporate Finance",
    track: "Capital Markets & Valuation",
    image: "/investment-banker.jpg",
    description: "Execute complex corporate financial models, debt structuring, M&A advisory, and capital market fundraising (IPOs) for domestic and global corporations.",
    salary: "₹16 - ₹40+ LPA (Directors / Partners: ₹70 LPA - ₹2 Cr+)",
    degree: "B.Com / BBA / B.Tech + CFA / CA / MBA Finance (IIMs / Top B-Schools)"
  },
  "Growth Marketing & Brand Strategy": {
    title: "Growth Marketing & Brand Strategy",
    track: "Customer Acquisition & Market Strategy",
    image: "/product-manager.jpg",
    description: "Direct customer acquisition budgets, performance marketing campaigns, brand identity initiatives, and data-driven user retention across consumer and D2C brands.",
    salary: "₹8 - ₹24+ LPA (Chief Marketing Officers: ₹40 - ₹80+ LPA)",
    degree: "Any Graduation + MBA in Marketing / Digital Strategy"
  },
  "Operations & Supply Chain Management": {
    title: "Operations & Supply Chain Management",
    track: "Supply Chain & Logistics Optimization",
    image: "/aerospace-engineer.jpg",
    description: "Architect end-to-end supply chains, manufacturing logistics, inventory algorithms, and warehouse automation for multinational corporations and e-commerce giants.",
    salary: "₹8 - ₹22+ LPA (Chief Operating Officers: ₹45 - ₹90+ LPA)",
    degree: "B.Tech / BBA + MBA in Operations / SCM (NITIE / IIMs)"
  },
  "Entrepreneurship & Venture Capital": {
    title: "Entrepreneurship & Venture Capital",
    track: "Venture Building & Early-Stage Equity",
    image: "/venture-capitalist.jpg",
    description: "Evaluate early-stage startups, perform due diligence, manage fund portfolios, or build high-growth venture-backed companies from ground zero.",
    salary: "₹15 - ₹40+ LPA + Carry / Equity upside",
    degree: "Any Graduation + Track Record / Top MBA (IIMs / ISB / Tier 1)"
  },
  "Corporate & Commercial Law": {
    title: "Corporate & Commercial Law",
    track: "Corporate Legal Advisory & Contracts",
    image: "/corporate-lawyer.jpg",
    description: "Draft international contracts, lead M&A due diligence, manage corporate insolvency proceedings (IBC), and handle regulatory compliance across top legal firms.",
    salary: "₹12 - ₹30+ LPA (Senior Partners: ₹60 LPA - ₹1.5 Cr+)",
    degree: "BA LLB / BBA LLB (NLUs / Top Tier Law Colleges) -> LLM"
  },
  "Criminal & Litigation Law": {
    title: "Criminal & Litigation Law",
    track: "Courtroom Advocacy & Litigation",
    image: "/corporate-lawyer.jpg",
    description: "Argue complex litigation matters before High Courts and the Supreme Court of India, handling constitutional matters, criminal defense, and public interest litigation.",
    salary: "₹6 - ₹25+ LPA (Senior Advocates: ₹50 LPA - ₹2 Cr+ on retainers)",
    degree: "LLB / Integrated Law Degree (NLUs / State Law Faculties)"
  },
  "Public Policy & Governance": {
    title: "Public Policy & Governance",
    track: "Legislative Advisory & Civil Governance",
    image: "/international-diplomat.jpg",
    description: "Formulate public welfare schemes, evaluate government policies, and consult for think tanks (NITI Aayog, CPR) and state development boards.",
    salary: "₹8 - ₹22+ LPA (Senior Policy Advisors: ₹30 - ₹50+ LPA)",
    degree: "Graduation + Master in Public Policy (MPP / NLSIU / IIMs)"
  },
  "International Relations & Diplomacy": {
    title: "International Relations & Diplomacy",
    track: "Foreign Policy & Diplomatic Affairs",
    image: "/international-diplomat.jpg",
    description: "Represent national interests, negotiate bilateral and multilateral trade agreements, and manage geopolitical strategic relationships in the foreign service or global bodies.",
    salary: "₹10 - ₹24+ LPA (UPSC Indian Foreign Service Cadre / UN Scales)",
    degree: "Graduation -> UPSC Civil Services (IFS) / Master’s in IR (JNU / Ashoka)"
  },
  "Architecture & Spatial Design": {
    title: "Architecture & Spatial Design",
    track: "Urban Architecture & Spatial Planning",
    image: "/architectural-designer.jpg",
    description: "Create sustainable architectural master plans, commercial towers, and spatial interiors balancing structural compliance, Council of Architecture codes, and aesthetics.",
    salary: "₹6 - ₹18+ LPA (Principal Architects / Firm Owners: ₹30 - ₹75+ LPA)",
    degree: "NATA / JEE Paper 2 -> B.Arch -> M.Arch (SPA / IITs / CEPT)"
  },
  "Fine Arts & Illustration": {
    title: "Fine Arts & Visual Arts",
    track: "Studio Arts & Digital Visuals",
    image: "/architectural-designer.jpg",
    description: "Create conceptual visual art, commercial illustrations, gallery exhibits, and cultural installations for media houses, galleries, and publishing firms.",
    salary: "₹4.5 - ₹15+ LPA (Established Artists / Art Directors: ₹25 - ₹50+ LPA)",
    degree: "Bachelor of Fine Arts (BFA) -> Master of Fine Arts (MFA)"
  },
  "Industrial & Product Design": {
    title: "Industrial & Product Design",
    track: "Hardware Ergonomics & Physical Prototyping",
    image: "/product-manager.jpg",
    description: "Design ergonomic consumer electronics, mobility equipment, home goods, and sustainable physical products engineered for scaled factory production.",
    salary: "₹8 - ₹22+ LPA (Design Directors: ₹35 - ₹65+ LPA)",
    degree: "UCEED / CEED -> B.Des / M.Des (NID / IIT IDC)"
  },
  "Psychology & Behavioral Science": {
    title: "Clinical Psychology & Behavioral Science",
    track: "Mental Health & Psychotherapy",
    image: "/clinical-psychologist.jpg",
    description: "Conduct psychological evaluations, provide cognitive-behavioral therapies, and treat mental health disorders across hospitals, clinics, and academic institutions.",
    salary: "₹5 - ₹16+ LPA (Licensed Private Practitioners: ₹20 - ₹45+ LPA)",
    degree: "BA/B.Sc Psychology -> M.Sc / M.A. -> M.Phil / Psy.D (RCI Recognized)"
  },
  "Journalism & Mass Media": {
    title: "Journalism & Mass Media",
    track: "Investigative Journalism & Broadcasting",
    image: "/investigative-journalist.jpg",
    description: "Report investigative news stories, produce digital broadcasts, and analyze political/economic events for news channels, digital publications, and agencies.",
    salary: "₹5 - ₹15+ LPA (Senior Editors / Prime Time Anchors: ₹25 - ₹60+ LPA)",
    degree: "Bachelor / Master in Journalism & Mass Communication (IIMC / Jamia / Asian College)"
  },
  "Sociology & Social Work": {
    title: "Sociology & Development Sector",
    track: "Social Impact & Community Development",
    image: "/clinical-psychologist.jpg",
    description: "Direct development projects, manage corporate social responsibility (CSR) programs, and organize community empowerment initiatives with national and global NGOs.",
    salary: "₹5 - ₹14+ LPA (CSR Directors / Program Heads: ₹22 - ₹45+ LPA)",
    degree: "BSW -> Master of Social Work (MSW) / Development Studies (TISS / Delhi School of Social Work)"
  },
  "Literature, History & Editorial": {
    title: "Literature, History & Editorial",
    track: "Editorial, Publishing & Cultural Curation",
    image: "/investigative-journalist.jpg",
    description: "Lead editorial management, historical archiving, literature publishing, and cultural curation for international publishing houses, academic journals, and cultural bodies.",
    salary: "₹4.5 - ₹14+ LPA (Commissioning Editors / Museum Curators: ₹20 - ₹40+ LPA)",
    degree: "BA -> MA in English Literature / History / Archival Studies"
  }
};

export default function DashboardPage() {
  const [results, setResults] = useState<any>(null);
  const [selectedCareer, setSelectedCareer] = useState<CareerDetails | null>(null);

  useEffect(() => {
    const data = sessionStorage.getItem('clarity_backend_results');
    if (data) {
      try {
        setResults(JSON.parse(data));
      } catch (e) {
        console.error("Failed to parse backend results", e);
      }
    }
  }, []);

  const openCareerDetails = (vectorTitle: string) => {
    if (CAREERS_DATABASE[vectorTitle]) {
      setSelectedCareer(CAREERS_DATABASE[vectorTitle]);
    } else {
      setSelectedCareer({
        title: vectorTitle,
        track: "Evaluated Professional Vector",
        image: "/girl-reading.jpg",
        description: "This specialized profile is matched through your psychometric and cognitive matrix responses.",
        salary: "₹8 - ₹25+ LPA (Benchmark)",
        degree: "Relevant Bachelor's / Master's Degree in Field"
      });
    }
  };

  const optimal = results?.optimal_vector || {
    title: "Product Management & UI/UX Design",
    match: 98.5
  };

  const evaluated = results?.evaluated_vectors || [
    { title: "Product Management & UI/UX Design", match: 98.5 },
    { title: "Data Science & Artificial Intelligence", match: 40.0 },
    { title: "Cybersecurity & Ethical Hacking", match: 5.0 },
    { title: "Cloud Architecture & DevOps", match: 5.0 },
    { title: "Game Development & Interactive Media", match: 5.0 },
    { title: "Advanced Academic Research & Higher Studies (MS / Ph.D.)", match: 5.0 },
    { title: "Full-Stack / Core Software Engineering", match: 0.0 }
  ];

  return (
    <main className="min-h-screen w-full relative bg-[#EFE6D5] text-[#0a1118] selection:bg-[#B89B72] selection:text-white flex flex-col font-sans">
      
      {/* Ambient Gradient */}
      <div className="absolute inset-0 z-0 pointer-events-none bg-[radial-gradient(ellipse_at_bottom_right,_var(--tw-gradient-stops))] from-[#E5D4C0] via-[#EFE6D5]/80 to-[#EFE6D5] opacity-90"></div>

      {/* Global Header */}
      <nav className="relative z-50 w-full max-w-[1400px] mx-auto px-8 md:px-16 flex justify-between items-center py-8">
        <a href="/" className="font-serif text-2xl tracking-[0.15em] text-[#0a1118] uppercase font-bold group">
          Clarity<span className="italic text-[#C2A878] font-light group-hover:text-[#0a1118] transition-colors">OS</span>
        </a>
        <div className="flex items-center gap-8">
          <a href="/assessment" className="text-[11px] font-bold uppercase tracking-[0.2em] text-[#0a1118]/60 hover:text-[#0a1118] transition-colors">
            Retake Assessment
          </a>
          <a href="/" className="border border-[#0a1118] text-[#0a1118] px-7 py-3 text-[10px] uppercase font-bold tracking-[0.2em] hover:bg-[#0a1118] hover:text-white transition-all duration-300 rounded-sm shadow-sm">
            Exit
          </a>
        </div>
      </nav>

      {/* Main Dashboard Layout */}
      <div className="relative z-10 w-full max-w-[1400px] mx-auto px-8 md:px-16 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Left Column: Top Match Highlight */}
          <div className="lg:col-span-2 space-y-8">
            <div className="bg-[#2B3A4A] text-white p-10 md:p-14 rounded-sm shadow-2xl relative overflow-hidden">
              <span className="text-[#C2A878] text-[10px] tracking-[0.3em] uppercase font-bold block mb-4">
                Optimal Career Vector
              </span>
              
              <h1 className="font-serif text-3xl md:text-5xl leading-tight mb-6">
                {optimal.title}
              </h1>

              <div className="inline-block bg-[#C2A878] text-[#0a1118] px-4 py-1.5 text-xs font-bold tracking-widest uppercase mb-6 rounded-sm">
                {optimal.match}% Match Alignment
              </div>

              <p className="text-gray-300 text-sm leading-relaxed max-w-xl">
                Derived from your 20-question psychometric and technical profile analysis. Your unique combination of problem-solving preferences and career priorities points toward this path.
              </p>

              <button 
                onClick={() => openCareerDetails(optimal.title)}
                className="mt-8 inline-block bg-white text-[#0a1118] px-6 py-3 text-[10px] font-bold uppercase tracking-[0.2em] hover:bg-[#C2A878] hover:text-white transition-all shadow-md cursor-pointer"
              >
                View Full Role Profile →
              </button>
            </div>

            {/* Evaluated Vectors List */}
            <div className="bg-white p-8 md:p-12 border border-[#E8E2D2] shadow-xl rounded-sm">
              <h2 className="font-serif text-xl tracking-[0.2em] uppercase text-[#0a1118] mb-8">
                All Evaluated Vectors <span className="text-xs text-gray-400 font-sans tracking-normal">(Click any row to inspect)</span>
              </h2>

              <div className="space-y-4">
                {evaluated.map((vec: any, idx: number) => (
                  <div 
                    key={idx}
                    onClick={() => openCareerDetails(vec.title)}
                    className="p-4 border border-[#E8E2D2] hover:border-[#C2A878] hover:bg-[#FBF8F1] transition-all cursor-pointer group rounded-sm"
                  >
                    <div className="flex justify-between items-center mb-2">
                      <span className="font-serif text-base text-[#0a1118] group-hover:text-[#C2A878] transition-colors">
                        {idx + 1}. {vec.title}
                      </span>
                      <span className="font-mono text-xs font-bold text-gray-500">
                        {vec.match}% Match
                      </span>
                    </div>
                    
                    {/* Visual Progress Bar */}
                    <div className="w-full h-1.5 bg-[#E8E2D2] overflow-hidden rounded-full">
                      <div 
                        className="h-full bg-[#C2A878] transition-all duration-700"
                        style={{ width: `${Math.max(2, vec.match)}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Right Column: Execution Roadmap Action */}
          <div className="space-y-8">
            <div className="bg-white p-8 md:p-10 border border-[#E8E2D2] shadow-xl rounded-sm">
              <span className="text-[#C2A878] text-[9px] tracking-[0.3em] uppercase font-bold block mb-3">
                Immediate Execution
              </span>
              <h3 className="font-serif text-2xl text-[#0a1118] mb-4">
                4-Week Tactical Roadmap
              </h3>
              <p className="text-gray-600 text-xs leading-relaxed mb-6">
                Your personalized execution milestone plan has been mapped out based on your target vector.
              </p>
              <a 
                href="/roadmap"
                className="w-full block text-center bg-[#0a1118] text-white py-4 text-[10px] font-bold uppercase tracking-[0.2em] hover:bg-[#C2A878] transition-all rounded-sm"
              >
                View Weekly Milestones →
              </a>
            </div>

            <div className="bg-[#FBF8F1] p-6 border border-[#E8E2D2] rounded-sm text-xs text-gray-500 font-mono">
              <span className="text-[#0a1118] font-bold block mb-1">Status:</span>
              Loaded calculated results from psychometric engine.
            </div>
          </div>

        </div>
      </div>

      {/* Career Details Modal */}
      {selectedCareer && (
        <div 
          className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fadeIn"
          onClick={() => setSelectedCareer(null)}
        >
          <div 
            className="bg-[#FBF8F1] w-full max-w-4xl max-h-[90vh] overflow-y-auto rounded-sm shadow-2xl relative flex flex-col md:flex-row"
            onClick={(e) => e.stopPropagation()}
          >
            <button 
              onClick={() => setSelectedCareer(null)}
              className="absolute top-4 right-4 z-10 w-8 h-8 flex items-center justify-center bg-white text-[#0a1118] shadow-md hover:bg-[#0a1118] hover:text-white transition-colors rounded-full"
            >
              ✕
            </button>

            <div className="w-full md:w-2/5 aspect-square md:aspect-auto bg-gray-200">
              <img 
                src={selectedCareer.image} 
                alt={selectedCareer.title} 
                className="w-full h-full object-cover"
                onError={(e) => { e.currentTarget.src = 'https://images.unsplash.com/photo-1456406644174-8ddd4cd52a06?q=80&w=600&auto=format&fit=crop'; }}
              />
            </div>

            <div className="w-full md:w-3/5 p-8 md:p-12 flex flex-col justify-center">
              <span className="text-[#C2A878] text-[10px] tracking-[0.3em] uppercase font-bold mb-3 block">
                {selectedCareer.track}
              </span>
              
              <h2 className="font-serif text-2xl md:text-3xl text-[#0a1118] leading-tight mb-4">
                {selectedCareer.title}
              </h2>
              
              <p className="text-gray-600 text-xs md:text-sm leading-relaxed mb-6">
                {selectedCareer.description}
              </p>
              
              <div className="space-y-4 mb-8 border-t border-[#E8E2D2] pt-6">
                <div>
                  <span className="block text-[10px] font-bold uppercase tracking-[0.2em] text-[#0a1118]/50">India Industry Compensation Benchmark</span>
                  <span className="block text-[#0a1118] font-bold text-sm mt-1">{selectedCareer.salary}</span>
                </div>
                <div>
                  <span className="block text-[10px] font-bold uppercase tracking-[0.2em] text-[#0a1118]/50">Typical Indian Degree & Certification Route</span>
                  <span className="block text-[#0a1118] font-medium text-xs mt-1">{selectedCareer.degree}</span>
                </div>
              </div>

              <button 
                onClick={() => setSelectedCareer(null)}
                className="bg-[#0a1118] text-white text-center px-8 py-3.5 text-[10px] uppercase font-bold tracking-[0.2em] hover:bg-[#C2A878] transition-colors duration-300 w-full rounded-sm"
              >
                Close Role Inspector
              </button>
            </div>
          </div>
        </div>
      )}

    </main>
  );
}