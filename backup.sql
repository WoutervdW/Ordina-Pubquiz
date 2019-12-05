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
-- Name: answer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE answer (
    id integer NOT NULL,
    team_id integer NOT NULL,
    question_id integer NOT NULL,
    answer_given character varying(255),
    correct boolean,
    answer_image bytea,
    confidence double precision,
    person_id integer NOT NULL
);


ALTER TABLE answer OWNER TO postgres;

--
-- Name: answer_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE answer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE answer_id_seq OWNER TO postgres;

--
-- Name: answer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE answer_id_seq OWNED BY answer.id;


--
-- Name: answersheet; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE answersheet (
    id integer NOT NULL,
    answersheet_image bytea,
    image_height integer,
    image_width integer
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
-- Name: person; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE person (
    id integer NOT NULL,
    personname character varying(255),
    password character varying(255)
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
    category_id integer,
    question character varying(255),
    correct_answer character varying(255),
    active boolean,
    person_id integer
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
-- Name: answer id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY answer ALTER COLUMN id SET DEFAULT nextval('answer_id_seq'::regclass);


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
-- Name: person id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY person ALTER COLUMN id SET DEFAULT nextval('person_id_seq'::regclass);


--
-- Name: question id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY question ALTER COLUMN id SET DEFAULT nextval('question_id_seq'::regclass);


--
-- Name: team id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY team ALTER COLUMN id SET DEFAULT nextval('team_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY alembic_version (version_num) FROM stdin;
f91f0c2a9fa8
\.


--
-- Data for Name: answer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY answer (id, team_id, question_id, answer_given, correct, answer_image, confidence, person_id) FROM stdin;
4	1	13	antwoord	t	\N	97	2
\.


--
-- Name: answer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('answer_id_seq', 4, true);


--
-- Data for Name: answersheet; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY answersheet (id, answersheet_image, image_height, image_width) FROM stdin;
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
3	natuur
4	muziek
5	sport
\.


--
-- Name: category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('category_id_seq', 5, true);


--
-- Data for Name: person; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY person (id, personname, password) FROM stdin;
1	admin	admin
2	answerchecker	answerchecker
\.


--
-- Name: person_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('person_id_seq', 2, true);


--
-- Data for Name: question; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY question (id, category_id, question, correct_answer, active, person_id) FROM stdin;
14	3	asdf	asdf	t	1
15	5	sdf	sdf	t	1
16	4	piet	dirk	t	1
17	3	dsaf	sadf	t	1
18	4	asfd	asdf	t	1
19	4	asdf	asdf	t	1
20	4	asdf	asdf	t	1
21	4	\N	\N	t	1
22	4	asdfasdfsa	dfasdfasdfasdfasdfsa	t	1
13	3	vraag?	antwoord	f	1
23	3	asdfasdf	adsfasdf	t	1
\.


--
-- Name: question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('question_id_seq', 23, true);


--
-- Data for Name: team; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY team (id, teamname, score) FROM stdin;
1	Marijn	123
2	Sander	23
3	Wouter	553
\.


--
-- Name: team_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('team_id_seq', 3, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: answer answer_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY answer
    ADD CONSTRAINT answer_pkey PRIMARY KEY (id);


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
-- Name: team team_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY team
    ADD CONSTRAINT team_pkey PRIMARY KEY (id);


--
-- Name: answer answer_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY answer
    ADD CONSTRAINT answer_person_id_fkey FOREIGN KEY (person_id) REFERENCES person(id);


--
-- Name: answer answer_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY answer
    ADD CONSTRAINT answer_question_id_fkey FOREIGN KEY (question_id) REFERENCES question(id);


--
-- Name: answer answer_team_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY answer
    ADD CONSTRAINT answer_team_id_fkey FOREIGN KEY (team_id) REFERENCES team(id);


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


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: answer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE answer (
    id integer NOT NULL,
    team_id integer NOT NULL,
    question_id integer NOT NULL,
    user_id integer NOT NULL,
    correct boolean,
    answer_image bytea,
    confidence double precision
);


ALTER TABLE answer OWNER TO postgres;

--
-- Name: answer_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE answer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE answer_id_seq OWNER TO postgres;

--
-- Name: answer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE answer_id_seq OWNED BY answer.id;


--
-- Name: answersheet; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE answersheet (
    id integer NOT NULL,
    answersheet_image bytea
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
-- Name: question; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE question (
    id integer NOT NULL,
    user_id integer,
    category_id character varying(255),
    question character varying(255),
    correct_answer character varying(255),
    active boolean
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
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE "user" (
    id integer NOT NULL,
    username character varying(255),
    password character varying(255)
);


ALTER TABLE "user" OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE user_id_seq OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE user_id_seq OWNED BY "user".id;


--
-- Name: answer id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY answer ALTER COLUMN id SET DEFAULT nextval('answer_id_seq'::regclass);


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
-- Name: question id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY question ALTER COLUMN id SET DEFAULT nextval('question_id_seq'::regclass);


--
-- Name: team id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY team ALTER COLUMN id SET DEFAULT nextval('team_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY "user" ALTER COLUMN id SET DEFAULT nextval('user_id_seq'::regclass);


--
-- Data for Name: answer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY answer (id, team_id, question_id, user_id, correct, answer_image, confidence) FROM stdin;
\.


--
-- Name: answer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('answer_id_seq', 1, false);


--
-- Data for Name: answersheet; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY answersheet (id, answersheet_image) FROM stdin;
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
\.


--
-- Name: category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('category_id_seq', 1, false);


--
-- Data for Name: question; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY question (id, user_id, category_id, question, correct_answer, active) FROM stdin;
\.


--
-- Name: question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('question_id_seq', 1, false);


--
-- Data for Name: team; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY team (id, teamname, score) FROM stdin;
1	Marijn	123
2	Sander	23
3	Wouter	553
\.


--
-- Name: team_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('team_id_seq', 3, true);


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "user" (id, username, password) FROM stdin;
\.


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('user_id_seq', 1, false);


--
-- Name: answer answer_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY answer
    ADD CONSTRAINT answer_pkey PRIMARY KEY (id);


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
-- Name: question question_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY question
    ADD CONSTRAINT question_pkey PRIMARY KEY (id);


--
-- Name: team team_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY team
    ADD CONSTRAINT team_pkey PRIMARY KEY (id);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: answer answer_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY answer
    ADD CONSTRAINT answer_question_id_fkey FOREIGN KEY (question_id) REFERENCES question(id);


--
-- Name: answer answer_team_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY answer
    ADD CONSTRAINT answer_team_id_fkey FOREIGN KEY (team_id) REFERENCES team(id);


--
-- Name: answer answer_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY answer
    ADD CONSTRAINT answer_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id);


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
-- Name: question question_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY question
    ADD CONSTRAINT question_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id);


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

