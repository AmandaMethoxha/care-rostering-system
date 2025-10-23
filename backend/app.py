from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import os
from typing import Optional

app = FastAPI()

# ============================================================
# --- Database Connection ---
# ============================================================
DB_HOST = "db"
DB_NAME = "care_roster"
DB_USER = "postgres"
DB_PASS = "postgres"
DB_PORT = "5432"

def get_connection():
    import psycopg2
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        print("✅ Connected to database successfully!")
        return conn
    except Exception as e:
        print("❌ Database connection failed:", e)
        raise



# ============================================================
# --- 1️⃣ STAFF DETAILS ---
# ============================================================
@app.get("/staff")
def get_staff():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM staff_details;")
    columns = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(zip(columns, row)) for row in rows]

# ============================================================
# --- 2️⃣ SERVICE USER DETAILS ---
# ============================================================
@app.get("/service-users")
def get_service_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM service_user_details;")
    columns = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(zip(columns, row)) for row in rows]

# ============================================================
# --- Pydantic Models ---
# ============================================================
class StaffCreate(BaseModel):
    first_name: str
    last_name: str
    job_role: str
    line_manager: Optional[str] = None
    contracted_hours: Optional[float] = None
    primary_team: Optional[str] = None
    preferred_travel_type: Optional[str] = None
    start_date: Optional[str] = None
    leave_date: Optional[str] = None
    email: str
    work_number: Optional[str] = None
    postcode: Optional[str] = None

class ServiceUserCreate(BaseModel):
    unique_reference_code: str
    first_name: str
    last_name: str
    date_of_birth: str
    gender: str
    rag_rating: Optional[str] = None
    nhs_number: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    primary_team: Optional[str] = None
    contact_number: Optional[str] = None
    contact_email: Optional[str] = None
    full_address: Optional[str] = None
    keysafe_code: Optional[str] = None

