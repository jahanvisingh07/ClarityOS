'use client';

import React, { useState } from 'react';

export default function AssessmentPage() {
  const [stage, setStage] = useState('level');
  const [selectedLevel, setSelectedLevel] = useState('');
  const [selectedStream, setSelectedStream] = useState('');
  const [currentStep, setCurrentStep] = useState(1);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [validationError, setValidationError] = useState('');

  // Arrays (PCB, PCM, Commerce, Arts, Med, Tech, Eng, Business, Arts, Law, Creative)
  const pcbQuestions = [
    { id: 1, title: "Which subject do you enjoy the most?", options: ["Biology", "Chemistry", "Physics", "All three equally", "None particularly"] },
    { id: 2, title: "Which part of Biology interests you the most?", options: ["Human body and diseases", "Animals and wildlife", "Plants and environment", "Genetics and DNA", "Microorganisms", "Brain and behaviour", "Cells and molecular biology", "I am not sure yet"] },
    { id: 3, title: "Which sounds most exciting to you?", options: ["Diagnosing and treating a patient", "Discovering a new medicine or treatment", "Understanding how the human body works", "Studying diseases at a cellular or genetic level", "Working with animals", "Studying the environment and living organisms", "Helping people improve their health", "Conducting scientific research"] },
    { id: 4, title: "How comfortable are you with direct patient interaction?", options: ["I would love it", "I would be comfortable with it", "I am unsure", "I would rather have limited interaction", "I do not want patient interaction"] },
    { id: 5, title: "How comfortable are you with blood, injuries, and medical procedures?", options: ["Completely comfortable", "Mostly comfortable", "I can handle it", "A little uncomfortable", "Very uncomfortable"] },
    { id: 6, title: "Which sounds more satisfying?", options: ["Helping one patient directly", "Developing something that could help thousands or millions of people", "Discovering new scientific knowledge", "Educating people about health", "Protecting and improving the health of communities"] },
    { id: 7, title: "How interested are you in the human body?", options: ["Extremely interested", "Very interested", "Somewhat interested", "Not particularly interested"] },
    { id: 8, title: "Which type of work environment would you prefer?", options: ["Hospital or clinic", "Laboratory", "Research institute or university", "Pharmaceutical or biotech company", "Field or outdoor environment", "Office or health organization", "A combination"] },
    { id: 9, title: "How do you feel about Chemistry?", options: ["I love it", "I like it", "It is okay", "I struggle with it", "I really dislike it"] },
    { id: 10, title: "How do you feel about Physics?", options: ["I love it", "I like it", "It is okay", "I struggle with it", "I really dislike it"] },
    { id: 11, title: "How do you feel about memorization-heavy studying?", options: ["I do not mind it", "I am okay with it", "I prefer understanding over memorizing", "I really dislike memorization"] },
    { id: 12, title: "Which statement sounds more like you?", options: ["I want a career where I interact with people every day.", "I want a career where I can work deeply with science and information.", "I want a balance of both."] },
    { id: 13, title: "How interested are you in research and experimentation?", options: ["Extremely interested", "Very interested", "Somewhat interested", "Not particularly interested", "Not interested"] },
    { id: 14, title: "Which population would you most enjoy working with?", options: ["Children", "Adults", "Elderly people", "Animals", "Everyone", "Researchers or scientists rather than patients", "I do not know"] },
    { id: 15, title: "How important is direct impact on people's lives to you?", options: ["Extremely important", "Very important", "Somewhat important", "Not particularly important"] },
    { id: 16, title: "What matters MOST to you in your future career? (Pick up to 3)", options: ["High earning potential", "Helping people", "Scientific discovery", "Intellectual challenge", "Work-life balance", "Prestige or status", "Job security", "International opportunities", "Innovation", "Working in healthcare", "Making an environmental or social impact", "Leadership"] },
    { id: 17, title: "How do you feel about working under high pressure?", options: ["I perform well under pressure", "I can handle it", "Depends on the situation", "I prefer a low-pressure environment", "I strongly dislike high-pressure environments"] },
    { id: 18, title: "Are you willing to spend many years in education and training before becoming established in your career?", options: ["Yes, absolutely", "Yes, if the career is worth it", "I am unsure", "I would prefer a shorter path"] },
    { id: 19, title: "What best describes your current career situation?", options: ["I definitely want to become a doctor", "I know I want Biology or healthcare, but not medicine", "I am interested in research or science", "I am interested in medicines or pharmaceuticals", "I am interested in psychology or brain behaviour", "I am interested in environment, animals, or life sciences", "I have no idea yet", "I have several options and cannot decide"] },
    { id: 20, title: "If MBBS did not exist, which of these careers would you be most curious to explore?", options: ["Dentist", "Veterinarian", "Pharmacist", "Physiotherapist", "Psychologist", "Biotechnology and Genetics", "Microbiology", "Neuroscience", "Nutrition and Dietetics", "Public Health", "Medical Laboratory Science", "Forensic Science", "Research Scientist", "Environmental or Life Sciences", "Something completely different", "I have no idea"] }
  ];

  const pcmQuestions = [
    { id: 1, title: "Which subject do you enjoy solving problems in the most?", options: ["Mathematics", "Physics", "Chemistry", "Computer Science / Coding", "I like them equally"] },
    { id: 2, title: "Which area of Mathematics do you find most interesting?", options: ["Algebra and Number Theory", "Geometry and Trigonometry", "Probability and Statistics", "Advanced Calculus, Differential Equations, and Fourier Series", "I do not enjoy math much"] },
    { id: 3, title: "Which activity sounds the most exciting to you?", options: ["Writing code and building software", "Designing and building physical machines", "Analyzing complex data to find patterns", "Designing buildings and physical structures", "Solving pure, abstract logical problems"] },
    { id: 4, title: "How do you prefer to approach a complex problem?", options: ["Applying theoretical formulas to find the exact answer", "Building a physical prototype and testing it", "Writing a script or algorithm to automate the solution", "Drawing or visualizing the solution first"] },
    { id: 5, title: "What is your relationship with programming/coding?", options: ["I love it and code frequently", "I have tried it and like it", "I have not tried it much, but I am interested", "I have tried it and do not like it", "I have no interest in coding"] },
    { id: 6, title: "Which part of Physics fascinates you the most?", options: ["Mechanics and Motion", "Electricity, Magnetism, and Circuits", "Thermodynamics and Fluids", "Quantum and Modern Physics", "I am not very interested in Physics"] },
    { id: 7, title: "How easy is it for you to visualize 3D objects and structures in your mind?", options: ["Very easy, I can rotate them in my head", "Somewhat easy", "It takes some effort", "I struggle with 3D visualization"] },
    { id: 8, title: "Which type of work environment appeals to you most?", options: ["A modern tech office or remote setup", "A manufacturing plant or testing facility", "A research laboratory", "A construction site or project field", "A design or architecture studio"] },
    { id: 9, title: "When a system or code fails, what is your reaction?", options: ["I will sit for hours debugging until I fix it", "I get frustrated but will push through", "I prefer asking for help or moving on to something else"] },
    { id: 10, title: "How do you prefer to work?", options: ["Deep, uninterrupted solo work", "Collaborating closely with a technical team", "Leading a project and managing resources", "Working directly with clients to design what they want"] },
    { id: 11, title: "How do you feel about Chemistry?", options: ["I enjoy Physical Chemistry (equations/thermodynamics)", "I enjoy Organic/Inorganic Chemistry", "I tolerate it because I have to", "I strongly dislike Chemistry"] },
    { id: 12, title: "Do you prefer focusing on micro-details or the big picture?", options: ["Micro-details (like a single line of code or data point)", "The big picture (like the overall structural design of a bridge or system)"] },
    { id: 13, title: "What kind of innovation would you want to be a part of?", options: ["Creating the next big digital app or software", "Building advanced robotics or aerospace tech", "Developing new AI and machine learning models", "Designing sustainable smart cities and infrastructure"] },
    { id: 14, title: "Hardware or Software?", options: ["Pure Software (Apps, Web, AI)", "Pure Hardware (Engines, Structures, Materials)", "A mixture of both (Robotics, Microchips, IoT)"] },
    { id: 15, title: "How would you prefer to apply mathematics in your career?", options: ["Using algorithms to predict financial or digital trends", "Applying engineering physics to ensure machines work safely", "Exploring pure theories, models, and complex equations for research", "Using geometry to ensure structural integrity and aesthetics"] },
    { id: 16, title: "What matters MOST to you in your future career? (Pick up to 3)", options: ["High earning potential", "Building tangible, physical things", "Being at the forefront of digital tech", "Designing sustainable/eco-friendly systems", "Remote work flexibility", "Deep scientific or mathematical research", "Job security", "Creative expression"] },
    { id: 17, title: "How do you feel about abstract logic puzzles?", options: ["I absolutely love them", "They are okay", "I do not enjoy them"] },
    { id: 18, title: "What are your thoughts on higher education?", options: ["I want to start working right after my B.Tech/Degree", "I want to pursue a Master's degree (M.Tech/MS/MBA)", "I want to pursue a PhD and go into deep research"] },
    { id: 19, title: "What best describes your current career leanings?", options: ["I definitely want to go into IT/Computer Science", "I want a core engineering field (Mechanical/Civil/Electrical)", "I am highly interested in Architecture/Design", "I want to work with data, AI, or pure mathematics", "I am completely undecided"] },
    { id: 20, title: "If Software Engineering did not exist, which of these would you explore?", options: ["Data Analyst / Quant", "Aerospace Engineer", "Architect", "Robotics & Electronics Engineer", "Civil Engineer", "Research Mathematician", "Product Designer", "I have no idea"] }
  ];

  const commerceQuestions = [
    { id: 1, title: "Which core subject do you find the most interesting?", options: ["Accountancy", "Economics", "Business Studies", "Mathematics", "None of these"] },
    { id: 2, title: "What type of data are you most comfortable working with?", options: ["Financial balance sheets and tax numbers", "Macro market trends and stock charts", "Legal documents and contracts", "Consumer behaviour and brand analytics", "Employee performance and team data"] },
    { id: 3, title: "Which activity sounds the most exciting to you?", options: ["Auditing a massive company's financials for fraud", "Predicting the stock market and investing millions", "Arguing a high-stakes corporate legal case", "Designing a viral marketing campaign", "Building a business from zero to a million dollars"] },
    { id: 4, title: "What is your relationship with Mathematics and Statistics?", options: ["I love advanced math (Calculus/Probability)", "I am great at basic arithmetic and percentages, but hate calculus", "I can tolerate it if I have to", "I strongly dislike anything involving math"] },
    { id: 5, title: "How do you feel about rules, laws, and compliance?", options: ["I strictly follow them and ensure others do too", "I like finding creative loopholes within the rules", "I find rules restricting and prefer total freedom", "I enjoy studying how laws are made and enforced"] },
    { id: 6, title: "What is your natural risk appetite?", options: ["Very high: High risk, high reward (I want to build my own empire)", "Calculated: I only take risks backed by heavy data", "Low: I prefer job security, stability, and guaranteed income"] },
    { id: 7, title: "If you had a budget of $10,000 for a business, where would you spend it?", options: ["Invest it in stocks or mutual funds", "Hire a legal and financial team to secure assets", "Spend it on Facebook ads and branding", "Build a prototype of a new product to sell", "Save it in a high-interest account"] },
    { id: 8, title: "What kind of work environment do you prefer?", options: ["A quiet desk dealing with complex spreadsheets", "A high-adrenaline trading floor or investment bank", "A professional law firm or courtroom", "A vibrant, creative advertising studio", "A chaotic but exciting startup hub"] },
    { id: 9, title: "How do you feel about public speaking and presenting?", options: ["I love pitching ideas and convincing crowds", "I am great at debating and arguing my point", "I prefer presenting data and facts to a small board", "I strongly dislike speaking in front of people"] },
    { id: 10, title: "How do you deal with high-pressure, strict deadlines?", options: ["I thrive under extreme pressure and long hours", "I can manage it if the pay is excellent", "I prefer a structured 9-to-5 with no overtime"] },
    { id: 11, title: "How do you feel about reading hundreds of pages of text or case studies?", options: ["I actually enjoy reading deep laws and cases", "I can skim them to find what I need", "I would much rather look at a spreadsheet than read text"] },
    { id: 12, title: "Are you more interested in the 'Product' or the 'People'?", options: ["The Product/Service (Sales, Marketing, Quality)", "The People (Hiring, Psychology, Culture)", "The Numbers (Revenue, Margins, Taxes)"] },
    { id: 13, title: "When solving a business problem, what is your first instinct?", options: ["Check the budget and financial limitations", "Look at the legal risks and contracts", "Brainstorm creative workarounds", "Analyze what the competitors are doing"] },
    { id: 14, title: "What sounds like the most painful part of a job?", options: ["Doing repetitive math and data entry every day", "Having zero creative freedom", "Dealing with angry employees or clients", "Reading boring legal clauses"] },
    { id: 15, title: "How would you prefer to interact with a client?", options: ["Advising them on how to save money on taxes", "Defending them in a dispute", "Pitching them a new brand strategy", "Helping them merge their company with another"] },
    { id: 16, title: "What matters MOST to you in your future career? (Pick up to 3)", options: ["Extreme wealth / High salary", "Work-life balance", "Power and influence", "Creative expression", "Job security", "Building something of my own", "Helping people / Social impact"] },
    { id: 17, title: "How do you feel about 'Sales'?", options: ["I am a natural salesperson", "I can sell if I believe in the product", "I want absolutely nothing to do with sales"] },
    { id: 18, title: "What are your higher education goals?", options: ["I want to clear competitive professional exams (CA/CS/CFA)", "I want to get a top-tier MBA", "I want to go to Law School (LLB)", "I want to start working or building a business immediately"] },
    { id: 19, title: "What best describes your current career leanings?", options: ["I want a hardcore finance/accounting role", "I want to be a corporate lawyer", "I want to go into marketing or management", "I want to be an entrepreneur", "I am completely undecided"] },
    { id: 20, title: "If you could only choose one title, what would it be?", options: ["Chief Financial Officer (CFO)", "Investment Banker", "Corporate Lawyer", "Chief Marketing Officer (CMO)", "Startup Founder / CEO", "Chief Human Resources Officer (HR)", "Actuary / Risk Analyst"] }
  ];

  const artsQuestions = [
    { id: 1, title: "Which core subject captivates you the most?", options: ["Psychology", "Political Science", "Literature / English", "History", "Fine Arts / Design", "Sociology"] },
    { id: 2, title: "How do you prefer to express your ideas?", options: ["Through creative writing or storytelling", "Through public speaking and debate", "Through visual art, graphics, or photography", "Through factual reporting and articles", "Through listening and offering advice"] },
    { id: 3, title: "Which activity sounds the most fulfilling to you?", options: ["Helping an individual overcome mental health struggles", "Reporting on a major global news event", "Drafting policies to solve a social issue", "Writing a novel or editing a magazine", "Creating a beautiful painting or animation", "Studying ancient ruins and civilizations"] },
    { id: 4, title: "How do you feel about heavy reading and research?", options: ["I love reading deep academic or historical texts", "I enjoy reading fiction and creative writing", "I prefer staying updated with daily news and global affairs", "I prefer visual media over heavy reading"] },
    { id: 5, title: "What excites you more to understand?", options: ["Why an individual behaves the way they do", "How society and cultures evolve over time", "How governments negotiate and hold power", "How to make information visually appealing"] },
    { id: 6, title: "How do you usually handle highly emotional situations?", options: ["I am highly empathetic and absorb others' feelings", "I try to analyze the psychology behind it objectively", "I channel those emotions into art or writing", "I focus on the social justice or systemic issue causing it"] },
    { id: 7, title: "What kind of work environment sounds ideal?", options: ["A quiet, one-on-one therapy office", "A fast-paced newsroom or media studio", "A government office, embassy, or UN branch", "A creative design studio or art gallery", "A museum, archive, or archaeological site", "Working in the community with an NGO"] },
    { id: 8, title: "If you wanted to change the world, how would you do it?", options: ["By healing one person's mind at a time", "By exposing the truth to the masses", "By rewriting laws and international treaties", "By creating art or literature that inspires a generation", "By organizing community social work"] },
    { id: 9, title: "What is your relationship with writing?", options: ["I love creative, poetic, or fictional writing", "I prefer factual, journalistic, or investigative writing", "I write heavy academic, historical, or political essays", "I do not enjoy writing much; I prefer visual or spoken work"] },
    { id: 10, title: "How do you feel about public speaking and debating?", options: ["I thrive in debates and model UNs", "I am great at communicating via a camera or microphone", "I prefer one-on-one conversations", "I prefer communicating purely through text or art"] },
    { id: 11, title: "What is your relationship with visual arts and design?", options: ["I have strong artistic/design skills and do it constantly", "I dabble in it and have a good aesthetic eye", "I do not create art, but I heavily appreciate it", "I have zero interest in visual arts"] },
    { id: 12, title: "How do you feel about working with vulnerable or distressed populations?", options: ["I feel a strong calling to directly help them (Social Work/Therapy)", "I want to document their stories (Journalism)", "I want to change the laws affecting them (Politics)", "I would struggle to handle it emotionally"] },
    { id: 13, title: "Which of these topics dominates your internet browsing or reading?", options: ["Mental health, human behavior, or self-improvement", "Global conflicts, elections, and government policies", "Current events, pop culture, and social media trends", "Book reviews, literature, and creative writing", "Art portfolios, design trends, and aesthetics", "Documentaries about history or ancient cultures"] },
    { id: 14, title: "How interested are you in foreign languages and cultures?", options: ["Extremely interested, I want to travel or work internationally", "I am interested in their historical evolution", "I am mostly focused on my own region's societal issues"] },
    { id: 15, title: "What is your preferred conflict resolution style?", options: ["Mediation, understanding, and psychological support", "Debate, diplomacy, and legal frameworks", "Raising public awareness about the conflict"] },
    { id: 16, title: "What matters MOST to you in your future career? (Pick up to 3)", options: ["Creative freedom", "Social impact and helping others", "Understanding the human mind", "Influence and shaping policies", "Uncovering the truth", "Creating aesthetic beauty", "Preserving history", "Work-life balance"] },
    { id: 17, title: "Are you more interested in the Past, Present, or Future?", options: ["The Past (History, Anthropology, Classics)", "The Present (Journalism, Sociology, Therapy)", "The Future (Policy making, International Relations)"] },
    { id: 18, title: "What are your thoughts on higher education?", options: ["I plan to get a Master's/PhD in Psychology or Counseling", "I want to go to a specialized Journalism or Media school", "I want to get a Master's in International Relations or Public Policy", "I want to build a creative portfolio rather than do heavy academics"] },
    { id: 19, title: "What best describes your current career leanings?", options: ["I want to be a psychologist or therapist", "I want to work in media, journalism, or mass comm", "I want to enter politics, civil services, or diplomacy", "I want to be a writer, author, or editor", "I want to be a designer, animator, or fine artist", "I want to be a historian or archaeologist"] },
    { id: 20, title: "If you could only choose one title, what would it be?", options: ["Clinical Psychologist", "Investigative Journalist", "Diplomat / Policy Advisor", "Published Author / Editor", "Creative Art Director", "Social Worker", "Historian / Archaeologist"] }
  ];

  const collegeMedQuestions = [
    { id: 1, title: "What is your absolute favorite part of your classes so far?", options: ["Learning about human diseases and patient care", "Working in the lab with DNA and cells", "Understanding how chemical drugs affect the body", "Looking at big data, trends, and global health", "Learning about muscles, movement, and physical recovery"] },
    { id: 2, title: "Where do you feel most comfortable working?", options: ["A fast-paced hospital or clinic", "A quiet, high-tech research lab", "A pharmaceutical manufacturing lab", "An office analyzing data and making policies", "A gym or physical rehabilitation center"] },
    { id: 3, title: "How much do you actually want to talk to patients every day?", options: ["All day long, I love direct patient care", "Just a little bit, I prefer the science side", "None at all, leave me in the lab", "I'd rather talk to whole communities or policymakers", "I want to spend weeks or months getting to know a patient's recovery journey"] },
    { id: 4, title: "How do you handle fast-paced, life-or-death stress?", options: ["Bring it on, I thrive in intense situations", "I can handle it, but I prefer a predictable schedule", "I prefer deep, slow, and careful research timelines", "I want to work on preventing the emergencies from happening in the first place"] },
    { id: 5, title: "Be honest: how do you feel about blood, surgery, and intense medical procedures?", options: ["Fascinated. I want to be in the operating room", "I can handle it, but it's not my favorite part", "I would rather work with medicines and pills", "I prefer working with microscopes and pipettes", "Nope, keep me away from needles and blood"] },
    { id: 6, title: "At what scale do you want to help people?", options: ["One person at a time, face-to-face", "Thousands of people by helping invent a new drug", "Entire cities or countries by improving health systems", "People recovering from physical injuries or disabilities"] },
    { id: 7, title: "Which of these sounds like a fun puzzle to solve?", options: ["Figuring out what illness a patient has based on their symptoms", "Finding a hidden genetic mutation in a DNA sequence", "Figuring out how to make a pill absorb into the body faster", "Mapping out exactly how a virus spread through a city", "Creating a custom exercise plan to fix a runner's bad knee"] },
    { id: 8, title: "Who do you want as your main coworkers?", options: ["Other doctors, surgeons, and nurses", "Scientists, biologists, and researchers", "Chemists and medical regulators", "Government officials, data analysts, and social workers", "Physical therapists, dietitians, and coaches"] },
    { id: 9, title: "Do you like having a predictable daily routine?", options: ["Not at all, I want every day to be a surprise (like the ER)", "Yes, I like the steady routine of running lab experiments", "I like having steady, scheduled patient appointments", "I like analyzing data at my own pace at a desk"] },
    { id: 10, title: "Which subject makes the most sense to your brain?", options: ["Pure anatomy and how the human body works", "Chemistry and molecular bonds", "Statistics, graphs, and maps", "Genetics and microbiology", "Kinesiology, sports, and body movement"] },
    { id: 11, title: "What would frustrate you the most in your career?", options: ["Losing a patient despite trying everything", "An experiment failing after months of hard work", "A new drug failing its safety trials", "People ignoring public health warnings and getting sick", "A patient not doing their rehab exercises at home"] },
    { id: 12, title: "What kind of news articles do you actually click on?", options: ["Crazy medical case studies and surgeries", "Breakthroughs in CRISPR and DNA editing", "New FDA drug approvals and pharmacy news", "Global health updates and pandemic tracking", "Sports medicine, wellness, or physical fitness tips"] },
    { id: 13, title: "How long are you willing to wait to see the results of your work?", options: ["I want immediate results (like fixing a wound or doing surgery)", "A few weeks or months (like watching a patient learn to walk again)", "Years (like developing a new drug or vaccine)"] },
    { id: 14, title: "Do you want to be the one calling the shots?", options: ["Yes, I want to be the lead doctor or surgeon in charge", "I want to run my own research lab", "I want to manage a city's health department", "I prefer being a supportive, hands-on team member"] },
    { id: 15, title: "If you had to pick one main tool for your career, what is it?", options: ["A stethoscope or scalpel", "A microscope or DNA sequencer", "Chemistry flasks and testing equipment", "A laptop with data software and maps", "Exercise equipment and therapy bands"] },
    { id: 16, title: "How do you feel about strict rules and FDA regulations?", options: ["They are crucial for drug safety and manufacturing", "They are important for protecting public health", "I follow hospital protocols strictly", "I find them annoying when I just want to innovate in the lab"] },
    { id: 17, title: "When you are 40 years old, what do you want to be known for?", options: ["Being an incredible, life-saving doctor", "Discovering a new gene or biological process", "Running a highly successful rehab or therapy clinic", "Developing a blockbuster medicine", "Stopping a major disease outbreak"] },
    { id: 18, title: "Let's talk lifestyle. What are your boundaries?", options: ["I don't mind crazy on-call hours if the work matters and pays well", "I want a strict 9-to-5 job with weekends off", "I want flexibility to do my research and publish papers", "I want a balanced schedule running a daily clinic"] },
    { id: 19, title: "How much more school are you realistically willing to do?", options: ["4-7+ more years (Medical School + Residency)", "I want to get my Master's or PhD for research", "I want a shorter specialized degree so I can start working soon"] },
    { id: 20, title: "If you had to switch to a completely non-medical field right now, what would it be?", options: ["Detective or Investigator", "Chemical Engineer", "Data Analyst or Politician", "Fitness Coach or Teacher", "Software Developer"] }
  ];

  const collegeTechQuestions = [
    { id: 1, title: "What gives you the biggest rush when working on a tech project?", options: ["Fixing a complex bug and seeing the app finally work", "Training a predictive model and seeing it output accurate data", "Finding a hidden security loophole in a system", "Automating a massive server deployment perfectly", "Making a 3D character or environment move and look amazing", "Sketching out the perfect, frictionless user journey", "Proving a new theoretical computer science algorithm or publishing a paper"] },
    { id: 2, title: "When you look at a popular app like Spotify or Instagram, what do you notice first?", options: ["How fast it loads and how the databases must be structured", "The recommendation algorithm that suggests new things to me", "How secure my personal data and passwords are", "How it stays online without crashing during viral moments", "The fluid animations and graphics rendering", "Where the buttons are placed and how easy it is to navigate", "The foundational computer science theory behind its distributed systems"] },
    { id: 3, title: "Be honest about debugging. How do you feel about tracking down a broken issue for 3 hours?", options: ["It's frustrating, but I love the satisfaction of finally fixing the code", "I'd rather be tweaking math and algorithms than hunting app bugs", "I enjoy reverse-engineering the exploit to see how it broke", "I'd rather automate the testing pipelines so it doesn't happen at all", "I'd rather spend that time tweaking physics or shaders for a visual", "I hate it. I want to focus on the big picture and the user flow", "I prefer analyzing mathematical proofs rather than debugging commercial code"] },
    { id: 4, title: "Which of these sounds like the most fun weekend project?", options: ["Building a fully functional web or mobile app from scratch", "Scraping a website to find cool data trends and graphs", "Competing in a 'Capture The Flag' hackathon to break into a server", "Setting up a home network or a Raspberry Pi cluster", "Building a mini 2D/3D game in a game engine", "Designing a beautiful Figma prototype for a startup idea", "Reading and summarizing a cutting-edge research paper on AI or Quantum Computing"] },
    { id: 5, title: "How much math do you actually want to do in your daily job?", options: ["Just basic logic and arithmetic to make functions work", "A massive amount. I love statistics, calculus, and probability", "Moderate amount, mostly cryptography and discrete math", "Not much, mostly just calculating server bandwidth and load", "A lot of physics, geometry, and linear algebra", "None if possible. I care about human psychology and design", "Extreme theoretical math, formal proofs, and complexity theory"] },
    { id: 6, title: "Who do you want to spend most of your time talking to at work?", options: ["Just my IDE and a few other software developers", "Data analysts and business executives", "Security auditors and compliance officers", "Network engineers and sysadmins", "Artists, animators, and sound designers", "The actual users, customers, and the marketing team", "Professors, research fellows, and academic peers"] },
    { id: 7, title: "If your team is building a new tech startup, what is your role?", options: ["The Lead Developer writing the core features", "The AI Wizard making the app 'smart'", "The Head of Security keeping the hackers out", "The Infrastructure Boss keeping the servers online", "The Technical Artist creating the interactive experience", "The Visionary deciding what features we actually need to build", "The Chief Scientist researching new underlying tech that doesn't exist yet"] },
    { id: 8, title: "What is your relationship with visual aesthetics (colors, fonts, layouts)?", options: ["I don't care how it looks, as long as it works perfectly under the hood", "I care more about how the data visualization charts look", "I don't care at all, just make it secure", "I don't care, just make it scalable", "I am obsessed with rendering, lighting, and textures", "I am obsessed with layouts, wireframes, and user experience", "I care about mathematical precision rather than visual aesthetics"] },
    { id: 9, title: "How do you feel about presenting your work in front of a room full of people?", options: ["I prefer just doing a quick screen-share demo of my working code", "I can do it if I'm explaining a cool data discovery", "I'd rather explain threat models and risks to management", "I'd rather show uptime metrics and performance charts", "I'd love to show off a cool visual demo or trailer", "I love it! I want to pitch the product vision to investors", "I want to present my research findings at international academic conferences"] },
    { id: 10, title: "What is your favorite type of puzzle?", options: ["Logic puzzles, coding katas, and riddles", "Number games, Sudoku, and pattern recognition", "Escape rooms where I have to break out (or break in)", "Optimizing a messy closet or organizing a complex system", "Spatial puzzles, Rubik's cubes, or building blocks", "Understanding why people make the decisions they do", "Solving unsolved theoretical theorems or abstract math problems"] },
    { id: 11, title: "What sounds like an absolute nightmare at work?", options: ["An app crashing because of a messy, tangled codebase", "A machine learning model giving completely biased or wrong answers", "Getting hacked and experiencing a massive data breach", "Servers crashing and going offline during a huge product launch", "Massive frame drops and laggy visuals ruining the experience", "Building an app that works perfectly but nobody actually wants to use", "Doing routine commercial coding instead of deep intellectual research"] },
    { id: 12, title: "Which tools or languages make you the most excited?", options: ["JavaScript, React, Node.js, or Java", "Python, R, SQL, and TensorFlow", "Kali Linux, Wireshark, or Metasploit", "AWS, Docker, Kubernetes, or Bash", "C++, C#, Unity, or Unreal Engine", "Figma, Adobe Creative Suite, or Trello", "LaTeX, MATLAB, Python, and research papers"] },
    { id: 13, title: "Do you prefer building things or breaking things?", options: ["Building! I want to create features from nothing", "Analyzing! I want to find hidden patterns in the noise", "Breaking! I want to find vulnerabilities before the bad guys do", "Optimizing! I want to make things run faster behind the scenes", "Creating! I want to build interactive worlds and simulations", "Designing! I want to make things beautiful and intuitive", "Exploring! I want to discover fundamental new computer science principles"] },
    { id: 14, title: "How do you feel about working with messy, unpredictable human behavior?", options: ["Keep it away from me. Code is logical, humans are not", "I like analyzing human behavior through massive datasets", "I assume humans are the weakest link and try to secure them", "I just want to route their web traffic efficiently", "I want to entertain them and evoke emotion through interaction", "I find it fascinating. I want to build products that solve their problems", "I prefer working with formal academic models over human messiness"] },
    { id: 15, title: "Where do you want to be in 10 years?", options: ["A Senior Developer or Chief Technology Officer (CTO)", "A Chief Data Scientist leading AI innovations", "A Chief Information Security Officer (CISO)", "A VP of Cloud Infrastructure or Lead DevOps Engineer", "A Lead Game Director or Technical Art Director", "A Chief Executive Officer (CEO) or Head of Product", "A University Professor, Research Scientist, or Lab Director with a Ph.D."] },
    { id: 16, title: "How do you handle rapid changes in technology?", options: ["I love learning the newest frontend/backend coding frameworks", "I focus on the core math and stats—those never really change", "I stay constantly updated on the latest zero-day vulnerabilities", "I constantly learn new cloud services and deployment automation", "I explore new rendering engines and graphics capabilities", "I focus on timeless human psychology and business strategy", "I study the deep theoretical fundamentals that govern all technology evolution"] },
    { id: 17, title: "If you had to read a 500-page book right now, what would it be about?", options: ["Clean Architecture and writing better software", "The future of Artificial Intelligence and Neural Networks", "The history of famous cyber attacks and hackers", "Site Reliability Engineering and scaling massive systems", "The making of a legendary video game or CGI movie", "Steve Jobs and the psychology of building iconic products", "An advanced academic textbook on Quantum Computing or Deep Learning theory"] },
    { id: 18, title: "What is your biggest strength?", options: ["Writing clean, efficient, and bug-free code", "Finding hidden trends in data that nobody else sees", "Thinking like an attacker to defend a system", "Organizing, automating, and scaling massive digital systems", "Blending heavy technical logic with creative visual art", "Communicating ideas and understanding what users really want", "Rigorous academic thinking, deep focus, and theoretical analysis"] },
    { id: 19, title: "When an app updates and changes its layout completely, what is your reaction?", options: ["I wonder what new code libraries they used to build it", "I wonder if they used A/B testing data to make this decision", "I wonder if this new update introduced any security bugs", "I wonder how their servers are handling the millions of downloads", "I critique the new UI animations and micro-interactions", "I critique whether the new layout is actually easier to use", "I wonder if they published a whitepaper explaining their algorithmic architecture"] },
    { id: 20, title: "What are your immediate goals regarding higher education?", options: ["I want to start working at a tech company right after my Bachelor's degree", "I want to work for a few years, then maybe get an MBA", "I definitely want to pursue a Master's degree (MS / M.Tech) immediately in a specialized field", "I want to pursue a Master's and eventually a Ph.D. to go into deep research or academia", "I want to build a creative portfolio rather than do heavy formal academics"] }
  ];

  const collegeEngineeringQuestions = [
    { id: 1, title: "What excites you the most when you look at the physical world around you?", options: ["How engines, robots, and machines actually move and operate", "How massive skyscrapers and bridges stay standing without collapsing", "The tiny microchips and circuit boards inside our electronics", "The raw materials, chemicals, and energy powering everything", "The deep mathematical physics and theoretical laws governing the universe"] },
    { id: 2, title: "Where is your absolute ideal work environment?", options: ["An aerospace hangar, automotive plant, or robotics lab", "Outdoors on a massive construction site or urban planning office", "A cleanroom designing hardware or an electronics workbench", "A heavy industrial processing plant or chemistry lab", "A quiet university office or national research laboratory"] },
    { id: 3, title: "If you had a free weekend and a $500 budget, what would you build?", options: ["A custom drone or a motorized go-kart", "A scale model of a sustainable, self-cooling house", "A smart-home gadget using Arduino or Raspberry Pi", "I'd experiment with making my own bio-plastics or battery cells", "I'd buy textbooks or software to run advanced math physics simulations"] },
    { id: 4, title: "When something you build completely fails, what is your first instinct?", options: ["Check the gears, motors, or moving parts", "Check the structural load and weight distribution math", "Get the multimeter and check the voltage and wiring", "Check the chemical balance, heat, or material properties", "Re-evaluate the fundamental equations and theoretical assumptions"] },
    { id: 5, title: "How do you feel about coding and software?", options: ["I only code if it makes my robot or machine move", "I only code for structural analysis or CAD software", "I love coding, but mostly for microcontrollers and embedded hardware", "I prefer chemistry and physics; I don't really want to code", "I use code heavily to model complex theoretical physics and math"] },
    { id: 6, title: "What kind of innovation do you most want to be a part of in your lifetime?", options: ["Next-generation spacecraft or autonomous robotics", "Eco-friendly smart cities and high-speed rail networks", "The next leap in quantum computing chips or wearable tech", "Inventing a new clean energy source or biodegradable plastic", "Discovering a new law of physics or publishing a breakthrough paper"] },
    { id: 7, title: "Which of these subjects makes the most sense to your brain?", options: ["Thermodynamics, fluid mechanics, and kinematics", "Statics, concrete design, and soil mechanics", "Electromagnetism, signals, and digital logic", "Organic chemistry, mass transfer, and polymer science", "Advanced calculus, quantum mechanics, and pure theory"] },
    { id: 8, title: "How do you prefer to tackle a problem?", options: ["Designing a 3D part and printing/machining it to see if it works", "Drawing a massive blueprint and calculating the safety factors", "Soldering components on a breadboard and testing the current", "Mixing compounds in a lab to test their reaction to heat", "Writing pages of equations on a whiteboard until it clicks"] },
    { id: 9, title: "What is your relationship with 'scale'?", options: ["I like things I can build and hold, like an engine or a robot", "I like massive scale—bridges, dams, and entire cities", "I like microscopic scale—transistors and nano-chips", "I like molecular scale—chemical bonds and atomic structures", "I like universal scale—theoretical concepts that apply everywhere"] },
    { id: 10, title: "How do you feel about strict safety regulations and compliance?", options: ["Crucial for making sure planes don't crash and machines don't fail", "The most important part of my job. If a building falls, people get hurt", "Important for avoiding electrical fires and short circuits", "Critical for preventing chemical spills and environmental disasters", "I find them annoying; I just want to focus on pure scientific discovery"] },
    { id: 11, title: "Who do you want as your primary coworkers?", options: ["Machinists, automotive designers, and aerospace technicians", "Architects, urban planners, and construction managers", "Software developers, hardware testers, and electrical techs", "Biologists, material scientists, and industrial plant operators", "Fellow Ph.D. students, professors, and research grants officers"] },
    { id: 12, title: "What sounds like the most frustrating part of a job?", options: ["A machine part wearing out due to friction after months of design", "A project getting delayed due to bad weather or zoning laws", "A tiny short circuit ruining an entire custom motherboard", "A chemical batch getting contaminated by one wrong drop", "Being forced to work on a commercial product instead of my own research"] },
    { id: 13, title: "What kind of YouTube videos or documentaries do you watch?", options: ["How jet engines work or Boston Dynamics robots", "Mega-engineering projects like the Burj Khalifa or the Panama Canal", "Tear-downs of new iPhones or custom PC builds", "How things are made in massive factories or chemistry experiments", "Deep dives into black holes, string theory, or advanced math"] },
    { id: 14, title: "Which tool do you naturally gravitate towards?", options: ["Wrenches, 3D printers, and AutoCAD", "Surveying equipment, hard hats, and blueprints", "Soldering irons, oscilloscopes, and wire strippers", "Beakers, safety goggles, and lab centrifuges", "Chalkboards, MATLAB, and massive research libraries"] },
    { id: 15, title: "Where do you see yourself in 10 years?", options: ["A Lead Mechanical Engineer at an aerospace or robotics firm", "A Senior Project Manager overseeing a massive city infrastructure build", "A Hardware Architect at a top tech company like Apple or Intel", "A Process Engineering Director at a chemical or energy plant", "A Tenured University Professor or Lead Research Scientist"] },
    { id: 16, title: "What is your stance on the environment and climate change?", options: ["We need to build better electric engines and aerodynamic transport", "We need to design greener buildings and better water management", "We need to build more efficient smart-grids and low-power devices", "We need to invent carbon-capture materials and better batteries", "We need to research the fundamental physics of climate models"] },
    { id: 17, title: "If you had to present your work, what would you show?", options: ["A working prototype of a physical machine I designed", "A massive 3D render of a proposed suspension bridge", "A perfectly functioning custom circuit board", "The results of a successful chemical synthesis", "A published academic paper with rigorous mathematical proofs"] },
    { id: 18, title: "What is your biggest strength?", options: ["Understanding how physical parts move and fit together", "Managing massive, complex, multi-stage physical projects", "Extreme attention to detail with tiny, fragile components", "Understanding complex chemical reactions and industrial processes", "Deep, uninterrupted focus on abstract theoretical concepts"] },
    { id: 19, title: "When you look at an electric car like a Tesla, what do you think about?", options: ["The aerodynamics and the dual-motor drivetrain", "How this will change city infrastructure and charging stations", "The embedded software, sensors, and the internal computer", "The lithium-ion battery chemistry and material cooling", "The academic physics research that made the battery tech possible"] },
    { id: 20, title: "What are your immediate goals regarding higher education?", options: ["Start working in the core engineering industry right after my B.Tech/B.E.", "Work for a few years, then maybe get an MBA for project management", "Get a quick Master's (MS/M.Tech) to specialize in a specific hardware/tech field", "Pursue a Master's and eventually a Ph.D. for deep academic research", "I haven't decided yet, I just want to learn everything I can right now"] }
  ];

  const collegeBusinessQuestions = [
    { id: 1, title: "What excites you most about the business world?", options: ["Analyzing financial models, valuations, and corporate M&A", "Designing viral marketing campaigns and brand identities", "Optimizing supply chains, logistics, and operational efficiency", "Building a high-risk startup and pitching to venture capitalists", "Conducting deep macroeconomic research and publishing economic papers"] },
    { id: 2, title: "Where is your ideal work environment?", options: ["A high-stakes trading floor or investment bank", "A creative advertising agency or modern marketing firm", "A massive corporate headquarters or global distribution center", "A chaotic, fast-paced startup incubator", "A quiet university office or government economic think tank"] },
    { id: 3, title: "If your team launches a new product, what is your primary focus?", options: ["Calculating its profit margins, ROI, and financial projections", "Creating a go-to-market strategy to acquire millions of users", "Figuring out how to manufacture and ship it globally at the lowest cost", "Securing seed funding to scale the business quickly", "Analyzing its long-term impact on global market trends"] },
    { id: 4, title: "How do you handle risk?", options: ["I manage it meticulously using financial derivatives and data", "I take creative risks to make a brand stand out", "I hate risk; I want predictable, efficient, and stable operations", "I thrive on extreme risk—high risk, high reward", "I prefer studying risk models theoretically rather than taking personal financial risks"] },
    { id: 5, title: "What type of data do you prefer working with?", options: ["Balance sheets, cash flow statements, and stock charts", "Consumer behavior metrics, social media analytics, and engagement rates", "Inventory levels, shipping times, and production yields", "Pitch deck projections and user acquisition costs", "Massive datasets of national GDP, inflation, and unemployment statistics"] },
    { id: 6, title: "Who do you want to spend most of your time talking to?", options: ["CFOs, bankers, and financial auditors", "Creative directors, influencers, and the target audience", "Suppliers, warehouse managers, and logistics partners", "Angel investors, co-founders, and early adopters", "Fellow researchers, professors, and policymakers"] },
    { id: 7, title: "What is your primary strength in a team setting?", options: ["Number-crunching and financial accuracy", "Brainstorming creative ideas and communicating them effectively", "Organizing chaos into a smooth, step-by-step process", "Leading the vision, taking charge, and inspiring people", "Providing deep, evidence-based research to inform decisions"] },
    { id: 8, title: "How do you feel about high-pressure, strict deadlines?", options: ["I thrive under the intense pressure of Wall Street hours", "I can handle it when launching a major ad campaign", "I prefer a steady, predictable operational schedule", "I expect it; startup founders never truly clock out", "I prefer long-term, self-paced research timelines"] },
    { id: 9, title: "What sounds like the most frustrating part of a job?", options: ["A minor math error ruining a million-dollar valuation", "A brilliant product failing because of boring marketing", "A supply chain bottleneck delaying thousands of orders", "Working for someone else and having zero equity in the company", "Being forced to focus on quarterly profits instead of long-term economic theory"] },
    { id: 10, title: "Which of these tools do you gravitate towards?", options: ["Advanced Excel, Bloomberg Terminals, and financial modeling software", "Google Analytics, HubSpot, and Adobe Creative Cloud", "SAP, Oracle, and enterprise resource planning (ERP) software", "Trello, Slack, and investor pitch decks", "Stata, R, Python, and econometric databases"] },
    { id: 11, title: "How do you view 'sales'?", options: ["It's about closing high-value corporate deals and mergers", "It's about understanding consumer psychology and brand loyalty", "It's a numbers game of volume and distribution efficiency", "It's about selling the vision of your company to anyone who will listen", "I prefer to analyze consumer demand academically rather than sell directly"] },
    { id: 12, title: "What kind of news do you read first?", options: ["Stock market movements, interest rates, and corporate earnings", "Pop culture trends, viral social media, and brand controversies", "Global trade agreements, shipping crises, and manufacturing updates", "TechCrunch startup funding rounds and unicorn valuations", "In-depth analyses from The Economist or academic journals"] },
    { id: 13, title: "If you had $100,000 to invest right now, what would you do?", options: ["Diversify it across index funds, bonds, and high-yield stocks", "Spend it on Facebook/Google ads to scale an e-commerce brand", "Invest in better software to automate a business's operations", "Use it as seed money to launch your own tech startup", "Fund an academic study on behavioral economics"] },
    { id: 14, title: "How do you approach a complex problem?", options: ["Build a financial model to see if it makes economic sense", "Run an A/B test or survey to see what the audience wants", "Map out the entire process flowchart to find the bottleneck", "Pivot the business strategy and try a completely new angle", "Read peer-reviewed literature to see how it was solved historically"] },
    { id: 15, title: "Where do you see yourself in 10 years?", options: ["A Managing Director at a top Investment Bank or Private Equity firm", "A Chief Marketing Officer (CMO) at a global consumer brand", "A Chief Operating Officer (COO) ensuring massive corporate efficiency", "A successful CEO / Founder who just took their startup public", "A Tenured Professor of Economics or Lead Researcher at a Think Tank"] },
    { id: 16, title: "What is your stance on corporate ethics?", options: ["Maximize shareholder value within the legal financial frameworks", "Ensure the brand maintains a positive, trustworthy public image", "Ensure suppliers follow fair labor and environmental practices", "Build a company culture that disrupts the industry but stays mission-driven", "Study the systemic impact of corporate monopolies on wealth inequality"] },
    { id: 17, title: "If you had to present your work, what would you show?", options: ["A flawless 50-page financial valuation report", "A highly engaging video ad that went viral", "A dashboard showing a 20% reduction in operational waste", "A pitch deck that secured $5M in venture capital", "A published academic paper on macroeconomic policy"] },
    { id: 18, title: "What is your biggest motivation?", options: ["Generating extreme wealth and financial power", "Having a creative impact on culture and trends", "Creating perfect order and efficiency out of chaos", "Building something of my own from scratch", "Advancing human knowledge in economics or business theory"] },
    { id: 19, title: "When a major company like Apple releases a new product, what do you think about?", options: ["How this impacts their stock price and quarterly revenue", "The psychology behind their minimalist marketing strategy", "The incredible logistics required to ship millions of units on day one", "How I could build a startup to compete with a niche feature they missed", "The broader economic implications on the global tech market"] },
    { id: 20, title: "What are your immediate goals regarding higher education?", options: ["Get my CFA or CPA and enter the corporate finance grind", "Start working in digital marketing or brand management immediately", "Get an MBA to transition into high-level operations or consulting", "Drop out or skip grad school to build my startup full-time", "Pursue a Master's and a Ph.D. in Economics or Business Administration"] }
  ];

  const collegeArtsQuestions = [
    { id: 1, title: "Which core area captivates you the most?", options: ["Understanding the human mind, trauma, and cognitive behavior", "Investigating stories, interviewing people, and reporting the truth", "Understanding community struggles, social justice, and systemic inequality", "Reading classic literature, writing stories, and analyzing historical texts", "Conducting deep, theoretical research in humanities or philosophy"] },
    { id: 2, title: "Where is your ideal work environment?", options: ["A quiet, private clinical therapy office or counseling center", "A fast-paced newsroom, media studio, or on-the-ground reporting", "Out in the community, working with NGOs or social services", "A publishing house, library, archive, or quiet writing desk", "A university classroom or advanced academic research institute"] },
    { id: 3, title: "If you wanted to change the world, how would you do it?", options: ["By helping individuals heal from mental health struggles one-on-one", "By exposing corruption and bringing truth to the masses", "By organizing community programs and fighting for marginalized groups", "By writing a novel or historical account that changes how people think", "By publishing groundbreaking sociological or psychological research"] },
    { id: 4, title: "How do you prefer to interact with people?", options: ["Deep, empathetic, one-on-one listening sessions", "Asking tough, direct questions to get to the bottom of a story", "Advocating for them, helping them navigate welfare systems", "I prefer interacting with their stories through text and history rather than face-to-face", "I prefer presenting lectures and discussing academic theories with peers"] },
    { id: 5, title: "What type of reading do you enjoy most?", options: ["Case studies on human psychology and brain development", "Current events, investigative journalism, and global news", "Books on social justice, activism, and societal structures", "Classic literature, fiction, poetry, or historical biographies", "Dense, peer-reviewed academic journals and philosophical treatises"] },
    { id: 6, title: "How do you handle highly emotional situations?", options: ["I naturally want to counsel them and analyze the root psychological cause", "I try to document it objectively to tell their story to the public", "I feel a strong urge to intervene and provide systemic resources to help them", "I process it internally and channel it into creative or editorial writing", "I step back and analyze it through an academic or theoretical lens"] },
    { id: 7, title: "What is your primary strength?", options: ["Extreme empathy and understanding of human behavior", "Excellent communication, writing under pressure, and networking", "Resilience in the face of societal struggles and a passion for advocacy", "A deep appreciation for language, narrative, and historical context", "Rigorous academic discipline and critical thinking skills"] },
    { id: 8, title: "What sounds like the most frustrating part of a job?", options: ["Having a client who refuses to do the work to improve their mental health", "A major news story breaking and you are stuck at a desk unable to cover it", "Bureaucratic red tape preventing a vulnerable person from getting help", "Dealing with writers' block or a terrible editorial team", "Being forced to teach basic classes instead of doing deep research"] },
    { id: 9, title: "Which of these tools do you gravitate towards?", options: ["Diagnostic manuals (DSM-5), therapy notes, and psychological assessments", "Microphones, cameras, press passes, and digital publishing platforms", "Case files, community resource directories, and intervention plans", "Manuscripts, historical archives, and word processors", "University databases, academic citations, and peer-review systems"] },
    { id: 10, title: "How do you feel about writing?", options: ["I write mostly clinical notes and patient observations", "I love writing fast, punchy, fact-driven articles on tight deadlines", "I write grants, policy proposals, and advocacy letters", "I love writing long-form creative narratives, poetry, or historical analyses", "I write highly structured, formally cited academic dissertations"] },
    { id: 11, title: "Who do you want to spend most of your time talking to?", options: ["Patients, clients, and fellow therapists", "Editors, sources, public figures, and the general public", "Vulnerable populations, social workers, and community leaders", "Authors, historians, publishers, and literary critics", "Fellow Ph.D. candidates, researchers, and university faculty"] },
    { id: 12, title: "What kind of news do you read first?", options: ["Breakthroughs in mental health treatments or cognitive science", "I read everything—I am obsessed with the media cycle itself", "Stories about housing, poverty, and local community issues", "Book reviews, cultural critiques, and historical retrospectives", "Academic discoveries and developments in higher education"] },
    { id: 13, title: "If you had a free weekend, what would you do?", options: ["Read a book on self-improvement or psychology", "Start a podcast or write a blog post about a trending topic", "Volunteer at a local shelter or community center", "Visit a museum, read a novel, or write in a journal", "Attend a lecture or dive into an academic research paper"] },
    { id: 14, title: "How do you approach a complex societal problem (like poverty)?", options: ["I look at how it affects the mental health and trauma of the individual", "I want to interview those affected and broadcast their reality", "I want to get on the ground and directly provide food, shelter, or resources", "I want to study how poverty was handled in different historical eras", "I want to research the systemic, sociological root causes and publish findings"] },
    { id: 15, title: "Where do you see yourself in 10 years?", options: ["A Licensed Clinical Psychologist with a successful private practice", "An Investigative Journalist or Chief Editor at a major news network", "A Director of a non-profit organization or Lead Social Worker", "A Published Author, Senior Editor, or Museum Curator", "A Tenured Professor or Lead Researcher in the Humanities"] },
    { id: 16, title: "What is your stance on objectivity?", options: ["I must remain a neutral blank slate so my client can heal", "I must remain completely unbiased to report the news accurately", "I cannot be objective; I must actively advocate for the marginalized", "Art and history are subjective; it's all about interpretation", "I rely strictly on peer-reviewed evidence and academic rigor"] },
    { id: 17, title: "If you had to present your work, what would you show?", options: ["A case study showing a patient's recovery over six months", "A viral documentary or a front-page investigative article", "A successful community program that lowered homelessness", "A beautifully edited anthology or a historical exhibition", "A defended Ph.D. dissertation or published academic journal"] },
    { id: 18, title: "What is your biggest motivation?", options: ["Understanding the human mind and helping people heal", "Seeking the truth and holding power accountable", "Fighting for social justice and equity", "Preserving human culture, language, and history", "Advancing theoretical knowledge in the social sciences"] },
    { id: 19, title: "When you watch a historical movie, what do you think about?", options: ["The psychological motivations of the characters", "How the media and propaganda of the time influenced the events", "The class struggles and social inequality depicted", "How accurate the costumes, dialogue, and historical timelines are", "How it aligns with the academic consensus of that era"] },
    { id: 20, title: "What are your immediate goals regarding higher education?", options: ["I need a Master's/Psy.D to get my clinical therapy license", "I want to start working in media or journalism immediately", "I need an MSW (Master of Social Work) to advance in my field", "I want to write or edit while perhaps getting an MFA in Creative Writing", "I am fully committed to pursuing a Ph.D. for a career in academia"] }
  ];

  const collegeLawQuestions = [
    { id: 1, title: "Which aspect of law and policy excites you the most?", options: ["Corporate mergers, contracts, and high-stakes business deals", "Being in a courtroom, defending the accused, or prosecuting criminals", "Writing legislation, shaping public policy, and advising government", "Cross-border negotiations, treaties, and global diplomacy", "Studying legal theory, constitutional history, and academic jurisprudence"] },
    { id: 2, title: "Where is your ideal work environment?", options: ["A sleek, high-end corporate law firm in a major city", "A busy courtroom, the prosecutor's office, or a public defender's desk", "A government office, think tank, or the halls of Congress/Parliament", "An embassy, the United Nations, or an international NGO", "A quiet university office or an advanced legal research institute"] },
    { id: 3, title: "If you were handed a complex case, what is your first instinct?", options: ["Look for loopholes in the contract to protect my corporate client's money", "Analyze the evidence to build a compelling narrative for the jury", "Consider how this case might change future public policy and laws", "Analyze how this impacts international trade or foreign relations", "Research historical Supreme Court precedents and write a theoretical paper"] },
    { id: 4, title: "How do you prefer to interact with people?", options: ["Advising CEOs and executives in private boardrooms", "Cross-examining witnesses and persuading a jury", "Debating with politicians, lobbyists, and civic leaders", "Diplomatically negotiating with foreign officials from different cultures", "Lecturing law students and debating with fellow academics"] },
    { id: 5, title: "What type of reading do you enjoy most?", options: ["Lengthy corporate contracts, compliance codes, and financial documents", "Police reports, witness testimonies, and case files", "Draft legislation, policy briefs, and civic demographic data", "International treaties, foreign news, and geopolitical history", "Dense, peer-reviewed legal journals and constitutional theory"] },
    { id: 6, title: "How do you handle conflict?", options: ["I negotiate settlements behind closed doors to avoid public trials", "I thrive on direct, aggressive debate and courtroom confrontation", "I try to find a legislative compromise that benefits the most people", "I use tact, cultural understanding, and diplomacy to de-escalate", "I analyze the conflict objectively through established legal frameworks"] },
    { id: 7, title: "What is your primary strength?", options: ["Attention to detail, contract drafting, and business acumen", "Public speaking, quick thinking, and persuasive argumentation", "Strategic planning, understanding government, and drafting policy", "Cultural adaptability, language skills, and global awareness", "Rigorous academic discipline, deep reading, and theoretical analysis"] },
    { id: 8, title: "What sounds like the most frustrating part of a job?", options: ["A deal falling through because of a tiny regulatory compliance issue", "Losing a trial when you know the jury made the wrong decision", "A brilliant policy failing to pass because of partisan political gridlock", "A diplomatic mission failing due to cultural misunderstandings", "Being forced to do routine paperwork instead of deep legal research"] },
    { id: 9, title: "Which of these tools do you gravitate towards?", options: ["Corporate databases, tax codes, and merger agreements", "The penal code, evidence boards, and trial transcripts", "Public polling data, legislative drafts, and policy memos", "Passports, international law texts, and translation tools", "University databases, academic citations, and legal archives"] },
    { id: 10, title: "How do you feel about public speaking?", options: ["I prefer speaking in small, private corporate board meetings", "I absolutely love it—I want to command a courtroom", "I enjoy giving speeches to the public or debating policy on a panel", "I am careful and measured; every word in diplomacy matters", "I prefer presenting formal academic lectures to students or peers"] },
    { id: 11, title: "Who do you want to spend most of your time talking to?", options: ["Corporate clients, business partners, and financial regulators", "Judges, juries, police officers, and defendants", "Senators, mayors, policy analysts, and advocacy groups", "Ambassadors, foreign dignitaries, and global NGO leaders", "Fellow Ph.D. candidates, researchers, and law professors"] },
    { id: 12, title: "What kind of news do you read first?", options: ["Corporate acquisitions, antitrust lawsuits, and financial regulations", "High-profile criminal trials and true crime stories", "Elections, domestic policy changes, and civic issues", "Global conflicts, international trade, and foreign affairs", "Supreme Court rulings and academic legal critiques"] },
    { id: 13, title: "If you had a free weekend, what would you do?", options: ["Read about a famous corporate hostile takeover", "Watch a courtroom drama or true crime documentary", "Volunteer for a political campaign or local civic group", "Learn a new language or read about a foreign culture", "Attend a lecture or dive into an academic legal paper"] },
    { id: 14, title: "How do you approach a complex societal problem (like climate change)?", options: ["I look at how environmental regulations affect corporate compliance", "I want to prosecute companies that illegally pollute", "I want to draft new federal policies to subsidize green energy", "I want to negotiate international climate treaties like the Paris Agreement", "I want to research the legal constitutionality of environmental mandates"] },
    { id: 15, title: "Where do you see yourself in 10 years?", options: ["A Partner at a top Corporate Law Firm or In-House Counsel for a Fortune 500", "A Lead Prosecutor or highly successful Criminal Defense Attorney", "A Senior Policy Advisor, Senator, or Think Tank Director", "An Ambassador, Diplomat, or International Human Rights Lawyer", "A Tenured Law Professor or Legal Scholar"] },
    { id: 16, title: "What is your stance on the justice system?", options: ["It provides the necessary framework for secure business and trade", "It is an adversarial arena where the best argument wins", "It is a system of policies that must constantly be updated and reformed", "It must be aligned with international human rights standards", "It is a theoretical construct that requires deep academic critique"] },
    { id: 17, title: "If you had to present your work, what would you show?", options: ["A flawlessly executed 500-page corporate merger agreement", "A 'Not Guilty' verdict won through a brilliant closing argument", "A new piece of legislation that successfully passed into law", "A successfully negotiated international peace or trade treaty", "A defended LL.M/Ph.D. dissertation published in the Yale Law Journal"] },
    { id: 18, title: "What is your biggest motivation?", options: ["Generating extreme wealth and protecting corporate assets", "Fighting for justice, freedom, and courtroom victories", "Shaping the future of society through smart government policy", "Solving global crises and bridging cultural divides", "Advancing theoretical knowledge in jurisprudence and legal history"] },
    { id: 19, title: "When a major scandal breaks out in the news, what do you think about?", options: ["How this will affect the company's stock and legal liability", "Who is going to jail and how the trial will play out", "What new laws need to be written to prevent this from happening again", "How this impacts the country's reputation on the global stage", "The underlying constitutional law principles involved in the scandal"] },
    { id: 20, title: "What are your immediate goals regarding higher education?", options: ["Go to Law School (JD), pass the bar, and join a corporate firm", "Go to Law School (JD), pass the bar, and get into the courtroom", "Get a Master's in Public Policy (MPP) or Public Administration (MPA)", "Get a Master's in International Relations or Global Affairs", "Pursue an LL.M (Master of Laws) and eventually a Ph.D. or S.J.D for academia"] }
  ];

  const collegeCreativeQuestions = [
    { id: 1, title: "Which creative process excites you the most?", options: ["Designing the layout and structure of a physical building or interior", "Painting, drawing, or creating stunning 2D/3D visual art", "Bringing characters and worlds to life through animation and game engines", "Designing sleek, ergonomic, and functional physical products", "Studying the history of art, critical theory, and academic design philosophies"] },
    { id: 2, title: "Where is your ideal work environment?", options: ["An architectural firm with drafting tables and 3D models", "A quiet, messy art studio surrounded by canvases and paints", "A dark, high-tech studio with dual monitors running Unity or Maya", "A modern industrial design workshop with 3D printers and CNC machines", "A quiet university office, archive, or museum curation backroom"] },
    { id: 3, title: "If you were handed a blank canvas or empty space, what is your first instinct?", options: ["Think about spatial flow, lighting, and structural integrity", "Focus purely on color, emotion, and aesthetic expression", "Imagine how a character would move and interact within that space", "Think about how a human hand would hold or use an object in that space", "Analyze the cultural and historical significance of the space itself"] },
    { id: 4, title: "How do you prefer to interact with people?", options: ["Presenting blueprints to clients and coordinating with construction teams", "Showcasing my work in a gallery and letting the art speak for itself", "Collaborating with programmers and sound designers on a massive digital project", "Watching users test my physical prototype to see if it's comfortable", "Lecturing students or discussing art theory with fellow academics"] },
    { id: 5, title: "What type of tools do you enjoy most?", options: ["AutoCAD, Revit, SketchUp, and architectural scale models", "Brushes, charcoal, Wacom tablets, and Photoshop", "Blender, Unreal Engine, ZBrush, and rigging software", "SolidWorks, clay modeling, 3D printing, and injection molding", "Dense, peer-reviewed art history journals and critical theory texts"] },
    { id: 6, title: "How do you handle constraints (like a tight budget or strict physics)?", options: ["I love it—architecture requires balancing creativity with strict physics", "I hate constraints; I want total freedom for pure artistic expression", "I optimize my digital polygons and frame rates to make the game run smoothly", "I love finding the cheapest, most durable materials for mass production", "I analyze how historical artists navigated the constraints of their eras"] },
    { id: 7, title: "What is your primary strength?", options: ["Spatial awareness, structural math, and large-scale vision", "Mastery of color, composition, and evoking human emotion", "Understanding digital timing, weight, physics, and storytelling", "Understanding ergonomics, material science, and user comfort", "Rigorous academic discipline, deep reading, and theoretical analysis"] },
    { id: 8, title: "What sounds like the most frustrating part of a job?", options: ["A city zoning board rejecting my building design", "A client asking me to change the colors of my painting to match their couch", "A game engine crashing and losing hours of rendering progress", "A factory manufacturing my product with cheap, breakable plastic", "Being forced to do commercial commercial design instead of deep research"] },
    { id: 9, title: "Which of these projects sounds the most fun?", options: ["Designing a sustainable, eco-friendly modern home", "Illustrating a beautiful graphic novel or painting a mural", "Animating a high-action combat sequence for a video game", "Designing the sleek outer shell of a new electric car or smartphone", "Writing a comprehensive book on the evolution of Renaissance art"] },
    { id: 10, title: "How do you feel about functionality vs. aesthetics?", options: ["A building must be safe and functional first, beautiful second", "Aesthetics are everything. Art doesn't need to 'do' anything but exist", "It needs to look great, but also run at 60 frames per second", "Functionality is critical; if the product is uncomfortable, it's garbage", "I prefer to debate the philosophical definitions of both in academia"] },
    { id: 11, title: "Who do you want to spend most of your time talking to?", options: ["Civil engineers, city planners, and interior designers", "Fellow painters, gallery owners, and art collectors", "Game directors, level designers, and VFX artists", "Manufacturing engineers, material scientists, and consumers", "Fellow Ph.D. candidates, researchers, and art history professors"] },
    { id: 12, title: "What kind of media do you consume first?", options: ["Architectural Digest or videos of incredible home tours", "Art station portfolios, gallery exhibitions, and illustration blogs", "Behind-the-scenes documentaries on Pixar or Naughty Dog games", "Industrial design blogs, tech tear-downs, and product reviews", "Academic journals on aesthetics and historical art movements"] },
    { id: 13, title: "If you had a free weekend, what would you do?", options: ["Wander around a city admiring the skyscrapers and urban flow", "Go to a park and sketch or paint the scenery", "Play a visually stunning video game or watch an animated film", "Take apart a household appliance to see how it was manufactured", "Attend a lecture or dive into an academic paper on art theory"] },
    { id: 14, title: "How do you approach a complex design problem?", options: ["I look at the site map, building codes, and structural limits", "I experiment with different color palettes and abstract shapes", "I storyboard the frames and map out the animation timeline", "I mold a quick physical prototype out of clay or cardboard", "I read peer-reviewed literature to see how it was solved historically"] },
    { id: 15, title: "Where do you see yourself in 10 years?", options: ["A Lead Architect designing iconic city skylines", "A successful Fine Artist exhibited in major global galleries", "A Lead Animator or Art Director at a AAA game studio", "A Senior Industrial Designer at a company like Apple or Tesla", "A Tenured Art History Professor or Museum Chief Curator"] },
    { id: 16, title: "What is your stance on technology in art?", options: ["I use it to render buildings, but the physical structure is what matters", "I prefer traditional mediums (paint, clay) over digital screens", "Technology IS my medium—I live and breathe 3D software", "I use CAD to design, but the final result is a tangible physical object", "I study the theoretical impact of technology on modern art movements"] },
    { id: 17, title: "If you had to present your work, what would you show?", options: ["A massive, highly detailed scale model of a new library", "A completed gallery exhibition of my original paintings", "A fully playable demo of a beautifully animated video game", "A perfectly functioning, ergonomic prototype of a new chair", "A defended MFA/Ph.D. dissertation published in a major journal"] },
    { id: 18, title: "What is your biggest motivation?", options: ["Creating physical spaces that define human cities", "Expressing my inner soul and making people feel deep emotion", "Building immersive, interactive digital worlds", "Creating beautiful, useful objects that make daily life better", "Advancing theoretical knowledge in art history and design theory"] },
    { id: 19, title: "When you look at a sleek new chair, what do you think about?", options: ["How it fits into the broader spatial design of the room", "The color theory and visual emotional impact of the chair", "I don't care much, unless I need to 3D model it for a game", "The ergonomics, the materials used, and how it was manufactured", "The historical Bauhaus or Mid-Century design movements it borrows from"] },
    { id: 20, title: "What are your immediate goals regarding higher education?", options: ["Get my B.Arch/M.Arch and pass my architectural licensing exams", "Build my portfolio and start selling or exhibiting my art immediately", "Get a specialized degree in Animation or Game Design and enter the industry", "Get a degree in Industrial Design and start building prototypes", "Pursue a Master's and eventually a Ph.D. or MFA for academia/curation"] }
  ];

  let currentQuestions = pcbQuestions;
  if (selectedStream === 'Science (PCM)') currentQuestions = pcmQuestions;
  if (selectedStream === 'Commerce') currentQuestions = commerceQuestions;
  if (selectedStream === 'Arts / Humanities') currentQuestions = artsQuestions;
  if (selectedStream === 'College - Medicine & Life Sciences') currentQuestions = collegeMedQuestions;
  if (selectedStream === 'College - Computer Science & IT') currentQuestions = collegeTechQuestions;
  if (selectedStream === 'College - Core Engineering & Physical Sciences') currentQuestions = collegeEngineeringQuestions;
  if (selectedStream === 'College - Business, Finance & Commerce') currentQuestions = collegeBusinessQuestions;
  if (selectedStream === 'College - Arts, Humanities & Social Sciences') currentQuestions = collegeArtsQuestions;
  if (selectedStream === 'College - Law, Policy & International Relations') currentQuestions = collegeLawQuestions;
  if (selectedStream === 'College - Creative Arts, Architecture & Design') currentQuestions = collegeCreativeQuestions;

  const handleSelectOption = (qId: number, val: string) => {
    setValidationError('');
    setAnswers(prev => {
      if (qId === 16 && selectedLevel === 'High School') {
        const currentSelections = prev[qId] ? String(prev[qId]).split(', ') : [];
        let newSelections;
        if (currentSelections.includes(val)) {
          newSelections = currentSelections.filter(item => item !== val);
        } else if (currentSelections.length < 3) {
          newSelections = [...currentSelections, val];
        } else {
          return prev;
        }
        return { ...prev, [qId]: newSelections.join(', ') };
      } else {
        return { ...prev, [qId]: val };
      }
    });
  };

  const handleNextStep = async () => {
    // Validate current 4 questions are answered before proceeding
    const startIndex = (currentStep - 1) * 4;
    const currentBatch = currentQuestions.slice(startIndex, startIndex + 4);
    const unselected = currentBatch.some(q => !answers[q.id]);

    if (unselected) {
      setValidationError('Please answer all visible questions before proceeding.');
      return;
    }

    if (currentStep < 5) {
      setCurrentStep(prev => prev + 1);
    } else {
      setIsSubmitting(true);
      try {
        const answersAsNumbers = Object.keys(answers).reduce((acc, key) => {
          acc[parseInt(key)] = answers[key];
          return acc;
        }, {} as Record<number, string>);

        const response = await fetch('https://clarityos-backend.onrender.com/analyze-quiz', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            stream: selectedStream,
            answers: answersAsNumbers
          }),
        });
        const data = await response.json();
        sessionStorage.setItem('clarity_backend_results', JSON.stringify(data));
        sessionStorage.setItem('clarity_quiz_stream', selectedStream);
        window.location.href = '/dashboard';
      } catch (error) {
        console.error("Backend error:", error);
        window.location.href = '/dashboard';
      }
    }
  };

  const getStepTitle = (step: number) => {
    switch(step) {
      case 1: return "Step 1/5 — Your Interests";
      case 2: return "Step 2/5 — Your Strengths";
      case 3: return "Step 3/5 — Your Work Style";
      case 4: return "Step 4/5 — Your Priorities";
      case 5: return "Step 5/5 — Your Future & Passions";
      default: return "";
    }
  };

  const getPercentage = (step: number) => `${step * 20}%`;

  if (isSubmitting) {
    return (
      <main className="min-h-screen w-full bg-[#EFE6D5] flex flex-col items-center justify-center text-[#0a1118]">
        <div className="text-center space-y-6">
          <div className="w-12 h-12 border-2 border-[#C2A878] border-t-transparent rounded-full animate-spin mx-auto"></div>
          <p className="font-serif text-2xl tracking-widest uppercase">Compiling Your Cognitive Matrix...</p>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen w-full relative bg-[#EFE6D5] text-[#0a1118] selection:bg-[#B89B72] selection:text-white flex flex-col font-sans">
      <nav className="relative z-50 w-full max-w-[1400px] mx-auto px-8 md:px-16 flex justify-between items-center py-8">
        <a href="/" className="font-serif text-2xl tracking-[0.15em] text-[#0a1118] uppercase font-bold">
          Clarity<span className="italic text-[#C2A878] font-light">OS</span>
        </a>
      </nav>

      <div className="relative z-10 flex-1 flex items-center justify-center px-6 py-12">
        <div className="w-full max-w-4xl bg-white border border-[#E8E2D2] shadow-2xl p-8 md:p-14 relative rounded-sm">
          
          {/* Phase 00: Select Level */}
          {stage === 'level' && (
            <div className="space-y-8 animate-fadeIn">
              <div>
                <span className="text-[#C2A878] text-[10px] tracking-[0.3em] uppercase font-bold">Phase 00</span>
                <h2 className="font-serif text-3xl text-[#0a1118] mt-2 tracking-wide">Where are you in your journey?</h2>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
                <button 
                  onClick={() => { setSelectedLevel('High School'); setStage('identity'); }}
                  className="p-8 border-2 border-[#E8E2D2] hover:border-[#C2A878] bg-[#FBF8F1] text-center transition-all cursor-pointer font-serif text-xl"
                >
                  High School (11th/12th)
                </button>
                <button 
                  onClick={() => { setSelectedLevel('College'); setStage('identity'); }}
                  className="p-8 border-2 border-[#E8E2D2] hover:border-[#C2A878] bg-[#FBF8F1] text-center transition-all cursor-pointer font-serif text-xl"
                >
                  Current College Student
                </button>
              </div>
            </div>
          )}

          {/* Phase 01: Select Stream/Track */}
          {stage === 'identity' && (
            <div className="space-y-8 animate-fadeIn">
              <div>
                <span className="text-[#C2A878] text-[10px] tracking-[0.3em] uppercase font-bold">Phase 01</span>
                <h2 className="font-serif text-3xl text-[#0a1118] mt-2 tracking-wide">
                  {selectedLevel === 'High School' ? 'Select Your 12th Stream' : 'Select Your University Track'}
                </h2>
              </div>
              
              {selectedLevel === 'High School' && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
                  {['Science (PCM)', 'Science (PCB)', 'Commerce', 'Arts / Humanities'].map((stream, idx) => (
                    <button 
                      key={idx}
                      onClick={() => { setSelectedStream(stream); setStage('quiz'); }}
                      className="p-6 border-2 border-[#E8E2D2] hover:border-[#C2A878] bg-[#FBF8F1] text-left transition-all cursor-pointer font-serif text-lg"
                    >
                      {stream}
                    </button>
                  ))}
                </div>
              )}

              {selectedLevel === 'College' && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
                  {[
                    'College - Computer Science & IT', 
                    'College - Core Engineering & Physical Sciences',
                    'College - Medicine & Life Sciences', 
                    'College - Business, Finance & Commerce',
                    'College - Arts, Humanities & Social Sciences',
                    'College - Law, Policy & International Relations',
                    'College - Creative Arts, Architecture & Design'
                  ].map((stream, idx) => (
                    <button 
                      key={idx}
                      onClick={() => { setSelectedStream(stream); setStage('quiz'); }}
                      className="p-6 border-2 border-[#E8E2D2] hover:border-[#C2A878] bg-[#FBF8F1] text-left transition-all cursor-pointer font-serif text-base"
                    >
                      {stream.replace('College - ', '')}
                    </button>
                  ))}
                </div>
              )}

              <div className="pt-4">
                <button onClick={() => setStage('level')} className="text-xs uppercase font-bold cursor-pointer text-gray-500 hover:text-[#0a1118]">← Back</button>
              </div>
            </div>
          )}

          {/* Phase 02: Quiz */}
          {stage === 'quiz' && (
            <div className="space-y-8 animate-fadeIn">
              <div>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-[#C2A878] text-[10px] tracking-[0.3em] uppercase font-bold">{getStepTitle(currentStep)}</span>
                  <span className="text-xs font-mono text-gray-500">{getPercentage(currentStep)}</span>
                </div>
                <div className="w-full h-1.5 bg-[#E8E2D2] overflow-hidden">
                  <div className="h-full bg-[#C2A878] transition-all duration-500" style={{ width: getPercentage(currentStep) }}></div>
                </div>
              </div>

              {validationError && (
                <div className="p-3 bg-red-50 border border-red-200 text-red-700 text-xs rounded">
                  {validationError}
                </div>
              )}

              <div className="space-y-10">
                {currentQuestions.slice((currentStep - 1) * 4, currentStep * 4).map((q) => {
                  const selectedVal = answers[q.id] || '';
                  const isMultiSelect = q.id === 16 && selectedLevel === 'High School';
                  return (
                    <div key={q.id} className="space-y-4">
                      <h3 className="font-serif text-lg text-[#0a1118] leading-snug">
                        {q.id}. {q.title} {isMultiSelect && <span className="text-[10px] text-[#C2A878]">(Pick up to 3)</span>}
                      </h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-2.5">
                        {q.options.map((opt, i) => {
                          const isSelected = isMultiSelect ? selectedVal.includes(opt) : selectedVal === opt;
                          return (
                            <button
                              key={i}
                              onClick={() => handleSelectOption(q.id, opt)}
                              className={`p-3 text-left text-xs transition-all border cursor-pointer font-sans ${isSelected ? 'bg-[#0a1118] text-white font-bold shadow-md' : 'bg-[#FBF8F1] text-gray-800 border-[#E8E2D2] hover:border-[#C2A878]'}`}
                            >
                              {opt}
                            </button>
                          );
                        })}
                      </div>
                    </div>
                  );
                })}
              </div>

              <div className="flex justify-between pt-6 border-t border-[#E8E2D2]">
                <button onClick={() => { if (currentStep > 1) setCurrentStep(prev => prev - 1); else setStage('identity'); }} className="text-xs uppercase font-bold cursor-pointer hover:text-[#C2A878]">← Back</button>
                <button onClick={handleNextStep} className="bg-[#C2A878] text-white px-8 py-4 text-[10px] uppercase font-bold tracking-widest hover:bg-[#0a1118] shadow-xl cursor-pointer transition-all">
                  {currentStep === 5 ? 'Analyze Profile ⚡' : 'Next Step →'}
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}