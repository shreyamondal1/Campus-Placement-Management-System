from app.database.models import db, User, Company, Student, Education, Experience, Project, Drive, Application, Interview, Placement
from app.utils.helpers import date, get_ist_datetime, hash_password

def seed_data():

    if not User.query.first():

        admin = User(
            username="administrator",
            email="administrator@placementconnect.com",
            password=hash_password("administrator123"),
            role="Admin"
        )
        db.session.add(admin)
        db.session.commit()

        print("Default admin created.")

        companies = [
            ("OpenAI", "Artificial Intelligence", "Product-Based"),
            ("Google", "Technology", "Product-Based"),
            ("Microsoft", "Technology", "Product-Based"),
            ("Amazon", "Technology", "Product-Based"),
            ("Meta", "Digital Advertising", "Product-Based"),
            ("Apple", "Consumer Electronics", "Product-Based"),
            ("Oracle", "Enterprise Software", "Product-Based"),
            ("IBM", "Enterprise Software", "Product-Based"),
            ("Nvidia", "AI Infrastructure", "Product-Based"),
            ("Samsung", "Consumer Electronics", "Product-Based")
        ]

        for name, industry, type in companies:

            username = name.lower().replace(" ", "")

            company_user = User(
                username=username,
                email=f"careers@{username}.com",
                password=hash_password(f"{username}123"),
                role="Company"
            )
            db.session.add(company_user)
            db.session.commit()

            user = User.query.filter(User.username == username).first()

            company_profile = Company(
                user_id=user.id,
                name=name,
                description=f"{name} is a leading organization in the {industry} industry.",
                industry=industry,
                type=type,
                website=f"https://www.{username}.com",
                hr_contact_name=f"HR {name}",
                hr_contact_number=f"{user.id - 2}" * 10
            )
            db.session.add(company_profile)
            db.session.commit()

        print("Company users created.")
        print("Company profiles created.")

        students = [
            ("Priyanka Mukherjee", "BTech", "CSE", 2025, 8.5, "Python, C++, Data Structures and Algorithms, Database Design, Operating Systems", "AWS Certified Cloud Solutions Architect", "ACM-ICPC Regional Finalist, Dean's List"),
            ("Simran Kaur", "MTech", "ECE", 2024, 7.9, "Embedded Systems, VLSI Design, Verilog, Arduino, CMOS Digital Circuits", "Cisco Certfied Network Associate", "IEEE Project Excellence Award, Institute Medal"),
            ("Anjali Deshpande", "BS", "DS", 2025, 8.2, "Python, Pandas, NumPy, SQL, Machine Learning", "Google Data Scientist Professional Certificate", "DS Hackathon Winner, Best ML Research Paper Award"),
            ("Deepika Reddy", "MS", "AI", 2026, 8.0, "Python, TensorFlow, PyTorch, Deep Learning, Natural Language Processing", "Google Cloud Professional Data Engineer", "Best Research Publication Award, AI Challenge Winner"),
            ("Tenzin Yangzom", "BE", "IT", 2026, 7.5, "Java, Spring Boot, React, Git, MySQL", "Oracle Certified Professional Java Programmer", "Inter-College Innovation Award, Tech Fest Grand Prize Winner"),
            ("Sayan Majumdar", "BTech", "CSE", 2023, 7.8, "Python, Django, PostgreSQL, Docker, Linux", "Microsoft Certified Azure Developer Associate", "Intra-College Coding Competition Runner-up"),
            ("Harvinder Singh", "MTech", "ECE", 2023, 7.3, "Digital Electronics, PCB Design, MATLAB, C, VHDL", "Xilinx Certified VLSI Designer", "Department Best Project Recognition"),
            ("Arjun Patel", "BS", "DS", 2023, 7.0, "R, Shiny, Tableau, Power BI, Excel", "Google Data Analyst Certificate", "University Fest Data Visualization Contest Winner"),
            ("Adithya Subramanian", "MS", "AI", 2023, 8.1, "Python, Scipy, Scikit-learn, Tableau, Statsmodels", "IBM Certified Machine Learning Associate", "Departmental Seminar Presentation Certificate"),
            ("Lobsang Sangma", "BE", "IT", 2024, 7.6, "Python, JavaScript, React, NodeJS, MongoDB", "Red Hat Certified System Administrator", "Annual Project Showcase Award")
        ]

        for name, degree, department, graduation_year, cgpa, skills, certifications, achievements in students:

            username = name.lower().replace(" ", "")

            student_user = User(
                username=username,
                email=f"{username}@gmail.com",
                password=hash_password(f"{username}123"),
                role="Student"
            )
            db.session.add(student_user)
            db.session.commit()

            user = User.query.filter(User.username == username).first()

            student_profile = Student(
                user_id=user.id,
                name=name,
                contact_number=f"{user.id - 12}" * 10,
                degree=degree,
                department=department,
                graduation_year=graduation_year,
                cgpa=cgpa,
                skills=skills,
                certifications=certifications,
                achievements=achievements,
                linkedin=f"https://www.linkedin.com/in/{username}",
                github=f"https://www.github.com/{username}",
                portfolio=f"https://{username}.github.io",
                resume=f"https://drive.google.com/file/d/{username}_resume/view"
            )
            db.session.add(student_profile)
            db.session.commit()

        print("Student users created.")
        print("Student profiles created.")
        
        print("Admin, Company users, Student users, Company profiles and Student profiles created.")

        all_students = Student.query.all()

        for student in all_students:
            start_year = student.graduation_year - (4 if "B" in student.degree else 2 if "M" in student.degree else 3)

            education_1 = Education(
                student_id=student.id,
                degree=student.degree,
                institution="Global University",
                start_date=date(start_year, 7, 1),
                end_date=date(student.graduation_year, 6, 30),
                coursework="Data Structures and Algorithms, Operating Systems, Database Management, Networks & Security, Object-Oriented Programming, Software "
                           "Design, Full-Stack Development, Cloud Computing, Artificial Intelligence"
            )
            db.session.add(education_1)

            experience_1 = Experience(
                student_id=student.id,
                role="Software Engineering Intern",
                organization="Capgemini",
                start_date=date(2023, 1, 1),
                end_date=date(2023, 4, 30),
                description="Collaborated within an Agile development environment to design, build, and deploy scalable web applications and system components "
                            "using Java, Python, and JavaScript. Focused on the full software development life cycle (SDLC), from initial requirements gathering "
                            "to final unit testing and version control via Git. Notable projects included developing a high-performance scientific quiz "
                            "application and optimizing core application logic through the implementation of robust Object-Oriented design patterns. Contributed "
                            "to peer code reviews and technical documentation to ensure long-term code maintainability and team alignment on complex features."
            )
            db.session.add(experience_1)

            experience_2 = Experience(
                student_id=student.id,
                role="Data Engineering Intern",
                organization="Cognizant",
                start_date=date(2022, 8, 1),
                end_date=date(2022, 11, 30),
                description="Designed and optimized high-volume data pipelines to ingest, transform, and deliver large-scale datasets for downstream business "
                            "intelligence reporting. Leveraged dbt to build complex data models within Snowflake and BigQuery, significantly enhancing dashboard "
                            "performance and data integrity. Automated critical data cleaning and validation workflows to improve accuracy for enterprise-level "
                            "reporting, while collaborating with data scientists to structure raw data into efficient, queryable models. Implemented rigorous data testing "
                            "protocols to support global data requirements and modernized internal workflows by migrating legacy scripts into scalable, version-controlled ETL processes."
            )
            db.session.add(experience_2)

            project_1 = Project(
                student_id=student.id,
                name="AI-Powered Technical Documentation Assistant",
                link=f"https://www.github.com/{student.user.username}/ai-doc-assistant",
                description="A tool that integrates with a developer's GitHub repository. It automatically reads updated code commits and uses an LLM (like "
                            "GPT-5 or Claude 4) to generate or update the README.md or internal wiki documentation. Built with a Python-based backend, it "
                            "utilizes the GitHub Webhooks API for event-driven automation, LangChain for LLM orchestration, and OpenAI and Claude API for "
                            "intelligent content generation. Key Features include automated pull request scanning, context-aware summarization of code "
                            "changes, and a CLI or dashboard interface for developers to approve the suggested documentation updates."
            )
            db.session.add(project_1)

            project_2 = Project(
                student_id=student.id,
                name="Peer-to-Peer Knowledge Exchange Platform",
                link=f"https://www.github.com/{student.user.username}/p2p-knowledge-exchange",
                description="A full-stack web application that solves the problem of academic isolation by enabling users to swap skills through a "
                            "reciprocal matching algorithm. Built on the PERN stack (PostgreSQL, Express, React, Node.js), the platform allows users to "
                            "catalog their specific 'Strengths' and 'Needs' while providing an intelligent dashboard that identifies and connects "
                            "individuals with complementary skill sets. Key features include a robust relational database for tracking skill-based "
                            "pairings, an interactive dashboard for managing collaboration requests, and secure authentication to foster a reliable community."
            )
            db.session.add(project_2)

            project_3 = Project(
                student_id=student.id,
                name="Smart Inventory Forecast System",
                link=f"https://www.github.com/{student.user.username}/smart-inventory-forecast",
                description="A data-driven predictive engine designed to optimize supply chain efficiency and reduce overhead costs. Built using Python, it "
                            "leverages Scikit-learn for time-series forecasting, and a FastAPI-driven architecture. The system ingests historical sales data "
                            "to project future inventory demands with high accuracy, utilizing ensemble learning methods to account for market volatility. Key "
                            "features include an automated reorder notification system, integration with RESTful inventory APIs to sync live stock levels, and "
                            "a centralized dashboard that visualizes seasonal trends, enabling proactive inventory management and stockout prevention."
            )   
            db.session.add(project_3)

            db.session.commit()

        print("Student educations, experiences, projects created.")

        all_companies = Company.query.all()

        for company in all_companies:

            drive_1 = Drive(
                company_id=company.id,
                job_title="Software Developer",
                job_description="We are seeking a Software Developer to design, build, and maintain high-quality software solutions that solve complex user "
                                "problems. In this role, you will be responsible for the full software development lifecycle, from translating requirements "
                                "into technical specifications to writing clean, scalable code. Your responsibilities will include performing rigorous testing "
                                "and code reviews, as well as deploying production-ready features. You will collaborate closely with cross-functional teams to "
                                "iterate on features, optimize system performance, and ensure our applications deliver a seamless, reliable experience. A key "
                                "focus of this role is ensuring that our codebase remains robust, secure, and ready for rapid iteration as we scale. The ideal "
                                "candidate is a proactive problem-solver who stays current with emerging technologies and is committed to writing maintainable "
                                "code that drives long-term product success.",
                job_location="Bangalore, India",
                job_type="Permanent",
                job_mode="Hybrid",
                salary_package=800000,
                eligibility_criteria="Candidates should possess a Bachelor's degree in Computer Science or a related field, or equivalent practical experience, "
                                     "alongwith expert-level proficiency in at least one modern programming language (e.g., Python, Java, C++). Key technical "
                                     "requirements include a strong foundation in data structures, algorithms, and design patterns, alongside hands-on "
                                     "experience in building scalable, reliable distributed systems, managing version control (Git), integrating RESTful APIs, "
                                     "and working with relational or NoSQL databases. Candidates must be proficient in ensuring code quality through rigorous "
                                     "unit, integration, and end-to-end testing. Preferred qualifications include professional certifications in cloud "
                                     "technologies (AWS, Azure, or GCP) and familiarity with CI/CD pipelines (e.g., GitHub Actions, Docker, Kubernetes). "
                                     "Successful applicants must also demonstrate a proactive, problem-solving mindset, the ability to thrive in cross-functional "
                                     "Agile teams, and a proven commitment to writing clean, maintainable, and scalable code.",
                minimum_cgpa=7.0,
                application_start=get_ist_datetime(-40, 00, 00),
                application_deadline=get_ist_datetime(-10, 23, 59)
            )
            db.session.add(drive_1)

            drive_2 = Drive(
                company_id=company.id,
                job_title="Data Scientist",
                job_description="We are seeking a Data Scientist to transform massive datasets into strategic insights and high-impact predictive models. You "
                                "will be responsible for the end-to-end data pipeline, including sourcing and cleaning complex datasets, feature engineering, "
                                "training robust machine learning models, and orchestrating their deployment into production systems with continuous performance "
                                "monitoring. Your role is to uncover actionable patterns, and translate these complex findings into clear visualizations and "
                                "data-driven narratives for business stakeholders. By balancing deep technical rigor with a keen business sense, you will "
                                "ensure your analytical output directly influences product strategy and operational efficiency. To succeed, you must excel at "
                                "both programming and communication, collaborating across teams to ensure every data-driven decision translates into measurable "
                                "growth, long-term innovation, and solutions to real-world challenges.",
                job_location="Hyderabad, India",
                job_type="Permanent",
                job_mode="Onsite",
                salary_package=1000000,
                eligibility_criteria="Candidates should possess a Bachelor's or Master's degree in a quantitative field (e.g., Computer Science, Statistics, "
                                     "or Mathematics) alongside advanced proficiency in Python, including libraries like Pandas and NumPy. Candidates must be "
                                     "comfortable using SQL for complex data extraction and possess a deep understanding of machine learning frameworks, such as "
                                     "Scikit-learn to build and iterate on high-impact predictive models. Applicants should demonstrate hands-on experience "
                                     "with MLOps practices, containerization (Docker), and cloud platforms (AWS, GCP, or Azure) to facilitate production deployment "
                                     "and continuous performance monitoring. A strong foundation in statistical analysis, and experimental design (A/B testing) "
                                     "is required to ensure model robustness. Successful candidates must demonstrate the ability to bridge the gap between "
                                     "complex algorithms and actionable business strategy through proficiency in data visualization tools like Tableau, PowerBI, "
                                     "or libraries like Plotly and Matplotlib to effectively communicate insights to non-technical stakeholders",
                minimum_cgpa=7.5,
                application_start=get_ist_datetime(-5, 00, 00),
                application_deadline=get_ist_datetime(5, 23, 59)
            )
            db.session.add(drive_2)

            db.session.commit()

        print("Company drives created.")

        for student in all_students:

            for company in all_companies:

                drive = Drive.query.filter(Drive.company_id == company.id).first()

                application = Application(
                    student_id=student.id,
                    drive_id=drive.id
                )
                db.session.add(application)

                db.session.commit()

        print("Student applications created.")

        all_applications = Application.query.order_by(Application.id).all()

        for application in all_applications[:50]:
            application.status = "Shortlisted"

        for application in all_applications[50:75]:
            application.status = "Applied"

        for application in all_applications[75:]:
            application.status = "Rejected"

        db.session.commit()

        shortlisted_applications = all_applications[:50]

        for application in shortlisted_applications[:25]:

            interview = Interview(
                application_id=application.id,
                start_datetime=get_ist_datetime(0, 10, 00),
                end_datetime=get_ist_datetime(0, 11, 00),
                mode="On-Campus",
                status="Selected"
            )
            db.session.add(interview)

        for application in shortlisted_applications[25:38]:

            interview = Interview(
                application_id=application.id,
                start_datetime=get_ist_datetime(5, 10, 00),
                end_datetime=get_ist_datetime(5, 11, 00),
                mode="Off-Campus",
                status="Scheduled"
            )
            db.session.add(interview)

        for application in shortlisted_applications[38:]:

            interview = Interview(
                application_id=application.id,
                start_datetime=get_ist_datetime(-5, 10, 00),
                end_datetime=get_ist_datetime(-5, 11, 00),
                mode="Virtual",
                status="Not Selected"
            )
            db.session.add(interview)

        db.session.commit()

        print("Interview records created.")

        all_interviews = Interview.query.order_by(Interview.id).all()

        selected_interviews = all_interviews[:25]

        for interview in selected_interviews[:13]:

            placement = Placement(
                interview_id=interview.id,
                joining_datetime=get_ist_datetime(15, 9, 00),
                status="Accepted"
            )
            db.session.add(placement)

        for interview in selected_interviews[13:19]:

            placement = Placement(
                interview_id=interview.id,
                joining_datetime=get_ist_datetime(20, 9, 00),
                status="Offered"
            )
            db.session.add(placement)

        for interview in selected_interviews[19:]:

            placement = Placement(
                interview_id=interview.id,
                joining_datetime=get_ist_datetime(10, 9, 00),
                status="Declined"
            )
            db.session.add(placement)

        db.session.commit()

        print("Placement records created.")

        print("Demo data seeded successfully.")
