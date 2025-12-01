"""Check and update database schema"""
from core.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    # Check room table columns
    result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'room'"))
    room_cols = [row[0] for row in result]
    print("Room table columns:", room_cols)
    
    # Check if admin_id exists in room (already added above)
    if 'admin_id' not in room_cols:
        print("Adding admin_id to room...")
        conn.execute(text("ALTER TABLE room ADD COLUMN admin_id INTEGER REFERENCES adminstaff(admin_id) ON DELETE CASCADE"))
        conn.commit()
    
    # Check groupclass table - missing admin_id
    result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'groupclass'"))
    groupclass_cols = [row[0] for row in result]
    print("\nGroupclass table columns:", groupclass_cols)
    
    if 'admin_id' not in groupclass_cols:
        print("Adding admin_id to groupclass...")
        conn.execute(text("ALTER TABLE groupclass ADD COLUMN admin_id INTEGER REFERENCES adminstaff(admin_id) ON DELETE CASCADE"))
        conn.commit()
    
    # Check maintenancerecord table - missing admin_id  
    result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'maintenancerecord'"))
    maint_cols = [row[0] for row in result]
    print("\nMaintenancerecord table columns:", maint_cols)
    
    if 'admin_id' not in maint_cols:
        print("Adding admin_id to maintenancerecord...")
        conn.execute(text("ALTER TABLE maintenancerecord ADD COLUMN admin_id INTEGER REFERENCES adminstaff(admin_id) ON DELETE CASCADE"))
        conn.commit()

    # Update foreign key constraints to add CASCADE for existing FKs
    print("\nUpdating foreign key constraints for CASCADE delete...")
    
    # Drop and recreate constraints with CASCADE
    cascade_updates = [
        # Room -> Admin (already has CASCADE from our addition)
        # Equipment -> Room
        ("equipment", "equipment_room_id_fkey", "room_id", "room", "room_id"),
        # MaintenanceRecord -> Equipment
        ("maintenancerecord", "maintenancerecord_equipment_id_fkey", "equipment_id", "equipment", "equipment_id"),
        # GroupClass -> Room
        ("groupclass", "groupclass_room_id_fkey", "room_id", "room", "room_id"),
        # GroupClass -> Trainer (keep this, not admin related)
        # ClassRegistration -> GroupClass
        ("classregistration", "classregistration_class_id_fkey", "class_id", "groupclass", "class_id"),
    ]
    
    for table, constraint, col, ref_table, ref_col in cascade_updates:
        try:
            # Check if constraint exists
            result = conn.execute(text(f"SELECT constraint_name FROM information_schema.table_constraints WHERE table_name = '{table}' AND constraint_name = '{constraint}'"))
            if result.fetchone():
                print(f"Updating {constraint}...")
                conn.execute(text(f"ALTER TABLE {table} DROP CONSTRAINT {constraint}"))
                conn.execute(text(f"ALTER TABLE {table} ADD CONSTRAINT {constraint} FOREIGN KEY ({col}) REFERENCES {ref_table}({ref_col}) ON DELETE CASCADE"))
                conn.commit()
        except Exception as e:
            print(f"Could not update {constraint}: {e}")
            conn.rollback()

print("\nDatabase schema updated!")

