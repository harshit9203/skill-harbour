import streamlit as st
import pandas as pd
import os

# ==================== FILES ====================
USERS_FILE = "users.csv"
COURSES_FILE = "courses.csv"
ENROLLMENTS_FILE = "enrollments.csv"

# ==================== INIT ====================
if not os.path.exists(USERS_FILE):
    pd.DataFrame(columns=['username', 'password']).to_csv(USERS_FILE, index=False)

if not os.path.exists(COURSES_FILE):
    pd.DataFrame([
        {'title': 'Web Development', 'overview': 'HTML, CSS, JS basics'},
        {'title': 'Data Science', 'overview': 'Python, ML basics'},
        {'title': 'Cloud Computing', 'overview': 'AWS/Azure/GCP basics'}
    ]).to_csv(COURSES_FILE, index=False)

if not os.path.exists(ENROLLMENTS_FILE):
    pd.DataFrame(columns=['username', 'title']).to_csv(ENROLLMENTS_FILE, index=False)

if 'username' not in st.session_state:
    st.session_state.username = None
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# ==================== STYLE ====================
st.markdown(
    """
    <style>
    p, div[data-testid="stMarkdownContainer"], div[class*="stText"] {
        font-size: 1.2rem !important;
    }
    h1 {
        font-size: 3rem !important;
        font-weight: bold;
    }
    h2 {
        font-size: 2.2rem !important;
        font-weight: bold;
    }
    h3 {
        font-size: 1.8rem !important;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==================== HEADER ====================
st.title('SkillHarbour')
if not st.session_state.username:
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button('🏠 Home'):
            st.session_state.page = "Home"
    with col2:
        if st.button('🔐 Login'):
            st.session_state.page = "Login"
    with col3:
        if st.button('📝 Register'):
            st.session_state.page = "Register"
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button('🏠 Home'):
            st.session_state.page = "Home"
    with col2:
        if st.button('📖 My Courses'):
            st.session_state.page = "My Courses"
    with col3:
        if st.sidebar.button('Logout'):
            st.session_state.username = None
            st.session_state.page = "Home"
            st.rerun()

# ==================== PAGES ====================
page = st.session_state.page

# ========== HOME ==========
if page == "Home":
    st.header('Courses Offered')
    st.markdown(
        "<style>.stButton>button {width: 100%; padding: 1.5rem; font-size: 1.1rem; margin-bottom: 1rem;}</style>",
        unsafe_allow_html=True
    )
    courses = pd.read_csv(COURSES_FILE)
    if not courses.empty:
        for idx, row in courses.iterrows():
            if st.button(f"{row['title']} — {row['overview']}"):
                st.session_state.page = row['title']
                st.rerun()
    else:
        st.info("No courses available yet.")

# ========== REGISTER ==========
elif page == "Register":
    st.header('Register')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Submit Registration'):
        if not username or not password:
            st.error("Username and password cannot be empty.")
        else:
            users = pd.read_csv(USERS_FILE)
            if username in users['username'].values:
                st.error('User already exists!')
            else:
                pd.concat([users, pd.DataFrame([{'username': username, 'password': password}])]).to_csv(USERS_FILE, index=False)
                st.success('User registered successfully! Please log in.')
                st.session_state.page = "Login"
                st.rerun()

# ========== LOGIN ==========
elif page == "Login":
    st.header('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Submit Login'):
        users = pd.read_csv(USERS_FILE)
        if ((users['username'] == username) & (users['password'] == password)).any():
            st.session_state.username = username
            st.success(f'Welcome, {username}!')
            st.session_state.page = "Home"
            st.rerun()
        else:
            st.error('Invalid username or password.')

# ========== MY COURSES ==========
elif page == "My Courses":
    if not st.session_state.username:
        st.warning('Please log in first.')
    else:
        st.header('My Courses')
        enrollments = pd.read_csv(ENROLLMENTS_FILE)
        my_courses = enrollments[enrollments['username'] == st.session_state.username]['title'].tolist()
        if my_courses:
            for c in my_courses:
                st.write(f"✅ {c}")
        else:
            st.info('You are not enrolled in any courses.')

# ========== COURSE PAGES ==========
elif page == "Web Development":
    st.header('Web Development')
    st.subheader('Syllabus')
    st.write("This Web Development course provides a thorough introduction to the fundamental technologies that power the modern web. You’ll begin by learning the building blocks of websites — HTML5 for structuring content, CSS3 for styling and creating responsive, mobile-friendly layouts, and JavaScript for making your pages dynamic and interactive.")
    st.write("Beyond the basics, you’ll explore more advanced topics like semantic markup, accessibility best practices, CSS frameworks such as Bootstrap, responsive grid systems, and JavaScript frameworks for client-side scripting. Throughout the course, you will also dive into the principles of version control with Git, gain an understanding of browser developer tools, and explore introductory concepts for hosting websites on popular platforms like GitHub Pages.")
    st.write("By the end, you’ll have a strong grasp of modern front-end development and be ready to tackle real-world web projects.")
    st.subheader('Projects')
    st.write("Throughout this course, you’ll tackle hands-on projects that help you practice real-world web development.")
    st.write("The first project will have you creating a personal portfolio website where you will practice structuring a homepage, creating responsive navigation, and using CSS to make the site look polished and professional.")
    st.write("Next, you’ll build an interactive game in the browser using vanilla JavaScript to understand event handling, DOM manipulation, and basic animation techniques.")
    st.write("Finally, you’ll design and implement a simple blog platform with dynamic data — allowing you to explore front-end and back-end integration while reinforcing concepts like forms, validation, and responsive UI design.")
    st.subheader('What You’ll Learn')
    st.write("By the end of this course, you’ll have a strong grasp of all the fundamentals of front-end web development — including HTML, CSS, and JavaScript — and an appreciation for modern best practices.")
    st.write("You’ll be comfortable creating clean layouts, applying responsive design principles, and making websites interactive.")
    st.write("Beyond the basics, you’ll also have hands-on experience with Git for version control and be prepared to deploy a simple web application so that others can access it on the internet.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Enroll'):
            if st.session_state.username:
                enrollments = pd.read_csv(ENROLLMENTS_FILE)
                if not ((enrollments['username']==st.session_state.username) & (enrollments['title']==page)).any():
                    pd.concat(
                        [enrollments, pd.DataFrame([{'username': st.session_state.username, 'title': page}])],
                        ignore_index=True
                    ).to_csv(ENROLLMENTS_FILE, index=False)
                    st.success(f'Enrolled in {page}!')
                else:
                    st.info(f'You are already enrolled in {page}.')
            else:
                st.error('Please log in to enroll.')
    with col2:
        if st.button('Back to Home'):
            st.session_state.page = "Home"
            st.rerun()

elif page == "Data Science":
    st.header('Data Science')
    st.subheader('Syllabus')
    st.write("This Data Science course takes you step-by-step through the full data lifecycle — from gathering raw data, to cleaning and transforming it into a usable format, and finally to extracting meaningful insights.")
    st.write("You’ll begin with hands-on practice using Python and its key data libraries — NumPy for efficient numerical computing, pandas for data manipulation, and Matplotlib/Seaborn for visualization. You’ll also explore core statistical concepts and implement these techniques on a variety of datasets.")
    st.write("Moving further, you’ll gain a solid introduction to machine learning, including concepts like supervised vs. unsupervised learning, common algorithms like linear regression and decision trees, and model evaluation techniques. Throughout the course, practical exercises will help you gain hands-on experience applying these tools to solve real-world data problems. By the end, you’ll be equipped to explore, analyze, visualize, and model data for a variety of use cases.")
    st.subheader('Projects')
    st.write("The hands-on projects in this course will give you practical experience in every stage of the data science workflow.")
    st.write("First, you’ll explore and clean a real-world dataset using pandas, handling missing data and inconsistencies while learning data transformation techniques.")
    st.write("You’ll then move on to visualizing your findings with Matplotlib and Seaborn to clearly communicate trends and insights.")
    st.write("Finally, you’ll implement a predictive model using scikit-learn — choosing appropriate features, training and testing a model, and interpreting its performance — so you can appreciate what goes into building machine learning solutions.")
    st.subheader('What You’ll Learn')
    st.write("By the end of this course, you’ll have built a practical skill set for working with data, allowing you to load, clean, analyze, and visualize data efficiently.")
    st.write("You’ll also understand key statistical concepts and basic predictive modeling, giving you the tools to explore data-driven questions on your own.")
    st.write("More importantly, you’ll gain the confidence to tackle new datasets, identify patterns and correlations, and present your findings in a clear and engaging way.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Enroll'):
            if st.session_state.username:
                enrollments = pd.read_csv(ENROLLMENTS_FILE)
                if not ((enrollments['username']==st.session_state.username) & (enrollments['title']==page)).any():
                    pd.concat(
                        [enrollments, pd.DataFrame([{'username': st.session_state.username, 'title': page}])],
                        ignore_index=True
                    ).to_csv(ENROLLMENTS_FILE, index=False)
                    st.success(f'Enrolled in {page}!')
                else:
                    st.info(f'You are already enrolled in {page}.')
            else:
                st.error('Please log in to enroll.')
    with col2:
        if st.button('Back to Home'):
            st.session_state.page = "Home"
            st.rerun()

elif page == "Cloud Computing":
    st.header('Cloud Computing')
    st.subheader('Syllabus')
    st.write("This Cloud Computing course provides a comprehensive introduction to cloud technologies and the principles that power today’s on-demand computing environments. You’ll begin by understanding the history and evolution of cloud computing, exploring how it has transformed the way applications are developed, deployed, and scaled.")
    st.write("The course will guide you through the core service models of cloud computing — Infrastructure as a Service (IaaS), Platform as a Service (PaaS), and Software as a Service (SaaS) — explaining when and why each is used. You’ll also learn about different deployment models, including public, private, hybrid, and multi-cloud, and analyze their use cases in various industries.")
    st.write("As you progress, you’ll gain hands-on experience working with popular cloud platforms such as AWS, Azure, and Google Cloud. You’ll practice setting up and configuring virtual machines, creating and managing cloud storage buckets, configuring basic networking components, and applying security policies such as firewall rules and identity management.")
    st.write("The syllabus also includes instruction on monitoring and managing cloud resources effectively using built-in tools and dashboards. You will explore how to automate deployments using simple scripts, templates, and services like AWS CloudFormation or Azure Resource Manager.")
    st.write("Finally, you’ll tackle advanced topics such as high availability, load balancing, auto-scaling, disaster recovery, and cost optimization. By the end of this syllabus, you will have a clear understanding of how to architect and manage cloud environments that are secure, scalable, and resilient to failure.")
    st.subheader('Projects')
    st.write("The practical assignments in this course will expose you to real-world cloud computing tasks.")
    st.write("You’ll begin by launching and configuring a virtual machine on a public cloud platform like AWS or Azure, becoming familiar with its dashboard, security groups, and basic administration.")
    st.write("From there, you’ll deploy a simple website to the cloud using managed hosting services, giving you hands-on experience with domains, storage, and making your app accessible to the public.")
    st.write("Finally, you’ll practice setting up a scalable cloud architecture — working with concepts like load balancers and auto-scaling groups — so that you can appreciate what it takes to deploy and manage a production-ready cloud application.")
    st.subheader('What You’ll Learn')
    st.write("After completing this course, you’ll have a solid understanding of the core concepts and tools that power cloud computing — from on-demand servers and networking to scalable storage and security basics.")
    st.write("You’ll feel confident working within the AWS or Azure dashboard, launching instances, configuring basic security policies, and deploying a simple app or website to the cloud.")
    st.write("Equally important, you’ll gain a deeper appreciation for the scalability and flexibility that cloud platforms offer, preparing you to leverage the cloud for your own future projects.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Enroll'):
            if st.session_state.username:
                enrollments = pd.read_csv(ENROLLMENTS_FILE)
                if not ((enrollments['username']==st.session_state.username) & (enrollments['title']==page)).any():
                    pd.concat(
                        [enrollments, pd.DataFrame([{'username': st.session_state.username, 'title': page}])],
                        ignore_index=True
                    ).to_csv(ENROLLMENTS_FILE, index=False)
                    st.success(f'Enrolled in {page}!')
                else:
                    st.info(f'You are already enrolled in {page}.')
            else:
                st.error('Please log in to enroll.')
    with col2:
        if st.button('Back to Home'):
            st.session_state.page = "Home"
            st.rerun()
