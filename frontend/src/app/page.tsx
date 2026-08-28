'use client';

import React, { useEffect, useState } from 'react';

const CAREERS = [
  {
    id: 'ai-engineer',
    title: 'Artificial Intelligence Engineer',
    track: 'Tech & Computer Science',
    image: '/ai-engineer.jpg',
    description: 'Design, train, and deploy advanced machine learning models and neural networks. Build the algorithms that power autonomous systems, natural language processing, and predictive analytics for Indian tech giants and high-growth startups.',
    salary: '₹12 - ₹35+ LPA (Lead Staff: ₹50 - ₹80+ LPA)',
    degree: 'B.Tech in CSE / Data Science / AI (IITs / NITs / IIITs)'
  },
  {
    id: 'aerospace-engineer',
    title: 'Aerospace Engineer',
    track: 'Core Engineering',
    image: '/aerospace-engineer.jpg',
    description: 'Design and test aircraft, launch vehicles, satellites, and propulsion systems. Work with national aerospace bodies like ISRO, DRDO, or private space-tech startups to push the boundaries of flight.',
    salary: '₹8 - ₹22+ LPA (Senior Scientists / Specialists: ₹30 - ₹55+ LPA)',
    degree: 'B.Tech / M.Tech in Aerospace or Mechanical Engineering'
  },
  {
    id: 'product-manager',
    title: 'Product Manager',
    track: 'Tech & Business',
    image: '/product-manager.jpg',
    description: 'Direct digital product lifecycles across tech companies. Bridge engineering, UI/UX design, and business strategy to build platforms used by millions across India and global markets.',
    salary: '₹14 - ₹35+ LPA (Director / VP of Product: ₹60 LPA - ₹1.2 Cr)',
    degree: 'B.Tech / BBA + MBA (IIMs / Top B-Schools)'
  },
  {
    id: 'neurological-surgeon',
    title: 'Neurological Surgeon',
    track: 'Medicine & Life Sciences',
    image: '/neurological-surgeon.jpg',
    description: 'Diagnose and surgically treat complex disorders of the central nervous system, brain, and spinal column in premier medical research institutes and private super-specialty hospitals.',
    salary: '₹24 - ₹60+ LPA (Renowned Senior Consultants: ₹80 LPA - ₹2 Cr+)',
    degree: 'NEET UG -> MBBS + NEET PG -> MS/M.Ch in Neurosurgery (AIIMS / Top Tier)'
  },
  {
    id: 'genomic-researcher',
    title: 'Genomic Research Scientist',
    track: 'Biotechnology & Genetics',
    image: '/genomic-researcher.jpg',
    description: 'Study DNA sequencing, genetic mutations, and molecular biology to develop therapeutic innovations, diagnostics, and personalized medicine for leading research labs and biopharma hubs.',
    salary: '₹7 - ₹18+ LPA (Principal Scientists: ₹25 - ₹45+ LPA)',
    degree: 'B.Tech / B.Sc Biotech -> M.Tech/M.Sc -> Ph.D. (IISc / IITs / TIFR)'
  },
  {
    id: 'investment-banker',
    title: 'Investment Banker',
    track: 'Finance & Commerce',
    image: '/investment-banker.jpg',
    description: 'Advise top Indian and multinational corporations on major financial transactions, structured debt, private equity deals, mergers & acquisitions (M&A), and IPOs.',
    salary: '₹16 - ₹40+ LPA (MDs / Partners: ₹80 LPA - ₹2 Cr+)',
    degree: 'B.Com / Economics / B.Tech + CFA / CA / Top Tier MBA (IIM A/B/C)'
  },
  {
    id: 'corporate-lawyer',
    title: 'Corporate Mergers Lawyer',
    track: 'Law & Policy',
    image: '/corporate-lawyer.jpg',
    description: 'Structure high-value cross-border acquisitions, corporate joint ventures, private equity investments, and regulatory compliance at India’s top tier-1 law firms.',
    salary: '₹12 - ₹32+ LPA (Equity Partners: ₹75 LPA - ₹1.8 Cr+)',
    degree: 'CLAT -> BA LLB / BBA LLB (NLUs) -> LL.M / Corporate Practice'
  },
  {
    id: 'venture-capitalist',
    title: 'Venture Capitalist',
    track: 'Entrepreneurship & Business',
    image: '/venture-capitalist.jpg',
    description: 'Identify, fund, and mentor high-potential technology startups across India. Evaluate pitch decks, conduct financial audits, and deploy investment capital.',
    salary: '₹18 - ₹45+ LPA + Carried Interest / Equity',
    degree: 'Engineering / Economics Undergrad + IIM/ISB MBA'
  },
  {
    id: 'clinical-psychologist',
    title: 'Clinical Psychologist',
    track: 'Arts & Humanities',
    image: '/clinical-psychologist.jpg',
    description: 'Diagnose and treat mental health and behavioral conditions. Provide evidence-based cognitive therapy in hospitals, psychiatric rehabilitation centers, and private clinical setups.',
    salary: '₹5 - ₹16+ LPA (Established Consultants: ₹20 - ₹40+ LPA)',
    degree: 'BA/B.Sc Psychology -> MA/M.Sc -> M.Phil/Psy.D (RCI Approved)'
  },
  {
    id: 'international-diplomat',
    title: 'International Diplomat',
    track: 'International Relations',
    image: '/international-diplomat.jpg',
    description: 'Represent India on international stages, embassies, and multilateral forums. Negotiate bilateral treaties, manage diplomatic missions, and execute foreign policy.',
    salary: '₹10 - ₹24+ LPA (UPSC Indian Foreign Service Cadre / Allowances)',
    degree: 'Any Graduation -> UPSC Civil Services Examination (IFS Cadre)'
  },
  {
    id: 'investigative-journalist',
    title: 'Investigative Journalist',
    track: 'Media & Communications',
    image: '/investigative-journalist.jpg',
    description: 'Conduct investigative reporting, expose policy malpractices, and author impactful long-form features for prominent newsrooms, digital portals, and national publications.',
    salary: '₹5 - ₹16+ LPA (Senior Editors / Columnists: ₹25 - ₹50+ LPA)',
    degree: 'BA/MA in Journalism & Mass Communication (IIMC / Jamia / ACJ)'
  },
  {
    id: 'architectural-designer',
    title: 'Architectural Designer',
    track: 'Creative Arts & Design',
    image: '/architectural-designer.jpg',
    description: 'Create architectural blueprints, commercial workspaces, and sustainable urban infrastructure compliant with local municipal codes and green building standards.',
    salary: '₹6 - ₹18+ LPA (Principal Architects / Firm Founders: ₹30 - ₹70+ LPA)',
    degree: 'NATA / JEE -> B.Arch (SPA Delhi / CEPT / IITs)'
  }
];

