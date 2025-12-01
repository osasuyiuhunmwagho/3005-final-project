"""Update database foreign key constraints to use CASCADE DELETE"""
from core.database import engine
from sqlalchemy import text

# All foreign key constraints that need CASCADE DELETE
constraints = [
    # (table, constraint_name, column, ref_table, ref_column)
    ("room", "room_admin_id_fkey", "admin_id", "adminstaff", "admin_id"),
    ("equipment", "equipment_room_id_fkey", "room_id", "room", "room_id"),
    ("fitnessgoal", "fitnessgoal_member_id_fkey", "member_id", "member", "member_id"),
    ("healthmetric", "healthmetric_member_id_fkey", "member_id", "member", "member_id"),
    ("traineravailability", "traineravailability_trainer_id_fkey", "trainer_id", "trainer", "trainer_id"),
    ("groupclass", "groupclass_trainer_id_fkey", "trainer_id", "trainer", "trainer_id"),
    ("groupclass", "groupclass_room_id_fkey", "room_id", "room", "room_id"),
    ("groupclass", "groupclass_admin_id_fkey", "admin_id", "adminstaff", "admin_id"),
    ("classregistration", "classregistration_member_id_fkey", "member_id", "member", "member_id"),
    ("classregistration", "classregistration_class_id_fkey", "class_id", "groupclass", "class_id"),
    ("personaltrainingsession", "personaltrainingsession_member_id_fkey", "member_id", "member", "member_id"),
    ("personaltrainingsession", "personaltrainingsession_trainer_id_fkey", "trainer_id", "trainer", "trainer_id"),
    ("personaltrainingsession", "personaltrainingsession_room_id_fkey", "room_id", "room", "room_id"),
    ("maintenancerecord", "maintenancerecord_equipment_id_fkey", "equipment_id", "equipment", "equipment_id"),
    ("maintenancerecord", "maintenancerecord_admin_id_fkey", "admin_id", "adminstaff", "admin_id"),
]

with engine.connect() as conn:
    for table, constraint, col, ref_table, ref_col in constraints:
        try:
            # Check if constraint exists
            result = conn.execute(text(
                f"SELECT constraint_name FROM information_schema.table_constraints "
                f"WHERE table_name = '{table}' AND constraint_type = 'FOREIGN KEY'"
            ))
            existing_constraints = [row[0] for row in result]
            
            if constraint in existing_constraints:
                print(f"Updating {constraint}...")
                conn.execute(text(f"ALTER TABLE {table} DROP CONSTRAINT {constraint}"))
                conn.execute(text(
                    f"ALTER TABLE {table} ADD CONSTRAINT {constraint} "
                    f"FOREIGN KEY ({col}) REFERENCES {ref_table}({ref_col}) ON DELETE CASCADE"
                ))
                conn.commit()
                print(f"  ✓ Updated {constraint} with CASCADE DELETE")
            else:
                # Try to add if it doesn't exist
                print(f"Adding {constraint}...")
                try:
                    conn.execute(text(
                        f"ALTER TABLE {table} ADD CONSTRAINT {constraint} "
                        f"FOREIGN KEY ({col}) REFERENCES {ref_table}({ref_col}) ON DELETE CASCADE"
                    ))
                    conn.commit()
                    print(f"  ✓ Added {constraint} with CASCADE DELETE")
                except Exception as add_e:
                    print(f"  ✗ Could not add {constraint}: {add_e}")
                    conn.rollback()
        except Exception as e:
            print(f"  ✗ Error with {constraint}: {e}")
            conn.rollback()

print("\n✓ Database constraints updated!")
