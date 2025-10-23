import streamlit as st
import requests
import pandas as pd
import datetime

# --- Base API URL ---
API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="CareLink Rostering Dashboard", layout="wide")
st.title("👩‍⚕️ CareLink Rostering Dashboard")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["👨‍💼 Staff", "🧓 Service Users", "📅 Staff Availability", "📋 Service User Assignments", "🩺 Service User Needs"])

# =========================================================
# ------------------- STAFF TAB -------------------
# =========================================================
with tab1:
    st.header("👨‍💼 Staff Details")

    # --- Load staff data ---
    def load_staff():
        resp = requests.get(f"{API_BASE}/staff")
        if resp.status_code == 200:
            return pd.DataFrame(resp.json(), columns=[
                "id", "first_name", "last_name", "job_role", "line_manager",
                "contracted_hours", "primary_team", "preferred_travel_type",
                "start_date", "leave_date", "email", "work_number", "postcode"
            ])
        else:
            st.error("Failed to fetch staff data")
            return pd.DataFrame()

    staff_data = load_staff()

    if not staff_data.empty:
        # --- Show all staff records ---
        st.subheader("📋 All Staff Records")
        st.dataframe(staff_data, use_container_width=True)
        st.markdown("---")

        # --- Filter section ---
        st.subheader("🔍 Filter & Search Staff")

        col1, col2, col3 = st.columns(3)
        with col1:
            team_filter = st.selectbox(
                "Filter by Team",
                ["All"] + sorted(staff_data["primary_team"].dropna().unique().tolist())
            )
        with col2:
            manager_filter = st.selectbox(
                "Filter by Line Manager",
                ["All"] + sorted(staff_data["line_manager"].dropna().unique().tolist())
            )
        with col3:
            search_name = st.text_input("Search by Name")

        # --- Apply filters ---
        filtered = staff_data.copy()
        if team_filter != "All":
            filtered = filtered[filtered["primary_team"].fillna("") == team_filter]
        if manager_filter != "All":
            filtered = filtered[filtered["line_manager"].fillna("") == manager_filter]
        if search_name:
            mask = (
                filtered["first_name"].fillna("").str.contains(search_name, case=False)
                | filtered["last_name"].fillna("").str.contains(search_name, case=False)
            )
            filtered = filtered[mask]

        # --- Show filtered results ---
        st.markdown("#### 🎯 Filtered Results")
        st.dataframe(filtered.sort_values("first_name"), use_container_width=True)
        st.caption("💡 Tip: Click column headers to sort ↑↓")
        st.markdown("---")

        # --- Select staff for edit/delete ---
        selected_id = st.selectbox("Select a staff member by ID to manage:", staff_data["id"])
        selected_staff = staff_data[staff_data["id"] == selected_id].iloc[0]

        # --- Edit form ---
        with st.form("edit_staff_form"):
            st.subheader("✏️ Edit Staff Details")
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name", selected_staff["first_name"])
                last_name = st.text_input("Last Name", selected_staff["last_name"])
                job_role = st.text_input("Job Role", selected_staff["job_role"])
                line_manager = st.text_input("Line Manager", selected_staff["line_manager"])
                contracted_hours = st.number_input("Contracted Hours", value=float(selected_staff["contracted_hours"]))
                start_date = st.date_input(
                    "Start Date",
                    pd.to_datetime(selected_staff["start_date"]).date() if selected_staff["start_date"] else datetime.date(2020, 1, 1),
                    min_value=datetime.date(1990, 1, 1)
                )
                leave_date = st.date_input(
                    "Leave Date",
                    pd.to_datetime(selected_staff["leave_date"]).date() if selected_staff["leave_date"] else datetime.date(2020, 1, 1),
                    min_value=datetime.date(1990, 1, 1)
                )
            with col2:
                email = st.text_input("Email", selected_staff["email"])
                primary_team = st.text_input("Primary Team", selected_staff["primary_team"])
                preferred_travel_type = st.text_input("Preferred Travel Type", selected_staff["preferred_travel_type"])
                work_number = st.text_input("Work Number", selected_staff["work_number"])
                postcode = st.text_input("Postcode", selected_staff["postcode"])

            save_changes = st.form_submit_button("💾 Save Changes")

            if save_changes:
                payload = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "job_role": job_role,
                    "line_manager": line_manager,
                    "contracted_hours": contracted_hours,
                    "primary_team": primary_team,
                    "preferred_travel_type": preferred_travel_type,
                    "start_date": str(start_date),
                    "leave_date": str(leave_date),
                    "email": email,
                    "work_number": work_number,
                    "postcode": postcode
                }
                res = requests.put(f"{API_BASE}/staff/{selected_id}", json=payload)
                if res.status_code == 200:
                    st.success("✅ Staff updated successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to update staff.")

        # --- Delete button ---
        if st.button("🗑️ Delete This Staff Member"):
            res = requests.delete(f"{API_BASE}/staff/{selected_id}")
            if res.status_code == 200:
                st.success("✅ Staff deleted successfully!")
                st.rerun()
            else:
                st.error("❌ Failed to delete staff.")

    else:
        st.info("ℹ️ No staff data available yet.")

    # --- Add new staff form ---
    st.markdown("---")
    st.subheader("➕ Add New Staff")
    with st.form("new_staff_form"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            job_role = st.text_input("Job Role")
            line_manager = st.text_input("Line Manager")
            contracted_hours = st.number_input("Contracted Hours", 0.0)
            primary_team = st.text_input("Primary Team")
        with col2:
            preferred_travel_type = st.text_input("Preferred Travel Type")
            start_date = st.date_input("Start Date", min_value=datetime.date(1990, 1, 1))
            email = st.text_input("Email")
            work_number = st.text_input("Work Number")
            postcode = st.text_input("Postcode")

        submitted = st.form_submit_button("Add Staff")
        if submitted:
            data = {
                "first_name": first_name,
                "last_name": last_name,
                "job_role": job_role,
                "line_manager": line_manager,
                "contracted_hours": contracted_hours,
                "primary_team": primary_team,
                "preferred_travel_type": preferred_travel_type,
                "start_date": str(start_date),
                "email": email,
                "work_number": work_number,
                "postcode": postcode
            }
            res = requests.post(f"{API_BASE}/staff", json=data)
            if res.status_code == 200:
                st.success("✅ Staff added successfully!")
                st.rerun()
            else:
                st.error("❌ Failed to add staff.")

# =========================================================
# ------------------- SERVICE USER TAB -------------------
# =========================================================
with tab2:
    st.header("🧓 Service User Details")

    # --- Load service user data ---
    def load_users():
        resp = requests.get(f"{API_BASE}/service-users")
        if resp.status_code == 200:
            return pd.DataFrame(resp.json(), columns=[
                "id", "unique_reference_code", "first_name", "last_name",
                "date_of_birth", "gender", "rag_rating", "nhs_number",
                "start_date", "end_date", "primary_team", "contact_number",
                "contact_email", "full_address", "keysafe_code"
            ])
        else:
            st.error("Failed to fetch service user data")
            return pd.DataFrame()

    user_data = load_users()

    if not user_data.empty:
        # --- Show all users ---
        st.subheader("📋 All Service Users")
        st.dataframe(user_data, use_container_width=True)
        st.markdown("---")

        # --- Filter Section ---
        st.subheader("🔍 Filter & Search Service Users")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            team_filter = st.selectbox(
                "Filter by Team",
                ["All"] + sorted(user_data["primary_team"].dropna().unique().tolist())
            )
        with col2:
            gender_filter = st.selectbox(
                "Filter by Gender",
                ["All"] + sorted(user_data["gender"].dropna().unique().tolist())
            )
        with col3:
            rag_filter = st.selectbox(
                "Filter by RAG Rating",
                ["All"] + sorted(user_data["rag_rating"].dropna().unique().tolist())
            )
        with col4:
            search_name = st.text_input("Search by Name or Reference")

        # --- Apply filters safely ---
        filtered = user_data.copy()
        if team_filter != "All":
            filtered = filtered[filtered["primary_team"].fillna("") == team_filter]
        if gender_filter != "All":
            filtered = filtered[filtered["gender"].fillna("") == gender_filter]
        if rag_filter != "All":
            filtered = filtered[filtered["rag_rating"].fillna("") == rag_filter]
        if search_name:
            mask = (
                filtered["first_name"].fillna("").str.contains(search_name, case=False)
                | filtered["last_name"].fillna("").str.contains(search_name, case=False)
                | filtered["unique_reference_code"].fillna("").str.contains(search_name, case=False)
            )
            filtered = filtered[mask]

        st.markdown("#### 🎯 Filtered Results")
        st.dataframe(filtered.sort_values("first_name"), use_container_width=True)
        st.caption("💡 Tip: Click column headers to sort ↑↓")
        st.markdown("---")

        # --- Edit Service User ---
        selected_user_id = st.selectbox("Select a service user by ID to manage:", user_data["id"])
        selected_user = user_data[user_data["id"] == selected_user_id].iloc[0]

        with st.form("edit_user_form"):
            st.subheader("✏️ Edit Service User Details")
            col1, col2 = st.columns(2)
            with col1:
                unique_reference_code = st.text_input("Reference Code", selected_user["unique_reference_code"])
                first_name = st.text_input("First Name", selected_user["first_name"])
                last_name = st.text_input("Last Name", selected_user["last_name"])
                date_of_birth = st.date_input(
                    "Date of Birth",
                    pd.to_datetime(selected_user["date_of_birth"]).date() if selected_user["date_of_birth"] else datetime.date(1970, 1, 1),
                    min_value=datetime.date(1900, 1, 1)
                )
                gender = st.selectbox(
                    "Gender",
                    ["Male", "Female", "Other"],
                    index=["Male", "Female", "Other"].index(selected_user["gender"])
                    if selected_user["gender"] in ["Male", "Female", "Other"] else 0
                )
                rag_rating = st.text_input("RAG Rating", selected_user["rag_rating"])
            with col2:
                primary_team = st.text_input("Primary Team", selected_user["primary_team"])
                contact_number = st.text_input("Contact Number", selected_user["contact_number"])
                contact_email = st.text_input("Contact Email", selected_user["contact_email"])
                full_address = st.text_area("Full Address", selected_user["full_address"])
                keysafe_code = st.text_input("Keysafe Code", selected_user["keysafe_code"])

            update_user = st.form_submit_button("💾 Save Changes")
            if update_user:
                payload = {
                    "unique_reference_code": unique_reference_code,
                    "first_name": first_name,
                    "last_name": last_name,
                    "date_of_birth": str(date_of_birth),
                    "gender": gender,
                    "rag_rating": rag_rating,
                    "primary_team": primary_team,
                    "contact_number": contact_number,
                    "contact_email": contact_email,
                    "full_address": full_address,
                    "keysafe_code": keysafe_code
                }
                res = requests.put(f"{API_BASE}/service-users/{selected_user_id}", json=payload)
                if res.status_code == 200:
                    st.success("✅ Service user updated successfully!")
                    st.rerun()
                else:
                    st.error(f"❌ Failed to update service user ({res.status_code})")

        if st.button("🗑️ Delete This Service User"):
            res = requests.delete(f"{API_BASE}/service-users/{selected_user_id}")
            if res.status_code == 200:
                st.success("✅ Service user deleted successfully!")
                st.rerun()
            else:
                st.error("❌ Failed to delete service user.")
    else:
        st.info("ℹ️ No service user data available yet.")

    # --- Add new user ---
    st.markdown("---")
    st.subheader("➕ Add New Service User")
    with st.form("new_user_form"):
        col1, col2 = st.columns(2)
        with col1:
            unique_reference_code = st.text_input("Reference Code")
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            date_of_birth = st.date_input("Date of Birth", min_value=datetime.date(1900, 1, 1))
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            rag_rating = st.text_input("RAG Rating")
        with col2:
            primary_team = st.text_input("Primary Team")
            contact_number = st.text_input("Contact Number")
            contact_email = st.text_input("Contact Email")
            full_address = st.text_area("Full Address")
            keysafe_code = st.text_input("Keysafe Code")

        submitted = st.form_submit_button("Add Service User")
        if submitted:
            data = {
                "unique_reference_code": unique_reference_code,
                "first_name": first_name,
                "last_name": last_name,
                "date_of_birth": str(date_of_birth),
                "gender": gender,
                "rag_rating": rag_rating,
                "primary_team": primary_team,
                "contact_number": contact_number,
                "contact_email": contact_email,
                "full_address": full_address,
                "keysafe_code": keysafe_code
            }
            res = requests.post(f"{API_BASE}/service-users", json=data)
            if res.status_code == 200:
                st.success("✅ Service user added successfully!")
                st.rerun()
            else:
                st.error("❌ Failed to add service user.")


# =========================================================
# ------------------- STAFF AVAILABILITY TAB -------------------
# =========================================================
with tab3:
    st.header("📅 Staff Regular Availability")

    # --- Load staff for dropdown ---
    staff_resp = requests.get(f"{API_BASE}/staff")
    if staff_resp.status_code in [200, 201]:
        staff_list = staff_resp.json()
        staff_df = pd.DataFrame(staff_list, columns=[
            "id", "first_name", "last_name", "job_role", "line_manager",
            "contracted_hours", "primary_team", "preferred_travel_type",
            "start_date", "leave_date", "email", "work_number", "postcode"
        ])
        staff_map = {f"{r.first_name} {r.last_name}": r.id for _, r in staff_df.iterrows()}
    else:
        st.error("❌ Failed to load staff list")
        staff_map = {}

    if staff_map:
        selected_staff = st.selectbox("Select a staff member", list(staff_map.keys()))
        staff_id = staff_map[selected_staff]

        st.markdown("### Set Available Days")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            monday = st.checkbox("Monday")
            tuesday = st.checkbox("Tuesday")
        with col2:
            wednesday = st.checkbox("Wednesday")
            thursday = st.checkbox("Thursday")
        with col3:
            friday = st.checkbox("Friday")
            saturday = st.checkbox("Saturday")
        with col4:
            sunday = st.checkbox("Sunday")

        start_time = st.time_input("Start Time", datetime.time(9, 0))
        end_time = st.time_input("End Time", datetime.time(17, 0))

        if st.button("💾 Save Availability"):
            data = {
                "staff_id": staff_id,
                "monday": monday,
                "tuesday": tuesday,
                "wednesday": wednesday,
                "thursday": thursday,
                "friday": friday,
                "saturday": saturday,
                "sunday": sunday,
                "start_time": str(start_time),
                "end_time": str(end_time)
            }

            # Send to backend
            res = requests.post(f"{API_BASE}/staff-availability", json=data)

            # Debug info
            st.write("📤 Payload Sent:", data)
            st.write("🔁 Response Code:", res.status_code)
            st.write("🧾 Response Text:", res.text)

            if res.status_code in [200, 201]:
                st.success("✅ Availability saved successfully!")
                st.rerun()
            else:
                st.error(f"❌ Failed to save availability (Code: {res.status_code})")

    st.markdown("---")
    st.subheader("🧾 Current Availability Records")

    avail_resp = requests.get(f"{API_BASE}/staff-availability")
    if avail_resp.status_code in [200, 201] and len(avail_resp.json()) > 0:
        df = pd.DataFrame(avail_resp.json())
        if "staff_id" in df.columns and not df.empty:
            df = df.merge(
                staff_df[["id", "first_name", "last_name"]],
                left_on="staff_id",
                right_on="id",
                how="left"
            )
            df["staff_name"] = df["first_name"] + " " + df["last_name"]
            st.dataframe(df.drop(columns=["id_y", "first_name", "last_name"], errors="ignore"))
        else:
            st.dataframe(df)
    else:
        st.info("ℹ️ No availability data found yet.")


# =========================================================
# ---------------- SERVICE USER ASSIGNMENTS TAB ------------
# =========================================================
with tab4:
    st.header("📋 Service User Assignments")

    API_BASE = "http://127.0.0.1:8000"  # ✅ Ensure this matches backend address

    # --- Load data ---
    staff_resp = requests.get(f"{API_BASE}/staff")
    user_resp = requests.get(f"{API_BASE}/service-users")
    assign_resp = requests.get(f"{API_BASE}/assignments")

    if (
        staff_resp.status_code in [200, 201]
        and user_resp.status_code in [200, 201]
    ):
        staff_df = pd.DataFrame(staff_resp.json())
        user_df = pd.DataFrame(user_resp.json())

        # Filter service users who "need" assignment
        if "end_date" in user_df.columns:
            user_df = user_df[user_df["end_date"].isna()]
        if "rag_rating" in user_df.columns:
            user_df = user_df[user_df["rag_rating"].isin(["High", "Medium", None])]

        staff_map = {
            f"{r['first_name']} {r['last_name']}": r["id"] for _, r in staff_df.iterrows()
        }
        user_map = {
            f"{r['first_name']} {r['last_name']}": r["id"] for _, r in user_df.iterrows()
        }

    else:
        st.error("❌ Failed to load staff or service users.")
        staff_map, user_map = {}, {}

    # --- New Assignment Form ---
    st.subheader("➕ Create New Assignment")

    if staff_map and user_map:
        with st.form("new_assignment"):
            col1, col2, col3 = st.columns(3)
            with col1:
                selected_staff = st.selectbox("Select Staff", list(staff_map.keys()))
            with col2:
                selected_user = st.selectbox("Select Service User (needs support)", list(user_map.keys()))
            with col3:
                assignment_date = st.date_input("Assignment Date", datetime.date.today())

            start_time = st.time_input("Start Time", datetime.time(9, 0))
            end_time = st.time_input("End Time", datetime.time(17, 0))
            notes = st.text_area("Notes (optional)")

            submit = st.form_submit_button("💾 Save Assignment")

            if submit:
                # --- DUPLICATE CHECK ---
                existing = []
                if assign_resp.status_code in [200, 201]:
                    df = pd.DataFrame(assign_resp.json())
                    if not df.empty:
                        existing = df[
                            (df["service_user_id"] == user_map[selected_user])
                            & (df["assignment_date"] == str(assignment_date))
                        ]

                if len(existing) > 0:
                    st.warning(
                        f"🧭 This service user already has a staff assigned on {assignment_date}. "
                        "Please choose another date or service user."
                    )
                else:
                    data = {
                        "staff_id": staff_map[selected_staff],
                        "service_user_id": user_map[selected_user],
                        "assignment_date": str(assignment_date),
                        "start_time": str(start_time),
                        "end_time": str(end_time),
                        "notes": notes,
                    }

                    res = requests.post(f"{API_BASE}/assignments", json=data)

                    st.write("📤 Payload Sent:", data)
                    st.write("🔁 Response Code:", res.status_code)
                    st.write("🧾 Response Text:", res.text)

                    if res.status_code in [200, 201]:
                        st.success("✅ Assignment created successfully!")
                        st.rerun()
                    else:
                        st.error(f"❌ Failed to create assignment (Code: {res.status_code})")

    else:
        st.info("ℹ️ No eligible staff or service users available.")

    # --- Existing Assignments ---
    st.markdown("---")
    st.subheader("📋 Existing Assignments")

    assign_resp = requests.get(f"{API_BASE}/assignments")

    if assign_resp.status_code in [200, 201]:
        df = pd.DataFrame(assign_resp.json())

        if not df.empty:
            df["Staff"] = df["staff_first_name"] + " " + df["staff_last_name"]
            df["Service User"] = df["user_first_name"] + " " + df["user_last_name"]
            df = df[
                ["Staff", "Service User", "assignment_date", "start_time", "end_time", "notes"]
            ].sort_values(by="assignment_date", ascending=False)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("ℹ️ No assignments found yet.")
    else:
        st.error("❌ Failed to fetch assignments.")




with tab5:
    st.header("🩺 Service User Care Needs")

    needs_resp = requests.get(f"{API_BASE}/service-user-needs")
    if needs_resp.status_code == 200:
        needs = pd.DataFrame(needs_resp.json())
        st.dataframe(needs)
    else:
        st.error("Failed to load care needs")

    st.subheader("➕ Add New Care Need")
    with st.form("add_need"):
        user_id = st.number_input("Service User ID", min_value=1)
        care_type = st.text_input("Care Type (e.g. Nurse, Carer, Doctor)")
        description = st.text_area("Description")
        frequency = st.text_input("Frequency (e.g. Daily, Mon/Wed/Fri)")
        preferred_time = st.time_input("Preferred Time")
        duration = st.number_input("Duration (minutes)", min_value=5, max_value=300, value=30)

        submitted = st.form_submit_button("Save")
        if submitted:
            payload = {
                "service_user_id": user_id,
                "care_type": care_type,
                "description": description,
                "frequency": frequency,
                "preferred_time": str(preferred_time),
                "duration_minutes": duration
            }
            res = requests.post(f"{API_BASE}/service-user-needs", json=payload)
            if res.status_code in [200, 201]:
                st.success("✅ Care need added successfully!")
                st.rerun()
            else:
                st.error(f"❌ Failed to add care need ({res.status_code})")