export default function HomePage() {
  const [selectedCareer, setSelectedCareer] = useState<typeof CAREERS[0] | null>(null);
  
  useEffect(() => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('opacity-100', 'translate-y-0');
          entry.target.classList.remove('opacity-0', 'translate-y-12');
        }
      });
    }, { threshold: 0.1 });

    const hiddenElements = document.querySelectorAll('.reveal-on-scroll');
    hiddenElements.forEach((el) => observer.observe(el));

    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    if (selectedCareer) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'auto';
    }
  }, [selectedCareer]);

  return (
    <main className="min-h-screen w-full relative bg-[#EFE6D5] text-[#0a1118] selection:bg-[#B89B72] selection:text-white flex flex-col font-sans overflow-x-hidden">
      
      <div className="absolute inset-0 z-0 pointer-events-none bg-[radial-gradient(ellipse_at_bottom_right,_var(--tw-gradient-stops))] from-[#E5D4C0] via-[#EFE6D5]/80 to-[#EFE6D5] opacity-90"></div>

      <nav className="relative z-50 w-full max-w-[1400px] mx-auto px-8 md:px-16 flex justify-between items-center py-8">
        <a href="/" className="font-serif text-2xl tracking-[0.15em] text-[#0a1118] uppercase font-bold group">
          Clarity<span className="italic text-[#C2A878] font-light group-hover:text-[#0a1118] transition-colors">OS</span>
        </a>
        <div className="flex items-center gap-8">
          <a href="/assessment" className="hidden md:block text-[11px] font-bold uppercase tracking-[0.2em] text-[#0a1118]/60 hover:text-[#0a1118] transition-colors">
            Take Assessment
          </a>
          <a href="/signup" className="border border-[#0a1118] text-[#0a1118] px-7 py-3 text-[10px] uppercase font-bold tracking-[0.2em] hover:bg-[#0a1118] hover:text-white transition-all duration-300 rounded-sm shadow-sm">
            Sign In
          </a>
        </div>
      </nav>

      <div className="relative z-10 w-full max-w-[1400px] mx-auto px-8 md:px-16 pt-8 pb-28 flex flex-col lg:flex-row items-center gap-16 lg:gap-20">
        <div className="flex-1 space-y-8 w-full">
          <h1 className="font-serif text-6xl md:text-7xl lg:text-[5.5rem] text-[#0a1118] leading-[1.05] tracking-wide uppercase">
            Elevate Your <br /> Vision. <br/> 
            <span className="italic text-[#4a5568] font-light">Build Your <br /> Career.</span>
          </h1>
          <div className="w-12 h-[2px] bg-[#C2A878]"></div>
          <p className="text-sm md:text-base text-[#0a1118]/70 font-sans tracking-wide max-w-md leading-relaxed">
            A smart, personalized career guide for every student. Discover your true path and unlock a roadmap tailored to your unique strengths and passions.
          </p>
          <div className="pt-4">
            <a 
              href="/assessment" 
              className="bg-[#C2A878] text-white px-8 py-5 text-[10px] uppercase font-bold tracking-[0.2em] hover:bg-[#a89060] shadow-[0_12px_30px_rgba(194,168,120,0.35)] hover:-translate-y-0.5 transition-all duration-300 inline-block rounded-sm"
            >
              Uncover Your Direction
            </a>
          </div>
        </div>

        <div className="flex-1 w-full relative mt-12 lg:mt-0 flex justify-center lg:justify-end">
          <div className="relative w-full max-w-md aspect-[3/4] shadow-[0_20px_50px_rgba(0,0,0,0.15)] group overflow-hidden cursor-pointer rounded-sm bg-transparent">
            <img 
              src="/girl-reading.jpg" 
              alt="Student planning career" 
              onError={(e) => { e.currentTarget.src = 'https://images.unsplash.com/photo-1456406644174-8ddd4cd52a06?q=80&w=1200&auto=format&fit=crop'; }}
              className="w-full h-full object-cover transition-transform duration-1000 ease-out group-hover:scale-105"
            />
            <div className="absolute inset-0 w-[200%] h-full bg-gradient-to-r from-transparent via-white/35 to-transparent -translate-x-[150%] group-hover:translate-x-[100%] transition-transform duration-1000 ease-in-out skew-x-12 pointer-events-none z-20"></div>
          </div>
        </div>
      </div>

      {/* Discover Careers Grid */}
      <div className="relative z-10 w-full max-w-[1400px] mx-auto px-8 md:px-16 py-24 border-t border-[#C2A878]/30">
        <div className="flex justify-center mb-16">
          <h2 className="font-serif text-xl tracking-[0.2em] uppercase text-[#0a1118] text-center">
            Discover Careers
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {CAREERS.map((career, index) => (
            <div 
              key={career.id}
              onClick={() => setSelectedCareer(career)}
              className="reveal-on-scroll opacity-0 translate-y-12 transition-all duration-700 ease-out group cursor-pointer flex flex-col"
              style={{ transitionDelay: `${index * 50}ms` }}
            >
              <div className="w-full aspect-square overflow-hidden shadow-lg mb-4 rounded-sm bg-[#e8ded1] relative">
                <img 
                  src={career.image} 
                  alt={career.title} 
                  className="w-full h-full object-cover transition-transform duration-700 ease-out group-hover:scale-110"
                  onError={(e) => { e.currentTarget.src = 'https://images.unsplash.com/photo-1456406644174-8ddd4cd52a06?q=80&w=600&auto=format&fit=crop'; }}
                />
                <div className="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition-colors duration-500"></div>
              </div>
              
              <h3 className="font-serif text-lg text-[#0a1118] leading-snug group-hover:text-[#C2A878] transition-colors duration-300">
                {career.title}
              </h3>
              <p className="text-[10px] uppercase tracking-[0.15em] text-[#0a1118]/50 mt-1 font-bold">
                {career.track}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Quotes Section */}
      <div className="relative z-10 w-full max-w-[1400px] mx-auto px-8 md:px-16 py-24 border-t border-[#C2A878]/30">
        <div className="flex justify-center mb-16">
          <h2 className="font-serif text-xl tracking-[0.2em] uppercase text-[#0a1118] text-center">
            Inspiration
          </h2>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="group relative reveal-on-scroll opacity-0 translate-y-12 transition-all duration-1000 ease-out delay-100 bg-[#2B3A4A] text-white p-12 shadow-xl flex flex-col justify-center items-center h-full min-h-[320px] cursor-pointer hover:-translate-y-3 hover:shadow-2xl overflow-hidden rounded-sm text-center">
            <div className="absolute inset-0 w-[200%] h-full bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-[150%] group-hover:translate-x-[100%] transition-transform duration-1000 ease-in-out skew-x-12 pointer-events-none"></div>
            <p className="font-serif text-lg lg:text-xl italic leading-relaxed text-gray-100 relative z-10">
              “The only way to do great work is to love what you do. If you haven't found it yet, keep looking. Don't settle.”
            </p>
            <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-[#C2A878] mt-8 relative z-10">
              — Steve Jobs
            </p>
          </div>

          <div className="group relative reveal-on-scroll opacity-0 translate-y-12 transition-all duration-1000 ease-out delay-300 bg-[#2B3A4A] text-white p-12 shadow-xl flex flex-col justify-center items-center h-full min-h-[320px] cursor-pointer hover:-translate-y-3 hover:shadow-2xl overflow-hidden rounded-sm text-center">
            <div className="absolute inset-0 w-[200%] h-full bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-[150%] group-hover:translate-x-[100%] transition-transform duration-1000 ease-in-out skew-x-12 pointer-events-none"></div>
            <p className="font-serif text-lg lg:text-xl italic leading-relaxed text-gray-100 relative z-10">
              “Nothing will work unless you do.”
            </p>
            <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-[#C2A878] mt-8 relative z-10">
              — Maya Angelou
            </p>
          </div>

          <div className="group relative reveal-on-scroll opacity-0 translate-y-12 transition-all duration-1000 ease-out delay-500 bg-[#2B3A4A] text-white p-12 shadow-xl flex flex-col justify-center items-center h-full min-h-[320px] cursor-pointer hover:-translate-y-3 hover:shadow-2xl overflow-hidden rounded-sm text-center">
            <div className="absolute inset-0 w-[200%] h-full bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-[150%] group-hover:translate-x-[100%] transition-transform duration-1000 ease-in-out skew-x-12 pointer-events-none"></div>
            <p className="font-serif text-lg lg:text-xl italic leading-relaxed text-gray-100 relative z-10">
              “All our dreams can come true, if we have the courage to pursue them.”
            </p>
            <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-[#C2A878] mt-8 relative z-10">
              — Walt Disney
            </p>
          </div>
        </div>
      </div>

      {/* Modal Inspector */}
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

              <a 
                href="/assessment" 
                className="bg-[#0a1118] text-white text-center px-8 py-3.5 text-[10px] uppercase font-bold tracking-[0.2em] hover:bg-[#C2A878] transition-colors duration-300 w-full rounded-sm"
              >
                Are you a match? Take Assessment
              </a>
            </div>
          </div>
        </div>
      )}

    </main>
  );
}