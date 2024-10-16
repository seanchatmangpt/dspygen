from openai import OpenAI
from pydantic import BaseModel
from typing import List, Optional
import openai
import pyperclip


# Define Pydantic models for LinkedIn profile
class Experience(BaseModel):
    title: str
    company: str
    duration: str
    location: Optional[str]


class LinkedInProfile(BaseModel):
    name: str
    headline: str
    location: str
    contact_info: str
    followers: int
    connections: int
    experiences: List[Experience]


# Function to extract and parse LinkedIn data
def parse_linkedin_profile(linkedin_text: str) -> Optional[LinkedInProfile]:
    openai.api_key = "your-openai-api-key"

    try:
        # Call the OpenAI API with structured output
        client = OpenAI()

        completion = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a LinkedIn profile parser."},
                {"role": "user", "content": linkedin_text}
            ],
            response_format=LinkedInProfile
        )

        linkedin_profile = completion.choices[0].message.parsed
        return linkedin_profile

    except Exception as e:
        print("Error:", e)
        return None



# Retrieve LinkedIn profile text from the clipboard
linkedin_text = pyperclip.paste()

linkedin_text = """
🤖 Sean Chatman 🤖
Me

For Business
Advertise
Background Image

🤖 Sean Chatman 🤖, #OPEN_TO_WORK

🤖 Sean Chatman 🤖 
 (He/Him)
Available for Distinguished Front End Generative AI Web Development
Los Angeles, California, United States  Contact info
linkedin.com/seanchatman
21,519 followers 
500+ connections
Open to
Add profile section

Enhance profile

More
Open to work
Staff Software Engineer, Senior Staff Engineer, Principal Software Engineer, Distinguished Software Engineer and Frontend Developer roles

Show details

Edit
Share that you’re hiring and attract qualified candidates.

Get started


AnalyticsAnalytics
 Private to you Private to you

471 profile views471 profile views
Discover who's viewed your profile.Discover who's viewed your profile.
2,933 post impressions2,933 post impressions
Check out who's engaging with your posts.Check out who's engaging with your posts.
Past 7 daysPast 7 days
268 search appearances268 search appearances
See how often you appear in search results.See how often you appear in search results.
Show all analytics
ResourcesResources
 Private to you Private to you

My networkMy network
See and manage your connections and interests.See and manage your connections and interests.
Saved itemsSaved items
Keep track of your jobs, courses, and articles.Keep track of your jobs, courses, and articles.
Show all 4 resources
AboutAbout
With over 24 years of experience in software engineering, I have cultivated a deep expertise in front-end web development, generative AI, and full-stack solutions. My professional journey has been marked by continuous learning, innovation, and a commitment to excellence.

Recent Experience:

As a consultant and contractor doing Distinguished Front End Generative AI Web Development, I focus on harnessing the power of generative AI to revolutionize front-end web development. My role involves creating dynamic and responsive prototypes, showcasing the immense potential of AI-driven technologies. I design and implement AI tools that automated the development process, enhancing user experience and delivering sophisticated interfaces. My work is not just about coding; it is about understanding stakeholder needs, solving complex problems, and staying ahead of the latest technological trends.

Previous Roles:

At Intuit, as a Staff Software Engineer in Artificial Intelligence, Analytics, and Data, I played a key role in integrating AI and analytics into business applications, driving innovation and efficiency. My contributions ranged from architectural design to full-stack development, using technologies like React, Node.js, MongoDB, and OpenAI's GPT models.

My journey also includes significant roles at companies like Method Studios, AT&T, Playsino, Riot Games, and Neopets, where I developed and led projects that spanned from web development and software architecture to full-stack engineering and DevOps. Each role allowed me to refine my skills and contribute to cutting-edge projects, mentoring teams, and driving technological advancements.

Skills and Expertise:

- Front-End Development: Proficient in HTML5, CSS, JavaScript, React, Angular, and Vue.

- Generative AI: Expertise in using OpenAI’s GPT models to enhance web development and create intelligent applications.

- Full-Stack Development: Experienced with Node.js, MongoDB, MySQL, Docker, and Kubernetes.

- Prototyping and UX: Skilled in creating dynamic, responsive prototypes and ensuring optimal user experience.

- Collaboration and Problem-Solving: Strong track record of working with cross-functional teams to deliver tailored solutions that meet strategic objectives.

My professional ethos is rooted in the belief that technology should empower and transform. I am passionate about exploring new frontiers in AI and web development, and I look forward to leveraging my skills and experience in a full-time role where I can continue to make a meaningful impact.With over 24 years of experience in software engineering, I have cultivated a deep expertise in front-end web development, generative AI, and full-stack solutions. My professional journey has been marked by continuous learning, innovation, and a commitment to excellence. Recent Experience: As a consultant and contractor doing Distinguished Front End Generative AI Web Development, I focus on harnessing the power of generative AI to revolutionize front-end web development. My role involves creating dynamic and responsive prototypes, showcasing the immense potential of AI-driven technologies. I design and implement AI tools that automated the development process, enhancing user experience and delivering sophisticated interfaces. My work is not just about coding; it is about understanding stakeholder needs, solving complex problems, and staying ahead of the latest technological trends. Previous Roles: At Intuit, as a Staff Software Engineer in Artificial Intelligence, Analytics, and Data, I played a key role in integrating AI and analytics into business applications, driving innovation and efficiency. My contributions ranged from architectural design to full-stack development, using technologies like React, Node.js, MongoDB, and OpenAI's GPT models. My journey also includes significant roles at companies like Method Studios, AT&T, Playsino, Riot Games, and Neopets, where I developed and led projects that spanned from web development and software architecture to full-stack engineering and DevOps. Each role allowed me to refine my skills and contribute to cutting-edge projects, mentoring teams, and driving technological advancements. Skills and Expertise: - Front-End Development: Proficient in HTML5, CSS, JavaScript, React, Angular, and Vue. - Generative AI: Expertise in using OpenAI’s GPT models to enhance web development and create intelligent applications. - Full-Stack Development: Experienced with Node.js, MongoDB, MySQL, Docker, and Kubernetes. - Prototyping and UX: Skilled in creating dynamic, responsive prototypes and ensuring optimal user experience. - Collaboration and Problem-Solving: Strong track record of working with cross-functional teams to deliver tailored solutions that meet strategic objectives. My professional ethos is rooted in the belief that technology should empower and transform. I am passionate about exploring new frontiers in AI and web development, and I look forward to leveraging my skills and experience in a full-time role where I can continue to make a meaningful impact.
Top skillsTop skills
Artificial Intelligence (AI) • TypeScript • Python (Programming Language) • Generative AI • Revenue & Profit GrowthArtificial Intelligence (AI) • TypeScript • Python (Programming Language) • Generative AI • Revenue & Profit Growth
ServicesServices
Web Development • Application Development • Custom Software Development • SaaS DevelopmentWeb Development • Application Development • Custom Software Development • SaaS Development
Show all
FeaturedFeatured

NewsletterNewsletter
Image for ChatGPT For Jobs & Work
Image for ChatGPT For Jobs & Work
ChatGPT For Jobs & WorkChatGPT For Jobs & Work
Published daily · 4,668 subscribersPublished daily · 4,668 subscribers

Learn how to best utilize ChatGPT in the modern job hunt and workspaceLearn how to best utilize ChatGPT in the modern job hunt and workspace

Subscribed
PostPost

🎨 Picasso: AI Interview
🤖 Sean Chatman 🤖 on LinkedIn • 5 min read
likesupportcelebrate
21
3 comments
ActivityActivity
21,519 followers21,519 followers

Create a post

Posts

Newsletter

Comments

Images
Loaded 3 Newsletter posts

ChatGPT For Jobs & Work
Published daily
•
4,668 subscribers
Learn how to best utilize ChatGPT in the modern job hunt and workspace


Subscribed

Innovations in the ResMkr System Using the PLAN Pro Stack
The ResMkr system is a cutting-edge platform designed to automate the process of customizing resumes based on job descriptions. Leveraging the PLAN PrThe ResMkr system is a cutting-edge platform designed to automate the process of customizing resumes based on job descriptions. Leveraging the PLAN Pr
5 min read


How the PLAN Pro Stack Enables New Revenue Streams Through Automation and Innovation
What Is a Revenue Stream? A revenue stream is a source of income that a company generates from selling goods, providing services, or other business acWhat Is a Revenue Stream? A revenue stream is a source of income that a company generates from selling goods, providing services, or other business ac
5 min read

Show all editions
ExperienceExperience

Distinguished Front End Generative AI Web Development ContractorDistinguished Front End Generative AI Web Development Contractor
Consulting · ContractConsulting · Contract
May 2023 - Aug 2024 · 1 yr 4 mosMay 2023 to Aug 2024 · 1 yr 4 mos
Los Angeles County, California, United States · RemoteLos Angeles County, California, United States · Remote
I focus on developing innovative solutions leveraging generative AI for front-end web development. My work has involved creating dynamic and responsive prototypes to showcase the potential of AI-driven front-end technologies.

Key Achievements:

- AI-Powered Front-End Prototyping: Designed and implemented AI-driven tools that automated the creation of dynamic and responsive web prototypes.

- Advanced Front-End Development: Utilized cutting-edge web frameworks and technologies, including React, Vue, HTML5, CSS, Typescript, and JavaScript, to develop sophisticated user interfaces.

- Integration of Generative AI: Applied OpenAI's GPT-3.5 and GPT-4 to enhance user experience and streamline development processes through intelligent automation.

- Collaborative Problem Solving: Worked closely with stakeholders to understand their needs and deliver tailored prototype solutions that aligned with their strategic objectives.

- Continuous Learning and Adaptation: Stayed up-to-date with the latest trends and technologies in AI and front-end development to ensure the delivery of state-of-the-art solutions.I focus on developing innovative solutions leveraging generative AI for front-end web development. My work has involved creating dynamic and responsive prototypes to showcase the potential of AI-driven front-end technologies. Key Achievements: - AI-Powered Front-End Prototyping: Designed and implemented AI-driven tools that automated the creation of dynamic and responsive web prototypes. - Advanced Front-End Development: Utilized cutting-edge web frameworks and technologies, including React, Vue, HTML5, CSS, Typescript, and JavaScript, to develop sophisticated user interfaces. - Integration of Generative AI: Applied OpenAI's GPT-3.5 and GPT-4 to enhance user experience and streamline development processes through intelligent automation. - Collaborative Problem Solving: Worked closely with stakeholders to understand their needs and deliver tailored prototype solutions that aligned with their strategic objectives. - Continuous Learning and Adaptation: Stayed up-to-date with the latest trends and technologies in AI and front-end development to ensure the delivery of state-of-the-art solutions.
Intuit logo
IntuitIntuit
2 yrs 5 mos2 yrs 5 mos
Staff Software Engineer - Artificial Intelligence, Analytics, and DataStaff Software Engineer - Artificial Intelligence, Analytics, and Data
Full-timeFull-time
Dec 2021 - Jun 2023 · 1 yr 7 mosDec 2021 to Jun 2023 · 1 yr 7 mos
Los Angeles, California, United States · RemoteLos Angeles, California, United States · Remote
In my role as a Staff Software Engineer at Intuit, I focused on harnessing the power of AI, analytics, and data to innovate and streamline business processes. My contributions were integral to the architectural design and development of advanced business applications, utilizing my expertise in modern web frameworks and full-stack technologies. 

Key responsibilities and achievements include:

Innovation through AI, Analytics, and Data: 
- Spearheaded projects to integrate AI and analytics into business applications, driving efficiency and innovation.

Architectural Design and Development: 
- Played a critical role in the planning and execution of application architectures, ensuring scalability and performance.

Expertise in Cutting-Edge Technologies: 
- Demonstrated proficiency in a range of technologies including React for front-end development, and Node.js, MongoDB, MySQL for backend infrastructure. OpenAI API GPT-3.5 and GPT-4 for generative AI features.

Mentorship and Collaboration: 
- Actively engaged in mentoring team members, sharing expertise in both technical and soft skills to promote team growth and cohesion.

Software Solution Excellence: 
- Contributed significantly to the development of robust, scalable, and innovative software solutions that met and exceeded project goals.

My tenure at Intuit not only allowed me to contribute to the technological advancement of the company but also enabled me to foster a culture of learning and collaboration. I am proud to have played a part in driving Intuit's mission forward through my dedication to technological innovation and team development.In my role as a Staff Software Engineer at Intuit, I focused on harnessing the power of AI, analytics, and data to innovate and streamline business processes. My contributions were integral to the architectural design and development of advanced business applications, utilizing my expertise in modern web frameworks and full-stack technologies. Key responsibilities and achievements include: Innovation through AI, Analytics, and Data: - Spearheaded projects to integrate AI and analytics into business applications, driving efficiency and innovation. Architectural Design and Development: - Played a critical role in the planning and execution of application architectures, ensuring scalability and performance. Expertise in Cutting-Edge Technologies: - Demonstrated proficiency in a range of technologies including React for front-end development, and Node.js, MongoDB, MySQL for backend infrastructure. OpenAI API GPT-3.5 and GPT-4 for generative AI features. Mentorship and Collaboration: - Actively engaged in mentoring team members, sharing expertise in both technical and soft skills to promote team growth and cohesion. Software Solution Excellence: - Contributed significantly to the development of robust, scalable, and innovative software solutions that met and exceeded project goals. My tenure at Intuit not only allowed me to contribute to the technological advancement of the company but also enabled me to foster a culture of learning and collaboration. I am proud to have played a part in driving Intuit's mission forward through my dedication to technological innovation and team development.
Python (Programming Language), Artificial Intelligence (AI) and +3 skills
Full-Stack Software Consultant - Artificial Intelligence, Analytics, and DataFull-Stack Software Consultant - Artificial Intelligence, Analytics, and Data
ContractContract
Feb 2021 - Dec 2021 · 11 mosFeb 2021 to Dec 2021 · 11 mos
Los Angeles Metropolitan AreaLos Angeles Metropolitan Area
In my role as a Full-Stack Software Consultant at Intuit, I concentrated on utilizing my extensive expertise in HTML5, CSS, GraphQL, TypeScript, and JavaScript to develop full-stack solutions. My responsibilities involved working closely with various teams to deliver data-centric and AI-powered applications, optimizing them for performance and user experience. I engaged in hands-on development, ensuring that the client-side interfaces were seamlessly integrated with server-side functionalities. My approach combined technical skill with a deep understanding of business requirements, aligning software solutions with strategic objectives.

Highlights:
 - Developed AI and analytics-driven full-stack solutions.
 - Expertise in HTML5, CSS, GraphQL, TypeScript, and JavaScript.
 - Ensured optimal performance and user experience in application development.
 - Integrated client-side and server-side functionalities effectively.
 - Delivered solutions aligned with business strategies and user needs.In my role as a Full-Stack Software Consultant at Intuit, I concentrated on utilizing my extensive expertise in HTML5, CSS, GraphQL, TypeScript, and JavaScript to develop full-stack solutions. My responsibilities involved working closely with various teams to deliver data-centric and AI-powered applications, optimizing them for performance and user experience. I engaged in hands-on development, ensuring that the client-side interfaces were seamlessly integrated with server-side functionalities. My approach combined technical skill with a deep understanding of business requirements, aligning software solutions with strategic objectives. Highlights: - Developed AI and analytics-driven full-stack solutions. - Expertise in HTML5, CSS, GraphQL, TypeScript, and JavaScript. - Ensured optimal performance and user experience in application development. - Integrated client-side and server-side functionalities effectively. - Delivered solutions aligned with business strategies and user needs.
HTML5, GraphQL and +3 skills
Method Studios logo
Principal Engineer (Web)Principal Engineer (Web)
Method Studios · Full-timeMethod Studios · Full-time
Feb 2018 - Jun 2020 · 2 yrs 5 mosFeb 2018 to Jun 2020 · 2 yrs 5 mos
Greater Los Angeles AreaGreater Los Angeles Area
At Method Studios, as a Principal Engineer focusing on web technologies, I provided extensive expertise in the architectural design and development of sophisticated business applications. I was deeply involved in hands-on development and architectural decisions, utilizing major web frameworks like React, Angular, and Vue to deliver robust and scalable web solutions. My role extended to full-stack infrastructure development, where I demonstrated proficiency with technologies such as Node.js, MongoDB, MySQL, Docker, and Kubernetes. Beyond technical responsibilities, I played a pivotal role in mentoring junior colleagues, sharing knowledge and guiding their professional growth in a dynamic and fast-paced environments. My contributions at Method Studios were characterized by a blend of technical acumen, leadership, and a commitment to fostering a collaborative and learning-driven work culture.

Highlights:
 - Led the architectural design and development of advanced business applications using React, Angular, and Vue.
 - Managed full-stack infrastructure projects involving Node.js, MongoDB, MySQL, Docker, and Kubernetes.
 - Instrumental in introducing and implementing modern web technologies and frameworks.
 - Played a key role in mentoring and guiding junior engineers, enhancing team capabilities and knowledge.
 - Contributed to building scalable and efficient web solutions, aligning with business goals and user needs.At Method Studios, as a Principal Engineer focusing on web technologies, I provided extensive expertise in the architectural design and development of sophisticated business applications. I was deeply involved in hands-on development and architectural decisions, utilizing major web frameworks like React, Angular, and Vue to deliver robust and scalable web solutions. My role extended to full-stack infrastructure development, where I demonstrated proficiency with technologies such as Node.js, MongoDB, MySQL, Docker, and Kubernetes. Beyond technical responsibilities, I played a pivotal role in mentoring junior colleagues, sharing knowledge and guiding their professional growth in a dynamic and fast-paced environments. My contributions at Method Studios were characterized by a blend of technical acumen, leadership, and a commitment to fostering a collaborative and learning-driven work culture. Highlights: - Led the architectural design and development of advanced business applications using React, Angular, and Vue. - Managed full-stack infrastructure projects involving Node.js, MongoDB, MySQL, Docker, and Kubernetes. - Instrumental in introducing and implementing modern web technologies and frameworks. - Played a key role in mentoring and guiding junior engineers, enhancing team capabilities and knowledge. - Contributed to building scalable and efficient web solutions, aligning with business goals and user needs.
Docker, React.js and +3 skills
AT&T logo
Lead Software EngineerLead Software Engineer
AT&TAT&T
Feb 2016 - Nov 2017 · 1 yr 10 mosFeb 2016 to Nov 2017 · 1 yr 10 mos
Greater Los Angeles AreaGreater Los Angeles Area
In my role as Lead Software Engineer at AT&T, I specialized in AngularJS 2, focusing primarily on developing robust client-side applications. My responsibilities included the creation and integration of dspy_modules and components to build highly functional and performance-oriented user interfaces. I worked closely with artistic designers, translating their HTML templates into dynamic and responsive web designs, complete with animations and CSS stylings. Collaborating effectively with back-end development teams, I ensured seamless API integrations and data communication. My approach to development was marked by a commitment to creating intuitive, efficient, and visually appealing user experiences, backed by solid technical execution and team coordination.

Highlights:
 - Spearheaded the development of client-side applications using AngularJS 2, enhancing user experience and application performance.
 - Translated artistic design concepts into responsive web interfaces, incorporating animations and CSS stylings.
 - Led module and component creation, integrating them to form cohesive and functional applications.
 - Facilitated effective collaboration between front-end and back-end teams for seamless API integrations.
 - Focused on delivering high-quality user interfaces with an emphasis on performance and user engagement.In my role as Lead Software Engineer at AT&T, I specialized in AngularJS 2, focusing primarily on developing robust client-side applications. My responsibilities included the creation and integration of dspy_modules and components to build highly functional and performance-oriented user interfaces. I worked closely with artistic designers, translating their HTML templates into dynamic and responsive web designs, complete with animations and CSS stylings. Collaborating effectively with back-end development teams, I ensured seamless API integrations and data communication. My approach to development was marked by a commitment to creating intuitive, efficient, and visually appealing user experiences, backed by solid technical execution and team coordination. Highlights: - Spearheaded the development of client-side applications using AngularJS 2, enhancing user experience and application performance. - Translated artistic design concepts into responsive web interfaces, incorporating animations and CSS stylings. - Led module and component creation, integrating them to form cohesive and functional applications. - Facilitated effective collaboration between front-end and back-end teams for seamless API integrations. - Focused on delivering high-quality user interfaces with an emphasis on performance and user engagement.
Angular2, Engineering Consulting and +1 skill
Playsino logo
Software ArchitectSoftware Architect
PlaysinoPlaysino
Jun 2012 - May 2015 · 3 yrsJun 2012 to May 2015 · 3 yrs
Santa Monica,CASanta Monica,CA
As a Software Architect at Playsino, I was instrumental in the development of 'Bingo Around the World.' My role involved utilizing a diverse technology stack including Jenkins, Java, Intellij, JavaScript, JSON, REST, EC2, Python, XHTML, Facebook's Open Graph, and Linux. I led the Client Engineering team, fostering a collaborative environments and introducing new technologies. My approach to software architecture was marked by a keen focus on the 'why' behind every project, ensuring that each solution was not only technically sound but also purpose-driven and user-centric. My mentorship of junior team members, including interns like Clinton Jake VanSciver, was geared towards nurturing their potential and instilling a similar approach to technology and project execution. This period was marked by significant contributions to the foundational aspects of eSports and a constant engagement with emerging technologies to keep ahead of industry trends.

Highlights:
 - Led the architectural development of 'Bingo Around the World,' a key project at Playsino, leveraging advanced Java and web technologies.
 - Managed the Client Engineering team, introducing and integrating new technologies to enhance project outcomes.
 - Played a mentorship role, providing guidance and technical leadership to junior team members and interns.
 - Maintained a focus on purpose-driven development, ensuring that projects delivered both technical excellence and meaningful user experiences.
 - Actively engaged with new and emerging technologies, contributing to the foundational growth of eSports and maintaining a forward-thinking approach in software architecture.As a Software Architect at Playsino, I was instrumental in the development of 'Bingo Around the World.' My role involved utilizing a diverse technology stack including Jenkins, Java, Intellij, JavaScript, JSON, REST, EC2, Python, XHTML, Facebook's Open Graph, and Linux. I led the Client Engineering team, fostering a collaborative environments and introducing new technologies. My approach to software architecture was marked by a keen focus on the 'why' behind every project, ensuring that each solution was not only technically sound but also purpose-driven and user-centric. My mentorship of junior team members, including interns like Clinton Jake VanSciver, was geared towards nurturing their potential and instilling a similar approach to technology and project execution. This period was marked by significant contributions to the foundational aspects of eSports and a constant engagement with emerging technologies to keep ahead of industry trends. Highlights: - Led the architectural development of 'Bingo Around the World,' a key project at Playsino, leveraging advanced Java and web technologies. - Managed the Client Engineering team, introducing and integrating new technologies to enhance project outcomes. - Played a mentorship role, providing guidance and technical leadership to junior team members and interns. - Maintained a focus on purpose-driven development, ensuring that projects delivered both technical excellence and meaningful user experiences. - Actively engaged with new and emerging technologies, contributing to the foundational growth of eSports and maintaining a forward-thinking approach in software architecture.
Software Architecture, PHP and +1 skill
Show all 19 experiences
EducationEducation
Santa Monica College logo
Santa Monica CollegeSanta Monica College
VolunteeringVolunteering
Santa Monica Chamber of Commerce logo
Executive Volunteer 
Executive Volunteer 
Santa Monica Chamber of CommerceSanta Monica Chamber of Commerce
Jun 2015 - Present · 9 yrs 3 mosJun 2015 - Present · 9 yrs 3 mos
Economic EmpowermentEconomic Empowerment
SkillsSkills
OpenAIOpenAI

Staff Software Engineer - Artificial Intelligence, Analytics, and Data at IntuitStaff Software Engineer - Artificial Intelligence, Analytics, and Data at Intuit
Generative AIGenerative AI

Staff Software Engineer - Artificial Intelligence, Analytics, and Data at IntuitStaff Software Engineer - Artificial Intelligence, Analytics, and Data at Intuit
Show all 47 skills
RecommendationsRecommendations
Show all pending
"""


def main():
    """Main function"""
    from dspygen.utils.dspy_tools import init_ol
    init_ol()

    # Parse the profile
    linkedin_profile = parse_linkedin_profile(linkedin_text)

    # Print the parsed profile
    if linkedin_profile:
        print(linkedin_profile.model_dump_json(indent=2))

        # write to file
        with open("sean_chatman.json", "w") as f:
            f.write(linkedin_profile.model_dump_json(indent=2))

    else:
        print("Failed to parse the LinkedIn profile.")


if __name__ == '__main__':
    main()

"""

"""