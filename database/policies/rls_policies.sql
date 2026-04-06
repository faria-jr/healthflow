-- HealthFlow RLS Policies for Supabase
-- Execute this in Supabase SQL Editor after running migrations

-- ============================================
-- PATIENTS TABLE POLICIES
-- ============================================

-- Enable RLS
ALTER TABLE patients ENABLE ROW LEVEL SECURITY;

-- Policy: Users can view their own patient record
CREATE POLICY patients_select_own ON patients
    FOR SELECT
    TO authenticated
    USING (user_id = auth.uid());

-- Policy: Doctors can view their patients' records
CREATE POLICY patients_select_doctor ON patients
    FOR SELECT
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM appointments
            WHERE appointments.patient_id = patients.id
            AND appointments.doctor_id IN (
                SELECT id FROM doctors WHERE user_id = auth.uid()
            )
        )
    );

-- Policy: Admins can view all patients
CREATE POLICY patients_select_admin ON patients
    FOR SELECT
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM auth.users
            WHERE auth.users.id = auth.uid()
            AND auth.users.raw_user_meta_data->>'role' = 'admin'
        )
    );

-- Policy: Users can insert their own patient record
CREATE POLICY patients_insert_own ON patients
    FOR INSERT
    TO authenticated
    WITH CHECK (user_id = auth.uid());

-- Policy: Users can update their own patient record
CREATE POLICY patients_update_own ON patients
    FOR UPDATE
    TO authenticated
    USING (user_id = auth.uid())
    WITH CHECK (user_id = auth.uid());

-- Policy: Admins can update any patient
CREATE POLICY patients_update_admin ON patients
    FOR UPDATE
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM auth.users
            WHERE auth.users.id = auth.uid()
            AND auth.users.raw_user_meta_data->>'role' = 'admin'
        )
    );

-- ============================================
-- DOCTORS TABLE POLICIES
-- ============================================

-- Enable RLS
ALTER TABLE doctors ENABLE ROW LEVEL SECURITY;

-- Policy: Anyone can view active doctors (public)
CREATE POLICY doctors_select_public ON doctors
    FOR SELECT
    TO authenticated
    USING (is_active = true);

-- Policy: Doctors can view their own full record
CREATE POLICY doctors_select_own ON doctors
    FOR SELECT
    TO authenticated
    USING (user_id = auth.uid());

-- Policy: Admins can view all doctors
CREATE POLICY doctors_select_admin ON doctors
    FOR SELECT
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM auth.users
            WHERE auth.users.id = auth.uid()
            AND auth.users.raw_user_meta_data->>'role' = 'admin'
        )
    );

-- Policy: Users can become doctors (insert their own record)
CREATE POLICY doctors_insert_own ON doctors
    FOR INSERT
    TO authenticated
    WITH CHECK (user_id = auth.uid());

-- Policy: Doctors can update their own record
CREATE POLICY doctors_update_own ON doctors
    FOR UPDATE
    TO authenticated
    USING (user_id = auth.uid())
    WITH CHECK (user_id = auth.uid());

-- Policy: Admins can update any doctor
CREATE POLICY doctors_update_admin ON doctors
    FOR UPDATE
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM auth.users
            WHERE auth.users.id = auth.uid()
            AND auth.users.raw_user_meta_data->>'role' = 'admin'
        )
    );

-- ============================================
-- APPOINTMENTS TABLE POLICIES
-- ============================================

-- Enable RLS
ALTER TABLE appointments ENABLE ROW LEVEL SECURITY;

-- Policy: Patients can view their own appointments
CREATE POLICY appointments_select_patient ON appointments
    FOR SELECT
    TO authenticated
    USING (
        patient_id IN (
            SELECT id FROM patients WHERE user_id = auth.uid()
        )
    );

-- Policy: Doctors can view their own appointments
CREATE POLICY appointments_select_doctor ON appointments
    FOR SELECT
    TO authenticated
    USING (
        doctor_id IN (
            SELECT id FROM doctors WHERE user_id = auth.uid()
        )
    );

-- Policy: Admins can view all appointments
CREATE POLICY appointments_select_admin ON appointments
    FOR SELECT
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM auth.users
            WHERE auth.users.id = auth.uid()
            AND auth.users.raw_user_meta_data->>'role' = 'admin'
        )
    );

-- Policy: Patients can create appointments for themselves
CREATE POLICY appointments_insert_patient ON appointments
    FOR INSERT
    TO authenticated
    WITH CHECK (
        patient_id IN (
            SELECT id FROM patients WHERE user_id = auth.uid()
        )
    );

-- Policy: Patients can update their own appointments (cancel)
CREATE POLICY appointments_update_patient ON appointments
    FOR UPDATE
    TO authenticated
    USING (
        patient_id IN (
            SELECT id FROM patients WHERE user_id = auth.uid()
        )
    );

-- Policy: Doctors can update their own appointments
CREATE POLICY appointments_update_doctor ON appointments
    FOR UPDATE
    TO authenticated
    USING (
        doctor_id IN (
            SELECT id FROM doctors WHERE user_id = auth.uid()
        )
    );

-- Policy: Admins can update any appointment
CREATE POLICY appointments_update_admin ON appointments
    FOR UPDATE
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM auth.users
            WHERE auth.users.id = auth.uid()
            AND auth.users.raw_user_meta_data->>'role' = 'admin'
        )
    );

-- ============================================
-- MEDICAL RECORDS TABLE POLICIES
-- ============================================

-- Enable RLS
ALTER TABLE medical_records ENABLE ROW LEVEL SECURITY;

-- Policy: Patients can view their own medical records
CREATE POLICY medical_records_select_patient ON medical_records
    FOR SELECT
    TO authenticated
    USING (
        patient_id IN (
            SELECT id FROM patients WHERE user_id = auth.uid()
        )
    );

-- Policy: Doctors can view records of their patients
CREATE POLICY medical_records_select_doctor ON medical_records
    FOR SELECT
    TO authenticated
    USING (
        doctor_id IN (
            SELECT id FROM doctors WHERE user_id = auth.uid()
        )
    );

-- Policy: Admins can view all medical records
CREATE POLICY medical_records_select_admin ON medical_records
    FOR SELECT
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM auth.users
            WHERE auth.users.id = auth.uid()
            AND auth.users.raw_user_meta_data->>'role' = 'admin'
        )
    );

-- Policy: Doctors can create medical records for their appointments
CREATE POLICY medical_records_insert_doctor ON medical_records
    FOR INSERT
    TO authenticated
    WITH CHECK (
        doctor_id IN (
            SELECT id FROM doctors WHERE user_id = auth.uid()
        )
        AND
        EXISTS (
            SELECT 1 FROM appointments
            WHERE appointments.id = medical_records.appointment_id
            AND appointments.doctor_id = medical_records.doctor_id
            AND appointments.status = 'completed'
        )
    );

-- Policy: Doctors can update their own medical records
CREATE POLICY medical_records_update_doctor ON medical_records
    FOR UPDATE
    TO authenticated
    USING (
        doctor_id IN (
            SELECT id FROM doctors WHERE user_id = auth.uid()
        )
    );

-- Policy: Admins can update any medical record
CREATE POLICY medical_records_update_admin ON medical_records
    FOR UPDATE
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM auth.users
            WHERE auth.users.id