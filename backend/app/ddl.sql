-- ENUM types
CREATE TYPE chat_room_type AS ENUM ('group_chat', 'direct_message'); 
CREATE TYPE announcement_type AS ENUM ('general', 'leaks');

-- Classes
CREATE TABLE classes (
    id SERIAL PRIMARY KEY,
    speciality TEXT,
    major TEXT,
    group_name TEXT,
    generation TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Subjects
CREATE TABLE subjects (
    id SERIAL PRIMARY KEY,
    class_id INT REFERENCES classes(id) ON DELETE SET NULL,
    name TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT UNIQUE,
    password TEXT NOT NULL,
    avatar_url TEXT,
    class_id INT REFERENCES classes(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Chat Rooms
CREATE TABLE chat_rooms (
    id SERIAL PRIMARY KEY,
    chat_room_type chat_room_type NOT NULL,
    chat_room_name TEXT,
    avatar_url TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Chat Room Members
CREATE TABLE chat_room_members (
    id SERIAL PRIMARY KEY,
    chat_room_id INT REFERENCES chat_rooms(id) ON DELETE SET NULL,
    user_id INT REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Chats
CREATE TABLE chats (
    id SERIAL PRIMARY KEY,
    chat_room_id INT REFERENCES chat_rooms(id) ON DELETE SET NULL,
    user_id INT REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Assignments
CREATE TABLE assignments (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE SET NULL,
    subject_id INT REFERENCES subjects(id) ON DELETE SET NULL,
    class_id INT REFERENCES classes(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Assignment Replies
CREATE TABLE assignment_replies (
    id SERIAL PRIMARY KEY,
    assignment_id INT REFERENCES assignments(id) ON DELETE SET NULL,
    user_id INT REFERENCES users(id) ON DELETE SET NULL,
    up_vote INT DEFAULT 0,
    down_vote INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Announcements
CREATE TABLE announcements (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE SET NULL,
    class_id INT REFERENCES classes(id) ON DELETE SET NULL,
    type announcement_type NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Schedules
CREATE TABLE schedules (
    id SERIAL PRIMARY KEY,
    class_id INT REFERENCES classes(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Content tables
CREATE TABLE schedule_contents (
    id SERIAL PRIMARY KEY,
    text text,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE chat_contents (
    id SERIAL PRIMARY KEY
    text text,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE assignment_contents (
    id SERIAL PRIMARY KEY,
    text text,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE assignment_reply_contents (
    id SERIAL PRIMARY KEY,
    text text,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE announcement_contents (
    id SERIAL PRIMARY KEY
    text text,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Media table
CREATE TABLE medias (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    chat_id INT REFERENCES chat_contents(id) ON DELETE SET NULL,
    schedule_id INT REFERENCES schedule_contents(id) ON DELETE SET NULL,
    announcement_id INT REFERENCES announcement_contents(id) ON DELETE SET NULL,
    assignment_id INT REFERENCES assignment_contents(id) ON DELETE SET NULL,
    assignment_reply_id INT REFERENCES assignment_reply_contents(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT now(),  
    upadated_at TIMESTAMP DEFAULT now()
);