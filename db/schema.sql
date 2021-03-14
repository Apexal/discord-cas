SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: clients; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.clients (
    client_id integer NOT NULL,
    is_enabled boolean DEFAULT true NOT NULL,
    name character varying NOT NULL,
    welcome_message text,
    discord_server_id integer NOT NULL,
    discord_rpi_role_id integer NOT NULL,
    discord_non_rpi_role_id integer,
    contact_information character varying,
    is_rcs_id_in_nickname boolean DEFAULT true NOT NULL,
    is_public boolean DEFAULT false NOT NULL
);


--
-- Name: COLUMN clients.is_enabled; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.clients.is_enabled IS 'Whether users can currently join through this portal';


--
-- Name: COLUMN clients.name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.clients.name IS 'Public-facing name';


--
-- Name: COLUMN clients.welcome_message; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.clients.welcome_message IS 'Optional display message on client page';


--
-- Name: COLUMN clients.discord_server_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.clients.discord_server_id IS 'Unique ID of Discord server for client';


--
-- Name: COLUMN clients.discord_rpi_role_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.clients.discord_rpi_role_id IS 'Unique ID of role on Discord server for client to give to external (non-RPI) users';


--
-- Name: COLUMN clients.contact_information; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.clients.contact_information IS 'Who to reach out to about the client';


--
-- Name: COLUMN clients.is_rcs_id_in_nickname; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.clients.is_rcs_id_in_nickname IS 'Whether or not member nicknames in client servers should include RCS IDs';


--
-- Name: COLUMN clients.is_public; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.clients.is_public IS 'Whether the server of the client shows on a listing for all users';


--
-- Name: clients_client_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.clients_client_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: clients_client_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.clients_client_id_seq OWNED BY public.clients.client_id;


--
-- Name: schema_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.schema_migrations (
    version character varying(255) NOT NULL
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    rcs_id character varying NOT NULL,
    first_name character varying NOT NULL,
    last_name character varying NOT NULL,
    graduation_year integer,
    discord_user_id integer
);


--
-- Name: COLUMN users.rcs_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users.rcs_id IS 'RPI username of user from CAS';


--
-- Name: COLUMN users.first_name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users.first_name IS 'Given name of user';


--
-- Name: COLUMN users.last_name; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users.last_name IS 'Family name of user';


--
-- Name: COLUMN users.graduation_year; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users.graduation_year IS 'Null for non-students hopefully';


--
-- Name: COLUMN users.discord_user_id; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON COLUMN public.users.discord_user_id IS 'Unique ID of Discord user once connected';


--
-- Name: clients client_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.clients ALTER COLUMN client_id SET DEFAULT nextval('public.clients_client_id_seq'::regclass);


--
-- Name: clients clients_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.clients
    ADD CONSTRAINT clients_pkey PRIMARY KEY (client_id);


--
-- Name: schema_migrations schema_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.schema_migrations
    ADD CONSTRAINT schema_migrations_pkey PRIMARY KEY (version);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (rcs_id);


--
-- PostgreSQL database dump complete
--


--
-- Dbmate schema migrations
--

INSERT INTO public.schema_migrations (version) VALUES
    ('20210314032059'),
    ('20210314032749');
