/*Use  the sql file to populate the static information*/
PRAGMA foreign_keys = ON;

INSERT OR IGNORE INTO bow_types(id, bow_type) VALUES 
    ('bt_recurve', 'Recurve'),
    ('bt_eng_long_bow', 'English Long Bow'),
    ('bt_bare_bow', 'Bare Bow'),
    ('bt_full_length_yumi', 'Full LEngth Yumi');   

INSERT OR IGNORE INTO round_types(
    id, round_type_name, bow_type, indoor_outdoor, face_diameter,
    distance_unit, distance, total_shots, number_of_ends,shots_per_ends
) VALUES
    ('rt_portmounth_recurve', 'Portmouth Recurve', 'bt_recurve', 0, 120,'meter',20,60, 20,3),
    ('rt_portmounth_longbow', 'Portmouth Longbow', 'bt_eng_long_bow', 0, 120, 'meter',20,60, 20,3),
    ('rt_portmounth_barebow', 'Portmouth Barebow', 'bt_bare_bow', 0, 120, 'meter', 20,60, 20,3);
