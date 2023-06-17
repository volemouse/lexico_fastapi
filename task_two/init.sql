CREATE TABLE public.short_names (
    name VARCHAR(255) NOT NULL,
    status INTEGER NOT NULL
);

CREATE TABLE public.full_names (
    name VARCHAR(255) NOT NULL,
    status INTEGER
);

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;