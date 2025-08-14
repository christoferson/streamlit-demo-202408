import streamlit as st
import pandas as pd
from datetime import datetime, date
import uuid
import time

# Custom CSS for CRUD interface
st.markdown("""
<style>
    .crud-header {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .action-card {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #3498db;
    }
    
    .search-container {
        background: linear-gradient(135deg, #e8f4fd 0%, #f1f8ff 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 1px solid #d1ecf1;
    }
    
    .record-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        border-left: 3px solid #27ae60;
    }
    
    .stats-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem;
    }
    
    .success-message {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .error-message {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for data storage
if 'employees' not in st.session_state:
    st.session_state.employees = pd.DataFrame({
        'id': [str(uuid.uuid4())[:8] for _ in range(5)],
        'name': ['Alice Johnson', 'Bob Smith', 'Carol Davis', 'David Wilson', 'Eva Brown'],
        'email': ['alice@company.com', 'bob@company.com', 'carol@company.com', 'david@company.com', 'eva@company.com'],
        'department': ['Engineering', 'Marketing', 'Sales', 'Engineering', 'HR'],
        'position': ['Senior Developer', 'Marketing Manager', 'Sales Rep', 'DevOps Engineer', 'HR Specialist'],
        'salary': [95000, 75000, 65000, 88000, 70000],
        'hire_date': [date(2020, 1, 15), date(2021, 3, 10), date(2019, 8, 22), date(2022, 5, 5), date(2021, 11, 30)],
        'status': ['Active', 'Active', 'Active', 'Active', 'Active']
    })

if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'selected_department' not in st.session_state:
    st.session_state.selected_department = "All"
if 'editing_id' not in st.session_state:
    st.session_state.editing_id = None
if 'show_add_form' not in st.session_state:
    st.session_state.show_add_form = False

# Page header
st.markdown("""
<div class="crud-header">
    <h1>👥 Employee Management System</h1>
    <p>Complete CRUD operations with advanced search and filtering</p>
</div>
""", unsafe_allow_html=True)

# Statistics Dashboard Fragment
@st.fragment
def display_stats():
    df = st.session_state.employees
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stats-container">
            <h3>{len(df)}</h3>
            <p>Total Employees</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        active_count = len(df[df['status'] == 'Active'])
        st.markdown(f"""
        <div class="stats-container">
            <h3>{active_count}</h3>
            <p>Active Employees</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_salary = df['salary'].mean()
        st.markdown(f"""
        <div class="stats-container">
            <h3>${avg_salary:,.0f}</h3>
            <p>Average Salary</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        dept_count = df['department'].nunique()
        st.markdown(f"""
        <div class="stats-container">
            <h3>{dept_count}</h3>
            <p>Departments</p>
        </div>
        """, unsafe_allow_html=True)

# Search and Filter Fragment
@st.fragment
def search_and_filter():
    st.markdown("""
    <div class="search-container">
        <h4>🔍 Search & Filter</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_query = st.text_input(
            "Search employees...",
            value=st.session_state.search_query,
            placeholder="Search by name, email, or position",
            key="search_input"
        )
        if search_query != st.session_state.search_query:
            st.session_state.search_query = search_query
    
    with col2:
        departments = ['All'] + sorted(st.session_state.employees['department'].unique().tolist())
        selected_dept = st.selectbox(
            "Department",
            departments,
            index=departments.index(st.session_state.selected_department),
            key="dept_filter"
        )
        if selected_dept != st.session_state.selected_department:
            st.session_state.selected_department = selected_dept
    
    with col3:
        status_filter = st.selectbox(
            "Status",
            ["All", "Active", "Inactive"],
            key="status_filter"
        )
    
    return search_query, selected_dept, status_filter

# Add Employee Form Fragment
@st.fragment
def add_employee_form():
    if st.session_state.show_add_form:
        st.markdown("### ➕ Add New Employee")
        
        with st.form("add_employee_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name*", placeholder="Enter full name")
                email = st.text_input("Email*", placeholder="employee@company.com")
                department = st.selectbox("Department*", 
                                        ["Engineering", "Marketing", "Sales", "HR", "Finance", "Operations"])
            
            with col2:
                position = st.text_input("Position*", placeholder="Job title")
                salary = st.number_input("Salary*", min_value=30000, max_value=200000, value=60000, step=5000)
                hire_date = st.date_input("Hire Date*", value=date.today())
            
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                submitted = st.form_submit_button("💾 Add Employee", type="primary")
            
            with col2:
                cancelled = st.form_submit_button("❌ Cancel")
            
            if submitted:
                if name and email and department and position:
                    new_employee = {
                        'id': str(uuid.uuid4())[:8],
                        'name': name,
                        'email': email,
                        'department': department,
                        'position': position,
                        'salary': salary,
                        'hire_date': hire_date,
                        'status': 'Active'
                    }
                    
                    # Add to dataframe
                    new_row = pd.DataFrame([new_employee])
                    st.session_state.employees = pd.concat([st.session_state.employees, new_row], ignore_index=True)
                    
                    st.success(f"✅ Employee {name} added successfully!")
                    st.session_state.show_add_form = False
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Please fill in all required fields marked with *")
            
            if cancelled:
                st.session_state.show_add_form = False
                st.rerun()

# Edit Employee Form Fragment
@st.fragment
def edit_employee_form():
    if st.session_state.editing_id:
        employee = st.session_state.employees[st.session_state.employees['id'] == st.session_state.editing_id].iloc[0]
        
        st.markdown(f"### ✏️ Edit Employee: {employee['name']}")
        
        with st.form("edit_employee_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name", value=employee['name'])
                email = st.text_input("Email", value=employee['email'])
                department = st.selectbox("Department", 
                                        ["Engineering", "Marketing", "Sales", "HR", "Finance", "Operations"],
                                        index=["Engineering", "Marketing", "Sales", "HR", "Finance", "Operations"].index(employee['department']))
            
            with col2:
                position = st.text_input("Position", value=employee['position'])
                salary = st.number_input("Salary", min_value=30000, max_value=200000, value=int(employee['salary']), step=5000)
                status = st.selectbox("Status", ["Active", "Inactive"], 
                                    index=0 if employee['status'] == 'Active' else 1)
            
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                updated = st.form_submit_button("💾 Update", type="primary")
            
            with col2:
                cancelled = st.form_submit_button("❌ Cancel")
            
            if updated:
                # Update the employee record
                idx = st.session_state.employees[st.session_state.employees['id'] == st.session_state.editing_id].index[0]
                st.session_state.employees.loc[idx, 'name'] = name
                st.session_state.employees.loc[idx, 'email'] = email
                st.session_state.employees.loc[idx, 'department'] = department
                st.session_state.employees.loc[idx, 'position'] = position
                st.session_state.employees.loc[idx, 'salary'] = salary
                st.session_state.employees.loc[idx, 'status'] = status
                
                st.success(f"✅ Employee {name} updated successfully!")
                st.session_state.editing_id = None
                time.sleep(1)
                st.rerun()
            
            if cancelled:
                st.session_state.editing_id = None
                st.rerun()

# Employee List Fragment
@st.fragment
def display_employee_list():
    df = st.session_state.employees.copy()
    
    # Apply filters
    search_query, selected_dept, status_filter = search_and_filter()
    
    # Filter by search query
    if search_query:
        mask = (
            df['name'].str.contains(search_query, case=False, na=False) |
            df['email'].str.contains(search_query, case=False, na=False) |
            df['position'].str.contains(search_query, case=False, na=False)
        )
        df = df[mask]
    
    # Filter by department
    if selected_dept != "All":
        df = df[df['department'] == selected_dept]
    
    # Filter by status
    if status_filter != "All":
        df = df[df['status'] == status_filter]
    
    st.markdown(f"### 📋 Employee List ({len(df)} records)")
    
    if len(df) == 0:
        st.info("🔍 No employees found matching your search criteria.")
        return
    
    # Display employees in a more interactive way
    for idx, employee in df.iterrows():
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            
            with col1:
                status_emoji = "🟢" if employee['status'] == 'Active' else "🔴"
                st.markdown(f"""
                **{status_emoji} {employee['name']}**  
                📧 {employee['email']}  
                💼 {employee['position']}
                """)
            
            with col2:
                st.markdown(f"""
                🏢 **{employee['department']}**  
                💰 ${employee['salary']:,}  
                📅 {employee['hire_date']}
                """)
            
            with col3:
                if st.button(f"✏️ Edit", key=f"edit_{employee['id']}", help="Edit employee"):
                    st.session_state.editing_id = employee['id']
                    st.session_state.show_add_form = False
                    st.rerun()
            
            with col4:
                if st.button(f"🗑️ Delete", key=f"delete_{employee['id']}", help="Delete employee"):
                    st.session_state.employees = st.session_state.employees[st.session_state.employees['id'] != employee['id']]
                    st.success(f"✅ Employee {employee['name']} deleted successfully!")
                    time.sleep(1)
                    st.rerun()
            
            st.divider()

# Main layout
display_stats()

st.markdown("---")

# Action buttons
col1, col2, col3 = st.columns([1, 1, 4])

with col1:
    if st.button("➕ Add Employee", type="primary"):
        st.session_state.show_add_form = True
        st.session_state.editing_id = None
        st.rerun()

with col2:
    if st.button("📊 Export CSV"):
        csv = st.session_state.employees.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f'employees_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            mime='text/csv'
        )

# Forms section
add_employee_form()
edit_employee_form()

st.markdown("---")

# Employee list
display_employee_list()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #666;">
    <p>👥 <strong>Employee Management System</strong> - Efficient CRUD operations with real-time search</p>
    <p>💡 Features: Add, Edit, Delete, Search, Filter, Export, and Real-time Updates</p>
</div>
""", unsafe_allow_html=True)