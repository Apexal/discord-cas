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
    ('20210314032059');