# ============================================================
# --- CREATE / UPDATE / DELETE STAFF ---
# ============================================================
@app.post("/staff")
def create_staff(staff: StaffCreate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO staff_details (
            first_name, last_name, job_role, line_manager, contracted_hours,
            primary_team, preferred_travel_type, start_date, leave_date, email,
            work_number, postcode
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    """, (
        staff.first_name, staff.last_name, staff.job_role, staff.line_manager,
        staff.contracted_hours, staff.primary_team, staff.preferred_travel_type,
        staff.start_date, staff.leave_date, staff.email, staff.work_number, staff.postcode
    ))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Staff created successfully", "id": new_id}

@app.put("/staff/{staff_id}")
def update_staff(staff_id: int, staff: StaffCreate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE staff_details
        SET first_name=%s, last_name=%s, job_role=%s, line_manager=%s,
            contracted_hours=%s, primary_team=%s, preferred_travel_type=%s,
            start_date=%s, leave_date=%s, email=%s, work_number=%s, postcode=%s
        WHERE id=%s
        RETURNING id;
    """, (
        staff.first_name, staff.last_name, staff.job_role, staff.line_manager,
        staff.contracted_hours, staff.primary_team, staff.preferred_travel_type,
        staff.start_date, staff.leave_date, staff.email, staff.work_number,
        staff.postcode, staff_id
    ))
    updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not updated:
        raise HTTPException(status_code=404, detail="Staff not found")
    return {"message": "Staff updated successfully", "id": staff_id}

@app.delete("/staff/{staff_id}")
def delete_staff(staff_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM staff_details WHERE id=%s RETURNING id;", (staff_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not deleted:
        raise HTTPException(status_code=404, detail="Staff not found")
    return {"message": "Staff deleted successfully", "id": staff_id}

# ============================================================
# --- CREATE / UPDATE / DELETE SERVICE USERS ---
# ============================================================
@app.post("/service-users")
def create_service_user(user: ServiceUserCreate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO service_user_details (
            unique_reference_code, first_name, last_name, date_of_birth, gender,
            rag_rating, nhs_number, start_date, end_date, primary_team,
            contact_number, contact_email, full_address, keysafe_code
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
    """, (
        user.unique_reference_code, user.first_name, user.last_name,
        user.date_of_birth, user.gender, user.rag_rating, user.nhs_number,
        user.start_date, user.end_date, user.primary_team, user.contact_number,
        user.contact_email, user.full_address, user.keysafe_code
    ))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Service user created successfully", "id": new_id}

@app.put("/service-users/{user_id}")
def update_service_user(user_id: int, user: ServiceUserCreate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE service_user_details
        SET unique_reference_code=%s, first_name=%s, last_name=%s, date_of_birth=%s,
            gender=%s, rag_rating=%s, nhs_number=%s, start_date=%s, end_date=%s,
            primary_team=%s, contact_number=%s, contact_email=%s, full_address=%s,
            keysafe_code=%s
        WHERE id=%s
        RETURNING id;
    """, (
        user.unique_reference_code, user.first_name, user.last_name, user.date_of_birth,
        user.gender, user.rag_rating, user.nhs_number, user.start_date, user.end_date,
        user.primary_team, user.contact_number, user.contact_email, user.full_address,
        user.keysafe_code, user_id
    ))
    updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not updated:
        raise HTTPException(status_code=404, detail="Service user not found")
    return {"message": "Service user updated successfully", "id": user_id}

@app.delete("/service-users/{user_id}")
def delete_service_user(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM service_user_details WHERE id=%s RETURNING id;", (user_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not deleted:
        raise HTTPException(status_code=404, detail="Service user not found")
    return {"message": "Service user deleted successfully", "id": user_id}

# ============================================================
# ✅ STAFF AVAILABILITY (CREATE/UPDATE + GET)
# ============================================================
class StaffAvailability(BaseModel):
    staff_id: int
    monday: bool = False
    tuesday: bool = False
    wednesday: bool = False
    thursday: bool = False
    friday: bool = False
    saturday: bool = False
    sunday: bool = False
    start_time: Optional[str] = None
    end_time: Optional[str] = None

@app.post("/staff-availability")
def add_staff_availability(avail: StaffAvailability):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO staff_availability (
            staff_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday, start_time, end_time
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (staff_id)
        DO UPDATE SET
            monday=EXCLUDED.monday, tuesday=EXCLUDED.tuesday, wednesday=EXCLUDED.wednesday,
            thursday=EXCLUDED.thursday, friday=EXCLUDED.friday, saturday=EXCLUDED.saturday, sunday=EXCLUDED.sunday,
            start_time=EXCLUDED.start_time, end_time=EXCLUDED.end_time
        RETURNING id;
    """, (
        avail.staff_id, avail.monday, avail.tuesday, avail.wednesday, avail.thursday,
        avail.friday, avail.saturday, avail.sunday, avail.start_time, avail.end_time
    ))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Availability saved successfully", "id": new_id}

@app.get("/staff-availability")
def get_staff_availability():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT sa.id, s.first_name, s.last_name, sa.monday, sa.tuesday, sa.wednesday, sa.thursday,
               sa.friday, sa.saturday, sa.sunday, sa.start_time, sa.end_time
        FROM staff_availability sa
        JOIN staff_details s ON sa.staff_id = s.id;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# ============================================================
# ✅ SERVICE USER ASSIGNMENTS (CREATE + GET)
# ============================================================
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import psycopg2

class AssignmentCreate(BaseModel):
    staff_id: int
    service_user_id: int
    assignment_date: str
    start_time: str
    end_time: str
    notes: Optional[str] = None


@app.post("/assignments")
def create_assignment(a: AssignmentCreate):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # --- Validate staff existence ---
        cur.execute("SELECT id FROM staff_details WHERE id = %s;", (a.staff_id,))
        if not cur.fetchone():
            raise HTTPException(status_code=400, detail=f"Staff ID {a.staff_id} does not exist")

        # --- Validate service user existence ---
        cur.execute("SELECT id FROM service_user_details WHERE id = %s;", (a.service_user_id,))
        if not cur.fetchone():
            raise HTTPException(status_code=400, detail=f"Service user ID {a.service_user_id} does not exist")

        # --- Prevent duplicate assignments (same user + same date) ---
        cur.execute("""
            SELECT id FROM service_user_assignments
            WHERE service_user_id = %s AND assignment_date = %s;
        """, (a.service_user_id, a.assignment_date))
        duplicate = cur.fetchone()

        if duplicate:
            raise HTTPException(
                status_code=409,  # Conflict
                detail=f"Service user ID {a.service_user_id} already has an assignment on {a.assignment_date}"
            )

        # --- Insert the new assignment ---
        cur.execute("""
            INSERT INTO service_user_assignments (
                staff_id, service_user_id, assignment_date, start_time, end_time, notes
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (a.staff_id, a.service_user_id, a.assignment_date, a.start_time, a.end_time, a.notes))

        new_id = cur.fetchone()[0]
        conn.commit()
        return {"message": "Assignment created successfully", "id": new_id}

    except HTTPException as e:
        conn.rollback()
        raise e

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cur.close()
        conn.close()


@app.get("/assignments")
def get_assignments():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            a.id,
            a.staff_id,
            a.service_user_id,
            s.first_name AS staff_first_name,
            s.last_name AS staff_last_name,
            su.first_name AS user_first_name,
            su.last_name AS user_last_name,
            a.assignment_date,
            a.start_time,
            a.end_time,
            a.notes
        FROM service_user_assignments a
        JOIN staff_details s ON a.staff_id = s.id
        JOIN service_user_details su ON a.service_user_id = su.id
        ORDER BY a.assignment_date DESC;
    """)
    columns = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(zip(columns, row)) for row in rows]




#........................................................
class ServiceUserNeed(BaseModel):
    service_user_id: int
    care_type: str
    description: Optional[str] = None
    frequency: Optional[str] = None
    preferred_time: Optional[str] = None
    duration_minutes: Optional[int] = None
    active: bool = True


@app.post("/service-user-needs")
def add_service_user_need(need: ServiceUserNeed):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO service_user_needs (
            service_user_id, care_type, description, frequency,
            preferred_time, duration_minutes, active
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        RETURNING id;
    """, (
        need.service_user_id, need.care_type, need.description,
        need.frequency, need.preferred_time, need.duration_minutes, need.active
    ))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Need added successfully", "id": new_id}


@app.get("/service-user-needs")
def get_service_user_needs():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT n.id, n.care_type, n.description, n.frequency,
               n.preferred_time, n.duration_minutes, n.active,
               su.first_name, su.last_name
        FROM service_user_needs n
        JOIN service_user_details su ON n.service_user_id = su.id;
    """)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return [dict(zip(columns, row)) for row in rows]
