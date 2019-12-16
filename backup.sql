--
-- PostgreSQL database cluster dump
--

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Drop databases
--

DROP DATABASE "ordina-pubquiz";




--
-- Drop roles
--

DROP ROLE postgres;


--
-- Roles
--

CREATE ROLE postgres;
ALTER ROLE postgres WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS PASSWORD 'md532e12f215ba27cb750c9e093ce4b5127';






--
-- Database creation
--

CREATE DATABASE "ordina-pubquiz" WITH TEMPLATE = template0 OWNER = postgres;
REVOKE CONNECT,TEMPORARY ON DATABASE template1 FROM PUBLIC;
GRANT CONNECT ON DATABASE template1 TO PUBLIC;


\connect -reuse-previous=on "dbname='ordina-pubquiz'"

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.2
-- Dumped by pg_dump version 9.6.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE alembic_version OWNER TO postgres;

--
-- Name: answersheet; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE answersheet (
    id integer NOT NULL,
    answersheet_image bytea,
    image_width integer,
    image_height integer,
    team_id integer NOT NULL
);


ALTER TABLE answersheet OWNER TO postgres;

--
-- Name: answersheet_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE answersheet_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE answersheet_id_seq OWNER TO postgres;

--
-- Name: answersheet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE answersheet_id_seq OWNED BY answersheet.id;


--
-- Name: answersheetquestion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE answersheetquestion (
    id integer NOT NULL,
    answersheet_id integer,
    question_id integer
);


ALTER TABLE answersheetquestion OWNER TO postgres;

--
-- Name: answersheetquestion_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE answersheetquestion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE answersheetquestion_id_seq OWNER TO postgres;

--
-- Name: answersheetquestion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE answersheetquestion_id_seq OWNED BY answersheetquestion.id;


--
-- Name: category; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE category (
    id integer NOT NULL,
    name character varying(255)
);


ALTER TABLE category OWNER TO postgres;

--
-- Name: category_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE category_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE category_id_seq OWNER TO postgres;

--
-- Name: category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE category_id_seq OWNED BY category.id;


--
-- Name: line; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE line (
    id integer NOT NULL,
    answersheet_id integer,
    line_image bytea,
    image_width integer,
    image_height integer
);


ALTER TABLE line OWNER TO postgres;

--
-- Name: line_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE line_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE line_id_seq OWNER TO postgres;

--
-- Name: line_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE line_id_seq OWNED BY line.id;


--
-- Name: person; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE person (
    id integer NOT NULL,
    personname character varying(255)
);


ALTER TABLE person OWNER TO postgres;

--
-- Name: person_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE person_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE person_id_seq OWNER TO postgres;

--
-- Name: person_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE person_id_seq OWNED BY person.id;


--
-- Name: question; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE question (
    id integer NOT NULL,
    person_id integer,
    category_id integer,
    question character varying(255),
    active boolean,
    questionnumber integer
);


ALTER TABLE question OWNER TO postgres;

--
-- Name: question_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE question_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE question_id_seq OWNER TO postgres;

--
-- Name: question_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE question_id_seq OWNED BY question.id;


--
-- Name: subanswer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE subanswer (
    id integer NOT NULL,
    question_id integer
);


ALTER TABLE subanswer OWNER TO postgres;

--
-- Name: subanswer_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE subanswer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE subanswer_id_seq OWNER TO postgres;

--
-- Name: subanswer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE subanswer_id_seq OWNED BY subanswer.id;


--
-- Name: subanswergiven; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE subanswergiven (
    id integer NOT NULL,
    question_id integer NOT NULL,
    team_id integer NOT NULL,
    corr_answer_id integer NOT NULL,
    answer_given character varying(255),
    correct boolean,
    confidence double precision,
    person_id integer NOT NULL
);


ALTER TABLE subanswergiven OWNER TO postgres;

--
-- Name: subanswergiven_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE subanswergiven_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE subanswergiven_id_seq OWNER TO postgres;

--
-- Name: subanswergiven_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE subanswergiven_id_seq OWNED BY subanswergiven.id;


--
-- Name: team; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE team (
    id integer NOT NULL,
    teamname character varying(255),
    score integer
);


ALTER TABLE team OWNER TO postgres;

--
-- Name: team_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE team_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE team_id_seq OWNER TO postgres;

--
-- Name: team_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE team_id_seq OWNED BY team.id;


