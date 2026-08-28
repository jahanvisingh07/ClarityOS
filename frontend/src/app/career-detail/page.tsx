'use client';

import React, { useEffect, useState } from 'react';

export default function CareerDetailPage() {
  const [careerTitle, setCareerTitle] = useState('');

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const path = params.get('path');
    if (path) {
      setCareerTitle(path.trim());
    }
  }, []);

  // Comprehensive validated dictionary of real careers
  const careerData: Record<string, any> = {
    "Software Engineer": {
      tagline: "The Architecture of Digital Systems",
      definition: "A Software Engineer designs, builds, tests, and maintains scalable software systems using clean code and rigorous computer science fundamentals.",
      specializations: [
        { name: "Full-Stack Engineering", desc: "Building both client-facing interfaces and robust backend distributed systems." },
        { name: "Distributed Systems", desc: "Focusing on cloud architecture, microservices, and high-concurrency systems." },
        { name: "Systems & Infrastructure", desc: "Low-level optimization, networking protocols, and high-performance backend engines." }
      ],
      dayToDaly: "Writing code, debugging production logs, reviewing pull requests, and collaborating in sprint planning sessions.",
      salaryRange: "₹12L - ₹45L+ (Tier-1 Tech)",
      skillsNeeded: ["Data Structures & Algorithms", "System Design", "Database Management", "Git & CI/CD"]
    },
    "Product Manager (Tech)": {
      tagline: "The Intersection of Tech, Business, and Design",
      definition: "A Product Manager defines the 'what' and 'why' behind a product, bridging engineering capability with user needs and business strategy.",
      specializations: [
        { name: "Core Product Management", desc: "Owning end-to-end feature delivery, roadmap prioritization, and user metrics." },
        { name: "Growth PM", desc: "Focusing on acquisition, retention loops, data analytics, and conversion funnel optimization." },
        { name: "AI / Platform PM", desc: "Managing complex technical infrastructure products or AI platforms." }
      ],
      dayToDaly: "Writing PRDs, talking to users, analyzing retention metrics, and aligning engineering with business goals.",
      salaryRange: "₹15L - ₹50L+ (Product MNCs & Startups)",
      skillsNeeded: ["User Empathy", "Basic SQL/Data Analysis", "Wireframing & UX Thinking", "Strategic Prioritization"]
    },
    "Data Science / AI": {
      tagline: "Extracting Intelligence from Complex Data",
      definition: "Data Scientists and AI Engineers build predictive models, train machine learning systems, and turn raw data into strategic organizational assets.",
      specializations: [
        { name: "Applied Machine Learning", desc: "Training regression, classification, and deep learning models for production use cases." },
        { name: "LLM & Generative AI", desc: "Fine-tuning transformer models, building RAG pipelines, and deploying vector databases." },
        { name: "Data Analytics", desc: "Writing complex SQL queries, building executive dashboards, and statistical experimentation." }
      ],
      dayToDaly: "Cleaning datasets, training model weights, running A/B tests, and presenting insights to stakeholders.",
      salaryRange: "₹14L - ₹48L+",
      skillsNeeded: ["Python & PyTorch", "Statistics & Linear Algebra", "SQL", "Vector Databases"]
    },
    "Chef": {
      tagline: "Mastery of Gastronomy and Kitchen Execution",
      definition: "A Chef plans menus, prepares culinary dishes, manages kitchen staff, and maintains strict food quality and safety standards in professional hospitality establishments.",
      specializations: [
        { name: "Executive Chef", desc: "Overseeing overall kitchen operations, menu engineering, and culinary vision." },
        { name: "Pastry Chef", desc: "Specializing in baking, desserts, pastries, and confectionery arts." },
        { name: "Sous Chef", desc: "Managing day-to-day kitchen workflow, staff supervision, and line preparation." }
      ],
      dayToDaly: "Prepping ingredients, managing service rush hours, coordinating kitchen staff, and crafting new recipes.",
      salaryRange: "₹5L - ₹25L+ (Luxury Hotels & Fine Dining)",
      skillsNeeded: ["Culinary Techniques", "Kitchen Management", "Food Safety & Hygiene", "Creativity Under Pressure"]
    },
    "Actor": {
      tagline: "The Art of Performance and Character Portrayal",
      definition: "An Actor interprets scripts and portrays characters in theater, film, television, or digital media to entertain, inform, and emotionally engage audiences.",
      specializations: [
        { name: "Film & Television Acting", desc: "Performing for camera lenses, working closely with directors, and executing tight scene takes." },
        { name: "Theater & Stage Acting", desc: "Performing live in front of audiences with strong vocal projection and emotional sustained delivery." },
        { name: "Voice Acting", desc: "Providing voiceovers for animation, video games, commercials, and audiobooks." }
      ],
      dayToDaly: "Memorizing lines, attending auditions, rehearsing scenes, and collaborating with production crews.",
      salaryRange: "Variable / Project-Based (Freelance & Contract)",
      skillsNeeded: ["Emotional Expressiveness", "Script Analysis", "Vocal Projection", "Audition Resilience"]
    },
    "Singer": {
      tagline: "Vocal Mastery and Musical Expression",
      definition: "A Singer uses their voice as an instrument to perform songs, record studio tracks, and deliver compelling musical experiences to listeners.",
      specializations: [
        { name: "Recording Artist", desc: "Writing, recording, and releasing studio tracks for commercial music platforms." },
        { name: "Live Performance Singer", desc: "Touring, performing at concerts, festivals, and high-profile private events." },
        { name: "Session Vocalist", desc: "Providing professional backing vocals or commercial jingles for media projects." }
      ],
      dayToDaly: "Vocal warm-ups, recording sessions in sound studios, rehearsing with musicians, and performing live.",
      salaryRange: "Variable / Royalty & Performance Based",
      skillsNeeded: ["Vocal Pitch & Control", "Stage Presence", "Musical Ear", "Endurance"]
    },
    "VLSI Engineer": {
      tagline: "Advanced Semiconductor and Microchip Architecture",
      definition: "A VLSI (Very Large Scale Integration) Engineer designs, verifies, and optimizes complex integrated circuits and semiconductor microchips powering modern hardware.",
      specializations: [
        { name: "RTL Design", desc: "Writing Verilog/SystemVerilog code to define microchip behavior and logic architectures." },
        { name: "Physical Design", desc: "Floorplanning, routing, and timing closure for silicon wafer manufacturing." },
        { name: "Verification", desc: "Testing chip logic against bugs and timing failures using advanced simulation tools." }
      ],
      dayToDaly: "Writing hardware description code, running simulations, debugging logic flaws, and collaborating with fabrication teams.",
      salaryRange: "₹14L - ₹40L+ (Semiconductor MNCs)",
      skillsNeeded: ["Verilog / SystemVerilog", "Digital Electronics", "Computer Architecture", "Static Timing Analysis"]
    }
  };

  // Check if the requested career actually exists in our dictionary
  const isValidCareer = careerTitle && careerData[careerTitle];
  const currentCareer = isValidCareer ? careerData[careerTitle] : null;

  return (
    <main className="min-h-screen w-full relative bg-[#FBF8F1] text-[#0a1118] selection:bg-[#B89B72] selection:text-white flex flex-col">
      
      <div 
        className="absolute inset-0 z-0 opacity-[0.12] mix-blend-multiply pointer-events-none"
        style={{ 
          backgroundImage: "url('https://images.unsplash.com/photo-1618367588411-d9a90fefa881?q=80&w=2000&auto=format&fit=crop')", 
          backgroundSize: 'cover', 
          backgroundPosition: 'center',
        }}
      ></div>

      <nav className="relative z-50 w-full max-w-[1400px] mx-auto px-8 md:px-16 flex justify-between items-center py-10 border-b border-[#E8E2D2]">
        <a href="/" className="font-serif text-2xl tracking-[0.15em] text-[#0a1118] uppercase">
          Clarity<span className="italic text-[#B89B72]">OS</span>
        </a>
        <div className="flex items-center gap-6">
          <a href="/" className="text-[10px] font-bold tracking-[0.2em] text-[#4A5568] uppercase hover:text-[#0a1118] transition-colors">
            ← Back to Home
          </a>
        </div>
      </nav>

      <div className="relative z-10 w-full max-w-4xl mx-auto px-6 py-20 flex-1 flex flex-col justify-center">
        
        {isValidCareer ? (
          /* --- VALID CAREER DOSSIER VIEW --- */
          <div>
            <div className="border-b border-[#E8E2D2] pb-10 mb-12">
              <span className="text-[#B89B72] text-[9px] tracking-[0.3em] uppercase font-bold">Career Intelligence Dossier</span>
              <h1 className="font-serif text-4xl md:text-6xl text-[#0a1118] mt-3 tracking-wide">{careerTitle}</h1>
              <p className="text-sm md:text-base text-[#4A5568] italic font-serif mt-2">{currentCareer.tagline}</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-10 mb-16">
              <div className="lg:col-span-2 space-y-6">
                <h3 className="font-serif text-xl tracking-wider uppercase">What is this career?</h3>
                <p className="text-gray-700 leading-relaxed text-base font-light bg-white border border-[#E8E2D2] p-8 shadow-sm">
                  {currentCareer.definition}
                </p>

                <h3 className="font-serif text-xl tracking-wider uppercase pt-4">Day-to-Day Reality</h3>
                <p className="text-gray-700 leading-relaxed text-base font-light bg-white border border-[#E8E2D2] p-8 shadow-sm">
                  {currentCareer.dayToDaly}
                </p>
              </div>

              <div className="bg-[#2c3e50] text-white p-8 border-l-4 border-[#B89B72] space-y-6 shadow-xl">
                <div>
                  <p className="text-[9px] tracking-[0.3em] uppercase text-[#B89B72] font-bold mb-1">Estimated Compensation</p>
                  <p className="font-serif text-xl">{currentCareer.salaryRange}</p>
                </div>
                
                <div className="w-full h-[1px] bg-[#B89B72]/30"></div>

                <div>
                  <p className="text-[9px] tracking-[0.3em] uppercase text-[#B89B72] font-bold mb-3">Core Competencies</p>
                  <ul className="space-y-2">
                    {currentCareer.skillsNeeded.map((skill: string, i: number) => (
                      <li key={i} className="text-xs text-gray-300 font-light flex items-center gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-[#B89B72]"></span>
                        {skill}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>

            <div className="mb-16">
              <h3 className="font-serif text-2xl tracking-wider uppercase mb-8">Specialization Tracks</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {currentCareer.specializations.map((spec: any, index: number) => (
                  <div key={index} className="bg-white border border-[#E8E2D2] p-8 shadow-sm flex flex-col justify-between">
                    <div>
                      <span className="text-[#B89B72] text-[9px] tracking-[0.2em] uppercase font-bold">Track 0{index + 1}</span>
                      <h4 className="font-serif text-lg text-[#0a1118] mt-2 mb-4">{spec.name}</h4>
                      <p className="text-xs text-gray-600 leading-relaxed font-light">{spec.desc}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : (
          /* --- INVALID / NON-EXISTENT CAREER ERROR STATE --- */
          <div className="bg-white border border-[#E8E2D2] p-12 text-center shadow-xl space-y-6">
            <span className="text-4xl">⚠️</span>
            <h1 className="font-serif text-3xl md:text-4xl text-[#0a1118] tracking-wide">Career Path Not Found</h1>
            <p className="text-xs text-gray-600 max-w-md mx-auto leading-relaxed font-light">
              We searched our global index, but <strong className="font-bold text-[#0a1118]">"{careerTitle || 'this search'}"</strong> does not correspond to a recognized professional career path in ClarityOS.
            </p>
            <div className="pt-4">
              <a 
                href="/" 
                className="inline-block bg-[#B89B72] text-white px-8 py-4 text-[10px] tracking-[0.3em] uppercase hover:bg-[#0a1118] transition-colors font-bold"
              >
                Return to Career Directory
              </a>
            </div>
          </div>
        )}

      </div>
    </main>
  );
}