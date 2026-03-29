
PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS arrow_recordings;
DROP TABLE IF EXISTS ends_recordings;
DROP TABLE IF EXISTS round_recordings;
DROP TABLE IF EXISTS user_bow_types;
DROP TABLE IF EXISTS round_types;

DROP TABLE IF EXISTS bow_types;
DROP TABLE IF EXISTS users;
PRAGMA foreign_keys = ON;

/*0 for Admin, 1 for regular user */
/*0 for Female,1 for Male, 2 for other, 3 none-specify*/
/*0 for left hand and 1 for right hand */
/*0 for is active, 1 for not active*/
CREATE TABLE users(
    id TEXT PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    creation_date TEXT NOT NULL,
    role INTEGER  NOT NULL,
    gender INTEGER NOT NULL,
    left_right_handed INTEGER NOT NULL,
    updated_at TEXT,
    is_activity INTEGER  NOT NULL
);
CREATE TABLE sessions(
    uuid TEXT  PRIMARY KEY,
    session_id TEXT NOT NULL UNIQUE,
    user_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    expires_at  TEXT NOT NULL,
    isValid   INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
)

CREATE TABLE bow_types(
    id TEXT PRIMARY KEY,
    bow_type TEXT UNIQUE NOT NULL
);

CREATE TABLE user_bow_types(
    id TEXT PRIMARY KEY,
    poundage INTEGER NOT NULL,
    left_right_hand INTEGER NOT NULL,
    bow_name TEXT,
    arrow_material_type TEXT NOT NULL,
    arrow_length REAL,
    bow_length REAL,
    bow_type_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (bow_type_id) REFERENCES  bow_types(id)
);

/*0 for indoor 1 for outdoor*/
CREATE TABLE round_types(
    id TEXT PRIMARY KEY,
    round_type_name TEXT NOT NULL,
    bow_type TEXT NOT NULL,
    indoor_outdoor INTEGER NOT NULL,
    face_diameter REAL NOT NULL,
    distance_unit  TEXT NOT NULL,
    distance REAL NOT NULL,
    total_shots INTEGER  NOT NULL,
    number_of_ends INTEGER,
    shots_per_ends INTEGER
);

/*Round Recording Contains Multiple Instance of Ends*/
/*Ends contain multiple arrow shots */
/*0 for completed rounds 1 non-completed rounds*/
CREATE TABLE round_recordings(
    id TEXT PRIMARY KEY,
    round_score INTEGER NOT NULL,
    ends_count INTEGER NOT NULL,
    arrow_count INTEGER NOT NULL,
    startTime TEXT NOT NULL,
    endTime  TEXT NOT NULL,
    date TEXT NOT NULL,
    user_id TEXT NOT NULL,
    user_bow_id TEXT NOT NULL,
    user_round_type_id TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (user_bow_id) REFERENCES user_bow_types(id),
    FOREIGN KEY (user_round_type_id) REFERENCES round_types(id) 
);

CREATE TABLE ends_recording(
    id TEXT PRIMARY KEY,
    sequence_of_end_in_round INTEGER NOT NULL,
    end_score INTEGER NOT NULL,
    arrow_count  INTEGER NOT NULL,
    end_record_completion_time_stamp TEXT NOT NULL, 
    user_id TEXT NOT NULL,
    user_round_id TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (user_round_id) REFERENCES round_recordings(id)
);
CREATE TABLE arrow_recordings(
    id TEXT PRIMARY KEY,
    sequence_of_arrow_in_ends INTEGER,
    arrow_score INTEGER NOT NULL,
    user_id TEXT NOT NULL,
    ends_recording_id  TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (ends_recording_id) REFERENCES ends_recording(id)
);
