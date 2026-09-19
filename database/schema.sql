--assessment data base Felipe Abroad move consulting

-- Drop in reverse dependency order so the script can be re-run safely
DROP TABLE IF EXISTS payments   CASCADE;
DROP TABLE IF EXISTS bookings   CASCADE;
DROP TABLE IF EXISTS clients    CASCADE;
DROP TABLE IF EXISTS services   CASCADE;
DROP TABLE IF EXISTS move_types CASCADE;


-- move_types: how they are join in Ireland
CREATE TABLE move_types (
    id           SERIAL PRIMARY KEY,
    name         VARCHAR(100) NOT NULL UNIQUE,
    description  TEXT
);

-- clients: who hire the consultancy
CREATE TABLE clients (
    id                 SERIAL PRIMARY KEY,
    full_name          VARCHAR(120) NOT NULL,
    email              VARCHAR(255) NOT NULL UNIQUE,
    phone              VARCHAR(30),
    country_of_origin  VARCHAR(80)  NOT NULL DEFAULT 'Brazil',
    move_type_id       INTEGER      NOT NULL
                       REFERENCES move_types(id) ON DELETE RESTRICT,
    created_at         TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- services: our services
CREATE TABLE services (
    id                SERIAL PRIMARY KEY,
    name              VARCHAR(100)  NOT NULL UNIQUE,
    description       TEXT,
    price             NUMERIC(8,2)  NOT NULL CHECK (price >= 0),
    duration_minutes  INTEGER       CHECK (duration_minutes > 0),
    is_active         BOOLEAN       NOT NULL DEFAULT TRUE
);

-- bookings: schedules, in case remove a cliente remove also his schedule
CREATE TABLE bookings (
    id            SERIAL PRIMARY KEY,
    client_id     INTEGER      NOT NULL
                  REFERENCES clients(id)  ON DELETE CASCADE,
    service_id    INTEGER      NOT NULL
                  REFERENCES services(id) ON DELETE RESTRICT,
    scheduled_at  TIMESTAMP    NOT NULL,
    status        VARCHAR(20)  NOT NULL DEFAULT 'scheduled'
                  CHECK (status IN ('scheduled', 'completed', 'cancelled')),
    notes         TEXT,
    created_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- payments: one booking can have more than one payment, bacause they don't need to pay full at once.
CREATE TABLE payments (
    id          SERIAL PRIMARY KEY,
    booking_id  INTEGER       NOT NULL
                REFERENCES bookings(id) ON DELETE CASCADE,
    amount      NUMERIC(8,2)  NOT NULL CHECK (amount > 0),
    method      VARCHAR(20)   NOT NULL
                CHECK (method IN ('card', 'bank_transfer', 'cash', 'paypal')),
    status      VARCHAR(20)   NOT NULL DEFAULT 'pending'
                CHECK (status IN ('pending', 'paid')),
    paid_at     TIMESTAMP,
    CONSTRAINT paid_at_matches_status CHECK (
        (status = 'paid'    AND paid_at IS NOT NULL) OR
        (status = 'pending' AND paid_at IS NULL)
    )
);

-- Indexes on foreign keys (speed up joins and lookups)
CREATE INDEX idx_clients_move_type   ON clients(move_type_id);
CREATE INDEX idx_bookings_client     ON bookings(client_id);
CREATE INDEX idx_bookings_service    ON bookings(service_id);
CREATE INDEX idx_payments_booking    ON payments(booking_id);

-- This are the options they will have on the form
INSERT INTO move_types (name, description) VALUES
    ('Student',        'Moving to Ireland to study English or a course (Stamp 2).'),
    ('Work Visa',      'Moving with a job offer or a work permit.'),
    ('EU Passport',    'Moving with a European passport, no visa needed.'),
    ('Partner Visa',   'Moving as the partner of an EU citizen.');

INSERT INTO services (name, description, price, duration_minutes) VALUES
    ('Complete Consultancy', 'Full support from planning to the first weeks in Ireland.', 350.00, NULL),
    ('Basic Consultancy',    'One-hour meeting to answer your questions and plan the move.', 60.00, 60),
    ('CV Review',            'Review and adapt your CV to the Irish job market.', 40.00, 45),
    ('Housing Support',      'Help searching for accommodation and understanding renting in Ireland.', 80.00, 60);