--
-- Name: variant; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE variant (
    id integer NOT NULL,
    subanswer_id integer,
    answer character varying(255),
    "isNumber" boolean
);


ALTER TABLE variant OWNER TO postgres;

--
-- Name: variant_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE variant_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE variant_id_seq OWNER TO postgres;

--
-- Name: variant_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE variant_id_seq OWNED BY variant.id;


--
-- Name: word; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE word (
    id integer NOT NULL,
    line_id integer,
    word_image bytea,
    image_width integer,
    image_height integer
);


ALTER TABLE word OWNER TO postgres;

--
-- Name: word_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE word_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE word_id_seq OWNER TO postgres;

--
-- Name: word_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE word_id_seq OWNED BY word.id;


--
-- Name: answersheet id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY answersheet ALTER COLUMN id SET DEFAULT nextval('answersheet_id_seq'::regclass);


--
-- Name: answersheetquestion id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY answersheetquestion ALTER COLUMN id SET DEFAULT nextval('answersheetquestion_id_seq'::regclass);


--
-- Name: category id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY category ALTER COLUMN id SET DEFAULT nextval('category_id_seq'::regclass);


--
-- Name: line id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY line ALTER COLUMN id SET DEFAULT nextval('line_id_seq'::regclass);


--
-- Name: person id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY person ALTER COLUMN id SET DEFAULT nextval('person_id_seq'::regclass);


--
-- Name: question id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY question ALTER COLUMN id SET DEFAULT nextval('question_id_seq'::regclass);


--
-- Name: subanswer id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY subanswer ALTER COLUMN id SET DEFAULT nextval('subanswer_id_seq'::regclass);


--
-- Name: subanswergiven id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY subanswergiven ALTER COLUMN id SET DEFAULT nextval('subanswergiven_id_seq'::regclass);


--
-- Name: team id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY team ALTER COLUMN id SET DEFAULT nextval('team_id_seq'::regclass);


--
-- Name: variant id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY variant ALTER COLUMN id SET DEFAULT nextval('variant_id_seq'::regclass);


