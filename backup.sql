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
    personname character varying(255),
    password_hash character varying(255)
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
    person_id integer NOT NULL,
    line_id integer NOT NULL
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
    image_height integer,
    word_recognised character varying(255)
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
43f7a6ccbf73
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
4	Ordina
5	namen
6	tijd
7	multiple choice
8	\N
9	huh
10	test
11	cola
2	kerst
3	domme vragen
\.


--
-- Name: category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('category_id_seq', 4, true);


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

COPY person (id, personname, password_hash) FROM stdin;
1	Sander	\N
3	admin	pbkdf2:sha256:150000$BW4w7lUk$4650e6f5ad6babfe27929a2a05cbebae91c9a3ecc97174785f61d917abf84c63
36	systeem	\N
2	nog niet nagekeken	\N
\.


--
-- Name: person_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('person_id_seq', 36, true);


--
-- Data for Name: question; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY question (id, person_id, category_id, question, active, questionnumber) FROM stdin;
11	3	4	De jaren ‘90 culthelden Beavis en Butthead droegen allebei een t-shirt met daarop het logo van een beroemde band. Om welke twee bands ging het?	t	3
12	3	4	Een vraag voor alle scheikunde-liefhebbers! Wat is het chemische element met de allerkortste volledige naam?	t	4
13	3	4	Noem een jaar uit het leven van de beroemde wetenschapper Sir Isaac Newton. Elk willekeurig jaar levert dus een punt op; zolang het maar tussen zijn geboorte- en zijn sterftejaar valt!	t	5
14	3	4	Sportvraag! Bij welke sport duurt een wedstrijd langer (kijkend naar zuivere speeltijd)? Is dit A: basketbal of B: ijshockey?	t	6
15	3	4	Noem 5 merknamen in bezit van Heineken NV:	t	7
17	3	4	noem 5 albums van de beatles: (op wikipedia staan er 30, maar deze zouden ze moeten kennen)	t	8
20	3	4	Deze enorme robots komen van de planeet Cybertron en zijn een meter of 8 hoog. Ze hebben de mogelijkheid zich te camoufleren als doorsneevoertuigen. Hoe heet dit ‘ras’ van mega-robots?	t	10
8	3	4	Waar staat OSD voor?	t	9
9	3	4	noem alle open source afdelingen afdelingen van Ordina. + bonuspunt voor een BUM naam	t	2
21	3	4	Een vraag voor de puzzel-liefhebbers: welke beroemde acteur zit verstopt in het anagram ‘cool ego energy’?	f	9
19	3	4	Een pilsje is vernoemd naar het plaatsje pilzen. In welk land ligt dit plaatsje	t	33
22	3	4	Noem een dier in de top 5 luidste dieren op aarde	t	13
\.


--
-- Name: question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('question_id_seq', 22, true);


--
-- Data for Name: subanswer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY subanswer (id, question_id) FROM stdin;
8	8
9	9
10	9
11	9
12	9
13	9
16	11
17	11
18	12
19	13
20	14
21	15
22	15
23	15
24	15
25	15
31	17
32	17
33	17
34	17
35	17
38	19
39	20
40	21
41	22
\.


--
-- Name: subanswer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('subanswer_id_seq', 41, true);


--
-- Data for Name: subanswergiven; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY subanswergiven (id, question_id, team_id, corr_answer_id, answer_given, correct, confidence, person_id, line_id) FROM stdin;
\.


--
-- Name: subanswergiven_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('subanswergiven_id_seq', 1, false);


--
-- Data for Name: team; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY team (id, teamname, score) FROM stdin;
58	De Verliezers	\N
59	HO HO HO	0
60	Blanco	0
\.


--
-- Name: team_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('team_id_seq', 60, true);


--
-- Data for Name: variant; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY variant (id, subanswer_id, answer, "isNumber") FROM stdin;
8	8	Open Source Development	\N
9	9	Pythoneers	\N
10	10	JTech	\N
11	11	JSRoots	\N
12	12	CodeStar	\N
13	13	naam	\N
17	16	Metallica	\N
18	17	AC\\DC	\N
19	18	Tin	\N
20	19	1643 – 1727	\N
22	21	Amstel	\N
23	22	Sol	\N
24	23	Desperados	\N
25	24	Strongbow	\N
26	25	Jillz	\N
32	31	rubber soul	\N
33	32	st peppers lonely hearts club band	\N
34	33	revolver	\N
35	34	yellow submarine	\N
36	35	abbey road	\N
39	38	Tsjechie	\N
40	39	Autobots	\N
41	39	Transformers	\N
42	40	George Clooney	\N
43	41	Pistool Garnaal	\N
21	20	B	\N
\.


--
-- Name: variant_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('variant_id_seq', 43, true);


--
-- Data for Name: word; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY word (id, line_id, word_image, image_width, image_height, word_recognised) FROM stdin;
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
-- Name: subanswergiven subanswergiven_line_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY subanswergiven
    ADD CONSTRAINT subanswergiven_line_id_fkey FOREIGN KEY (line_id) REFERENCES line(id);


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

