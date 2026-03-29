
import uuid
from . import db
from flask import current_app 
def seed_db_static_information():
    try:
        data_base = db.get_db()
        with current_app.open_resource("seed.sql") as f :
            data_base.executescript(f.read().decode("utf8"))
        print("start seeding static tables")
    except:

        return "Failed to Seed the Static Part of the Database"

    return "Seed the Static Part of the Database Successful"


def seed_db_user_related_data():
    data_base = db.get_db()

    user_id_tony = str(uuid.uuid4())
    user_id_wini = str(uuid.uuid4())
    user_id_goblin = str(uuid.uuid4())

    user_bow_type_1 = str(uuid.uuid4())
    user_bow_type_2 = str(uuid.uuid4())
    user_bow_type_3 = str(uuid.uuid4())
    user_bow_type_4 = str(uuid.uuid4())
    user_bow_type_5 = str(uuid.uuid4())
    user_bow_type_6 = str(uuid.uuid4())

    user_round_id = str(uuid.uuid4())

    end1 = str(uuid.uuid4())
    end2 = str(uuid.uuid4())
    user_arrow_id_1 = str(uuid.uuid4())
    user_arrow_id_2 = str(uuid.uuid4())
    user_arrow_id_3 = str(uuid.uuid4())
    try:
        
        rows_users = [
            (user_id_tony, "tonyAdmin", "test_password", '2026-02-28T14:30:05Z', 0,0,0,'2026-03-28T14:30:05Z',1),
            (user_id_wini, "winni_test_acc", "test_password_2", '2026-02-28T14:30:05Z', 1,1,0,'2026-03-28T14:30:05Z',1),
            (user_id_goblin, "goblin_test_accm", "test_goblin", '22026-02-28T14:30:05Z', 1,0,0,'2026-03-28T14:30:05Z',1)
        ]
        data_base.executemany("INSERT INTO users(id,username,password,creation_date,role,gender,left_right_handed) VALUES(?,?,?,?,?,?,?,?,?)",
                rows_users
        )
        data_base.commit()
    except Exception as e:
        print("Seeding User Failed", e)
        return "Failed to Seed the User Table of the Database"
    

    try:
        
        rows_user_bow_type=[
            (user_bow_type_1, 26, 0,"afterbunner", "carbon_alu", 12, 180, 'bt_recurve', user_id_tony ),
            (user_bow_type_2, 26, 0,"firetruck", "carbon_alu", 12, 180, 'bt_recurve', user_id_wini ),
            (user_bow_type_3, 26, 0,"mylongbow", "wood", 12, 180, 'bt_eng_long_bow', user_id_tony ),
            (user_bow_type_4, 26, 0,"japneselongbow", "wood", 12, 180, 'bt_full_length_yumi', user_id_tony ),
            (user_bow_type_5, 26, 0,"alcoholicarcher", "carbon_alu", 12, 180, 'bt_bare_bow', user_id_goblin ),
            (user_bow_type_6, 26, 0,"firetruck_b", "carbon_alu", 12, 180, 'bt_bare_bow', user_id_wini ),
        ]
        data_base.executemany("INSERT INTO user_bow_types(id, poundage, left_right_hand, bow_name, arrow_material_type, arrow_length, bow_length, bow_type_id, user_id) VALUES(?,?,?,?,?,?,?,?,?)",            
                rows_user_bow_type
                )
        data_base.commit()
    except Exception as e:
        print("Seeding User Bow Type  Recording Failed", e)
        return "Failed to Seed the User Bow Type Table of the Database"

    try:
        
        rows_user_round_recording =[
            (user_round_id, 180, 20, 60, '2026-02-29T14:30:05Z', '2026-02-29T14:45:05Z', '2026-02-28', user_id_tony, user_bow_type_1, 'rt_portmounth_recurve'  )
        ]
        data_base.executemany("INSERT INTO round_recordings(id, round_score, ends_count, arrow_count, startTime, endTime, date, user_id, user_bow_id, user_round_type_id) VALUES(?,?,?,?,?,?,?,?,?,?)",            
                rows_user_round_recording
                )
        data_base.commit()
    except Exception as e:
        print("Seeding Round Recording Failed", e)
        return "Failed to Seed the User Round Table of the Database"

    
    try:
        
        rows_ends = [
            (end1, 1, 28, 3, "2026-02-29T14:31:05Z", user_id_tony, user_round_id),
            (end2, 2, 30, 3, "2026-02-29T14:33:05Z", user_id_tony, user_round_id),
        ]
        data_base.executemany(
            "INSERT INTO ends_recording(id, sequence_of_end_in_round, end_score, arrow_count, end_record_completion_time_stamp, user_id, user_round_id) "
            "VALUES(?,?,?,?,?,?,?)",
            rows_ends,
        )
        data_base.commit()
    except Exception as e:
        print("Seeding End Recording Failed", e)
        return "Failed to Seed the User Ends Table of the Database"
    

    try:

        user_arrow_recording = [
            (user_arrow_id_1, 1, 10, user_id_tony, end1),
            (user_arrow_id_2, 2, 10, user_id_tony, end1),
            (user_arrow_id_3, 3, 10, user_id_tony, end1)
        ]
        data_base.executemany("INSERT INTO arrow_recordings(id, sequence_of_arrow_in_ends, arrow_score, user_id, ends_recording_id) VALUES(?,?,?,?,?)",                           
                user_arrow_recording
                )
        data_base.commit()
    except Exception as e:
        print("Seeding Arrow  Recording Failed", e)
        return "Failed to Seed the User Ends Table of the Database"
    


    return "Seed the All Table of the Database Successful"
if (__name__ == "__main__"):
    pass