--
-- Name: word id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY word ALTER COLUMN id SET DEFAULT nextval('word_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY alembic_version (version_num) FROM stdin;
58f7a2362925
\.


--
-- Data for Name: answersheet; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY answersheet (id, answersheet_image, image_width, image_height, team_id) FROM stdin;
\.


--
-- Name: answersheet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('answersheet_id_seq', 1, false);


--
-- Data for Name: answersheetquestion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY answersheetquestion (id, answersheet_id, question_id) FROM stdin;
\.


--
-- Name: answersheetquestion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('answersheetquestion_id_seq', 1, false);


--
-- Data for Name: category; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY category (id, name) FROM stdin;
2	kerst
3	domme vragen
\.


--
-- Name: category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('category_id_seq', 3, true);


--
-- Data for Name: line; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY line (id, answersheet_id, line_image, image_width, image_height) FROM stdin;
\.


--
-- Name: line_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('line_id_seq', 1, false);


--
-- Data for Name: person; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY person (id, personname) FROM stdin;
1	antwoordchecker
2	admin
\.


--
-- Name: person_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('person_id_seq', 2, true);


--
-- Data for Name: question; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY question (id, person_id, category_id, question, active, questionnumber) FROM stdin;
3	2	3	is dit een vraag?	f	31
\.


--
-- Name: question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('question_id_seq', 3, true);


--
-- Data for Name: subanswer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY subanswer (id, question_id) FROM stdin;
2	3
3	3
\.


--
-- Name: subanswer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('subanswer_id_seq', 3, true);


--
-- Data for Name: subanswergiven; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY subanswergiven (id, question_id, team_id, corr_answer_id, answer_given, correct, confidence, person_id) FROM stdin;
\.


--
-- Name: subanswergiven_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('subanswergiven_id_seq', 1, false);


--
-- Data for Name: team; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY team (id, teamname, score) FROM stdin;
9	team1	\N
10	team2	\N
11	maak een team met enter\\	\N
\.


--
-- Name: team_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('team_id_seq', 41, true);


--
-- Data for Name: variant; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY variant (id, subanswer_id, answer, "isNumber") FROM stdin;
2	2	ja	\N
3	3	nee	\N
\.


--
-- Name: variant_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('variant_id_seq', 3, true);


--
-- Data for Name: word; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY word (id, line_id, word_image, image_width, image_height) FROM stdin;
\.


--
-- Name: word_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('word_id_seq', 1, false);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: answersheet answersheet_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY answersheet
    ADD CONSTRAINT answersheet_pkey PRIMARY KEY (id);


--
-- Name: answersheetquestion answersheetquestion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY answersheetquestion
    ADD CONSTRAINT answersheetquestion_pkey PRIMARY KEY (id);


--
-- Name: category category_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY category
    ADD CONSTRAINT category_pkey PRIMARY KEY (id);


--
-- Name: line line_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY line
    ADD CONSTRAINT line_pkey PRIMARY KEY (id);


--
-- Name: person person_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY person
    ADD CONSTRAINT person_pkey PRIMARY KEY (id);


--
-- Name: question question_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY question
    ADD CONSTRAINT question_pkey PRIMARY KEY (id);


--
-- Name: subanswer subanswer_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY subanswer
    ADD CONSTRAINT subanswer_pkey PRIMARY KEY (id);


--
-- Name: subanswergiven subanswergiven_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY subanswergiven
    ADD CONSTRAINT subanswergiven_pkey PRIMARY KEY (id);


--
-- Name: team team_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY team
    ADD CONSTRAINT team_pkey PRIMARY KEY (id);


--
-- Name: variant variant_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY variant
    ADD CONSTRAINT variant_pkey PRIMARY KEY (id);


--
-- Name: word word_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY word
    ADD CONSTRAINT word_pkey PRIMARY KEY (id);


--
-- Name: answersheet answersheet_team_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY answersheet
    ADD CONSTRAINT answersheet_team_id_fkey FOREIGN KEY (team_id) REFERENCES team(id);


--
-- Name: answersheetquestion answersheetquestion_answersheet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY answersheetquestion
    ADD CONSTRAINT answersheetquestion_answersheet_id_fkey FOREIGN KEY (answersheet_id) REFERENCES answersheet(id);


--
-- Name: answersheetquestion answersheetquestion_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY answersheetquestion
    ADD CONSTRAINT answersheetquestion_question_id_fkey FOREIGN KEY (question_id) REFERENCES question(id);


--
-- Name: line line_answersheet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY line
    ADD CONSTRAINT line_answersheet_id_fkey FOREIGN KEY (answersheet_id) REFERENCES answersheet(id);


--
-- Name: question question_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY question
    ADD CONSTRAINT question_category_id_fkey FOREIGN KEY (category_id) REFERENCES category(id);


--
-- Name: question question_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY question
    ADD CONSTRAINT question_person_id_fkey FOREIGN KEY (person_id) REFERENCES person(id);


--
-- Name: subanswer subanswer_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY subanswer
    ADD CONSTRAINT subanswer_question_id_fkey FOREIGN KEY (question_id) REFERENCES question(id);


--
-- Name: subanswergiven subanswergiven_corr_answer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY subanswergiven
    ADD CONSTRAINT subanswergiven_corr_answer_id_fkey FOREIGN KEY (corr_answer_id) REFERENCES subanswer(id);


--
-- Name: subanswergiven subanswergiven_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY subanswergiven
    ADD CONSTRAINT subanswergiven_person_id_fkey FOREIGN KEY (person_id) REFERENCES person(id);


--
-- Name: subanswergiven subanswergiven_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY subanswergiven
    ADD CONSTRAINT subanswergiven_question_id_fkey FOREIGN KEY (question_id) REFERENCES question(id);


--
-- Name: subanswergiven subanswergiven_team_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY subanswergiven
    ADD CONSTRAINT subanswergiven_team_id_fkey FOREIGN KEY (team_id) REFERENCES team(id);


--
-- Name: variant variant_subanswer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY variant
    ADD CONSTRAINT variant_subanswer_id_fkey FOREIGN KEY (subanswer_id) REFERENCES subanswer(id);


--
-- Name: word word_line_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY word
    ADD CONSTRAINT word_line_id_fkey FOREIGN KEY (line_id) REFERENCES line(id);


--
-- PostgreSQL database dump complete
--

\connect postgres

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.2
-- Dumped by pg_dump version 9.6.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: postgres; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE postgres IS 'default administrative connection database';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- PostgreSQL database dump complete
--

\connect template1

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.2
-- Dumped by pg_dump version 9.6.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: template1; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE template1 IS 'default template for new databases';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database cluster dump complete
--

